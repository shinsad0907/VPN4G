import requests
import json

class API_package:
    def __init__(self) -> None:
        url = 'https://66faae498583ac93b4096ce6.mockapi.io/API'
        self.response = requests.get(url).text
    def get_package(self):
        print(json.load(self.response))

API_package().get_package()