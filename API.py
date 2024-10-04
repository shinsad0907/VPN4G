import requests
import json
import base64
import ast


class API_package:
    def __init__(self) -> None:
        self.API = "https://66faae498583ac93b4096ce6.mockapi.io/API"
        self.headers_API = {
            "Authorization": "66faae498583ac93b4096ce6",
            "Content-Type": "application/json"
        }

        self.url_package_management = "https://66faae498583ac93b4096ce6.mockapi.io/package_management"
        self.headers_package_management = {
            "Authorization": "66faae498583ac93b4096ce6",
            "Content-Type": "application/json"
        }

        self.api = 'https://66faae498583ac93b4096ce6.mockapi.io/API'
        self.headers_api = {
            "Authorization": "66faae498583ac93b4096ce6",
            "Content-Type": "application/json"
        }
    def get_package(self, token):
        self.datas = requests.get(self.API,headers=self.headers_API).json()
        for data in self.datas:
            if data['token'] == token:
                print(data['data_package'])
                return data['data_package']
            
    def save_newdatepackage(self, dataname, packageFiles, dataLink, token):
        packages = requests.get(self.url_package_management,headers=self.headers_package_management).json()
        data_new = requests.get(dataLink).text
        # Decode data_new to get the file data  
        edit_datanew = self.edit_datanew(data_new)
        print(edit_datanew)
        for package in packages:
            if package['package_name'] == packageFiles:
                new_package = {
                    'dataname':dataname,
                    'package_name': packageFiles,
                    'dataLink': dataLink,
                    'data_package': edit_datanew,
                    'data_limit': package['data_limit'],
                    'device_limit': package['device_limit'].split('Id: ')[1].split(' Thiết bị/Gói')[0],
                    'token':token
                }
                break
        requests.post(self.api, headers=self.headers_api, json=new_package)

        
        # second_decoding

    def decode_datanew(self, data_new):
        def fix_base64_padding(encoded_string):
            # Calculate how many '=' are needed
            padding_needed = len(encoded_string) % 4
            if padding_needed:
                encoded_string += '=' * (4 - padding_needed)
            return encoded_string

        # Fix the padding for the given encoded string
        fixed_encoded_string = fix_base64_padding(data_new)

        # Decoding the base64 string again
        decoded_bytes = base64.b64decode(fixed_encoded_string)
        decoded_string = decoded_bytes.decode('utf-8', errors='ignore')

        return self.decode_datenew_level_2(decoded_string)
    
    def decode_datenew_level_2(self, data_decode_second):
        vmess_string = data_decode_second
        data_new = []

        for vmess_new in vmess_string.split():
            # Extract the base64 encoded string from the vmess format
            if vmess_new.startswith("vmess://"):
                base64_string = vmess_new[8:]  # Remove the "vmess://" prefix
            else:
                raise ValueError("Invalid string, does not start with 'vmess://'")

            # Decode the base64 string
            decoded_bytes = base64.b64decode(base64_string)
            decoded_json_string = decoded_bytes.decode('utf-8')

            # Convert the JSON string into a JSON object
            vmess_data = json.loads(decoded_json_string)

            # Append the result
            data_new.append(vmess_data)

        return data_new
    
    def edit_datanew(self, data_new):
        try:
            file_edit = self.decode_datanew(data_new)
        except:
            file_edit = self.decode_datenew_level_2(data_new)
            
        file_edit_new = []

        for item in file_edit:
            # Modify the 'ps' field and reformat the dictionary
            modified_item = {
                'v': item['v'], 
                'ps': f'{item["ps"]} By ShinNohope', 
                'add': item['add'], 
                'port': item['port'], 
                'id': item['id'], 
                'aid': item['aid'], 
                'net': item['net'], 
                'type': item['type'], 
                'host': item['host'], 
                'path': item['path'],
                'tls': item['tls']
            }
            file_edit_new.append(modified_item)
        
        return self.encode_part_1(file_edit_new)

    def encode_part_1(self, vmess_data_list):
        vmess_base64_list = []
        for vmess_data in vmess_data_list:
            # Convert the Python dictionary back to JSON string
            vmess_json_string = json.dumps(vmess_data)
            # Encode the JSON string into base64
            vmess_base64 = base64.b64encode(vmess_json_string.encode('utf-8')).decode('utf-8')
            # Append the encoded string with "vmess://" prefix
            vmess_base64_list.append(f"vmess://{vmess_base64}")

        # Join all the vmess strings into a single string separated by newlines
        vmess_combined = "\n".join(vmess_base64_list)
        print(vmess_combined)

        return self.encode_to_base64(vmess_combined)

    def encode_to_base64(self, decoded_string):
        # Encode the decoded string back to base64
        bytes_string = decoded_string.encode('utf-8')
        encoded_string = base64.b64encode(bytes_string).decode('utf-8')
        return encoded_string
