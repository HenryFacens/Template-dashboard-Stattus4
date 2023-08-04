from apps.banco.models_sql_server import Amostras, Clientes
from datetime import datetime
from django.db.models import Count, Q
import pytz
from django.db import DatabaseError, connections
from dateutil.relativedelta import relativedelta

def transform_date_keys(data):
    """Transform date keys in a dictionary to month names.
    Args:
    data (dict): A dictionary where keys are strings that represent dates in the format 'YYYY-MM'.
    Returns:
    dict: A new dictionary where keys are month names.
    """
    month_names = {
        '01': 'Janeiro',
        '02': 'Fevereiro',
        '03': 'Março',
        '04': 'Abril',
        '05': 'Maio',
        '06': 'Junho',
        '07': 'Julho',
        '08': 'Agosto',
        '09': 'Setembro',
        '10': 'Outubro',
        '11': 'Novembro',
        '12': 'Dezembro',
    }

    new_data = {}

    for key, value in data.items():
        date = datetime.strptime(key, '%Y-%m')
        month_number = date.strftime('%m')
        new_key = month_names[month_number]
        new_data[new_key] = value

    return new_data


def get_active_clients_with_sample_count(start_date, end_date):
    """Get a list of active clients with their respective sample count within a specific date range.

    Args:
    start_date (datetime): The start of the date range.
    end_date (datetime): The end of the date range.

    Returns:
    dict: A dictionary where each key is a master client ID, and the value is another dictionary with the master client's name and a list of its clients.
    """
    with connections['sql_server'].cursor() as cursor:
        cursor.execute("""
            SELECT c.id_cliente, c.razao_social, cm.razao_social AS nome_master, COUNT(a.id_amostra) AS count
            FROM clientes AS c
            LEFT JOIN amostras AS a ON c.id_cliente = a.id_cliente
            LEFT JOIN clientes AS cm ON c.id_cliente_master = cm.id_cliente
            WHERE c.ativo = 1 AND a.dt_amostra BETWEEN %s AND %s
            GROUP BY c.id_cliente, c.razao_social, c.id_cliente_master, cm.razao_social
        """, [start_date, end_date])
        results = cursor.fetchall()

    data = {}

    for id_cliente, razao_social, nome_master, count in results:
        master_name = nome_master if nome_master else 'Sem Cliente Master'

        if master_name not in data:
            data[master_name] = {
                'nome_master': master_name,
                'clientes': []
            }

        data[master_name]['clientes'].append({
            'id_cliente': id_cliente,
            'razao_social': razao_social,
            'count': count
        })
    return data

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

    transformed_data = transform_date_keys(data)

    return transformed_data
