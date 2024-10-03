import requests
import json

class API_package:
    def __init__(self) -> None:
        url = 'https://66faae498583ac93b4096ce6.mockapi.io/API'
        self.datas = requests.get(url).json()

    def get_package(self,token):
        for data in self.datas:
            if data['token'] == token:
                return data['package']
# API_package().get_package()

# Fixing padding by adding '=' as necessary

# import base64

# # Chuỗi đã giải mã từ đoạn mã trước
# decoded_string = """vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIlNOSVx1RkYxQU5cdTFFQzBOIFlUQiBWSU5BIFx1MDAyQiBWSUVUVEVMIiwNCiAgImFkZCI6ICIzNC45Mi4yNTEuMjIzIiwNCiAgInBvcnQiOiAiODAiLA0KICAiaWQiOiAiOTE5MWFmYjUtOTJmZS00MTNjLTk0OWEtMDdjNTFjZTI1YmFlIiwNCiAgImFpZCI6ICIwIiwNCiAgInNjeSI6ICJhdXRvIiwNCiAgIm5ldCI6ICJ3cyIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICJkbC5rZ3ZuLmdhcmVuYW5vdy5jb20iLA0KICAicGF0aCI6ICIvaGRwYXR0di5wcm8udm4iLA0KICAidGxzIjogIiIsDQogICJzbmkiOiAiIiwNCiAgImFscG4iOiAiIiwNCiAgImZwIjogIiINCn0=
# vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIkRhdGEgQ1x1MDBGMm4gbFx1MUVBMWlcdUZGMUEzMDAuMDAwIEdCIiwNCiAgImFkZCI6ICIzNC45Mi4yNTEuMjIzIiwNCiAgInBvcnQiOiAiODAiLA0KICAiaWQiOiAiOTE5MWFmYjUtOTJmZS00MTNjLTk0OWEtMDdjNTFjZTI1YmFlIiwNCiAgImFpZCI6ICIwIiwNCiAgInNjeSI6ICJhdXRvIiwNCiAgIm5ldCI6ICJ3cyIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICJkbC5rZ3ZuLmdhcmVuYW5vdy5jb20iLA0KICAicGF0aCI6ICIvaGRwYXR0di5wcm8udm4iLA0KICAidGxzIjogIiIsDQogICJzbmkiOiAiIiwNCiAgImFscG4iOiAiIiwNCiAgImZwIjogIiINCn0=
# vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIlJlc2V0IGRhdGEgc2F1XHVGRjFBNyBOZ1x1MDBFMHkiLA0KICAiYWRkIjogIjM0LjkyLjI1MS4yMjMiLA0KICAicG9ydCI6ICI4MCIsDQogICJpZCI6ICI5MTkxYWZiNS05MmZlLTQxM2MtOTQ5YS0wN2M1MWNlMjViYWUiLA0KICAiYWlkIjogIjAiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogIndzIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogImRsLmtndm4uZ2FyZW5hbm93LmNvbSIsDQogICJwYXRoIjogIi9oZHBhdHR2LnByby52biIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICIiLA0KICAiYWxwbiI6ICIiLA0KICAiZnAiOiAiIg0KfQ==
# vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIlx1RDgzQ1x1RERGOFx1RDgzQ1x1RERFQ1x1MjU3MFx1MjYwNlx1MjYwNiBcdUQ4MzVcdURDMEZcdUQ4MzVcdURDMDBcdUQ4MzVcdURDMTMgVk4gTlx1MUVDME4gWVRCIDFcdTI2QTFcdUQ4M0NcdURERjhcdUQ4M0NcdURERUMiLA0KICAiYWRkIjogIjM0LjkyLjI1MS4yMjMiLA0KICAicG9ydCI6ICI4MCIsDQogICJpZCI6ICI5MTkxYWZiNS05MmZlLTQxM2MtOTQ5YS0wN2M1MWNlMjViYWUiLA0KICAiYWlkIjogIjAiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogIndzIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogImRsLmtndm4uZ2FyZW5hbm93LmNvbSIsDQogICJwYXRoIjogIi9oZHBhdHR2LnByby52biIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICIiLA0KICAiYWxwbiI6ICIiLA0KICAiZnAiOiAiIg0KfQ==
# vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIkdcdTAwRjNpOiBOXHUxRUMwTiBZVEIgVklOQSIsDQogICJhZGQiOiAiMzQuOTIuMjUxLjIyMyIsDQogICJwb3J0IjogIjgwIiwNCiAgImlkIjogIjkxOTFhZmI1LTkyZmUtNDEzYy05NDlhLTA3YzUxY2UyNWJhZSIsDQogICJhaWQiOiAiMCIsDQogICJzY3kiOiAiYXV0byIsDQogICJuZXQiOiAid3MiLA0KICAidHlwZSI6ICJub25lIiwNCiAgImhvc3QiOiAiZGwua2d2bi5nYXJlbmFub3cuY29tIiwNCiAgInBhdGgiOiAiL2hkcGF0dHYucHJvLnZuIiwNCiAgInRscyI6ICIiLA0KICAic25pIjogIiIsDQogICJhbHBuIjogIiIsDQogICJmcCI6ICIiDQp9
# """

# def encode_to_base64(decoded_string):
#     # Mã hóa chuỗi thành bytes
#     bytes_string = decoded_string.encode('utf-8')
#     # Mã hóa bytes thành chuỗi base64
#     encoded_string = base64.b64encode(bytes_string)
#     return encoded_string.decode('utf-8')

# # Mã hóa lại chuỗi đã giải mã
# encoded_string = encode_to_base64(decoded_string)

# print(encoded_string)
