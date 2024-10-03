from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from Authentication import Authentication
from payload import Payload
import random
from manager_admin import admin_management
import os

app = Flask(__name__)
app.secret_key = '1c2416c5bc4eba1897aa21ac6b724ee7879199dd70d1967e'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, email):
        self.id = email
        self.is_admin = False  # Default to False, will be set to True for admin

@login_manager.user_loader
def load_user(email):
    return User(email)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Thay thế với logic xác thực quản trị viên
        if Authentication().data_loginadmin(email, password):  # Giả định có một phương thức xác thực cho admin
            user = User(email)
            login_user(user)
            return redirect(url_for('admin_page'))
        else:
            flash('Thông tin đăng nhập không chính xác cho quản trị viên!')
    return render_template('loginadmin.html')

@app.route('/update_user', methods=['POST'])
def update_user():
    print(request.form)  # Kiểm tra dữ liệu form
    email = request.form.get('email')
    password = request.form.get('password')
    package = request.form.get('package')
    data_amount = request.form.get('dataAmount')
    status = request.form.get('status')
    admin_management().save_change_user(email,password,package,data_amount,status)

    print(f"Thông tin người dùng đã được cập nhật: Email={email}, Gói={package}, Trạng thái={status}")
    
    return f"Thông tin người dùng đã được cập nhật: Email={email}, Gói={package}, Trạng thái={status}"


@app.route('/update_package', methods=['POST'])
def update_package():
    # Extract form data
    package_name = request.form.get('package_name')
    price = request.form.get('price')
    duration = request.form.get('duration')
    data_limit = request.form.get('data_limit')
    speed = request.form.get('speed')
    device_limit = request.form.get('device_limit')
    support = request.form.get('support')
    sms = request.form.get('sms')
    print(support,sms)
    
    if admin_management().add_package(package_name, price, duration, data_limit, speed, device_limit,support,sms):
        return 'package added successfully'
    else:
        return 'Error in package'
    
@app.route('/edit_package', methods=['POST'])
def edit_package():
    # Extract form data
    print(request.form)
    package_name = request.form.get('package_name')
    price = request.form.get('price')
    duration = request.form.get('duration')
    data_limit = request.form.get('data_limit')
    speed = request.form.get('speed')
    device_limit = request.form.get('device_limit')
    support = request.form.get('support')
    sms = request.form.get('sms_support')
    
    if admin_management().edit_package(package_name, price, duration, data_limit, speed, device_limit,support,sms):
        return 'package added successfully'
    else:
        return 'Error in package'
    

    
@app.route('/admin_page')
@login_required
def admin_page():
    return render_template('admin.html')

@app.route('/package_management')
@login_required
def package_management():
    users = admin_management().package_management()

    return render_template('package_management.html',users=users)

@app.route('/transaction_management')
@login_required
def transaction_management():
    return render_template('transaction_management.html')

@app.route('/user_management')
@login_required
def user_management():
    
    users = admin_management().User_management()

    return render_template('User_management.html',users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        awaypassword = request.form['awaypassword']
        status_login = Authentication().data_register(email, password, awaypassword)

        if status_login == 'Gmail is using':
            flash('Email đã được đăng ký!')
        else:
            if status_login == 'User registered successfully!':
                flash('Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.')
            else:
                flash('Mật Khẩu Nhập Lại Không Giống')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        status_login = Authentication().data_login(email, password)

        if status_login == 'Login Success':
            user = User(email)
            login_user(user)
            return redirect(url_for('home_page'))
        else:
            flash('Thông tin đăng nhập không chính xác!')
    return render_template('login.html')

login_manager.login_view = 'login'

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return ('dm1lc3M6Ly9leUoySWpvaU1pSXNJbkJ6SWpvaVIxeDFNREJtTTJrNklFNWNkVEZsWXpCT0lGbFVRaUJXU1U1Qklpd2lZV1JrSWpvaU16UXVPVEl1TWpVeExqSXlNeUlzSW5CdmNuUWlPaUk0TUNJc0ltbGtJam9pT1RFNU1XRm1ZalV0T1RKbVpTMDBNVE5qTFRrME9XRXRNRGRqTlRGalpUSTFZbUZsSWl3aVlXbGtJam9pTUNJc0ltNWxkQ0k2SW5keklpd2lkSGx3WlNJNkltNXZibVVpTENKb2IzTjBJam9pWkd3dWEyZDJiaTVuWVhKbGJtRnViM2N1WTI5dElpd2ljR0YwYUNJNklsd3ZhR1J3WVhSMGRpNXdjbTh1ZG00aUxDSjBiSE1pT2lJaWZRPT0NCnZtZXNzOi8vZXlKMklqb2lNaUlzSW5Ceklqb2lVMDVKWEhWbVpqRmhUbHgxTVdWak1FNGdXVlJDSUZaSlRrRWdLeUJXU1VWVVZFVk1JaXdpWVdSa0lqb2lNelF1T1RJdU1qVXhMakl5TXlJc0luQnZjblFpT2lJNE1DSXNJbWxrSWpvaU9URTVNV0ZtWWpVdE9USm1aUzAwTVROakxUazBPV0V0TURkak5URmpaVEkxWW1GbElpd2lZV2xrSWpvaU1DSXNJbTVsZENJNkluZHpJaXdpZEhsd1pTSTZJbTV2Ym1VaUxDSm9iM04wSWpvaVpHd3VhMmQyYmk1bllYSmxibUZ1YjNjdVkyOXRJaXdpY0dGMGFDSTZJbHd2YUdSd1lYUjBkaTV3Y204dWRtNGlMQ0owYkhNaU9pSWlmUT09DQp2bWVzczovL2V5SjJJam9pTWlJc0luQnpJam9pUkdGMFlTQkRYSFV3TUdZeWJpQnNYSFV4WldFeGFWeDFabVl4WVRJNE55NDRNaUJIUWlJc0ltRmtaQ0k2SWpNMExqa3lMakkxTVM0eU1qTWlMQ0p3YjNKMElqb2lPREFpTENKcFpDSTZJamt4T1RGaFptSTFMVGt5Wm1VdE5ERXpZeTA1TkRsaExUQTNZelV4WTJVeU5XSmhaU0lzSW1GcFpDSTZJakFpTENKdVpYUWlPaUozY3lJc0luUjVjR1VpT2lKdWIyNWxJaXdpYUc5emRDSTZJbVJzTG10bmRtNHVaMkZ5Wlc1aGJtOTNMbU52YlNJc0luQmhkR2dpT2lKY0wyaGtjR0YwZEhZdWNISnZMblp1SWl3aWRHeHpJam9pSW4wPQ0Kdm1lc3M6Ly9leUoySWpvaU1pSXNJbkJ6SWpvaVVtVnpaWFFnWkdGMFlTQnpZWFZjZFdabU1XRXhOeUJPWjF4MU1EQmxNSGtpTENKaFpHUWlPaUl6TkM0NU1pNHlOVEV1TWpJeklpd2ljRzl5ZENJNklqZ3dJaXdpYVdRaU9pSTVNVGt4WVdaaU5TMDVNbVpsTFRReE0yTXRPVFE1WVMwd04yTTFNV05sTWpWaVlXVWlMQ0poYVdRaU9pSXdJaXdpYm1WMElqb2lkM01pTENKMGVYQmxJam9pYm05dVpTSXNJbWh2YzNRaU9pSmtiQzVyWjNadUxtZGhjbVZ1WVc1dmR5NWpiMjBpTENKd1lYUm9Jam9pWEM5b1pIQmhkSFIyTG5CeWJ5NTJiaUlzSW5Sc2N5STZJaUo5DQp2bWVzczovL2V5SjJJam9pTWlJc0luQnpJam9pU0Z4MU1XVmhNVzRnVTBRNklESXdMVEV3TFRJd01qUWlMQ0poWkdRaU9pSXpOQzQ1TWk0eU5URXVNakl6SWl3aWNHOXlkQ0k2SWpnd0lpd2lhV1FpT2lJNU1Ua3hZV1ppTlMwNU1tWmxMVFF4TTJNdE9UUTVZUzB3TjJNMU1XTmxNalZpWVdVaUxDSmhhV1FpT2lJd0lpd2libVYwSWpvaWQzTWlMQ0owZVhCbElqb2libTl1WlNJc0ltaHZjM1FpT2lKa2JDNXJaM1p1TG1kaGNtVnVZVzV2ZHk1amIyMGlMQ0p3WVhSb0lqb2lYQzlvWkhCaGRIUjJMbkJ5Ynk1MmJpSXNJblJzY3lJNklpSjkNCnZtZXNzOi8vZXlKMklqb2lNaUlzSW5Ceklqb2lYSFZrT0ROalhIVmtaR1k0WEhWa09ETmpYSFZrWkdWalhIVXlOVGN3WEhVeU5qQTJYSFV5TmpBMklGeDFaRGd6TlZ4MVpHTXdabHgxWkRnek5WeDFaR013TUZ4MVpEZ3pOVngxWkdNeE15QldUaUJPWEhVeFpXTXdUaUJaVkVJZ01WeDFNalpoTVZ4MVpEZ3pZMXgxWkdSbU9GeDFaRGd6WTF4MVpHUmxZeUlzSW1Ga1pDSTZJak0wTGpreUxqSTFNUzR5TWpNaUxDSndiM0owSWpvaU9EQWlMQ0pwWkNJNklqa3hPVEZoWm1JMUxUa3labVV0TkRFell5MDVORGxoTFRBM1l6VXhZMlV5TldKaFpTSXNJbUZwWkNJNklqQWlMQ0p1WlhRaU9pSjNjeUlzSW5SNWNHVWlPaUp1YjI1bElpd2lhRzl6ZENJNkltUnNMbXRuZG00dVoyRnlaVzVoYm05M0xtTnZiU0lzSW5CaGRHZ2lPaUpjTDJoa2NHRjBkSFl1Y0hKdkxuWnVJaXdpZEd4eklqb2lJbjA9DQo=')

@app.route('/api/greet', methods=['POST'])
def greet():
    data = request.json
    name = data.get('name', 'Guest')
    return jsonify({"message": f"Hello, {name}!"})

@app.route('/home_page')
@login_required
def home_page():
    package = Authentication.user_package(current_user.id)
    print(package)
    return render_template('home_page.html',current_user=current_user.id,package=package)

@app.route('/document')
@login_required
def document():
    return render_template('document.html')

@app.route('/index')
@login_required
def index():
    users = admin_management().package_management()
    return render_template('index.html',users=users)

@app.route('/payment')
@login_required
def payment():
    user_email = current_user.id
    print(request.args)
    package_name = request.args.get('package_name', 'Tối Đa 2 Gbps')
    speed = request.args.get('speed', 'Tối Đa 2 Gbps')
    storage = request.args.get('storage', '512 GB')
    device_limit = request.args.get('device_limit', 'Id: 2 Thiết Bị/Gói')
    support = request.args.get('support', 'ADR - IOS')
    price = request.args.get('price', '10,000đ')
    sms = request.args.get('sms', ' ')
    duration = request.args.get('duration', '1 Tháng')

    order_id_buy = generate_order_id()
    order_id = datetime.now().strftime("%Y%m%d%H%M%S")
    order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    package_info = {
        'package_name':package_name,
        'name': 'Gói VIP',
        'speed': speed,
        'data': storage,
        'devices': device_limit,
        'support': support,
        'sms': sms,
        'price': price,
        'order_id_buy': order_id_buy,
        'duration':duration
    }

    session['payment_user'] = {
        'email': user_email,
        'order_id': order_id,
        'package': package_info,
        'time': order_time,
    }

    return render_template('payment.html', order_id_buy=order_id_buy, order_id=order_id, order_time=order_time, package=package_info)

def generate_order_id():
    time_component = datetime.now().strftime("%Y%m%d%H%M%S")
    random_component = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return time_component + random_component

@app.route('/QR')
@login_required
def QR():
    payment_info = session.get('payment_user')
    type = payment_info['package']['name']
    order_id = payment_info['package']['order_id_buy']
    price = payment_info['package']['price']
    package_name = request.args.get('package_name', '1 Tháng')
    money_transfer_content = current_user.id

    user_email = current_user.id
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    data = Payload().payload(current_time, user_email, type, order_id)
    if 'paying' in data and data['paying']:
        for payment in data['paying']:
            if payment_info['package']['name'] == payment['type']:
                order_time = payment['datetime']
                order_id_buy = payment['order_id_buy']
                break
        else:
            order_time = current_time
            order_id_buy = order_id
    else:
        order_time = current_time
        order_id_buy = order_id

    order_time = datetime.strptime(order_time, '%Y-%m-%d %H:%M:%S')
    time_remaining = (order_time + timedelta(minutes=30)) - now
    
    if time_remaining.total_seconds() < 0:
        time_remaining_seconds = 0
    else:
        time_remaining_seconds = int(time_remaining.total_seconds())

    return render_template('QR.html', time_remaining_seconds=time_remaining_seconds, package_info=order_id_buy, price=price,money_transfer_content=money_transfer_content,package_name=package_name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
