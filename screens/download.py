import tkinter as tk
from tkinter import ttk

def setup_ui(root):
    # Tạo Frame chính
    main_frame = ttk.Frame(root, padding="10")
    main_frame.place(x=0, y=0, width=500, height=600)

    # Tạo thanh tiêu đề
    download_button = ttk.Button(main_frame, text="Download", style="Accent.TButton")
    download_button.place(x=180, y=20, width=100, height=30)

    settings_button = ttk.Button(main_frame, text="⚙")
    settings_button.place(x=460, y=20, width=30, height=30)

    # Tạo ô tìm kiếm
    search_entry = ttk.Entry(main_frame, width=40)
    search_entry.place(x=50, y=70, width=350, height=30)
    
    search_button = ttk.Button(main_frame, text="🔍")
    search_button.place(x=410, y=70, width=30, height=30)

    # Tạo danh sách file
    files = [
        ("user-journey-01.pdf", "2m ago", "604KB"),
        ("Stock Photos", "3m ago", "2.20GB"),
        ("Optimised Photos", "3 days ago", "1.46MB"),
        ("Strategy-Pitch-Final.pptx", "3 days ago", "Error"),
        ("man-holding-mobile-phone-while...", "7 days ago", "929KB")
    ]
    
    y_position = 120
    for file in files:
        file_frame = ttk.Frame(main_frame)
        file_frame.place(x=50, y=y_position, width=400, height=30)
        
        name_label = ttk.Label(file_frame, text=file[0])
        name_label.place(x=0, y=0, width=200, height=30)
        
        time_label = ttk.Label(file_frame, text=file[1])
        time_label.place(x=200, y=0, width=100, height=30)
        
        size_label = ttk.Label(file_frame, text=file[2])
        size_label.place(x=300, y=0, width=50, height=30)
        
        download_button = ttk.Button(file_frame, text="⬇")
        download_button.place(x=350, y=0, width=30, height=30)
        
        if file[2] == "Error":
            retry_button = ttk.Button(file_frame, text="↻")
            retry_button.place(x=380, y=0, width=30, height=30)
            error_label = ttk.Label(file_frame, text="Error", foreground="red")
            error_label.place(x=350, y=0, width=50, height=30)

        y_position += 40

    # Nút View more
    view_more_button = ttk.Button(main_frame, text="View more")
    view_more_button.place(x=200, y=y_position, width=100, height=30)

    # Nhãn đồng bộ
    sync_label = ttk.Label(main_frame, text="Last synced: 3 mins ago")
    sync_label.place(x=180, y=y_position+40, width=200, height=30)

def main():
    root = tk.Tk()
    root.title("Download Screen")
    root.geometry("500x600")
    
    # Đặt style cho các nút Accent
    style = ttk.Style()
    style.configure("Accent.TButton", foreground="blue")
    
    setup_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
