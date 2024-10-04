import requests

class admin_management:
    def __init__(self) -> None:
        self.url = "https://66f957adafc569e13a9882cf.mockapi.io/Authentication"
        self.headers = {
            "Authorization": "66f957adafc569e13a9882cf",
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

    def User_management(self):
        self.users = requests.get(self.url, headers=self.headers).json()
        self.packages = requests.get(self.url_package_management, headers=self.headers_package_management).json()
        self.data_packages = requests.get(self.api, headers=self.headers_api).json()

        return self.users,self.packages,self.data_packages
    def save_change_user(self,email,password,package,data_amount,status):
        self.User_management()
        self.data_packages = requests.get(self.api, headers=self.headers_api).json()
        for user in self.users:
            if user['gmail'] == email:
                for data_package in self.data_packages:
                    if data_package['dataname'] == data_amount:
                        data = {
                            "password": password,
                            "package": f'https://vpn-4-g.vercel.app/api/v1/client/subscribe?token={data_package['token']}',
                            "service": package,
                            "status": status
                        }
                        print(345345345345345345345)
                        # Tạo URL cho bản ghi cụ thể
                        user_url = f"{self.url}/{user['id']}"
                        print(user_url)
                        # Cập nhật toàn bộ bản ghi bằng phương thức PUT
                        response_put = requests.put(user_url, json=data, headers=self.headers)

                        # Kiểm tra phản hồi
                        if response_put.status_code == 200:
                            print("Cập nhật thành công:", response_put.json())
                        else:
                            print("Lỗi khi cập nhật:", response_put.status_code)
                        return  # Kết thúc vòng lặp nếu đã tìm thấy người dùng và cập nhật

        print("Không tìm thấy người dùng với email:", email)

    def package_management(self):
        response = requests.get(self.url_package_management, headers=self.headers_package_management)
        self.packages = response.json()

        return self.packages
    
    def add_package(self,package_name, price, duration, data_limit, speed, device_limit,support,sms):

        new_package = {
                'package_name': package_name,
                'price': price,
                'duration': duration,
                'data_limit': data_limit,
                'speed': speed,
                'device_limit': device_limit,
                'support': support,
                'sms': sms
            }
        response = requests.post(self.url_package_management, headers=self.headers_package_management, json=new_package)
        if response.status_code == 201:  # Kiểm tra nếu tạo mới thành công
            status = True
        else:
            status = False
        return status

    def edit_package(self,package_name, price, duration, data_limit, speed, device_limit,support,sms):
        self.package_management()
        new_package = {
                'package_name': package_name,
                'price': price,
                'duration': duration,
                'data_limit': data_limit,
                'speed': speed,
                'device_limit': device_limit,
                'support': support,
                'sms': sms
            }

        for package in self.packages:
            if package['package_name'] == package_name:
                print(new_package)
                user_url = f"{self.url_package_management}/{package['id']}"
                
                # Cập nhật toàn bộ bản ghi bằng phương thức PUT
                response_put = requests.put(user_url, json=new_package, headers=self.headers_package_management)

                # Kiểm tra phản hồi
                if response_put.status_code == 200:
                    print("Cập nhật thành công:", response_put.json())
                else:
                    print("Lỗi khi cập nhật:", response_put.status_code)
                return  # Kết thúc vòng lặp nếu đã tìm thấy người dùng và cập nhật