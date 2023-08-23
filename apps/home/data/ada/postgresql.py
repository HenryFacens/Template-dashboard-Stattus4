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