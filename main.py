import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
from typing import Callable

# Hằng số
MAU_NEN_XAM = "#F0F0F0"
MAU_CHU_DEN = "#333333"
DUONG_DAN_THU_MUC_HIEN_HANH = os.path.dirname(os.path.abspath(__file__))

class UngDungChinh(tk.Tk):
    def __init__(self):
        super().__init__()
        CHIEU_RONG_CUA_SO = 400  
        CHIEU_DAI_CUA_SO = 250
        CHIEU_RONG_MAN_HINH = self.winfo_screenwidth()
        CHIEU_DAI_MAN_HINH = self.winfo_screenheight()
        toa_do_x = (CHIEU_RONG_MAN_HINH // 2) - (CHIEU_RONG_CUA_SO // 2)
        toa_do_y = (CHIEU_DAI_MAN_HINH // 2) - (CHIEU_DAI_CUA_SO // 2)

        self.title("Đồ Án AI Cá Nhân")
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_DAI_CUA_SO}+{toa_do_x}+{toa_do_y}")
        self.configure(bg=MAU_NEN_XAM)
        self.resizable(False, False)

        # Cấu hình giao diện
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure("TFrame", background=MAU_NEN_XAM)
        self.style.configure("TLabel", background=MAU_NEN_XAM, foreground=MAU_CHU_DEN, font=("Arial", 14, "bold"))
        self.style.configure("TCombobox", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        self.option_add('*TCombobox*Listbox.background', MAU_NEN_XAM)
        self.option_add('*TCombobox*Listbox.foreground', MAU_CHU_DEN)
        self.option_add('*TCombobox*Listbox.selectBackground', '#0078D7')
        self.option_add('*TCombobox*Listbox.selectForeground', 'white')

        self.khung_hien_tai = None
        self.hien_thi_khung(KhungLuaChonChinh)

    def hien_thi_khung(self, ten_khung_class: Callable):
        """Hiển thị khung giao diện mới."""
        if self.khung_hien_tai:
            self.khung_hien_tai.destroy()
        self.khung_hien_tai = ten_khung_class(self)
        self.khung_hien_tai.pack(fill="both", expand=True, padx=10, pady=10)

class KhungLuaChonChinh(ttk.Frame):
    def __init__(self, khung_cha):
        super().__init__(khung_cha, style="TFrame")
        self.khung_cha = khung_cha

        # Tiêu đề
        label_chon_chuc_nang = ttk.Label(self, text="Chọn Chức Năng:", style="TLabel")
        label_chon_chuc_nang.pack(pady=(10, 5))

        # Combobox lựa chọn chức năng
        self.cac_lua_chon_chuc_nang = [
            "Các bài toán chung",
            "Môi trường phức tạp",
            "Môi trường có ràng buộc",
            "Tìm kiếm AND-OR"
        ]
        self.bien_lua_chon = tk.StringVar()
        self.combobox_chuc_nang = ttk.Combobox(self, textvariable=self.bien_lua_chon, values=self.cac_lua_chon_chuc_nang,
                                               state="readonly", width=35, style="TCombobox")
        self.combobox_chuc_nang.current(0)
        self.combobox_chuc_nang.pack(pady=5, padx=20, fill='x')

        # Nút xác nhận và thoát
        khung_nut = ttk.Frame(self, style="TFrame")
        khung_nut.pack(pady=10)
        self.nut_xac_nhan = ttk.Button(khung_nut, text="Thực Hiện", command=self.xu_ly_lua_chon, width=15, style="TButton")
        self.nut_xac_nhan.pack(side="left", padx=5)
        self.nut_thoat = ttk.Button(khung_nut, text="Thoát", command=self.khung_cha.quit, width=15, style="TButton")
        self.nut_thoat.pack(side="left", padx=5)

    def xu_ly_lua_chon(self):
        """Xử lý lựa chọn chức năng."""
        lua_chon = self.bien_lua_chon.get()
        if lua_chon == "Các bài toán chung":
            chay_file_con("reinforcement_learning.py")
        elif lua_chon == "Môi trường phức tạp":
            chay_file_con("complex_envi.py")
        elif lua_chon == "Môi trường có ràng buộc":
            chay_file_con("constrain.py")
        elif lua_chon == "Tìm kiếm AND-OR":
            self.khung_cha.hien_thi_khung(KhungTimKiemAndOr)

class KhungTimKiemAndOr(ttk.Frame):
    def __init__(self, khung_cha):
        super().__init__(khung_cha, style="TFrame")
        self.khung_cha = khung_cha

        # Tiêu đề
        label_chon_thuat_toan = ttk.Label(self, text="Chọn Thuật Toán:", style="TLabel")
        label_chon_thuat_toan.pack(pady=(10, 5))

        # Combobox lựa chọn thuật toán
        self.cac_lua_chon_thuat_toan = ["Tìm Kiếm Đồ Thị AND-OR"]
        self.bien_lua_chon_thuat_toan = tk.StringVar()
        self.combobox_thuat_toan = ttk.Combobox(self, textvariable=self.bien_lua_chon_thuat_toan, values=self.cac_lua_chon_thuat_toan,
                                                state="readonly", width=35, style="TCombobox")
        self.combobox_thuat_toan.current(0)
        self.combobox_thuat_toan.pack(pady=5, padx=20, fill='x')

        # Nút xác nhận và quay lại
        khung_nut = ttk.Frame(self, style="TFrame")
        khung_nut.pack(pady=10)
        self.nut_xac_nhan = ttk.Button(khung_nut, text="Thực Hiện", command=self.xu_ly_lua_chon_thuat_toan, width=15, style="TButton")
        self.nut_xac_nhan.pack(side="left", padx=5)
        self.nut_quay_lai = ttk.Button(khung_nut, text="Quay Lại", command=lambda: self.khung_cha.hien_thi_khung(KhungLuaChonChinh),
                                       width=15, style="TButton")
        self.nut_quay_lai.pack(side="left", padx=5)

    def xu_ly_lua_chon_thuat_toan(self):
        """Xử lý lựa chọn thuật toán."""
        lua_chon = self.bien_lua_chon_thuat_toan.get()
        if lua_chon == "Tìm Kiếm Đồ Thị AND-OR":
            chay_file_con("and_or_search_main.py")

def chay_file_con(ten_file: str):
    """Chạy file con và xử lý lỗi."""
    duong_dan_day_du = os.path.join(DUONG_DAN_THU_MUC_HIEN_HANH, ten_file)
    try:
        subprocess.run([sys.executable, duong_dan_day_du], check=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", f"Không tìm thấy file: {ten_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy file {ten_file}:\n{e}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi không xác định với file {ten_file}:\n{e}")

if __name__ == "__main__":
    ung_dung = UngDungChinh()
    ung_dung.mainloop()