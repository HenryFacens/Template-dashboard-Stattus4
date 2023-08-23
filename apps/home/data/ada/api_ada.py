
import requests

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

        print(data)

    except Exception as error:
        print(error)