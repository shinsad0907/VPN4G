import requests

url = "https://neko4gvpn.pro.vn/api/v1/client/subscribe?token=bc61d007b46e3fb9724c50057ceb0fe6"


response = requests.get(url)
print(response.text)
