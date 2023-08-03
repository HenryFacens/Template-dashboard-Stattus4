from apps.banco.models_sql_server import Amostras, Clientes
from datetime import datetime
from django.db.models import Count, Q
import pytz
from django.db import DatabaseError, connections
from dateutil.relativedelta import relativedelta

def get_active_clients_with_sample_count(start_date, end_date):
    """Get a list of active clients with their respective sample count within a specific date range.

    Args:
    start_date (datetime): The start of the date range.
    end_date (datetime): The end of the date range.

    Returns:
    list: A list of dictionaries where each dictionary contains the ID, name, and sample count of an active client.
    """
    with connections['sql_server'].cursor() as cursor:
        cursor.execute("""
            SELECT c.id_cliente, c.razao_social, COUNT(a.id_amostra) AS count
            FROM clientes AS c
            LEFT JOIN amostras AS a ON c.id_cliente = a.id_cliente
            WHERE c.ativo = 1 AND a.dt_amostra BETWEEN %s AND %s
            GROUP BY c.id_cliente, c.razao_social
        """, [start_date, end_date])
        results = cursor.fetchall()

    active_clients = [
        {'id_cliente': id_cliente, 'razao_social': razao_social, 'count': count}
        for id_cliente, razao_social, count in results
    ]

    return active_clients

def get_past_three_months_data():
    """Get sample count of active clients for the past three complete months.

    Returns:
    dict: A dictionary where each key is a month and each value is a list of active clients with their sample count for that month.
    """
    tz = pytz.timezone('America/Sao_Paulo')
    today = datetime.now(tz=tz)

    data = {}
    for months_ago in range(1, 4):
        start_date = (today - relativedelta(months=months_ago)).replace(day=1)
        print("start_date")
        print(start_date)
        end_date = (start_date + relativedelta(months=1)) - relativedelta(days=1)
        print("end_date")
        print(end_date)


        data[start_date.strftime('%Y-%m')] = get_active_clients_with_sample_count(start_date, end_date)
    print(data)
    return data
