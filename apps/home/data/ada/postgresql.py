from django.db import connections
from itertools import groupby
import datetime


def get_cliente_ativos():
    with connections['default'].cursor() as cursor:
        cursor.execute(""" 
        SELECT id, trading_name
        FROM clients
        WHERE active = true AND trading_name <> 'Cliente Demonstração ';;
                       """)
        clientes_ativos = cursor.fetchall()

    return clientes_ativos


def get_regioes(id_cliente):

    with connections['default'].cursor() as cursor:
        cursor.execute(f"""
            SELECT id, neighborhood 
            FROM "4fluid-iot".install_points 
            WHERE client_id = { id_cliente};
                       """)
        subs_clientes = cursor.fetchall()
    print(subs_clientes)
    return subs_clientes


def get_devices_db(active_device_ids):

    # Convertendo a lista de device_ids em uma string para uso no SQL
    device_ids_string = ', '.join([f"'{device_id}'" for device_id in active_device_ids])

    with connections['default'].cursor() as cursor:
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

    # Transformando a lista de tuplas em uma lista de dicionários
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
    return combined_data
