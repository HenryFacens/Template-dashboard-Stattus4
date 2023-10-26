import datetime
from apps.home.data.conectDatabase import DataBase

db = DataBase('postgre')


def get_cliente_ativos():

    result = db.execute(""" 
        SELECT id, trading_name
        FROM clients
        WHERE active = true AND trading_name <> 'Cliente Demonstração ';;
                       """)

    return result


def get_regioes(id_cliente):


    result  = db.execute(f"""            SELECT id, neighborhood 
            FROM "4fluid-iot".install_points 
            WHERE client_id = { id_cliente};""")
    
    return result


def get_devices_db(active_device_ids):

    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])
    
    
    result = db.execute(f"""
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

    data = [
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
        } for info in result
    ]

    return data

def get_consistency(active_device_ids):


    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])

    result = db.execute(f"""            
            SELECT 
                d.serial_number,
                dd.single_value
            FROM "4fluid-iot".devices_data AS dd
            JOIN "4fluid-iot".devices AS d ON d.id = dd.device_id
            WHERE dd.device_id IN ({device_ids_string}) AND dd."timestamp" > current_date - interval '1 day'""")

    consistency_data = {}

    for data in result:
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

def avg_pressure_mvn(cursor, device_ids_string): #certa 
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

def funcaoAmplitudeHoraria(data, zmax=None):
    
    # Crie um dicionário para armazenar os valores máximos e mínimos para cada data
    date_extremes = {}
    
    for _, date, value in data:
        if date not in date_extremes:
            date_extremes[date] = {"max": value, "min": value}
        else:
            date_extremes[date]["max"] = max(date_extremes[date]["max"], value)
            if zmax is not None:  # Se zmax for fornecido
                date_extremes[date]["min"] = min(zmax, value)
            else:  # Se zmax não for fornecido, continue como antes
                date_extremes[date]["min"] = min(date_extremes[date]["min"], value)

    # Calcule a amplitude para cada dia e coloque-a em uma lista de dicionários
    amplitude_dicts = []
    for date, extremes in date_extremes.items():
        amplitude = extremes["max"] - extremes["min"]
        amplitude_dicts.append({"date": date, "amplitude": amplitude})
    
    return amplitude_dicts


def cal_hidraulica(active_device_ids,zmax):

    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])

    try:
        with db.get_cursor() as cursor:
            avg_data_mvn = avg_pressure_mvn(cursor, device_ids_string)
            hydraulic_data_mvn = hydraulic_load_for_mvn(avg_data_mvn)
            amplitudeHoraria = funcaoAmplitudeHoraria(hydraulic_data_mvn,zmax)
        return {
            "mvn_avg_pressure": avg_data_mvn,
            "mvn_hydraulic_load": hydraulic_data_mvn,
            "amplitudeHoraria" : amplitudeHoraria,
        }
    except Exception as e:
        print(f"Error in cal_hidraulica: {e}")
        return {}

def classify_communication(active_device_ids, start_date, end_date):
    
    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])
    
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    if start_date is None:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=30)
    

    results = db.execute(f"""
        SELECT cr.device_id, 
               date_trunc('day', cr."timestamp") as communication_day,
               mdi.created_at as commission_date
        FROM "4fluid-iot".connectivity_rate cr
        JOIN "4fluid-iot".meter_device_install_point mdi ON cr.device_id = mdi.device_id
        WHERE cr.device_id IN ({device_ids_string})
        AND cr."timestamp" BETWEEN '{start_date}' AND '{end_date}'
    """)


    device_data = {device_id: {'days': set(), 'commission_date': None} for device_id in active_device_ids}
    for device_id, communication_day, commission_date in results:
        device_data[device_id]['days'].add(communication_day)
        device_data[device_id]['commission_date'] = commission_date

    communicated_count = 0
    not_communicated_count = 0
    total_days = (end_date - start_date).days
    for device_id, data in device_data.items():
        days_without_communication = total_days - len(data['days'])
        
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

    return summary
