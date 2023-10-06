
import requests
from . postgresql import get_devices_db, get_consistency, cal_hidraulica

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

        print(f"Devices  = {active_device_ids}")
        
        hidraulioc = cal_hidraulica(active_device_ids)
        # print_results(hidraulioc)
        devices_lat_long_comrate = get_devices_db(active_device_ids)
        consistencia_dados = get_consistency(active_device_ids)

        # print(devices_lat_long_comrate)
        # Dados de comunicacao
        data_conn = transform_conn(devices_lat_long_comrate)

        return devices_lat_long_comrate, data_conn, consistencia_dados, hidraulioc
    
    except Exception as error:
        print(f"Error in get_devices: {error}")
        
        return None, None, None


def print_results(data):
    # if "average_pressure_daily" in data:
    #     print("\n=== Average Pressure Daily ===")
    #     for entry in data["average_pressure_daily"]:
    #         if all(entry):
    #             print(f"Date: {entry[1]} | Device: {entry[0]} | Average Pressure: {entry[2]:.2f} | Altitude: {entry[3]:.2f}")
    #         else:
    #             print(f"Date: {entry[1]} | Device: {entry[0]} | Error: Missing data")

    # if "hydraulic_load_daily" in data:
    #     print("\n=== Hydraulic Load Daily ===")
    #     for entry in data["hydraulic_load_daily"]:
    #         if all(entry):
    #             print(f"Date: {entry[1]} | Device: {entry[0]} | Hydraulic Load: {entry[2]:.2f}")
    #         else:
    #             print(f"Date: {entry[1]} | Device: {entry[0]} | Error: Missing data")
    
    if "mvn_avg_pressure" in data:
        print("\n=== MVN Average Pressure ===")
        for entry in data["mvn_avg_pressure"]:
            if all(entry):
                print(f"Date: {entry[1]} | Device: {entry[0]} | MVN Average Pressure: {entry[2]:.2f}")
            else:
                print(f"Date: {entry[1]} | Device: {entry[0]} | Error: Missing data")

    if "mvn_hydraulic_load" in data:
        print("\n=== MVN Hydraulic Load ===")
        for entry in data["mvn_hydraulic_load"]:
            if all(entry):
                print(f"Date: {entry[1]} | Device: {entry[0]} | MVN Hydraulic Load: {entry[2]:.2f}")
            else:
                print(f"Date: {entry[1]} | Device: {entry[0]} | Error: Missing data")


#funcao para pegar os dispositivos e passar para o boletim do ada
def get_devices_ada(get_client_sub, id_cliente, date1, date2):
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

            # Adiciona os IDs dos dispositivos ativos do setor atual à lista active_device_ids
            active_device_ids.extend([dvc['dvcId'] for dvc in dvc_list if dvc['activeCms']])

        except Exception as error:
            print(f"Error in get_devices for sector {sector_id}: {error}")

    print(f"Devices = {active_device_ids}")

    hidraulioc = cal_hidraulica(active_device_ids, date1, date2)
    # consistencia_dados = get_consistency(active_device_ids)

    return hidraulioc, active_device_ids
    
def get_alarmes(get_client_sub, id_cliente):
    print(f"dentro de alarmes = {get_client_sub}")
    alarms_list = []

    for sector_id in get_client_sub:
        payload = {
            "clientId": id_cliente,
            "sectorId": sector_id
        }

        try:
            response = requests.post(API_HOST + 'alarm_note/list_all', json=payload)
            alarms_data = response.json()
            alarms_list.extend(alarms_data)  # Adicione os alarmes do setor atual à lista

        except Exception as error:
            print(f"Erro em get_alarmes para o setor {sector_id}: {error}")

    return alarms_list

def get_press(get_client_sub, id_cliente, date1, date2):
    pressure_data_list = []

    for sector_id in get_client_sub:
        payload = {
            "clientId": id_cliente,
            "sectorId": sector_id,
            "dtf": date2,
            "dti": date1
        }

        try:
            response = requests.post(API_HOST + 'devices_data/sector/pressure_data', json=payload)
            pressure_data = response.json()
            pressure_data_list.extend(pressure_data)  # Adicione os dados de pressão do setor atual à lista

        except Exception as error:
            print(f"Erro em get_press para o setor {sector_id}: {error}")

    return pressure_data_list