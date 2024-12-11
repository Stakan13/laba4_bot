import requests
from config_reader import config
from requests.exceptions import ConnectionError
from Storage import Storage


class CoinAPI:

    def __init__(self):
        self.db = Storage()

    @staticmethod
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

    def add_to_storage(self):
        indexes = self.send_request()

        if indexes[0] == 'Connection failed':
            print('Cant connect')
        elif indexes[0] == 'No data for this request':
            print("Invalid request")
        else:
            for elem in indexes:
                for _, value in elem.items():
                    if config.index_id.get_secret_value() in value:
                        value = value.split("_")
                        self.db.add_index(value[-1])

    async def check_index(self):
        return self.db.indexes
