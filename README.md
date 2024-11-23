# Chia sẻ file theo mô hình Bittorent (P2P)

- tracker_server là một máy chủ tracker để tìm các shared_peer chứa file mà receiving_peer muốn tải dựa trên DHCP. Khi một peer đăng nhập thì tôi muốn tracker_server này hoạt động cấp IP cho các peer đăng nhập.
- Ở phần Storage, các peer sau khi đăng ký tài khoản sẽ được yêu cầu tạo một thư mục ở ổ D hoặc C vs tên là Shared_Files là nơi chứa các file có thể share.
- Mỗi 2 file thì được 1 lần tải (tính năng này có thể tạm bỏ qua ban đầu, thêm lúc sau).
- Ở phần download thì trước đó sẽ chưa có file gì hiện lên cả cho tới khi peer tìm kiếm. Lúc peer này download file của nhiều peer kia thì có thể hiện quá trình tải file.
- Yêu cầu download từ nhiều peer và chia nhỏ file.

# Repository

FILE_SHARING/
│
├── README.md
├── requirements.txt
├── main.py
├── dhcp/
│ ├── **init**.py
│ ├── dhcp_server.py
├── tracker/
│ ├── **init**.py
│ ├── server.py
│ └── database.py
├── peer/
│ ├── **init**.py
│ └── client.py
└── screens/
│ ├── download.py
│ ├── storage.py
│ ├── login.py
│ └── register.py
└── assets/
│ └── something.png
└──/

# Chi tiết

1. tracker

- server.py: Máy chủ tracker sẽ quản lý các peer, phân phối địa chỉ IP và giữ thông tin về các file được chia sẻ.
- database.py: Quản lý cơ sở dữ liệu lưu trữ thông tin về các peer và các file mà họ chia sẻ

2. peer

- client.py: chứa các phương thức xử lí việc đăng ký peer, tải file...

3. screens

- download.py:(CURRENT) Giao diện của regist_peer và download. Chứa các hàm gọi

# Tiến độ

- Đã tải được file (trên cùng một máy)
- Tạm bỏ qua DHCP
