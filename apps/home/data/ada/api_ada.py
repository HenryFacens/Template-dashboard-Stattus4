
import requests
from . postgresql import get_devices_db

API_HOST = "https://api-sistemas.stattus4.com/4fluid/iot/ada/"


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

        return devices_lat_long_comrate
    
    except Exception as error:
        print(error)
        
        return []
