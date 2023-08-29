
import requests
from . postgresql import get_devices_db

API_HOST = "https://api-sistemas.stattus4.com/4fluid/iot/ada/"

def transform_conn(data):
    # Inicializa o dicionário de dispositivos
    devices = {}
    for item in data:
        device_id = item['device_id']
        serial_number = item['serial_number']
        # Verifica se timestamp não é None antes de acessar .date()
        timestamp = item['timestamp'].date().strftime('%Y-%m-%d') if item['timestamp'] else None
        conn_evt = item['conn_evt']
        conn_rate = item['conn_rate']

        if not timestamp:
            continue

        if device_id not in devices:
            devices[device_id] = {
                'serial_number': serial_number,  # Armazena o serial_number no dicionário
                'communications': {},
                'total_conn_rate': 0,
                'count_conn_rate': 0
            }

        # Armazena conn_evt para o timestamp correspondente
        devices[device_id]['communications'][timestamp] = conn_evt
        # Acumula conn_rate para o cálculo da média
        devices[device_id]['total_conn_rate'] += conn_rate
        devices[device_id]['count_conn_rate'] += 1

    # Calcula a média de conn_rate para cada dispositivo
    for device_id, device_data in devices.items():
        avg_conn_rate = device_data['total_conn_rate'] / device_data['count_conn_rate']
        devices[device_id]['avg_conn_rate'] = avg_conn_rate
        del devices[device_id]['total_conn_rate']
        del devices[device_id]['count_conn_rate']

    # Transforma o dicionário em uma lista de dispositivos
    result = [{"device_id": device_id, **device_data} for device_id, device_data in devices.items()]
    print(result)
    return result

def get_sector(id_client):

    print(f'ID do cliente  = {id_client}')

    payload = {
        "clientId": id_client
    }

    try:
        response = requests.post(API_HOST + 'sector/all', json=payload)

        data = response.json()

        extracted_data = [{"sectorId": item["sectorId"], "sectorName": item["sectorName"]}
                          for item in data if "sectorId" in item and "sectorName" in item]

        return extracted_data

    except Exception as error:
        print(error)
        return []

def get_devices(get_client_sub, id_cliente):

    payload = {
    "clientId": id_cliente,
    "sectorId": get_client_sub
    }  

    try:
        response = requests.post(API_HOST + 'sector/scheme', json=payload)

        data = response.json()
        dvc_list = data['dvcList']

        active_device_ids = [dvc['dvcId'] for dvc in dvc_list if dvc['activeCms']]
        
        devices_lat_long_comrate = get_devices_db(active_device_ids)
        print(devices_lat_long_comrate)
        # Dados de comunicacao
        data_conn = transform_conn(devices_lat_long_comrate)

        return devices_lat_long_comrate, data_conn
    
    except Exception as error:
        print(error)
        
        return []
