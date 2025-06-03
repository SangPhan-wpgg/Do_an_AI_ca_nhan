import tkinter as tk
from tkinter import messagebox, ttk
import time
import heapq
from typing import Tuple, List, Optional

# Hằng số
KICH_THUOC_LUOI = 3
KICH_THUOC_BAI_TOAN = KICH_THUOC_LUOI * KICH_THUOC_LUOI
CHIEU_RONG_CUA_SO = 600
CHIEU_CAO_CUA_SO = 400
CAC_HANH_DONG_DI_CHUYEN = {
    'lên': -KICH_THUOC_LUOI,
    'xuống': KICH_THUOC_LUOI,
    'trái': -1,
    'phải': 1
}

# Biến toàn cục
trang_thai_ban_dau = tuple([0] * KICH_THUOC_BAI_TOAN)
trang_thai_muc_tieu = tuple([6, 7, 8, 0, 1, 2, 3, 4, 5])
lo_trinh_giai_phap = []
so_luong_trang_thai_da_mo = 0

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

def la_di_chuyen_hop_le(vi_tri_so_khong: int, huong: str) -> bool:
    """Kiểm tra xem hành động di chuyển có hợp lệ không."""
    if huong == 'lên' and vi_tri_so_khong < KICH_THUOC_LUOI:
        return False
    if huong == 'xuống' and vi_tri_so_khong >= KICH_THUOC_BAI_TOAN - KICH_THUOC_LUOI:
        return False
    if huong == 'trái' and vi_tri_so_khong % KICH_THUOC_LUOI == 0:
        return False
    if huong == 'phải' and vi_tri_so_khong % KICH_THUOC_LUOI == KICH_THUOC_LUOI - 1:
        return False
    return True

def ap_dung_hanh_dong_cho_trang_thai(huong: str, trang_thai: Tuple[int, ...]) -> Tuple[int, ...]:
    """Áp dụng hành động di chuyển cho trạng thái hiện tại."""
    vi_tri_so_khong = trang_thai.index(0)
    if la_di_chuyen_hop_le(vi_tri_so_khong, huong):
        trang_thai_moi = list(trang_thai)
        do_doi_vi_tri = CAC_HANH_DONG_DI_CHUYEN[huong]
        trang_thai_moi[vi_tri_so_khong], trang_thai_moi[vi_tri_so_khong + do_doi_vi_tri] = \
            trang_thai_moi[vi_tri_so_khong + do_doi_vi_tri], trang_thai_moi[vi_tri_so_khong]
        return tuple(trang_thai_moi)
    return trang_thai

def tinh_khoang_cach_manhattan(trang_thai: Tuple[int, ...], muc_tieu: Tuple[int, ...]) -> int:
    """Tính heuristic khoảng cách Manhattan."""
    khoang_cach = 0
    for i, gia_tri in enumerate(trang_thai):
        if gia_tri == 0:
            continue
        for j, muc_tieu_gia_tri in enumerate(muc_tieu):
            if muc_tieu_gia_tri == gia_tri:
                hang_hien_tai, cot_hien_tai = i // KICH_THUOC_LUOI, i % KICH_THUOC_LUOI
                hang_muc_tieu, cot_muc_tieu = j // KICH_THUOC_LUOI, j % KICH_THUOC_LUOI
                khoang_cach += abs(hang_hien_tai - hang_muc_tieu) + abs(cot_hien_tai - cot_muc_tieu)
                break
    return khoang_cach

class NutTimKiem:
    """Lớp đại diện cho một nút trong cây tìm kiếm."""
    def __init__(self, cha: Optional['NutTimKiem'], hanh_dong: Optional[str], trang_thai: Tuple[int, ...]):
        self.cha = cha
        self.hanh_dong = hanh_dong
        self.trang_thai = trang_thai
        self.chi_phi_g = (cha.chi_phi_g + 1) if cha else 0
        self.chi_phi_h = tinh_khoang_cach_manhattan(trang_thai, trang_thai_muc_tieu)

    def __lt__(self, nut_khac: 'NutTimKiem') -> bool:
        return (self.chi_phi_g + self.chi_phi_h) < (nut_khac.chi_phi_g + nut_khac.chi_phi_h)

def tim_kiem_a_sao(bai_toan: Dict[str, Tuple[int, ...]]) -> Optional[List[str]]:
    """Tìm kiếm A* để giải bài toán 8-puzzle."""
    global so_luong_trang_thai_da_mo
    so_luong_trang_thai_da_mo = 0
    danh_sach_mo = []
    heapq.heapify(danh_sach_mo)
    danh_sach_dong = set()
    nut_ban_dau = NutTimKiem(None, None, bai_toan['trang_thai_ban_dau'])
    heapq.heappush(danh_sach_mo, (nut_ban_dau.chi_phi_g + nut_ban_dau.chi_phi_h, nut_ban_dau))
    danh_sach_dong.add(nut_ban_dau.trang_thai)

    while danh_sach_mo:
        so_luong_trang_thai_da_mo += 1
        _, nut_hien_tai = heapq.heappop(danh_sach_mo)
        if nut_hien_tai.trang_thai == trang_thai_muc_tieu:
            duong_di = []
            while nut_hien_tai.cha:
                duong_di.append(nut_hien_tai.hanh_dong)
                nut_hien_tai = nut_hien_tai.cha
            return duong_di[::-1]
        for hanh_dong in CAC_HANH_DONG_DI_CHUYEN.keys():
            trang_thai_moi = ap_dung_hanh_dong_cho_trang_thai(hanh_dong, nut_hien_tai.trang_thai)
            if trang_thai_moi not in danh_sach_dong:
                nut_moi = NutTimKiem(nut_hien_tai, hanh_dong, trang_thai_moi)
                heapq.heappush(danh_sach_mo, (nut_moi.chi_phi_g + nut_moi.chi_phi_h, nut_moi))
                danh_sach_dong.add(trang_thai_moi)
    return None

def in_bang(trang_thai: Tuple[int, ...]):
    """In trạng thái bài toán ra console."""
    for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
        print(list(trang_thai[i:i + KICH_THUOC_LUOI]))
    print()

class GiaiDo8So(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Giải Đố 8 Số - Môi Trường Phức Tạp")
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_CAO_CUA_SO}")
        self.resizable(False, False)
        self.toc_do_moi_buoc_ms = 1000
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = []
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
        self.o_ket_qua = tk.Text(khung_ket_qua, height=10, width=50)
        self.o_ket_qua.grid(row=0, column=0, padx=5, pady=5)
        thanh_cuon = ttk.Scrollbar(khung_ket_qua, orient="vertical", command=self.o_ket_qua.yview)
        thanh_cuon.grid(row=0, column=1, sticky="ns")
        self.o_ket_qua.config(yscrollcommand=thanh_cuon.set)

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

    def xu_ly_nut_giai(self):
        """Xử lý sự kiện nhấn nút Giải."""
        global lo_trinh_giai_phap
        try:
            toc_do = float(self.o_toc_do.get())
            if toc_do < 0.001:
                raise ValueError("Tốc độ mỗi bước phải lớn hơn hoặc bằng 0.001 giây")
            self.toc_do_moi_buoc_ms = int(toc_do * 1000)
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
            return

        thoi_gian_bat_dau = time.perf_counter()
        bai_toan = {'trang_thai_ban_dau': trang_thai_ban_dau}
        chuoi_hanh_dong = tim_kiem_a_sao(bai_toan)

        print("Trạng thái ban đầu:", trang_thai_ban_dau)
        print("Trạng thái mục tiêu:", trang_thai_muc_tieu)
        print("Chuỗi hành động:", chuoi_hanh_dong)

        self.o_ket_qua.delete(1.0, tk.END)
        if chuoi_hanh_dong is None:
            messagebox.showinfo("Kết quả", "Không tìm thấy giải pháp!")
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc, "0")
            self.o_buoc.delete(0, tk.END)
            self.o_buoc, "0".insert(0, str(self.buoc_hien_tai))
        else:
            lo_trinh_giai_phap = [trang_thai_ban_dau]
            trang_thai_hien_tai trang_thai_ban_dau
            for hanh_dong in chuoi_hanh_dong:
                trang_thai_hien_tai = ap_dung_hanh_dong_cho(hanh_dong, trang_thai_hien_tai)
                lo_trinh_giai_phap.append(trang_thai_hien_tai)
            for buoc in lo_trinh_giai_phap:
                for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
                    self.o_ket_qua.insert(tk.END, f"{list(buoc[i:i + KICH_THUOC_LUOI])}\n")
                self.o_ket_qua.insert(tk.END, "\n")
            self.chay_giai_phap(lo_trinh_giai_phap)
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, str(len(lo_trinh_giai_phap) - 1))

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