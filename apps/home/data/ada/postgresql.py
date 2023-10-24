from django.db import connections
import datetime
import json
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

def avg_pressure_mvn(cursor, active_device_ids): #certa 
    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=30)

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

def funcaoAmplitudeHoraria(cursor, active_devices_ids):

    devices_id_string = ', '.join([f"'{device_id}'" for device_id in active_devices_ids])
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=30)

    query = f"""
        WITH HourlyExtremes AS (
        SELECT
            DATE(d."timestamp") as day_date,
            MAX(d.single_value) AS max_pressure,
            MIN(d.single_value) AS min_pressure
        FROM 
            "4fluid-iot".devices_data d
        WHERE
            d.device_id IN ({devices_id_string}) AND
            d."timestamp" BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY
            DATE(d."timestamp"), EXTRACT(HOUR FROM d."timestamp")
    )

    SELECT
        day_date,
        (max_pressure - min_pressure) AS amplitude_horaria
    FROM 
        HourlyExtremes
    ORDER BY 
        day_date;
        """

    cursor.execute(query)
    result = cursor.fetchall()

    # Agrupar os resultados por data e calcular a média das amplitudes horárias para cada dia
    daily_amplitudes = {}
    for day_date, amplitude in result:
        if day_date not in daily_amplitudes:
            daily_amplitudes[day_date] = []
        daily_amplitudes[day_date].append(amplitude)

    daily_avg_amplitudes = [{'date': str(day), 'amplitude_horaria': sum(amplitudes)/len(amplitudes)} for day, amplitudes in daily_amplitudes.items()]

    return daily_avg_amplitudes



def cal_hidraulica(active_device_ids):
    try:
        with connections['postgre'].cursor() as cursor:
            # avg_data_daily = avg_pressure_per_day(cursor, active_device_ids) #
            # hydraulic_data_daily = hydraulic_load_hourly(avg_data_daily) #
            avg_data_mvn = avg_pressure_mvn(cursor, active_device_ids)
            hydraulic_data_mvn = hydraulic_load_for_mvn(avg_data_mvn)
            amplitudeHoraria = funcaoAmplitudeHoraria(cursor,active_device_ids)
        return {
            # "average_pressure_daily": avg_data_daily,
            # "hydraulic_load_daily": hydraulic_data_daily,
            "mvn_avg_pressure": avg_data_mvn,
            "mvn_hydraulic_load": hydraulic_data_mvn,
            "amplitudeHoraria" : amplitudeHoraria,
        }
    except Exception as e:
        print(f"Error in cal_hidraulica: {e}")
        return {}

def get_press(active_device_ids, start_date, end_date):
    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])
    
    if start_date is None:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=30)


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

def classify_communication(active_device_ids, start_date, end_date):
    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])
    
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    if start_date is None:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=30)
    
    print("End Date:", end_date)
    print("Start Date:", start_date)
    print("Device IDs:", device_ids_string)

    with connections['postgre'].cursor() as cursor:
        query = f"""
        SELECT cr.device_id, 
               date_trunc('day', cr."timestamp") as communication_day,
               mdi.created_at as commission_date
        FROM "4fluid-iot".connectivity_rate cr
        JOIN "4fluid-iot".meter_device_install_point mdi ON cr.device_id = mdi.device_id
        WHERE cr.device_id IN ({device_ids_string})
        AND cr."timestamp" BETWEEN %s AND %s
        """
        
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

    # Creating a dictionary to store communication days and commission date for each device
    device_data = {device_id: {'days': set(), 'commission_date': None} for device_id in active_device_ids}
    for device_id, communication_day, commission_date in results:
        device_data[device_id]['days'].add(communication_day)
        device_data[device_id]['commission_date'] = commission_date

    # Counting the devices based on communication status
    communicated_count = 0
    not_communicated_count = 0
    total_days = (end_date - start_date).days
    for device_id, data in device_data.items():
        days_without_communication = total_days - len(data['days'])
        
        # Check if the device was commissioned within the date range
        if data['commission_date'] and data['commission_date'] > start_date:
            communicated_count += 1
        elif days_without_communication >= 6 or len(data['days']) == 0:
            not_communicated_count += 1
        else:
            communicated_count += 1

    summary = {
        communicated_count: "Comunicou",
        not_communicated_count: "Nao Comunicou"
    }
    print(summary)
    return summary
