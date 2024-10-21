# Chia sẻ file theo mô hình Bittorent (P2P)

- tracker_server là một máy chủ tracker để tìm các shared_peer chứa file mà receiving_peer muốn tải dựa trên DHCP. Khi một peer đăng nhập thì tôi muốn tracker_server này hoạt động cấp IP cho các peer đăng nhập.
- Ở phần Storage, các peer sau khi đăng ký tài khoản sẽ được yêu cầu tạo một thư mục ở ổ D hoặc C vs tên là Shared_Files là nơi chứa các file có thể share.
- Mỗi 2 file thì được 1 lần tải (tính năng này có thể tạm bỏ qua ban đầu, thêm lúc sau).
- Ở phần download thì trước đó sẽ chưa có file gì hiện lên cả cho tới khi peer tìm kiếm. Lúc peer này download file của nhiều peer kia thì có thể hiện quá trình tải file.
- Yêu cầu download từ nhiều peer và chia nhỏ file.

# Repository

bittorrent_project/
│
├── README.md
├── requirements.txt
├── main.py
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
└── images/
│ └── something.png
└──/

# Chi tiết

1. tracker

- server.py: Máy chủ tracker sẽ quản lý các peer, phân phối địa chỉ IP và giữ thông tin về các file được chia sẻ.
- database.py: Quản lý cơ sở dữ liệu lưu trữ thông tin về các peer và các file mà họ chia sẻ

# Các bước cần làm tiếp theo

1. Đăng ký và Hủy đăng ký với Máy chủ Tracker:

- Thiết kế logic gửi và nhận thông tin giữa peer và máy chủ tracker.

2. Chia sẻ File:

- Thiết kế máy chủ nhỏ trên peer để lắng nghe và xử lý các yêu cầu tải file từ các peer khác.

3. Tải File từ Peer khác:

- Thiết kế logic tìm kiếm file trên máy chủ tracker và tải file từ các peer khác.

4. Cập nhật Giao diện Người dùng:

- Cập nhật giao diện để hiển thị thông tin chia sẻ file và tiến trình tải file.
