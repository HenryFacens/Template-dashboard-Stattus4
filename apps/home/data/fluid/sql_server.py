from django.db import connections
from itertools import groupby
import datetime

def get_cliente_ativos():
    with connections['sql_server'].cursor() as cursor:
        cursor.execute(""" 
        SELECT id_cliente, razao_social
        FROM clientes
        WHERE ativo = 1;
                       """)
        clientes_ativos = cursor.fetchall()

    return clientes_ativos


def get_dti_dtf():

    now = datetime.datetime.now()

    start_date = (now - datetime.timedelta(days=90)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    end_date = now.replace(hour=23, minute=59, second=59, microsecond=999)

    start_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

    print(start_str)
    print(end_str)
    return start_str, end_str

def get_amostras_status():

    clientes = get_cliente_ativos()


    lista_ids_clientes = [str(cliente[0]) for cliente in clientes]
    ids_clientes_str = ",".join(lista_ids_clientes)
    start_str, end_str = get_dti_dtf()

    with connections['sql_server'].cursor() as cursor:

        cursor.execute(f"""
        SELECT 
            id_cliente,
            MONTH(dt_amostra) AS Mes,
            CASE 
                WHEN v.id_relatorio IS NULL THEN 'Pendente'
                WHEN v.tipo_vazamento = 'Sem Ponto Suspeito, ' THEN 'Ponto Não Confirmado'
                ELSE 'Pontos Confirmados'
            END AS ClassificacaoVazamento,
            COUNT(*) AS Total
        FROM (
            SELECT id_amostra, id_cliente, seq, dt_amostra,
                ROW_NUMBER() OVER(PARTITION BY seq ORDER BY dt_amostra DESC) AS rn
            FROM devstattus4_4fluid.dbo.amostras
            WHERE classificacao = N'LEAK' 
            AND dt_amostra BETWEEN '{start_str}' AND '{end_str}' 
            AND id_cliente IN ({ids_clientes_str})
        ) AS a
        LEFT JOIN (
            SELECT id_amostra, id_relatorio, 
                ROW_NUMBER() OVER(PARTITION BY id_amostra ORDER BY id_relatorio DESC) AS rn
            FROM devstattus4_4fluid.dbo.relatorio_amostras
        ) AS r ON a.id_amostra = r.id_amostra
        LEFT JOIN devstattus4_4fluid.dbo.relatorio_vazamento AS v ON r.id_relatorio = v.id_relatorio
        WHERE a.rn = 1 AND (r.rn = 1 OR r.id_amostra IS NULL)
        GROUP BY 
            id_cliente,
            MONTH(dt_amostra),
            CASE 
                WHEN v.id_relatorio IS NULL THEN 'Pendente'
                WHEN v.tipo_vazamento = 'Sem Ponto Suspeito, ' THEN 'Ponto Não Confirmado'
                ELSE 'Pontos Confirmados'
            END
        ORDER BY id_cliente, MONTH(dt_amostra), ClassificacaoVazamento;
        """)
        
        tipo_vazamento = cursor.fetchall()

    total_amostras_results = get_total_amostras_por_mes(start_str, end_str)

    merged_results = mesclar_resultados(tipo_vazamento, total_amostras_results,clientes)

    return tipo_vazamento

def get_total_amostras_por_mes(start_date, end_date):

    
    total_amostras_results = []

    with connections['sql_server'].cursor() as cursor:
            cursor.execute(f"""
            SELECT 
                id_cliente,
                MONTH(dt_amostra) AS Mes,
                COUNT(id_amostra) as total_de_amostras 
            FROM 
                devstattus4_4fluid.dbo.amostras 
            WHERE 
                dt_amostra BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY
                id_cliente,
                MONTH(dt_amostra)
            ORDER BY
                id_cliente,
                MONTH(dt_amostra);
    """)
            
            results = cursor.fetchall()
            total_amostras_results.extend(results)
    return total_amostras_results

def mesclar_resultados(tipo_vazamento, total_amostras_results,clientes):

    dict_clientes = {id_cliente: razao for id_cliente, razao in clientes}

    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio',
        6: 'Junho', 7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro',
        11: 'Novembro', 12: 'Dezembro'
    }

    # Criar um dicionário com (id_cliente, mês) como chave e total_de_amostras como valor
    dict_total_amostras = {(id_cliente, mes): total for id_cliente, mes, total in total_amostras_results}

    # Criar a lista mesclada
    merged_results = [
        (dict_clientes[id_cliente], meses[mes], classificacao, count, dict_total_amostras.get((id_cliente, mes), None))
        for id_cliente, mes, classificacao, count in tipo_vazamento
    ]
    print(merged_results)
    return merged_results
