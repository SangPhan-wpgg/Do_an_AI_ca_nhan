import tkinter as tk
from tkinter import messagebox, ttk
import time
from typing import List, Tuple
from copy import deepcopy

# Hằng số
KICH_THUOC_LUOI = 3
KICH_THUOC_BAI_TOAN = KICH_THUOC_LUOI * KICH_THUOC_LUOI
CHIEU_RONG_CUA_SO = 840
CHIEU_CAO_CUA_SO = 611

# Biến toàn cục
trang_thai_ban_dau = [-1] * KICH_THUOC_BAI_TOAN
trang_thai_muc_tieu = [6, 7, 8, 0, 1, 2, 3, 4, 5]
lo_trinh_giai_phap = []

def kiem_tra_kha_thi(ban_dau: List[int], muc_tieu: List[int]) -> bool:
    """Kiểm tra tính khả thi của bài toán 8-puzzle dựa trên số lần đảo ngược."""
    def tinh_so_dao_nguoc(trang_thai: List[int]) -> int:
        dao_nguoc = 0
        for i in range(KICH_THUOC_BAI_TOAN):
            if trang_thai[i] == 0:
                continue
            for j in range(i + 1, KICH_THUOC_BAI_TOAN):
                if trang_thai[j] == 0:
                    continue
                if trang_thai[i] > trang_thai[j]:
                    dao_nguoc += 1
        return dao_nguoc

    dao_nguoc_ban_dau = tinh_so_dao_nguoc(ban_dau)
    dao_nguoc_muc_tieu = tinh_so_dao_nguoc(muc_tieu)
    return (dao_nguoc_ban_dau % 2) == (dao_nguoc_muc_tieu % 2)

def in_bang(bang: List[int]):
    """In trạng thái bài toán ra console."""
    for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
        print(bang[i:i + KICH_THUOC_LUOI])
    print()

def tim_kiem_quay_lui(bang_hien_tai: List[int], vi_tri_dang_xet: int, cac_so_da_dung: List[bool], trang_thai_dich: List[int], duong_di: List[List[int]]) -> bool:
    """
    Tìm kiếm quay lui để giải bài toán 8-puzzle.
    Trả về True nếu tìm thấy giải pháp, False nếu không.
    """
    global lo_trinh_giai_phap
    if vi_tri_dang_xet == KICH_THUOC_BAI_TOAN:
        if bang_hien_tai == trang_thai_dich:
            lo_trinh_giai_phap = deepcopy(duong_di)
            print("Tìm thấy trạng thái đích:")
            for buoc in lo_trinh_giai_phap:
                in_bang(buoc)
            return True
        return False

    for so in range(KICH_THUOC_BAI_TOAN):
        if not cac_so_da_dung[so]:
            bang_hien_tai[vi_tri_dang_xet] = so
            cac_so_da_dung[so] = True
            duong_di.append(bang_hien_tai[:])
            if tim_kiem_quay_lui(bang_hien_tai, vi_tri_dang_xet + 1, cac_so_da_dung, trang_thai_dich, duong_di):
                return True
            duong_di.pop()
            cac_so_da_dung[so] = False
            bang_hien_tai[vi_tri_dang_xet] = -1
    return False

class GiaiDo8So(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Giải Đố 8 Số - Tìm Kiếm Quay Lui")
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_CAO_CUA_SO}")
        self.resizable(False, False)
        self.toc_do_moi_buoc_ms = 1000  # Mặc định 1 giây mỗi bước
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = []
        self.thiet_lap_giao_dien()

    def thiet_lap_giao_dien(self):
        """Thiết lập giao diện người dùng Tkinter."""
        # Khung giao diện
        khung_trang_thai_ban_dau = ttk.LabelFrame(self, text="Trạng Thái Ban Đầu")
        khung_trang_thai_ban_dau.grid(row=0, column=0, padx=10, pady=5, sticky="n")
        
        khung_trang_thai_muc_tieu = ttk.LabelFrame(self, text="Trạng Thái Mục Tiêu")
        khung_trang_thai_muc_tieu.grid(row=0, column=1, padx=10, pady=5, sticky="n")
        
        khung_hien_thi = ttk.LabelFrame(self, text="Trạng Thái Hiện Tại")
        khung_hien_thi.grid(row=0, column=2, padx=10, pady=5, sticky="n")
        
        khung_dieu_khien = ttk.Frame(self)
        khung_dieu_khien.grid(row=1, column=0, columnspan=3, pady=5)
        
        khung_ket_qua = ttk.LabelFrame(self, text="Kết Quả")
        khung_ket_qua.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        # Lưới nhập liệu (Trạng thái ban đầu)
        self.o_nhap_ban_dau = []
        for i in range(KICH_THUOC_LUOI):
            hang_o = []
            for j in range(KICH_THUOC_LUOI):
                o_nhap = ttk.Entry(khung_trang_thai_ban_dau, width=5, justify="center")
                o_nhap.grid(row=i, column=j, padx=2, pady=2)
                o_nhap.insert(0, "0")
                hang_o.append(o_nhap)
            self.o_nhap_ban_dau.append(hang_o)

        # Lưới mục tiêu
        self.o_nhap_muc_tieu = []
        for i in range(KICH_THUOC_LUOI):
            hang_o = []
            for j in range(KICH_THUOC_LUOI):
                o_nhap = ttk.Entry(khung_trang_thai_muc_tieu, width=5, justify="center")
                o_nhap.grid(row=i, column=j, padx=2, pady=2)
                o_nhap.insert(0, str(trang_thai_muc_tieu[i * KICH_THUOC_LUOI + j]))
                hang_o.append(o_nhap)
            self.o_nhap_muc_tieu.append(hang_o)

        # Lưới hiển thị (Trạng thái hiện tại)
        self.o_hien_thi = []
        for i in range(KICH_THUOC_LUOI):
            hang_o = []
            for j in range(KICH_THUOC_LUOI):
                nhan = ttk.Label(khung_hien_thi, text="0", width=5, anchor="center", relief="sunken")
                nhan.grid(row=i, column=j, padx=2, pady=2)
                hang_o.append(nhan)
            self.o_hien_thi.append(hang_o)

        # Điều khiển
        ttk.Label(khung_dieu_khien, text="Tốc Độ Mỗi Bước (giây):").grid(row=0, column=0, padx=5)
        self.o_toc_do = ttk.Entry(khung_dieu_khien, width=10)
        self.o_toc_do.grid(row=0, column=1, padx=5)
        self.o_toc_do.insert(0, "1.0")

        ttk.Label(khung_dieu_khien, text="Bước:").grid(row=0, column=2, padx=5)
        self.o_buoc = ttk.Entry(khung_dieu_khien, width=5, state="readonly")
        self.o_buoc.grid(row=0, column=3, padx=5)

        ttk.Label(khung_dieu_khien, text="Tổng Số Bước:").grid(row=0, column=4, padx=5)
        self.o_tong_buoc = ttk.Entry(khung_dieu_khien, width=5, state="readonly")
        self.o_tong_buoc.grid(row=0, column=5, padx=5)

        ttk.Label(khung_dieu_khien, text="Thời Gian Giải:").grid(row=0, column=6, padx=5)
        self.o_thoi_gian_giai = ttk.Entry(khung_dieu_khien, width=15, state="readonly")
        self.o_thoi_gian_giai.grid(row=0, column=7, padx=5)

        ttk.Button(khung_dieu_khien, text="Giải", command=self.xu_ly_nut_giai).grid(row=0, column=8, padx=5)
        ttk.Button(khung_dieu_khien, text="Tải Giá Trị", command=self.tai_gia_tri).grid(row=0, column=9, padx=5)

        # Khu vực kết quả
        self.o_ket_qua = tk.Text(khung_ket_qua, height=15, width=60)
        self.o_ket_qua.grid(row=0, column=0, padx=5, pady=5)
        thanh_cuon = ttk.Scrollbar(khung_ket_qua, orient="vertical", command=self.o_ket_qua.yview)
        thanh_cuon.grid(row=0, column=1, sticky="ns")
        self.o_ket_qua.config(yscrollcommand=thanh_cuon.set)

        # Bộ hẹn giờ
        self.bo_hen_gio = self.after(0, lambda: None)

    def tai_gia_tri(self):
        """Tải trạng thái ban đầu và mục tiêu từ các ô nhập liệu."""
        global trang_thai_ban_dau, trang_thai_muc_tieu
        try:
            ban_dau = []
            for hang in self.o_nhap_ban_dau:
                for o in hang:
                    gia_tri = o.get().strip()
                    ban_dau.append(0 if gia_tri == "" else int(gia_tri))
            muc_tieu = []
            for hang in self.o_nhap_muc_tieu:
                for o in hang:
                    gia_tri = o.get().strip()
                    muc_tieu.append(0 if gia_tri == "" else int(gia_tri))
            
            # Kiểm tra tính hợp lệ của trạng thái
            if len(set(ban_dau)) != KICH_THUOC_BAI_TOAN or len(set(muc_tieu)) != KICH_THUOC_BAI_TOAN:
                raise ValueError("Trạng thái phải chứa các số từ 0 đến 8 duy nhất!")
            
            if not kiem_tra_kha_thi(ban_dau, muc_tieu):
                messagebox.showerror("Lỗi", "Trạng thái ban đầu không thể đạt được trạng thái mục tiêu!")
                return
                
            trang_thai_ban_dau = ban_dau
            trang_thai_muc_tieu = muc_tieu
            messagebox.showinfo("Thành công", "Tải giá trị thành công!")
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e) if str(e) != "" else "Giá trị nhập vào không hợp lệ! Vui lòng nhập số nguyên từ 0-8 hoặc để trống cho 0.")

    def xu_ly_nut_giai(self):
        """Xử lý sự kiện nhấn nút Giải."""
        global lo_trinh_giai_phap
        try:
            toc_do = float(self.o_toc_do.get())
            if toc_do < 0.001:
                messagebox.showerror("Lỗi", "Tốc độ mỗi bước phải lớn hơn hoặc bằng 0.001 giây")
                return
            self.toc_do_moi_buoc_ms = int(toc_do * 1000)
        except ValueError:
            messagebox.showerror("Lỗi", "Tốc độ mỗi bước không hợp lệ!")
            return

        thoi_gian_bat_dau = time.time()
        lo_trinh_giai_phap = []
        bang_hien_tai = trang_thai_ban_dau[:]
        cac_so_da_dung = [False] * KICH_THUOC_BAI_TOAN
        for i, so in enumerate(bang_hien_tai):
            if so != -1:
                cac_so_da_dung[so] = True

        ket_qua = tim_kiem_quay_lui(bang_hien_tai, 0, cac_so_da_dung, trang_thai_muc_tieu, lo_trinh_giai_phap)

        print("Trạng thái ban đầu:", trang_thai_ban_dau)
        print("Trạng thái mục tiêu:", trang_thai_muc_tieu)
        print("Kết quả:", "Tìm thấy giải pháp" if ket_qua else "Không tìm thấy giải pháp")

        self.o_ket_qua.delete(1.0, tk.END)
        if ket_qua:
            for buoc in lo_trinh_giai_phap:
                for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
                    self.o_ket_qua.insert(tk.END, f"{buoc[i:i + KICH_THUOC_LUOI]}\n")
                self.o_ket_qua.insert(tk.END, "\n")
            self.chay_giai_phap(lo_trinh_giai_phap)
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, str(len(lo_trinh_giai_phap)))
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy giải pháp!")
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, "0")
            self.o_buoc.delete(0, tk.END)
            self.o_buoc.insert(0, "0")

        thoi_gian_ket_thuc = time.time()
        self.o_thoi_gian_giai.delete(0, tk.END)
        self.o_thoi_gian_giai.insert(0, f"{thoi_gian_ket_thuc - thoi_gian_bat_dau:.9f} (giây)")

    def chay_giai_phap(self, giai_phap: List[List[int]]):
        """Chạy giải pháp với hoạt hình."""
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = giai_phap
        self.after_cancel(self.bo_hen_gio)
        self.cap_nhat_buoc()

    def cap_nhat_buoc(self):
        """Cập nhật hiển thị cho bước hiện tại."""
        if self.buoc_hien_tai < len(self.giai_phap_dang_chay):
            trang_thai = self.giai_phap_dang_chay[self.buoc_hien_tai]
            self.buoc_hien_tai += 1
            self.o_buoc.delete(0, tk.END)
            self.o_buoc.insert(0, str(self.buoc_hien_tai))
            for i in range(KICH_THUOC_LUOI):
                for j in range(KICH_THUOC_LUOI):
                    gia_tri = trang_thai[i * KICH_THUOC_LUOI + j]
                    self.o_hien_thi[i][j].config(text="" if gia_tri == 0 else str(gia_tri))
            self.bo_hen_gio = self.after(self.toc_do_moi_buoc_ms, self.cap_nhat_buoc)
        else:
            self.after_cancel(self.bo_hen_gio)

if __name__ == "__main__":
    ung_dung = GiaiDo8So()
    ung_dung.mainloop()