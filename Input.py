import tkinter as tk
from tkinter import messagebox, ttk
import time
import copy
import heapq
from collections import deque
from typing import Dict, List, Tuple, Optional

# Hằng số
CHIEU_RONG_CUA_SO = 600
CHIEU_CAO_CUA_SO = 500
KICH_THUOC_LUOI = 3
KICH_THUOC_BAI_TOAN = KICH_THUOC_LUOI * KICH_THUOC_LUOI
CAC_HANH_DONG_DI_CHUYEN = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải

# Biến CSP
danh_sach_bien = ["X", "Y", "Z"]
cac_mien_gia_tri = {"X": [0, 1, 2, 3, 4, 5, 6, 7, 8], "Y": [0, 1, 2, 3, 4, 5, 6, 7, 8], "Z": [0, 1, 2, 3, 4, 5, 6, 7, 8]}

# Biến 8-puzzle
trang_thai_bat_dau_puzzle = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
trang_thai_dich_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
lo_trinh_giai_phap = []

def kiem_tra_kha_thi(ban_dau: List[List[int]], muc_tieu: List[List[int]]) -> bool:
    """Kiểm tra tính khả thi của bài toán 8-puzzle dựa trên số lần đảo ngược."""
    def tinh_so_dao_nguoc(trang_thai: List[List[int]]) -> int:
        dao_nguoc = 0
        flat = [num for row in trang_thai for num in row]
        for i in range(KICH_THUOC_BAI_TOAN):
            if flat[i] == 0:
                continue
            for j in range(i + 1, KICH_THUOC_BAI_TOAN):
                if flat[j] == 0:
                    continue
                if flat[i] > flat[j]:
                    dao_nguoc += 1
        return dao_nguoc
    return (tinh_so_dao_nguoc(ban_dau) % 2) == (tinh_so_dao_nguoc(muc_tieu) % 2)

def tinh_khoang_cach_manhattan(trang_thai: List[List[int]], muc_tieu: List[List[int]]) -> int:
    """Tính heuristic khoảng cách Manhattan."""
    khoang_cach = 0
    muc_tieu_map = {(muc_tieu[i][j], i, j) for i in range(3) for j in range(3)}
    for i in range(3):
        for j in range(3):
            if trang_thai[i][j] == 0:
                continue
            for val, ti, tj in muc_tieu_map:
                if val == trang_thai[i][j]:
                    khoang_cach += abs(i - ti) + abs(j - tj)
                    break
    return khoang_cach

# CSP
def kiem_tra_nhat_quan(bien: str, gia_tri: int, phep_gan: Dict[str, int]) -> bool:
    """Kiểm tra ràng buộc khác biệt."""
    return all(phep_gan.get(bien_khac) != gia_tri for bien_khac in phep_gan)

def chay_ac3(cac_mien: Dict[str, List[int]], cac_rang_buoc: Dict[str, List[str]]) -> bool:
    """Thuật toán AC-3 để thu hẹp miền giá trị."""
    hang_doi = deque([(b1, b2) for b1 in cac_mien for b2 in cac_rang_buoc[b1]])
    while hang_doi:
        b1, b2 = hang_doi.popleft()
        da_thay_doi = False
        for x in cac_mien[b1][:]:
            if not any(kiem_tra_nhat_quan(b2, y, {b1: x}) for y in cac_mien[b2]):
                cac_mien[b1].remove(x)
                da_thay_doi = True
        if da_thay_doi:
            if not cac_mien[b1]:
                return False
            for b_khac in cac_rang_buoc[b1]:
                if b_khac != b2:
                    hang_doi.append((b_khac, b1))
    return True

def quay_lui_csp(phep_gan: Dict[str, int], bien_con_lai: List[str], cac_mien: Dict[str, List[int]]) -> Optional[Dict[str, int]]:
    """Tìm kiếm quay lui với AC-3."""
    if len(phep_gan) == len(danh_sach_bien):
        return phep_gan
    bien = bien_con_lai[0]
    for gia_tri in cac_mien[bien]:
        if kiem_tra_nhat_quan(bien, gia_tri, phep_gan):
            phep_gan[bien] = gia_tri
            cac_mien_sao = copy.deepcopy(cac_mien)
            cac_mien_sao[bien] = [gia_tri]
            if chay_ac3(cac_mien_sao, {b: [b_khac for b_khac in danh_sach_bien if b_khac != b] for b in danh_sach_bien}):
                ket_qua = quay_lui_csp(phep_gan, bien_con_lai[1:], cac_mien_sao)
                if ket_qua:
                    return ket_qua
            del phep_gan[bien]
    return None

# 8-Puzzle
class NutTimKiem:
    """Nút trong thuật toán A*."""
    def __init__(self, trang_thai: List[List[int]], cha: Optional['NutTimKiem'], hanh_dong: Optional[Tuple[int, int]], chi_phi_g: int):
        self.trang_thai = trang_thai
        self.cha = cha
        self.hanh_dong = hanh_dong
        self.chi_phi_g = chi_phi_g
        self.chi_phi_h = tinh_khoang_cach_manhattan(trang_thai, trang_thai_dich_puzzle)

    def __lt__(self, other: 'NutTimKiem') -> bool:
        return (self.chi_phi_g + self.chi_phi_h) < (other.chi_phi_g + other.chi_phi_h)

def tim_kiem_a_sao(trang_thai_bat_dau: List[List[int]]) -> Optional[List[List[List[int]]]]:
    """Tìm kiếm A* cho bài toán 8-puzzle."""
    danh_sach_mo = []
    heapq.heapify(danh_sach_mo)
    danh_sach_dong = set()
    nut_ban_dau = NutTimKiem(trang_thai_bat_dau, None, None, 0)
    heapq.heappush(danh_sach_mo, (nut_ban_dau.chi_phi_g + nut_ban_dau.chi_phi_h, nut_ban_dau))
    danh_sach_dong.add(tuple(tuple(row) for row in nut_ban_dau.trang_thai))

    while danh_sach_mo:
        _, nut_hien_tai = heapq.heappop(danh_sach_mo)
        if nut_hien_tai.trang_thai == trang_thai_dich_puzzle:
            lo_trinh = []
            while nut_hien_tai:
                lo_trinh.append(nut_hien_tai.trang_thai)
                nut_hien_tai = nut_hien_tai.cha
            return lo_trinh[::-1]
        x0, y0 = next((i, j) for i in range(3) for j in range(3) if nut_hien_tai.trang_thai[i][j] == 0)
        for dx, dy in CAC_HANH_DONG_DI_CHUYEN:
            x1, y1 = x0 + dx, y0 + dy
            if 0 <= x1 < 3 and 0 <= y1 < 3:
                trang_thai_moi = copy.deepcopy(nut_hien_tai.trang_thai)
                trang_thai_moi[x0][y0], trang_thai_moi[x1][y1] = trang_thai_moi[x1][y1], trang_thai_moi[x0][y0]
                khoa_trang_thai = tuple(tuple(row) for row in trang_thai_moi)
                if khoa_trang_thai not in danh_sach_dong:
                    nut_moi = NutTimKiem(trang_thai_moi, nut_hien_tai, (dx, dy), nut_hien_tai.chi_phi_g + 1)
                    heapq.heappush(danh_sach_mo, (nut_moi.chi_phi_g + nut_moi.chi_phi_h, nut_moi))
                    danh_sach_dong.add(khoa_trang_thai)
    return None

class UngDungPuzzle(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle và CSP")
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_CAO_CUA_SO}")
        self.resizable(False, False)
        self.toc_do_moi_buoc_ms = 1000
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = []
        self.thiet_lap_giao_dien()

    def thiet_lap_giao_dien(self):
        """Thiết lập giao diện Tkinter."""
        # Khung chính
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
                o_nhap.insert(0, str(trang_thai_bat_dau_puzzle[i][j]))
                hang_o.append(o_nhap)
            self.o_nhap_ban_dau.append(hang_o)

        # Lưới mục tiêu
        self.o_nhap_muc_tieu = []
        for i in range(KICH_THUOC_LUOI):
            hang_o = []
            for j in range(KICH_THUOC_LUOI):
                o_nhap = ttk.Entry(khung_trang_thai_muc_tieu, width=5, justify="center")
                o_nhap.grid(row=i, column=j, padx=2, pady=2)
                o_nhap.insert(0, str(trang_thai_dich_puzzle[i][j]))
                hang_o.append(o_nhap)
            self.o_nhap_muc_tieu.append(hang_o)

        # Lưới hiển thị (Trạng thái hiện tại)
        self.o_hien_thi = []
        for i in range(KICH_THUOC_LUOI):
            hang_o = []
            for j in range(KICH_THUOC_LUOI):
                nhan = ttk.Label(khung_hien_thi, text=str(trang_thai_bat_dau_puzzle[i][j]), width=5, anchor="center", relief="sunken")
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

        ttk.Button(khung_dieu_khien, text="Giải CSP", command=self.giai_csp).grid(row=0, column=8, padx=5)
        ttk.Button(khung_dieu_khien, text="Giải Puzzle", command=self.giai_puzzle).grid(row=0, column=9, padx=5)
        ttk.Button(khung_dieu_khien, text="Tải Giá Trị", command=self.tai_gia_tri).grid(row=0, column=10, padx=5)
        ttk.Button(khung_dieu_khien, text="Đặt Lại", command=self.dat_lai).grid(row=0, column=11, padx=5)

        # Khu vực kết quả
        self.o_ket_qua = tk.Text(khung_ket_qua, height=12, width=50)
        self.o_ket_qua.grid(row=0, column=0, padx=5, pady=5)
        thanh_cuon = ttk.Scrollbar(khung_ket_qua, orient="vertical", command=self.o_ket_qua.yview)
        thanh_cuon.grid(row=0, column=1, sticky="ns")
        self.o_ket_qua.config(yscrollcommand=thanh_cuon.set)

        self.bo_hen_gio = self.after(0, lambda: None)

    def tai_gia_tri(self):
        """Tải trạng thái ban đầu và mục tiêu từ các ô nhập liệu."""
        global trang_thai_bat_dau_puzzle, trang_thai_dich_puzzle
        try:
            ban_dau = []
            for hang in self.o_nhap_ban_dau:
                row = []
                for o in hang:
                    gia_tri = o.get().strip()
                    row.append(0 if gia_tri == "" else int(gia_tri))
                ban_dau.append(row)
            muc_tieu = []
            for hang in self.o_nhap_muc_tieu:
                row = []
                for o in hang:
                    gia_tri = o.get().strip()
                    row.append(0 if gia_tri == "" else int(gia_tri))
                muc_tieu.append(row)

            if len(set(num for row in ban_dau for num in row)) != KICH_THUOC_BAI_TOAN or len(set(num for row in muc_tieu for num in row)) != KICH_THUOC_BAI_TOAN:
                raise ValueError("Trạng thái phải chứa các số từ 0 đến 8 duy nhất!")
            if not kiem_tra_kha_thi(ban_dau, muc_tieu):
                raise ValueError("Trạng thái ban đầu không thể đạt được trạng thái mục tiêu!")

            trang_thai_bat_dau_puzzle = ban_dau
            trang_thai_dich_puzzle = muc_tieu
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
                self.o_hien_thi[i][j].config(text=str(trang_thai_bat_dau_puzzle[i][j]) if trang_thai_bat_dau_puzzle[i][j] != 0 else "")
        self.after_cancel(self.bo_hen_gio)

    def giai_csp(self):
        """Giải bài toán CSP."""
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
        phep_giai = quay_lui_csp({}, danh_sach_bien.copy(), copy.deepcopy(cac_mien_gia_tri))
        thoi_gian_ket_thuc = time.perf_counter()

        if phep_giai:
            self.o_ket_qua_insert(tk.END, f"Lời giải CSP: {phep_giai}\n")
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, "1")
        else:
            self.o_ket_qua.insert(tk.END, "Không tìm được lời giải CSP!\n")
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, "0")

        self.o_thoi_gian.delete(0, tk.END)
        self.o_thoi_gian_insert(0, f"{thoi_gian_ket_thuc - thoi_gian_bat_dau:.2f} (giây)")

    def giai_puzzle(self):
        """Giải bài toán 8-puzzle."""
        try:
            toc_do = float(self.o_toc_do_get.get())
            if toc_do < 0.001:
                raise ValueError("Tốc độ tối thiểu là 0.001 giây")
            self.toc_do_moi_buoc_ms = int(toc_do * 1000)
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
            return

        thoi_gian_bat_dau = time.perf_counter()
        self.o_ket_qua.delete(1.0, tk.END)
        lo_trinh = tim_kiem_a_sao(copy.deepcopy(trang_thai_bat_dau_puzzle))
        thoi_gian_ket_thuc = time.perf_counter()

        if lo_trinh:
            global lo_trinh_giai_phap
            lo_trinh_giai_phap = lo_trinh
            for trang_thai in lo_trinh:
                for row in trang_thai:
                    self.o_ket_qua.insert(tk.END, f"{row}\n")
                self.o_ket_qua.insert(tk.END, "\n")
            self.chay_giai_phap()
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, str(len(lo_trinh) - 1))
        else:
            self.o_ket_qua.insert(tk.END, "Không tìm thấy giải pháp cho 8-puzzle!\n")
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, "0")

        self.o_thoi_gian.delete(0, tk.END)
        self.o_thoi_gian_insert(0, f"{thoi_gian_ket_thuc - thoi_gian_bat_dau:.2f} (giây)")

    def chay_giai_phap(self):
        """Chạy giải pháp với hoạt hình."""
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = lo_trinh_giai_phap
        self.after_cancel(self.bo_hen_gio)
        self.cap_nhat_buoc()

    def cap_nhat_buoc(self):
        """Cập nhật hiển thị cho bước hiện tại."""
        if self.buoc_hien_tai < len(self.giai_phap_dang_chay)):
            trang_thai = self.giai_phap_dang_chay[self.buoc_hien_tai]
            self.buoc_hien_tai += 1
            self.o_buoc.delete(0, tk.END)
            self.o_buoc.insert(0, str(self.buoc_hien_tai)))
            for i in range(self.KICH_THUOC_LUOI):
                for j in range(self.KICH_THUOC_LUOI):
                    gia_tri = trang_thai[i][j]
                    self.o_hien_thi[i][j].config(text="" if gia_tri == 0 else str(gia_tri))
            self.bo_hen_gio = self.after(self.toc_do_moi_buoc_ms, self.cap_nhat_buoc)
        else:
            self.after_cancel(self.bo_hen_gio)

if __name__ == "__main__":
    ung_dung = UngDungPuzzle()
    ung_dung.mainloop()