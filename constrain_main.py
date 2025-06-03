import tkinter as tk
from tkinter import messagebox, ttk
import time
from typing import Tuple, List, Optional, Dict
from collections import deque
from copy import deepcopy

# Hằng số
KICH_THUOC_LUOI = 3
KICH_THUOC_BAI_TOAN = KICH_THUOC_LUOI * KICH_THUOC_LUOI
CHIEU_RONG_CUA_SO = 600
CHIEU_CAO_CUA_SO = 400

# Biến toàn cục
trang_thai_ban_dau = tuple([0] * KICH_THUOC_BAI_TOAN)
trang_thai_muc_tieu = tuple([0] * KICH_THUOC_BAI_TOAN)
cac_muc_da_tham = []

def kiem_tra_kha_thi(ban_dau: Tuple[int, ...], muc_tieu: Tuple[int, ...]) -> bool:
    """Kiểm tra tính khả thi của bài toán 8-puzzle dựa trên số lần đảo ngược."""
    def tinh_so_dao_nguoc(trang_thai: Tuple[int, ...]) -> int:
        dao = 0
        for i in range(KICH_THUOC_BAI_TOAN):
            if trang_thai[i] == 0:
                continue
            for j in range(i + 1, KICH_THUOC_BAI_TOAN):
                if trang_thai[j] == 0:
                    continue
                if trang_thai[i] > trang_thai[j]:
                    dao += 1
        return dao
    return (tinh_so_dao_nguoc(ban_dau) % 2) == (tinh_so_dao_nguoc(muc_tieu) % 2)

def tinh_khoang_cach_manhattan(trang_thai: Tuple[int, ...], muc_tieu: Tuple[int, ...]) -> int:
    """Tính heuristic khoảng cách Manhattan."""
    khoang_cach = 0
    for i, gia_tri in enumerate(trang_thai):
        if gia_tri == -1:
            continue
        for j, muc_tieu_gia_tri in enumerate(muc_tieu):
            if muc_tieu_gia_tri == gia_tri:
                hang_hien_tai, cot_hien_tai = i // KICH_THUOC_LUOI, i % KICH_THUOC_LUOI
                hang_muc_tieu, cot_muc_tieu = j // KICH_THUOC_LUOI, j % KICH_THUOC_LUOI
                khoang_cach += abs(hang_hien_tai - hang_muc_tieu) + abs(cot_hien_tai - cot_muc_tieu)
                break
    return khoang_cach

def kiem_tra_rang_buoc_khac_biet(x: int, y: int) -> bool:
    """Kiểm tra ràng buộc khác biệt giữa hai giá trị."""
    return x != y

def chay_thuat_toan_ac3(cac_mien: Dict[str, List[int]], cac_bien_ke_can: Dict[str, List[str]]) -> bool:
    """Chạy thuật toán AC3 để thu hẹp miền giá trị."""
    hang_doi = deque([(b_i, b_j) for b_i in cac_mien for b_j in cac_bien_ke_can[b_i]])
    while hang_doi:
        hat, b_i, b_j = hang_doi.popleft()
        if dieu_chinh_mien(cac_mien, b_i, b_j):
            if not cac_mien[b_i]:
                return False
            for b_k in cac_bien_ke_can[b_i]:
                if b_k != b_j:
                    hang_doi.append((b_k, b_i))
    return True

def dieu_chinh_mien(cac_mien: Dict[str, List[int]], b_i: str, b_j: str) -> bool:
    """Điều chỉnh miền giá trị của biến b_i dựa trên b_j."""
    da_thuc_hien_dieu_chinh = False
    for x in cac_mien[b_i][:]:
        if all(not kiem_tra_rang_buoc_khac_biet(x, y) for y in cac_mien[b_j]):
            cac_mien[b_i].remove(x)
            da_thuc_hien_dieu_chinh = True
    return da_thuc_hien_dieu_chinh

def thuc_hien_tim_kiem_quay_lui(phep_gan: Dict[str, int], danh_sach_bien: List[str], cac_mien: Dict[str, List[int]], so_lan_thu_gan: List[int]) -> Optional[Dict[str, int]]:
    """Tìm kiếm quay lui với heuristic để giải bài toán CSP."""
    global cac_muc_da_tham
    if len(phep_gan) == len(danh_sach_bien):
        trang_thai = tuple([phep_gan.get(f'X{i+1}', -1) for i in range(KICH_THUOC_BAI_TOAN)])
        if trang_thai == trang_thai_muc_tieu:
            return phep_gan
        return None

    bien = next((b for b in danh_sach_bien if b not in phep_gan), None)
    if bien is None:
        return None

    trang_thai_hien_tai = [-1] * KICH_THUOC_BAI_TOAN
    for b, gt in phep_gan.items():
        trang_thai_hien_tai[int(b.strip("X")) - 1] = gt
    cac_gia_tri = sorted(cac_mien[bien], key=lambda x: tinh_khoang_cach_manhattan(
        tuple(trang_thai_hien_tai[:int(bien.strip("X")) - 1] + [x] + trang_thai_hien_tai[int(bien.strip("X")):]),
        trang_thai_muc_tieu
    ))

    for gia_tri in cac_gia_tri:
        so_lan_thu_gan[0] += 1
        if all(kiem_tra_rang_buoc_khac_biet(gia_tri, phep_gan.get(b_khac, -1)) for b_khac in phep_gan):
            phep_gan[bien] = gia_tri
            trang_thai = [-1] * KICH_THUOC_BAI_TOAN
            for b, gt in phep_gan.items():
                trang_thai[int(b.strip("X")) - 1] = gt
            cac_muc_da_tham.append(tuple(trang_thai))
            ket_qua = thuc_hien_tim_kiem_quay_lui(phep_gan, danh_sach_bien, cac_mien, so_lan_thu_gan)
            if ket_qua:
                return ket_qua
            del phep_gan[bien]
            cac_muc_da_tham.append(tuple(trang_thai))
    return None

def in_bang(trang_thai: Tuple[int, ...]):
    """In trạng thái bài toán ra console."""
    for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
        print(list(trang_thai[i:i + KICH_THUOC_LUOI]))
    print()

class GiaiDo8SoCSP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Giải Đố 8 Số - CSP")
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_CAO_CUA_SO}")
        self.resizable(False, False)
        self.toc_do = 1000
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = []
    def thiet_lap_giao_dien(self):
        """Thiết lập giao diện Tkinter."""
        khung_trang_thai_ban_dau = ttk.LabelFrame(self, text="Trạng Thái Ban Đầu"))
        khung_trang_thai_ban_dau.grid(row=0, column=0, padx=(10, pady=5, sticky="n"))
        
        khung_trang_thai_muc_tieu = ttk.LabelFrame(self, text="Trạng Thái Mục Tiêu"))
        khung_trang_thai_muc_tieu.grid(row=0, column=1, padx=(10, pady=5, sticky="n"))
        
        khung_hien_thi = ttk.LabelFrame(self, text="Trạng Thái Hiện Tại"))
        khung_hien_thi.grid(row=0, column=2, padx=10, pady=10, sticky="n")
        
        khung_dieu_khien = ttk.Frame(self)
        khung_dieu_khien.grid(row=1, column=0, columnspan=3, pady=5)
        
        khung_ket_qua = ttk.LabelFrame(self, text="Lộ Trình Giải Pháp"))
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
        ttk.Label(khung_dieu_khien, text="Thuật Toán:").grid(row=0, column=0, padx=5)
        self.thuat_toan ttk.Combobox(khung_dieu_khien, values=["Backtracking", "AC3 + Backtracking"], state="readonly")
        self.thuat_toan.grid(row=0, column=1, padx=5)
        self.thuat_toan.set("Backtracking")

        ttk.Label(khung_dieu_khien, text="Tốc Độ Mỗi Bước (giây):").grid(row=0, column=2, padx=5)
        self.toc_do = ttk.Entry(khung_dieu_khien, width=10)
        self.o_toc_do.grid(row=0, column=3, padx=5)
        self.o_toc_do.insert(0, "1.1.0")

        ttk.Label(khung_dieu_khien, text="Bước:").grid(row=0, column=4, padx=5)
        self.o_buoc = ttk.Entry(khung_dieu_khien, width=5, state="readonly")
        self.o_buoc.grid(row=0, column=5, padx=5)

        ttk.Label(khung_dieu_khien, text="Tổng Số Bước:").grid(row=0, column=6, padx=5)
        self.o_tong_buoc = ttk.Entry(khung_dieu_khien, width=5, state="readonly")
        self.o_tong_buoc.grid(row=0, column=7, padx=5)        ttk.Label(khung_dieu_khien, text="Thời Gian Giải:").grid(row=0, column=8, padx=5)
        self.o_thoi_gian_giai = ttk.Entry(khung_dieu_khien, width=15, state="readonly")
        self.o_thoi_gian_giai.grid(row=0, column=9, padx=5)

        ttk.Button(khung_dieu_khien, text="Giải", command=self.thuc_hien_giai_csp).grid(row=0, column=10, padx=5)        ttk.Button(khung_dieu_khien, text="Tải Giá Trị", command=self.tai_gia_tri).grid(row=0, column=11, padx=5)

        # Khu vực kết quả
        self.o_ket_qua = tk.Text(khung_ket_qua, height=10, width=50)
        self.o_ket_qua.grid(row=0, column=0, padx=5, pady=5)
        thanh_cuon = ttk.Scrollbar(khung_ket_qua, orient="vertical", command=self.o_ket_qua.yview)
        thanh_cuon.grid(row=0, column=1, sticky="ns")
        self.o_ket_qua.config(yscrollcommand=thanhcuon.set)

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
            
            if len(set(ban_dau)) != KICH_THUOC_BAI_TOAN or len(set(muc_tieu)) != KICH_THUOC_BAI_TOAN:
                raise ValueError("Trạng thái phải chứa các số từ 0 đến 8 duy nhất!")
            
            if not kiem_tra_kha_thi(ban_dau, muc_tieu):
                raise ValueError("Trạng thái ban đầu không thể đạt được trạng thái mục tiêu!")
            
            trang_thai_ban_dau = tuple(ban_dau)
            trang_thai_muc_tieu = tuple(muc_tieu)
            messagebox.showinfo("Thành công", "Tải giá trị thành công!")
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

        def thuc_hien_giai_csp(self):
            """Thực hiện giải bài toán CSP."""
            global cac_muc_da_tham
            try:
                toc_do = float(self.o_toc_do.get())
                if toc_do < 0.001:
                    raise ValueError("Tốc độ mỗi bước phải lớn hơn hoặc bằng 0.001 giây!")
                self.toc_do = int(toc_do * 1000)
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))
                return

            thoi_gian_bat_dau = time.perf_counter()
            cac_muc_da_tham = []
            loai_thuat_toan = self.thuat_toan.get()

            danh_sach_bien = [f'X{i+1}' for i in range(KICH_THUOC_BAI_TOAN)]
            cac_mien = {bien: list(range(9)) for bien in danh_sach_bien}
            cac_bien_ke_can = {bien: [b for b in danh_sach_bien if b != bien] for bien in danh_sach_bien}
            so_lan_thu_gan = [0]

            if loai_thuat_toan == "AC3 + Backtracking":
                if not chay_thuat_toan_ac3(cac_mien, cac_bien_ke_can):
                    messagebox.showerror("Lỗi", "Tìm thấy sự không nhất quán sau AC3. Không có giải pháp.")
                    self.o_tong_buoc.delete(0, tk.END)
                    self.o_tong_buoc.insert(0, "0")
                    self.o_buoc.delete(0, tk.END)
                    self.o_buoc.insert(0, "0")
                    self.o_thoi_gian_giai.delete(0, tk.END)
                    self.o_thoi_gian_giai.insert(0, "0.0")
                    return
            phep_gan = thuc_hien_tim_kiem_quay_lui({}, danh_sach_bien, cac_mien, so_lan_thu_gan)

            self.o_ket_qua.delete(1.0, tk.END)
            if phep_gan:
                for buoc in cac_muc_da_tham:
                    for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
                        self.o_ket_qua.insert(tk.END, f"{list(buoc[i:i + KICH_THUOC_LUOI])}\n")
                    self.o_ket_qua.insert(tk.END, "\n")
                self.chay_giai_phap(cac_muc_da_tham)
                self.o_tong_buoc.delete(0, tk.END)
                self.o_tong_buoc.insert(0, str(len(cac_muc_da_tham)))
            else:
                messagebox.showinfo("Kết quả", "Không tìm thấy giải pháp!")
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, "0")
            thoi_gian_ket_thuc = time.perf_counter()
            self.o_thoi_gian_giai.delete(0, tk.END)
            self.o_thoi_gian_giai.insert(0, f"{thoi_gian_ket_thuc - thoi_gian_bat_dau:.2f} (giây)")

        def chay_giai_phap(self, giai_phap: List[Tuple[int, ...]]):
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
                self.o_buoc.insert(0, str(self.buoc_hien_tai)                for i in range(KICH_THUOC_LUOI):
                    for j in range(KICH_THUOC_LUOI):
                        gia_tri = trang_thai[i * KICH_THUOC_LUOI + j]
                        self.o_hien_thi[i][j].config(text="" if gia_tri == -1 else str(gia_tri))
                self.bo_hen_gio = self.after(self.toc_do, self.cap_nhat_buoc)            else:
                self.after_cancel(self.bo_hen_gio)

if __name__ == "__main__":
    ung_dung = GiaiDo8SoCSP()
    ung_dung.mainloop()