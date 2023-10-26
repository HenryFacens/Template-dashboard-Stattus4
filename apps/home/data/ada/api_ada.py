
import requests
from . postgresql import get_devices_db, get_consistency, cal_hidraulica
import pandas as pd

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
    # print(result)
    return result

def get_sector(id_client):

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

        dataZmax = get_ref(get_client_sub, id_cliente)
        hidraulioc = cal_hidraulica(active_device_ids,dataZmax)

        hydraulic_data_mvn_df = pd.DataFrame(hidraulioc['mvn_hydraulic_load'], columns=['device_id', 'date', 'hydraulic_load'])

        pivot_hydraulic_load = hydraulic_data_mvn_df.pivot(index='date', columns='device_id', values='hydraulic_load')

        correlation_matrix = pivot_hydraulic_load.corr()

        correlation_matrix_json = correlation_matrix.to_json(orient='split')

        devices_lat_long_comrate = get_devices_db(active_device_ids)
        consistencia_dados = get_consistency(active_device_ids)

        data_conn = transform_conn(devices_lat_long_comrate)

        return devices_lat_long_comrate, data_conn, consistencia_dados, hidraulioc, correlation_matrix_json
    
    except Exception as error:
        print(f"Error in get_devices: {error}")
        
        return None, None, None


#funcao para pegar os dispositivos e passar para o boletim do ada
def get_devices_ada(get_client_sub, id_cliente):
    print(get_client_sub)
    print(id_cliente)

    active_device_ids = []

    for sector_id in get_client_sub:
        payload = {
            "clientId": id_cliente,
            "sectorId": sector_id
        }

        try:
            response = requests.post(API_HOST + 'sector/scheme', json=payload)

            data = response.json()
            dvc_list = data['dvcList']

            active_device_ids.extend([dvc['dvcId'] for dvc in dvc_list if dvc['activeCms']])

        except Exception as error:
            print(f"Error in get_devices for sector {sector_id}: {error}")

    
    return active_device_ids
    
def get_alarmes(get_client_sub,id_cliente):
    print(f"dentro de{get_client_sub}")
    payload = {
        "clientId": id_cliente,
        "sectorId": get_client_sub
        }
    try:
        response = requests.post(API_HOST + 'alarm_note/list_all', json=payload )
        return response.json()
    except Exception as error:
        print(f"erro  = {error}")


def get_ref(get_client_sub, id_cliente):
    payload = {
        "clientId": id_cliente,
        "sectorId": get_client_sub
        }

    try:
        response = requests.post(API_HOST + 'sector/general_infos', json=payload)

        data = response.json()

        return  data.pop('zmax', None)
    
    except Exception as error:
        print(f"erro  = {error}")