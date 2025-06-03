import tkinter as tk
from tkinter import messagebox, ttk
import time
from collections import deque
from typing import Tuple, List, Dict, Optional

# Hằng số
CHIEU_RONG_CUA_SO = 600
CHIEU_CAO_CUA_SO = 400
KICH_THUOC_LUOI = 3
KICH_THUOC_BAI_TOAN = KICH_THUOC_LUOI * KICH_THUOC_LUOI

# Biến toàn cục
trang_thai_ban_dau = tuple([0] * KICH_THUOC_BAI_TOAN)
trang_thai_muc_tieu = tuple([0] * KICH_THUOC_BAI_TOAN)
lo_trinh_giai_phap = None

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

def kiem_tra_trang_thai_muc_tieu(trang_thai: Tuple[int, ...]) -> bool:
    """Kiểm tra xem trạng thái hiện tại có phải là trạng thái mục tiêu không."""
    return trang_thai == trang_thai_muc_tieu

def tim_vi_tri_o_trong(trang_thai: Tuple[int, ...]) -> Tuple[int, int]:
    """Tìm vị trí (hàng, cột) của ô trống (0)."""
    chi_so = trang_thai.index(0)
    return chi_so // KICH_THUOC_LUOI, chi_so % KICH_THUOC_LUOI

def di_chuyen_o(trang_thai: Tuple[int, ...], huong: str) -> Tuple[int, ...]:
    """Di chuyển ô trống theo hướng chỉ định và trả về trạng thái mới."""
    hang, cot = tim_vi_tri_o_trong(trang_thai)
    chi_so_o_trong = hang * KICH_THUOC_LUOI + cot
    trang_thai_moi = list(trang_thai)

    if huong == 'lên' and hang > 0:
        chi_so_hoan_doi = (hang - 1) * KICH_THUOC_LUOI + cot
    elif huong == 'xuống' and hang < KICH_THUOC_LUOI - 1:
        chi_so_hoan_doi = (hang + 1) * KICH_THUOC_LUOI + cot
    elif huong == 'trái' and cot > 0:
        chi_so_hoan_doi = hang * KICH_THUOC_LUOI + (cot - 1)
    elif huong == 'phải' and cot < KICH_THUOC_LUOI - 1:
        chi_so_hoan_doi = hang * KICH_THUOC_LUOI + (cot + 1)
    else:
        return trang_thai

    trang_thai_moi[chi_so_o_trong], trang_thai_moi[chi_so_hoan_doi] = trang_thai_moi[chi_so_hoan_doi], trang_thai_moi[chi_so_o_trong]
    return tuple(trang_thai_moi)

def lay_danh_sach_hanh_dong_hop_le(trang_thai: Tuple[int, ...]) -> List[str]:
    """Trả về danh sách các hành động hợp lệ cho trạng thái hiện tại."""
    hang, cot = tim_vi_tri_o_trong(trang_thai)
    danh_sach_hanh_dong = []
    if hang > 0:
        danh_sach_hanh_dong.append('lên')
    if hang < KICH_THUOC_LUOI - 1:
        danh_sach_hanh_dong.append('xuống')
    if cot > 0:
        danh_sach_hanh_dong.append('trái')
    if cot < KICH_THUOC_LUOI - 1:
        danh_sach_hanh_dong.append('phải')
    return danh_sach_hanh_dong

def lay_trang_thai_ket_qua(trang_thai: Tuple[int, ...], hanh_dong: str) -> List[Tuple[int, ...]]:
    """Trả về trạng thái sau khi thực hiện hành động (xác định)."""
    return [di_chuyen_o(trang_thai, hanh_dong)]

def tim_kiem_and_or(bai_toan: Dict) -> Optional[List]:
    """Thực hiện tìm kiếm AND-OR để tìm kế hoạch đạt trạng thái mục tiêu."""
    bo_nho_tam = {}
    return tim_kiem_or(bai_toan['trang_thai_ban_dau'], bai_toan, [], 0, bo_nho_tam)

def tim_kiem_or(trang_thai: Tuple[int, ...], bai_toan: Dict, lo_trinh: List[Tuple[int, ...]], do_sau: int, bo_nho_tam: Dict) -> Optional[List]:
    """Tìm kiếm OR: Khám phá các hành động từ một trạng thái."""
    if kiem_tra_trang_thai_muc_tieu(trang_thai):
        return []
    if trang_thai in lo_trinh:
        return 'thất_bại'
    if do_sau > 1000:
        return 'thất_bại'
    if trang_thai in bo_nho_tam:
        return bo_nho_tam[trang_thai]

    for hanh_dong in lay_danh_sach_hanh_dong_hop_le(trang_thai):
        danh_sach_trang_thai_con = lay_trang_thai_ket_qua(trang_thai, hanh_dong)
        ke_hoach_con = tim_kiem_and(danh_sach_trang_thai_con, bai_toan, lo_trinh + [trang_thai], do_sau + 1, bo_nho_tam)
        if ke_hoach_con != 'thất_bại':
            ke_hoach_day_du = [hanh_dong, ke_hoach_con]
            bo_nho_tam[trang_thai] = ke_hoach_day_du
            return ke_hoach_day_du
    bo_nho_tam[trang_thai] = 'thất_bại'
    return 'thất_bại'

def tim_kiem_and(danh_sach_trang_thai: List[Tuple[int, ...]], bai_toan: Dict, lo_trinh: List[Tuple[int, ...]], do_sau: int, bo_nho_tam: Dict) -> Optional[List]:
    """Tìm kiếm AND: Xử lý nhiều trạng thái con."""
    danh_sach_ke_hoach = []
    for trang_thai_con in danh_sach_trang_thai:
        ke_hoach_con = tim_kiem_or(trang_thai_con, bai_toan, lo_trinh, do_sau + 1, bo_nho_tam)
        if ke_hoach_con == 'thất_bại':
            return 'thất_bại'
        danh_sach_ke_hoach.append(ke_hoach_con)
    return danh_sach_ke_hoach

def trich_xuat_chuoi_trang_thai(ke_hoach, trang_thai_hien_tai: Tuple[int, ...]) -> List[Tuple[int, ...]]:
    """Trích xuất chuỗi các trạng thái từ kế hoạch."""
    if ke_hoach == 'thất_bại' or ke_hoach == []:
        return [trang_thai_hien_tai]
    
    chuoi_trang_thai = [trang_thai_hien_tai]
    if isinstance(ke_hoach, list):
        hanh_dong = ke_hoach[0]
        ke_hoach_con = ke_hoach[1]
        trang_thai_tiep_theo = lay_trang_thai_ket_qua(trang_thai_hien_tai, hanh_dong)[0]
        if isinstance(ke_hoach_con, list) and all(isinstance(kh, list) for kh in ke_hoach_con):
            if ke_hoach_con:
                chuoi_trang_thai += trich_xuat_chuoi_trang_thai(ke_hoach_con[0], trang_thai_tiep_theo)
        else:
            chuoi_trang_thai += trich_xuat_chuoi_trang_thai(ke_hoach_con, trang_thai_tiep_theo)
    return chuoi_trang_thai

def in_trang_thai_ra_man_hinh(trang_thai: Tuple[int, ...]):
    """In trạng thái bài toán ra console."""
    for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
        print(list(trang_thai[i:i + KICH_THUOC_LUOI]))
    print("-" * 10)

class GiaiDo8So(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Giải Đố 8 Số - Tìm Kiếm AND-OR")
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_CAO_CUA_SO}")
        self.resizable(False, False)
        self.toc_do_moi_buoc_ms = 1000
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = []
        self.thiet_lap_giao_dien()

    def thiet_lap_giao_dien(self):
        """Thiết lập giao diện người dùng Tkinter."""
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
                o_nhap.insert(0, "0")
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

        # Hiển thị lộ trình giải pháp
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
        ke_hoach = tim_kiem_and_or(bai_toan)

        print("Trạng thái ban đầu:", trang_thai_ban_dau)
        print("Trạng thái mục tiêu:", trang_thai_muc_tieu)
        print("Kế hoạch tìm được:", ke_hoach)

        self.o_ket_qua.delete(1.0, tk.END)
        if ke_hoach == 'thất_bại':
            messagebox.showinfo("Kết quả", "Không tìm thấy giải pháp!")
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, "0")
            self.o_buoc.delete(0, tk.END)
            self.o_buoc.insert(0, "0")
        else:
            lo_trinh_giai_phap = trich_xuat_chuoi_trang_thai(ke_hoach, trang_thai_ban_dau)
            print("Lộ trình giải pháp:", lo_trinh_giai_phap)
            for buoc in lo_trinh_giai_phap:
                for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
                    self.o_ket_qua.insert(tk.END, f"{list(buoc[i:i + KICH_THUOC_LUOI])}\n")
                self.o_ket_qua.insert(tk.END, "\n")
            self.chay_giai_phap(lo_trinh_giai_phap)
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, str(len(lo_trinh_giai_phap) - 1))

        thoi_gian_ket_thuc = time.perf_counter()
        self.o_thoi_gian_giai.delete(0, tk.END)
        self.o_thoi_gian_giai.insert(0, f"{thoi_gian_ket_thuc - thoi_gian_bat_dau:.9f} (giây)")

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