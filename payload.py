import json
import requests
from datetime import datetime, timedelta

url = "https://66f957adafc569e13a9882cf.mockapi.io/Payloads"
headers = {
    "Authorization": "66f957adafc569e13a9882cf",
    "Content-Type": "application/json"
}

class Payload:
    def payload(self, current_time, user_email, type, order_id):
        new_payload = {
            "order_id_buy": order_id,
            "datetime": current_time,
            "type": type
        }
        print(new_payload)

        # Lấy dữ liệu người dùng từ API
        response = requests.get(url, headers=headers)
        users = response.json()
        
        # Tìm kiếm dữ liệu người dùng theo email
        user_data = next((user for user in users if user['user'] == user_email), None)

        if user_data:
            history = user_data.get('history', {})  # Chỉ lấy 'history'

            # Đảm bảo 'paying' và 'payed' tồn tại trong lịch sử
            history.setdefault('paying', [])
            history.setdefault('payed', [])

            # Kiểm tra xem giao dịch cũ có trùng với giao dịch mới và có quá 30 phút chưa
            for payment in history['paying']:
                if payment['type'] == type:
                    data_time = datetime.strptime(payment['datetime'], '%Y-%m-%d %H:%M:%S')
                    if (datetime.now() - data_time) > timedelta(minutes=30):
                        # Di chuyển giao dịch từ 'paying' sang 'payed'
                        history['payed'].append(payment)
                        history['paying'].remove(payment)
                        history['paying'].append(new_payload)
                        self._save_data(user_data['id'], {"history": history})  # Chỉ lưu 'history'
                        return new_payload
                    else:
                        return history

            # Nếu không có giao dịch tương tự, thêm giao dịch mới vào 'paying'
            history['paying'].append(new_payload)
            self._save_data(user_data['id'], {"history": history})  # Chỉ lưu 'history'
            return new_payload
        else:
            # Nếu người dùng chưa tồn tại, tạo người dùng mới với lịch sử
            new_user = {
                "user": user_email,
                "status": "active",
                "history": {
                    "paying": [new_payload],
                    "payed": []
                }
            }
            self._save_data(None, new_user)
            return new_payload

    def _save_data(self, user_id, data):
        if user_id:
            # Cập nhật dữ liệu cho người dùng đã tồn tại
            response = requests.put(f"{url}/{user_id}", headers=headers, json=data)
        else:
            # Tạo mới người dùng nếu không tìm thấy
            response = requests.post(url, headers=headers, json=data)

        if response.status_code not in [200, 201]:
            print(f"Error saving data: {response.text}")
