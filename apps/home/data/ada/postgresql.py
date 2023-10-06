from django.db import connections
import datetime

def get_cliente_ativos():
    with connections['postgre'].cursor() as cursor:
        cursor.execute(""" 
        SELECT id, trading_name
        FROM clients
        WHERE active = true AND trading_name <> 'Cliente Demonstração ';;
                       """)
        clientes_ativos = cursor.fetchall()

    return clientes_ativos


def get_regioes(id_cliente):

    with connections['postgre'].cursor() as cursor:
        cursor.execute(f"""
            SELECT id, neighborhood 
            FROM "4fluid-iot".install_points 
            WHERE client_id = { id_cliente};
                       """)
        subs_clientes = cursor.fetchall()
    # print(subs_clientes)
    return subs_clientes


def get_devices_db(active_device_ids):

    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])
    with connections['postgre'].cursor() as cursor:
        cursor.execute(f"""
            SELECT 
                d.id AS device_id, 
                d.install_point_id, 
                d."type",
                d.serial_number,
                cr.conn_evt,
                ip.lat,
                ip.long,
                cr.communication_day,
                cr.conn_rate,
                cr."timestamp"
            FROM "4fluid-iot".devices AS d
            LEFT JOIN "4fluid-iot".connectivity_rate AS cr ON d.id = cr.device_id AND cr."timestamp" > current_date - interval '7 days'
            LEFT JOIN "4fluid-iot".install_points AS ip ON d.install_point_id = ip.id
            WHERE d.id IN ({device_ids_string})
        """)
        
        combined_info = cursor.fetchall()
    # print(f'COMBINEDDATAAAAAAAAAAAAA {combined_info}')

    combined_data = [
        {
            "device_id": info[0], 
            "install_point_id": info[1], 
            "type": info[2],
            "serial_number": info[3],
            "conn_evt": info[4],
            "lat": info[5],
            "long": info[6],
            "communication_day": info[7],
            "conn_rate": info[8],
            "timestamp": info[9],
        } for info in combined_info
    ]
    # print(f'COMBINEDDATAAAAAAAAAAAAA {combined_data}')  

    return combined_data

def get_consistency(active_device_ids):
    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])

    with connections['postgre'].cursor() as cursor:
        cursor.execute(f"""
            SELECT 
                d.serial_number,
                dd.single_value
            FROM "4fluid-iot".devices_data AS dd
            JOIN "4fluid-iot".devices AS d ON d.id = dd.device_id
            WHERE dd.device_id IN ({device_ids_string}) AND dd."timestamp" > current_date - interval '1 day'
        """)

        data_values = cursor.fetchall()

    consistency_data = {}

    for data in data_values:
        serial_number = data[0]
        pressure_value = data[1]

        if pressure_value is None:
            consistency = "Sem comunicação"
            reason = "Sem comunicação"
        elif pressure_value == 0:
            consistency = "inconsistente"
            reason = "Valor igual a 0 por muito tempo"
        elif pressure_value < -10:
            consistency = "inconsistente"
            reason = "Valor abaixo de -10 mca"
        elif pressure_value > 120:
            consistency = "inconsistente"
            reason = "Valor acima de 120 mca"
        else:
            consistency = "consistente"
            reason = "Valor normal"
        
        consistency_data[serial_number] = {
            "consistency": consistency,
            "reason": reason
        }

    return consistency_data


# def avg_pressure_per_day(cursor, active_device_ids): #Errada
#     device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])
#     end_date = datetime.datetime.now()
#     start_date = end_date - datetime.timedelta(days=30)

#     query = f"""
#     SELECT
#         d.device_id,
#         DATE(d."timestamp") as day_date,
#         AVG(d.single_value) as avg_pressure,
#         p.alt
#     FROM 
#         "4fluid-iot".devices_data d
#     JOIN
#         "4fluid-iot".install_points p ON d.install_point_id = p.id
#     WHERE
#         d.device_id IN ({device_ids_string}) AND
#         d."timestamp" BETWEEN '{start_date}' AND '{end_date}'
#     GROUP BY
#         d.device_id, DATE(d."timestamp"), p.alt
#     ORDER BY
#         d.device_id, day_date;
#     """
    
#     cursor.execute(query)
#     return cursor.fetchall()

# def hydraulic_load_hourly(avg_pressure_data):
#     try:
#         return [(entry[0], entry[1], (entry[2] or 0) + (entry[3] or 0)) for entry in avg_pressure_data]
#     except Exception as e:
#         print(f"Error in hydraulic_load_hourly: {e}")
#         return []

def avg_pressure_mvn(cursor, active_device_ids,start_date=None,end_date=None): #certa 
    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])
    if start_date is None:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=30)
    print(end_date)
    print(start_date)
    print(device_ids_string)
    query = f"""
        SELECT
            dev.serial_number,
            DATE(d."timestamp") as day_date,
            AVG(d.single_value) as avg_pressure,
            p.alt
        FROM 
            "4fluid-iot".devices_data d
        JOIN
            "4fluid-iot".install_points p ON d.install_point_id = p.id
        JOIN
            "4fluid-iot".devices dev ON d.device_id = dev.id
        WHERE
            d.device_id IN ({device_ids_string}) AND
            d."timestamp" BETWEEN '{start_date}' AND '{end_date}' AND
            EXTRACT(HOUR FROM d."timestamp") >= 4 AND EXTRACT(HOUR FROM d."timestamp") < 5
        GROUP BY
            dev.serial_number, DATE(d."timestamp"), p.alt
        ORDER BY
            dev.serial_number, day_date;
    """
    
    cursor.execute(query)
    return cursor.fetchall()

def hydraulic_load_for_mvn(avg_pressure_mvn_data):
    return [(entry[0], entry[1], (entry[2] or 0) + (entry[3] or 0)) for entry in avg_pressure_mvn_data]

def cal_hidraulica(active_device_ids,date1=None,date2=None):
    try:
        with connections['postgre'].cursor() as cursor:
            # avg_data_daily = avg_pressure_per_day(cursor, active_device_ids) #
            # hydraulic_data_daily = hydraulic_load_hourly(avg_data_daily) #
            avg_data_mvn = avg_pressure_mvn(cursor, active_device_ids,date1,date2)
            hydraulic_data_mvn = hydraulic_load_for_mvn(avg_data_mvn)

        return {
            # "average_pressure_daily": avg_data_daily,
            # "hydraulic_load_daily": hydraulic_data_daily,
            "mvn_avg_pressure": avg_data_mvn,
            "mvn_hydraulic_load": hydraulic_data_mvn
        }
    except Exception as e:
        print(f"Error in cal_hidraulica: {e}")
        return {}

def get_press(active_device_ids, start_date, end_date):
    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])
    
    if start_date is None:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=30)
    
    print("End Date:", end_date)
    print("Start Date:", start_date)
    print("Device IDs:", device_ids_string)

    with connections['postgre'].cursor() as cursor:
        query = f"""
        SELECT d.serial_number, 
               date_trunc('hour', dd."timestamp") as hour,
               SUM(dd.single_value) as total_value,
               COUNT(dd.single_value) as count
        FROM "4fluid-iot".devices_data dd
        JOIN "4fluid-iot".devices d ON dd.device_id = d.id
        WHERE dd.device_id IN ({device_ids_string})
        AND dd."timestamp" BETWEEN %s AND %s
        GROUP BY d.serial_number, date_trunc('hour', dd."timestamp")
        ORDER BY d.serial_number, hour
        """
        
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

    # Calculating the average for each serial number and hour
    averaged_results = [(serial_number, hour, total_value/count) for serial_number, hour, total_value, count in results]

    # for serial_number, hour, avg_value in averaged_results:
    #     print(f"Serial Number: {serial_number}, Hour: {hour}, Average Value: {avg_value:.2f}")

    return averaged_results
