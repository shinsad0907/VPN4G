import qrcode

# Thông tin chuyển khoản
ten_ngan_hang = "ABC Bank"
so_tai_khoan = "123456789"
so_tien = "1000000"
noi_dung = "Chuyển tiền cho bạn"

# Định dạng thông tin theo mẫu
thong_tin = f"BANK:{ten_ngan_hang};{so_tai_khoan};{so_tien};{noi_dung}"

# Tạo mã QR
qr = qrcode.QRCode(
    version=1,  # Độ lớn của mã QR
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Độ chính xác
    box_size=10,  # Kích thước mỗi ô
    border=4,  # Độ dày của biên
)

qr.add_data(thong_tin)
qr.make(fit=True)

# Tạo hình ảnh mã QR
img = qr.make_image(fill_color="black", back_color="white")

# Lưu mã QR vào file
img.save("ma_qr_chuyen_khoan.png")

print("Mã QR đã được tạo và lưu thành công!")
