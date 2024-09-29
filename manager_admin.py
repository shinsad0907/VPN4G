import requests

url = "https://66f957adafc569e13a9882cf.mockapi.io/Authentication"
headers = {
    "Authorization": "66f957adafc569e13a9882cf",
    "Content-Type": "application/json"
}

class Admin:
    def user_manager():
        response = requests.get(url, headers=headers)
        users = response.json()

        return users