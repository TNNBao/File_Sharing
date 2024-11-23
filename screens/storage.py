import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

def setup_ui(root):
    # Tạo Frame chính
    main_frame = ttk.Frame(root, padding="10")
    main_frame.place(x=10, y=20, width=360, height=300)

    # Thông tin người dùng
    user_image = PhotoImage(file=r"assets/images/auth.png")  # Đặt đường dẫn đến ảnh của bạn
    user_image_label = tk.Label(main_frame, image=user_image)
    user_image_label.image = user_image  # Giữ tham chiếu đến ảnh để không bị xóa
    user_image_label.place(x=10, y=10, width=50, height=50)

    user_name_label = ttk.Label(main_frame, text="Laura Eddy", font=("Helvetica", 12, "bold"))
    user_name_label.place(x=70, y=10)

    user_email_label = ttk.Label(main_frame, text="info@lauraeddy.com.au", font=("Helvetica", 10))
    user_email_label.place(x=70, y=30)

    settings_button = ttk.Button(main_frame, text="⚙")
    settings_button.place(x=320, y=10, width=30, height=30)

    # Storage thông tin
    storage_label = ttk.Label(main_frame, text="Storage", font=("Helvetica", 10, "bold"))
    storage_label.place(x=10, y=70)

    storage_info_label = ttk.Label(main_frame, text="84GB OF 120GB", font=("Helvetica", 10))
    storage_info_label.place(x=10, y=90)

    storage_progress = ttk.Progressbar(main_frame, length=300, mode="determinate")
    storage_progress.place(x=10, y=110, width=340, height=10)
    storage_progress["value"] = 70  # Đặt giá trị của thanh tiến trình

    # Đường kẻ ngang
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.place(x=10, y=140, width=340)

    # Storage location
    location_label = ttk.Label(main_frame, text="Storage location", font=("Helvetica", 10, "bold"))
    location_label.place(x=10, y=170)

    location_info_label = ttk.Label(main_frame, text="C: Laura\\My Documents", font=("Helvetica", 10))
    location_info_label.place(x=10, y=190)

    change_button = ttk.Button(main_frame, text="Change")
    change_button.place(x=270, y=175, width=60, height=30)

    # Nút Upgrade
    upgrade_button = ttk.Button(main_frame, text="Upgrade", style="Accent.TButton")
    upgrade_button.place(x=230, y=230, width=100, height=30)


def main():
    root = tk.Tk()
    root.title("Settings")
    root.geometry("400x320")
    root.resizable(False, False)
    
    # Đặt style cho các nút Accent
    style = ttk.Style()
    style.configure("Accent.TButton", foreground="black", background="#4A90E2")
    
    setup_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
