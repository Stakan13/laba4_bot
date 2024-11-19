import requests
from config_reader import config
from requests.exceptions import ConnectionError


def send_request(added_data=""):
    url = str(config.indexes_url.get_secret_value()) + added_data

    payload = {}
    headers = {
      'Accept': 'text/plain',
      'X-CoinAPI-Key': f'{config.api_key.get_secret_value()}'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 550 or response.status_code == 404:
            raise ValueError
        else:
            return response.json()
    except ValueError:
        return ["No data for this request"]
    except ConnectionError:
        return ["Connection failed"]

