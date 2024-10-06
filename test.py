import urllib.parse

# Trojan URL ban đầu
trojan_url = "trojan://0026432f-9f34-4c28-877d-73d286ad454e@api2-t3.musical.ly.vina2.4gmienphi.asia:443?security=tls&sni=m.youtube.com&allowInsecure=1&type=tcp&headerType=none#%5B2%5D%E2%80%BA%20%F0%9F%87%AD%F0%9F%87%B0%20%5B2%5D%20Vina%20GGCL%20Youtube%20Trojan"

# Tách phần cấu trúc của URL
parsed_url = urllib.parse.urlparse(trojan_url)

# Giải mã phần mô tả (fragment)
fragment = urllib.parse.unquote(parsed_url.fragment)

# In fragment trước khi chỉnh sửa
print(f"Phần mô tả trước khi chỉnh sửa: {fragment}")

# Thay đổi phần mô tả tên
new_name = "[2]› 🇻🇳 [2] Vina GGCL By Vo Le Trieu Lan"
new_fragment = urllib.parse.quote(new_name)

# Tạo lại URL với tên mới
new_trojan_url = urllib.parse.urlunparse((
    parsed_url.scheme,  # trojan://
    parsed_url.netloc,  # UUID và máy chủ
    parsed_url.path,    # cổng và đường dẫn
    parsed_url.params,  # không có tham số
    parsed_url.query,   # các tham số bảo mật
    new_fragment        # fragment mới sau khi chỉnh sửa
))

# In ra URL mới
print(f"URL sau khi chỉnh sửa: {new_trojan_url}")
