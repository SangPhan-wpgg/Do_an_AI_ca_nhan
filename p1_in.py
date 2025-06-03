import tkinter as tk
from tkinter import messagebox, ttk
import random
from collections import defaultdict
from copy import deepcopy
import time
from typing import Tuple, List, Dict, Optional

# Hằng số
CHIEU_RONG_CUA_SO = 600
CHIEU_CAO_CUA_SO = 500
KICH_THUOC_LUOI = 3
KICH_THUOC_BAI_TOAN = KICH_THUOC_LUOI * KICH_THUOC_LUOI
CAC_HANH_DONG = ['Up', 'Down', 'Left', 'Right']
CAC_BUOC_DI_CHUYEN = {'Up': -3, 'Down': 3, 'Left': -1, 'Right': 1}

# Biến toàn cục
TRANG_THAI_BAT_DAU = (1, 2, 3, 4, 0, 6, 7, 5, 8)
TRANG_THAI_DICH = (1, 2, 3, 4, 5, 6, 7, 8, 0)
LO_TRINH_GIAI_PHAP = []

def kiem_tra_kha_thi(ban_dau: Tuple[int, ...], muc_tieu: Tuple[int, ...]) -> bool:
    """Kiểm tra tính khả thi của bài toán 8-puzzle dựa trên số lần đảo ngược."""
    def tinh_so_dao_nguoc(trang_thai: Tuple[int, ...]) -> int:
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
    return (tinh_so_dao_nguoc(ban_dau) % 2) == (tinh_so_dao_nguoc(muc_tieu) % 2)

def kiem_tra_trang_thai_dich(trang_thai: Tuple[int, ...], trang_thai_dich: Tuple[int, ...]) -> bool:
    """Kiểm tra xem trạng thái hiện tại có phải là trạng thái mục tiêu không."""
    return trang_thai == trang_thai_dich

def kiem_tra_di_chuyen_hop_le(vi_tri_khong: int, huong: str) -> bool:
    """Kiểm tra xem hành động di chuyển có hợp lệ không."""
    if huong == 'Up' and vi_tri_khong < KICH_THUOC_LUOI:
        return False
    if huong == 'Down' and vi_tri_khong >= KICH_THUOC_BAI_TOAN - KICH_THUOC_LUOI:
        return False
    if huong == 'Left' and vi_tri_khong % KICH_THUOC_LUOI == 0:
        return False
    if huong == 'Right' and vi_tri_khong % KICH_THUOC_LUOI == KICH_THUOC_LUOI - 1:
        return False
    return True

def thuc_hien_di_chuyen(trang_thai: Tuple[int, ...], huong: str) -> Optional[Tuple[int, ...]]:
    """Thực hiện di chuyển ô trống theo hướng chỉ định."""
    vi_tri_khong = trang_thai.index(0)
    if not kiem_tra_di_chuyen_hop_le(vi_tri_khong, huong):
        return None
    vi_tri_moi = vi_tri_khong + CAC_BUOC_DI_CHUYEN[huong]
    trang_thai_moi = list(trang_thai)
    trang_thai_moi[vi_tri_khong], trang_thai_moi[vi_tri_moi] = trang_thai_moi[vi_tri_moi], trang_thai_moi[vi_tri_khong]
    return tuple(trang_thai_moi)

def tinh_heuristic(trang_thai: Tuple[int, ...], trang_thai_dich: Tuple[int, ...]) -> int:
    """Tính heuristic khoảng cách Manhattan."""
    gia_tri_h = 0
    for i in range(1, KICH_THUOC_BAI_TOAN):
        x1, y1 = divmod(trang_thai.index(i), KICH_THUOC_LUOI)
        x2, y2 = divmod(trang_thai_dich.index(i), KICH_THUOC_LUOI)
        gia_tri_h += abs(x1 - x2) + abs(y1 - y2)
    return gia_tri_h

def giai_bang_q_learning(trang_thai_bat_dau: Tuple[int, ...], trang_thai_dich: Tuple[int, ...]) -> Optional[List[Tuple[int, ...]]]:
    """Giải bài toán 8-puzzle bằng Q-learning."""
    alpha = 0.1  # Tỷ lệ học
    gamma = 0.9  # Hệ số chiết khấu
    epsilon = 0.5  # Xác suất khám phá ban đầu
    epsilon_min = 0.01  # Xác suất khám phá tối thiểu
    epsilon_decay = 0.995  # Tỷ lệ giảm epsilon
    so_luong_episodes = 5000  # Giảm số episode để tăng tốc
    SO_BUOC_TOI_DA = 1000  # Giảm số bước tối đa

    bang_q = defaultdict(lambda: {a: 0.0 for a in CAC_HANH_DONG})

    for episode in range(so_luong_episodes):
        trang_thai_hien_tai = deepcopy(trang_thai_bat_dau)
        so_buoc = 0
        epsilon = max(epsilon_min, epsilon * epsilon_decay)  # Giảm epsilon

        while not kiem_tra_trang_thai_dich(trang_thai_hien_tai, trang_thai_dich) and so_buoc < SO_BUOC_TOI_DA:
            if random.uniform(0, 1) < epsilon:
                hanh_dong = random.choice(CAC_HANH_DONG)
            else:
                hanh_dong = max(bang_q[trang_thai_hien_tai], key=bang_q[trang_thai_hien_tai].get)

            trang_thai_tiep = thuc_hien_di_chuyen(trang_thai_hien_tai, hanh_dong)

            if trang_thai_tiep is None:
                phan_thuong = -50
                gia_tri_q_toi_da = 0
                xac_suat_chuyen = 0.0001
            else:
                phan_thuong = 100 if kiem_tra_trang_thai_dich(trang_thai_tiep, trang_thai_dich) else -1
                if trang_thai_tiep not in bang_q:
                    bang_q[trang_thai_tiep] = {a: 0 for a in CAC_HANH_DONG}
                gia_tri_q_toi_da = max(bang_q[trang_thai_tiep].values())
                heuristic_val = tinh_heuristic(trang_thai_tiep, trang_thai_dich)
                xac_suat_chuyen = 1 - heuristic_val / 41 if heuristic_val < 41 else 0.0001

            bang_q[trang_thai_hien_tai][hanh_dong] += alpha * (
                phan_thuong + gamma * xac_suat_chuyen * gia_tri_q_toi_da - bang_q[trang_thai_hien_tai][hanh_dong]
            )

            if trang_thai_tiep is None:
                break
            trang_thai_hien_tai = trang_thai_tiep
            so_buoc += 1

    # Truy vết lộ trình giải pháp
    trang_thai_hien_tai = deepcopy(trang_thai_bat_dau)
    giai_phap = [trang_thai_hien_tai]
    so_buoc_giai = 0
    while not kiem_tra_trang_thai_dich(trang_thai_hien_tai, trang_thai_dich) and so_buoc_giai < SO_BUOC_TOI_DA:
        if trang_thai_hien_tai not in bang_q:
            return None
        hanh_dong = max(bang_q[trang_thai_hien_tai], key=bang_q[trang_thai_hien_tai].get)
        trang_thai_tiep = thuc_hien_di_chuyen(trang_thai_hien_tai, hanh_dong)
        if trang_thai_tiep is None:
            return None
        trang_thai_hien_tai = trang_thai_tiep
        giai_phap.append(trang_thai_hien_tai)
        so_buoc_giai += 1

    if kiem_tra_trang_thai_dich(trang_thai_hien_tai, trang_thai_dich):
        return giai_phap
    return None

class UngDungPuzzle(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle - Q-Learning")
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_CAO_CUA_SO}")
        self.resizable(False, False)
        self.toc_do_moi_buoc_ms = 1000
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = []
        self.trang_thai_bat_dau = list(TRANG_THAI_BAT_DAU)
        self.trang_thai_dich = list(TRANG_THAI_DICH)
        self.thiet_lap_giao_dien()

    def thiet_lap_giao_dien(self):
        """Thiết lập giao diện Tkinter."""
        khung_trang_thai_ban_dau = ttk.LabelFrame(self, text="Trạng Thái Ban Đầu")
        khung_trang_thai_ban_dau.grid(row=0, column=0, padx=10, pady=5, sticky="n")

        khung_trang_thai_muc_tieu = ttk.LabelFrame(self, text="Trạng Thái Mục Tiêu")
        khung_trang_thai_muc_tieu.grid(row=0, column=1, padx=10, pady=5, sticky="n")

        khung_hien_thi = ttk.LabelFrame(self, text="Trạng Thái Hiện Tại")
        khung_hien_thi.grid(row=0, column=2, padx=10, pady=5, sticky="n")

        khung_dieu_khien = ttk.Frame(self)
        khung_dieu_khien.grid(row=1, column=0, columnspan=3, pady=5)

        khung_ket_qua = ttk.LabelFrame(self, text="Lộ Trình Giải Pháp")
        khung_ket_qua.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        # Lưới nhập liệu (Trạng thái ban đầu)
        self.o_nhap_ban_dau = []
        for i in range(KICH_THUOC_LUOI):
            hang_o = []
            for j in range(KICH_THUOC_LUOI):
                o_nhap = ttk.Entry(khung_trang_thai_ban_dau, width=5, justify="center")
                o_nhap.grid(row=i, column=j, padx=2, pady=2)
                o_nhap.insert(0, str(self.trang_thai_bat_dau[i * KICH_THUOC_LUOI + j]))
                hang_o.append(o_nhap)
            self.o_nhap_ban_dau.append(hang_o)

        # Lưới mục tiêu
        self.o_nhap_muc_tieu = []
        for i in range(KICH_THUOC_LUOI):
            hang_o = []
            for j in range(KICH_THUOC_LUOI):
                o_nhap = ttk.Entry(khung_trang_thai_muc_tieu, width=5, justify="center")
                o_nhap.grid(row=i, column=j, padx=2, pady=2)
                o_nhap.insert(0, str(self.trang_thai_dich[i * KICH_THUOC_LUOI + j]))
                hang_o.append(o_nhap)
            self.o_nhap_muc_tieu.append(hang_o)

        # Lưới hiển thị (Trạng thái hiện tại)
        self.o_hien_thi = []
        for i in range(KICH_THUOC_LUOI):
            hang_o = []
            for j in range(KICH_THUOC_LUOI):
                nhan = ttk.Label(khung_hien_thi, text=str(self.trang_thai_bat_dau[i * KICH_THUOC_LUOI + j]) if self.trang_thai_bat_dau[i * KICH_THUOC_LUOI + j] != 0 else "",
                                 width=5, anchor="center", relief="sunken")
                nhan.grid(row=i, column=j, padx=2, pady=2)
                hang_o.append(nhan)
            self.o_hien_thi.append(hang_o)

        # Điều khiển
        ttk.Label(khung_dieu_khien, text="Tốc Độ (giây):").grid(row=0, column=0, padx=5)
        self.o_toc_do = ttk.Entry(khung_dieu_khien, width=10)
        self.o_toc_do.grid(row=0, column=1, padx=5)
        self.o_toc_do.insert(0, "1.0")

        ttk.Label(khung_dieu_khien, text="Bước:").grid(row=0, column=2, padx=5)
        self.o_buoc = ttk.Entry(khung_dieu_khien, width=5, state="readonly")
        self.o_buoc.grid(row=0, column=3, padx=5)

        ttk.Label(khung_dieu_khien, text="Tổng Bước:").grid(row=0, column=4, padx=5)
        self.o_tong_buoc = ttk.Entry(khung_dieu_khien, width=5, state="readonly")
        self.o_tong_buoc.grid(row=0, column=5, padx=5)

        ttk.Label(khung_dieu_khien, text="Thời Gian:").grid(row=0, column=6, padx=5)
        self.o_thoi_gian = ttk.Entry(khung_dieu_khien, width=15, state="readonly")
        self.o_thoi_gian.grid(row=0, column=7, padx=5)

        ttk.Button(khung_dieu_khien, text="Giải", command=self.giai_puzzle).grid(row=0, column=8, padx=5)
        ttk.Button(khung_dieu_khien, text="Tải Giá Trị", command=self.tai_gia_tri).grid(row=0, column=9, padx=5)
        ttk.Button(khung_dieu_khien, text="Đặt Lại", command=self.dat_lai).grid(row=0, column=10, padx=5)

        # Khu vực kết quả
        self.o_ket_qua = tk.Text(khung_ket_qua, height=12, width=50)
        self.o_ket_qua.grid(row=0, column=0, padx=5, pady=5)
        thanh_cuon = ttk.Scrollbar(khung_ket_qua, orient="vertical", command=self.o_ket_qua.yview)
        thanh_cuon.grid(row=0, column=1, sticky="ns")
        self.o_ket_qua.config(yscrollcommand=thanh_cuon.set)

        self.bo_hen_gio = self.after(0, lambda: None)

    def tai_gia_tri(self):
        """Tải trạng thái ban đầu và mục tiêu từ các ô nhập liệu."""
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

            if len(set(ban_dau)) != KICH_THUOC_BAI_TOAN or len(set(muc_tieu)) != KICH_THUOC_BAI_TOAN:
                raise ValueError("Trạng thái phải chứa các số từ 0 đến 8 duy nhất!")
            if not kiem_tra_kha_thi(tuple(ban_dau), tuple(muc_tieu)):
                raise ValueError("Trạng thái ban đầu không thể đạt được trạng thái mục tiêu!")

            self.trang_thai_bat_dau = ban_dau
            self.trang_thai_dich = muc_tieu
            self.dat_lai()
            messagebox.showinfo("Thành công", "Tải giá trị thành công!")
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def dat_lai(self):
        """Đặt lại trạng thái giao diện."""
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = []
        self.o_buoc.delete(0, tk.END)
        self.o_buoc.insert(0, "0")
        self.o_tong_buoc.delete(0, tk.END)
        self.o_tong_buoc.insert(0, "0")
        self.o_thoi_gian.delete(0, tk.END)
        self.o_ket_qua.delete(1.0, tk.END)
        for i in range(KICH_THUOC_LUOI):
            for j in range(KICH_THUOC_LUOI):
                gia_tri = self.trang_thai_bat_dau[i * KICH_THUOC_LUOI + j]
                self.o_hien_thi[i][j].config(text=str(gia_tri) if gia_tri != 0 else "")
        self.after_cancel(self.bo_hen_gio)

    def giai_puzzle(self):
        """Giải bài toán 8-puzzle bằng Q-learning."""
        try:
            toc_do = float(self.o_toc_do.get())
            if toc_do < 0.001:
                raise ValueError("Tốc độ tối thiểu là 0.001 giây!")
            self.toc_do_moi_buoc_ms = int(toc_do * 1000)
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
            return

        thoi_gian_bat_dau = time.perf_counter()
        self.o_ket_qua.delete(1.0, tk.END)
        giai_phap = giai_bang_q_learning(tuple(self.trang_thai_bat_dau), tuple(self.trang_thai_dich))
        thoi_gian_ket_thuc = time.perf_counter()

        if giai_phap:
            global LO_TRINH_GIAI_PHAP
            LO_TRINH_GIAI_PHAP = giai_phap
            for trang_thai in giai_phap:
                for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
                    self.o_ket_qua.insert(tk.END, f"{list(trang_thai[i:i + KICH_THUOC_LUOI])}\n")
                self.o_ket_qua.insert(tk.END, "\n")
            self.chay_giai_phap()
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, str(len(giai_phap) - 1))
        else:
            self.o_ket_qua.insert(tk.END, "Không tìm thấy giải pháp!\n")
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, "0")

        self.o_thoi_gian.delete(0, tk.END)
        self.o_thoi_gian.insert(0, f"{thoi_gian_ket_thuc - thoi_gian_bat_dau:.2f} (giây)")

    def chay_giai_phap(self):
        """Chạy giải pháp với hoạt hình."""
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = LO_TRINH_GIAI_PHAP
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
                    self.o_hien_thi[i][j].config(text=str(gia_tri) if gia_tri != 0 else "")
            self.bo_hen_gio = self.after(self.toc_do_moi_buoc_ms, self.cap_nhat_buoc)
        else:
            self.after_cancel(self.bo_hen_gio)

if __name__ == "__main__":
    ung_dung = UngDungPuzzle()
    ung_dung.mainloop()