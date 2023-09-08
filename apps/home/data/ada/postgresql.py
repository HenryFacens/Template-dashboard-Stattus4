from django.db import connections


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
            consistency = "consistente"
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
        
        # Atualizar o dicionário com a consistência e a razão para cada serial_number
        consistency_data[serial_number] = {
            "consistency": consistency,
            "reason": reason
        }

    return consistency_data
