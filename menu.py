import tkinter as tk
import subprocess
import os

DUONG_DAN_THU_MUC_HIEN_HANH = os.path.dirname(__file__)

class UngDungChinh(tk.Tk):
    def __init__(self):
        super().__init__()
        CHIEU_RONG_MAN_HINH = self.winfo_screenwidth()
        CHIEU_DAI_MAN_HINH = self.winfo_screenheight()
        CHIEU_RONG_CUA_SO = 500
        CHIEU_DAI_CUA_SO = 550 
        toa_do_x_cua_so = (CHIEU_RONG_MAN_HINH // 2) - (CHIEU_RONG_CUA_SO // 2)
        toa_do_y_cua_so = (CHIEU_DAI_MAN_HINH // 2) - (CHIEU_DAI_CUA_SO // 2)
        self.title("Đồ án AI cá nhân") 
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_DAI_CUA_SO}+{toa_do_x_cua_so}+{toa_do_y_cua_so}")
        self["bg"] = "#99FFCC"
        self.khung_hien_tai = None
        self.hien_thi_khung(KhungBatDau)

    def hien_thi_khung(self, ten_khung_class):
        if self.khung_hien_tai:
            self.khung_hien_tai.destroy()
        self.khung_hien_tai = ten_khung_class(self)
        self.khung_hien_tai.pack(fill="both", expand=True)

class KhungBatDau(tk.Frame):
    def __init__(self, khung_cha):
        super().__init__(khung_cha)
        self["bg"] = "#99FFCC"
        tk.Label(self, text="Chọn Nhóm Thuật Toán:", font=("Times New Roman", 15, "bold"), width=30, fg="#008080", bg="#99FFCC").pack(pady=10)
        tk.Button(self, text="Môi Trường Quan Sát Đầy Đủ", font=("Times New Roman", 13), command=lambda: hien_thi_man_hinh_moi_truong_quan_sat_day_du(), width=35).pack(pady=5)
        tk.Button(self, text="Bài Toán No sensor", font=("Times New Roman", 13), command=lambda: hien_thi_man_hinh_van_de_khong_cam_bien(), width=35).pack(pady=5)
        tk.Button(self, text="Bài Toán Thỏa Mãn Ràng Buộc (CSP)", font=("Times New Roman", 13), command=lambda: hien_thi_man_hinh_van_de_thoa_man_rang_buoc(), width=35).pack(pady=5)
        tk.Button(self, text="Tìm Kiếm Trong MT Phức Tạp", font=("Times New Roman", 13), command=lambda: self.master.hien_thi_khung(KhungMoiTruongPhucTap), width=35).pack(pady=5)


class KhungMoiTruongPhucTap(tk.Frame):
    def __init__(self, khung_cha):
        super().__init__(khung_cha)
        self["bg"] = "#99FFCC"
        tk.Label(self, text="Chọn Thuật Toán (MT Phức Tạp):", font=("Times New Roman", 15, "bold"), width=30, fg="#008080", bg="#99FFCC").pack(pady=10)
        tk.Button(self, text="Tìm Kiếm Đồ Thị AND/OR", font=("Times New Roman", 13), command=lambda: hien_thi_man_hinh_tim_kiem_do_thi_and_or(), width=45).pack(pady=5)
        tk.Button(self, text="TK Không/Một Phần Quan Sát", font=("Times New Roman", 13), command=lambda: hien_thi_man_hinh_van_de_khong_cam_bien_phuc_tap(), width=45).pack(pady=5) 
        tk.Button(self, text="Quay lại Menu Chính", font=("Times New Roman", 13), command=lambda: self.master.hien_thi_khung(KhungBatDau), width=45).pack(pady=10)
def hien_thi_man_hinh_moi_truong_quan_sat_day_du():
    subprocess.run(["python", DUONG_DAN_THU_MUC_HIEN_HANH + "/fully_observered_environment_and_reinforcement_learning_screen.py"])
def hien_thi_man_hinh_tim_kiem_do_thi_and_or():
    subprocess.run(["python", DUONG_DAN_THU_MUC_HIEN_HANH + "/and_or_search.py"])
def hien_thi_man_hinh_van_de_khong_cam_bien(): 
    subprocess.run(["python", DUONG_DAN_THU_MUC_HIEN_HANH + "/complex_environment_main.py"]) 
def hien_thi_man_hinh_van_de_khong_cam_bien_phuc_tap():
    subprocess.run(["python", DUONG_DAN_THU_MUC_HIEN_HANH + "/complex_environment_main.py"])
def hien_thi_man_hinh_van_de_thoa_man_rang_buoc():
    subprocess.run(["python", DUONG_DAN_THU_MUC_HIEN_HANH + "/constrain_satisfaction_problem_screen.py"])
ung_dung = UngDungChinh()
ung_dung.mainloop()