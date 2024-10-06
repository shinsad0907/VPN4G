import requests
import json
import base64
import urllib.parse
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
            print(package)
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

    def update_package(self,token):
        response = requests.get(self.api, headers=self.headers_api)
        if response.status_code != 200:
            print(f"Lỗi khi lấy gói dữ liệu: {response.status_code}")
            return

        file_packages = response.json()

        # Duyệt qua từng gói và kiểm tra token
        for file_package in file_packages:
            if file_package['token'] == token:
                # Lấy dữ liệu từ dataLink
                data_response = requests.get(file_package['dataLink'])
                if data_response.status_code != 200:
                    print(f"Lỗi khi lấy dữ liệu: {data_response.status_code}")
                    return
                
                data = data_response.text
                print(f"Dữ liệu lấy được: {data}")
                
                # Chỉnh sửa dữ liệu mới
                edit_datanew = self.edit_datanew(data)
                print(f"Dữ liệu sau khi chỉnh sửa: {edit_datanew}")
                
                # Chuẩn bị gói dữ liệu để cập nhật
                new_package = {
                    'data_package': edit_datanew,
                }
                
                # Gửi yêu cầu PUT để cập nhật
                user_url = f"{self.api}/{file_package['id']}"
                response_put = requests.put(user_url, json=new_package, headers=self.headers_api)
                
                if response_put.status_code == 200:
                    print("Cập nhật thành công:", response_put.json())
                else:
                    print(f"Lỗi khi cập nhật: {response_put.status_code} - {response_put.text}")
                return

        # Nếu không tìm thấy token khớp
        print(f"Không tìm thấy gói dữ liệu với token: {token}")



    def decode_datanew(self, data_new):
        def fix_base64_padding(encoded_string):
            # Tính toán số lượng padding '=' cần thêm
            padding_needed = len(encoded_string) % 4
            if padding_needed:
                encoded_string += '=' * (4 - padding_needed)
            return encoded_string

        # Sửa lại chuỗi base64 nếu thiếu padding
        fixed_encoded_string = fix_base64_padding(data_new)

        # Giải mã chuỗi base64
        try:
            decoded_bytes = base64.b64decode(fixed_encoded_string)
            decoded_string = decoded_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            raise ValueError(f"Error decoding base64: {e}")

        # Gọi hàm cấp 2 để tiếp tục xử lý
        return self.decode_datenew_level_2(decoded_string)

    def decode_datenew_level_2(self, data_decode_second):
        vmess_string = data_decode_second
        data_new = []

        for vmess_new in vmess_string.split():
            if vmess_new.startswith("vmess://"):
                # Phần xử lý chuỗi vmess đã có, giữ nguyên như ban đầu
                base64_string = vmess_new[8:]  # Bỏ phần "vmess://"
                base64_string = self.fix_base64_padding(base64_string)

                try:
                    decoded_bytes = base64.b64decode(base64_string)
                    decoded_json_string = decoded_bytes.decode('utf-8')
                except Exception as e:
                    raise ValueError(f"Error decoding vmess base64: {e}")

                try:
                    vmess_data = json.loads(decoded_json_string)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Error decoding JSON: {e}")

                data_new.append(vmess_data)
            
            elif vmess_new.startswith("trojan://"):
                # Phần xử lý chuỗi trojan thêm vào đây
                trojan_url = vmess_new
                parsed_url = urllib.parse.urlparse(trojan_url)
                
                # Decode các phần của URL
                trojan_id = parsed_url.username
                host = parsed_url.hostname
                port = parsed_url.port
                query = urllib.parse.parse_qs(parsed_url.query)
                fragment = urllib.parse.unquote(parsed_url.fragment)

                # Thêm dữ liệu trojan vào danh sách
                trojan_data = {
                    "protocol": "trojan",
                    "id": trojan_id,
                    "host": host,
                    "port": port,
                    "query": query,
                    "name": fragment
                }
                data_new.append(trojan_data)

        return data_new

    def fix_base64_padding(self, encoded_string):
        padding_needed = len(encoded_string) % 4
        if padding_needed:
            encoded_string += '=' * (4 - padding_needed)
        return encoded_string

    def checkdata(self, data_new):
        try:
            file_edit = self.decode_datanew(data_new)
        except:
            file_edit = self.decode_datenew_level_2(data_new)

        for item in file_edit:
            print(item)

    def edit_datanew(self, data_new):
        try:
            file_edit = self.decode_datanew(data_new)
        except:
            file_edit = self.decode_datenew_level_2(data_new)

        file_edit_new = []

        for item in file_edit:
            if item.get("protocol") == "trojan":
                # Chỉnh sửa phần tên cho trojan
                item["name"] = f'{item["name"]} By ShinNohope'
            else:
                # Chỉnh sửa 'ps' cho vmess
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
            
            file_edit_new.append(item)

        return self.encode_part_1(file_edit_new)

    def encode_part_1(self, data_list):
        encoded_list = []
        for item in data_list:
            if item.get("protocol") == "trojan":
                # Mã hóa lại trojan URL
                query = urllib.parse.urlencode(item['query'], doseq=True)
                fragment = urllib.parse.quote(item['name'])
                trojan_url = f"trojan://{item['id']}@{item['host']}:{item['port']}?{query}#{fragment}"
                encoded_list.append(trojan_url)
            else:
                # Mã hóa lại vmess
                vmess_json_string = json.dumps(item)
                vmess_base64 = base64.b64encode(vmess_json_string.encode('utf-8')).decode('utf-8')
                encoded_list.append(f"vmess://{vmess_base64}")

        combined_encoded = "\n".join(encoded_list)
        print(combined_encoded)

        return self.encode_to_base64(combined_encoded)

    def encode_to_base64(self, decoded_string):
        bytes_string = decoded_string.encode('utf-8')
        encoded_string = base64.b64encode(bytes_string).decode('utf-8')
        return encoded_string