# Web_QuanLyDuLich
### Cách để khởi động chương trình:

  1. Hãy Clone Project Web_QuanLyDuLich về file mong muốn.
  2. Mở MySQL Workbench, tạo 1 cơ sở dữ liệu mới (new schema) với tên là `doan` (Name:) và Charset/Collation: `utf8mb4` / `utf8mb4_unicode_ci`.
  3. Mở Project `Web_QuanLyDuLich` bằng PyCharm. Đề xuất sử dụng `python 3.10.8`.
  4. Hãy thay thế mật khẩu root của MySQL trong file `_init_.py` và `main.py` trong hàng code `app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Mật khẩu root@localhost/doan?charset=utf8mb4"`.
  5. Trong PyCharm, mở Terminal và nhập lệnh `pip install -r requirements.txt` để cài đặt, cập nhật các yêu cầu cần có để chạy.
  6. Chạy file `models.py` bằng cách chuột phải vào file và nhấn `Run models`.
  7. Chạy file `main.py` bằng cách chuột phải vào file và nhấn `Run main`. 
  8. Cuối cùng, nhấn vào đường link trong cửa sổ run để mở web bằng trình duyệt.
