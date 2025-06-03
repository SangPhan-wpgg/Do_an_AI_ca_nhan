import tkinter as tk
from tkinter import messagebox, ttk
import time
from collections import deque
import heapq
from typing import Tuple, List, Optional, Dict

# Hằng số
KICH_THUOC_LUOI = 3
KICH_THUOC_BAI_TOAN = KICH_THUOC_LUOI * KICH_THUOC_LUOI
CHIEU_RONG_CUA_SO = 840
CHIEU_CAO_CUA_SO = 611

# Biến toàn cục
trang_thai_ban_dau = tuple([0] * KICH_THUOC_BAI_TOAN)
trang_thai_muc_tieu = tuple([6, 7, 8, 0, 1, 2, 3, 4, 5])
lo_trinh_giai_phap = []

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

def tinh_khoang_cach_manhattan(trang_thai: Tuple[int, ...], muc_tieu: Tuple[int, ...]) -> int:
    """Tính heuristic khoảng cách Manhattan từ trạng thái hiện tại đến mục tiêu."""
    khoang_cach = 0
    for i, gia_tri in enumerate(trang_thai):
        if gia_tri == 0:
            continue
        hang_hien_tai, cot_hien_tai = i // KICH_THUOC_LUOI, i % KICH_THUOC_LUOI
        for j, muc_tieu_gia_tri in enumerate(muc_tieu):
            if muc_tieu_gia_tri == gia_tri:
                hang_muc_tieu, cot_muc_tieu = j // KICH_THUOC_LUOI, j % KICH_THUOC_LUOI
                khoang_cach += abs(hang_hien_tai - hang_muc_tieu) + abs(cot_hien_tai - cot_muc_tieu)
                break
    return khoang_cach

class NutTimKiem:
    """Lớp đại diện cho một nút trong cây tìm kiếm."""
    def __init__(self, cha: Optional['NutTimKiem'] = None, hanh_dong: Optional[str] = None, trang_thai: Tuple[int, ...] = tuple([0] * KICH_THUOC_BAI_TOAN)):
        self.cha = cha
        self.hanh_dong = hanh_dong
        self.trang_thai = trang_thai
        self.chi_phi_g = (cha.chi_phi_g + 1) if cha else 0
        self.chi_phi_h = tinh_khoang_cach_manhattan(trang_thai, trang_thai_muc_tieu)

    def __lt__(self, nut_khac: 'NutTimKiem') -> bool:
        return (self.chi_phi_g + self.chi_phi_h) < (nut_khac.chi_phi_g + nut_khac.chi_phi_h)

class DanhSachMo:
    """Lớp quản lý danh sách các nút đang chờ xử lý."""
    def __init__(self, loai_tim_kiem: str):
        self.loai_tim_kiem = loai_tim_kiem
        self.danh_sach = deque() if loai_tim_kiem in ["BFS", "DFS"] else []
        if self.loai_tim_kiem in ["UCS", "A*", "Greedy"]:
            heapq.heapify(self.danh_sach)

    def them(self, nut: NutTimKiem):
        """Thêm nút vào danh sách mở."""
        if self.loai_tim_kiem == "BFS":
            self.danh_sach.append(nut)
        elif self.loai_tim_kiem == "DFS":
            self.danh_sach.append(nut)
        elif self.loai_tim_kiem == "UCS":
            heapq.heappush(self.danh_sach, (nut.chi_phi_g, nut))
        elif self.loai_tim_kiem == "A*":
            heapq.heappush(self.danh_sach, (nut.chi_phi_g + nut.chi_phi_h, nut))
        elif self.loai_tim_kiem == "Greedy":
            heapq.heappush(self.danh_sach, (nut.chi_phi_h, nut))

    def lay_phan_tu(self) -> Optional[NutTimKiem]:
        """Lấy nút tiếp theo từ danh sách mở."""
        if self.la_rong():
            return None
        if self.loai_tim_kiem == "BFS":
            return self.danh_sach.popleft()
        elif self.loai_tim_kiem == "DFS":
            return self.danh_sach.pop()
        elif self.loai_tim_kiem in ["UCS", "A*", "Greedy"]:
            return heapq.heappop(self.danh_sach)[1]
        return None

    def la_rong(self) -> bool:
        """Kiểm tra danh sách mở có rỗng không."""
        return len(self.danh_sach) == 0

class DanhSachDong:
    """Lớp quản lý danh sách các trạng thái đã duyệt."""
    def __init__(self):
        self.tap_hop_trang_thai = set()

    def tra_cuu(self, trang_thai: Tuple[int, ...]) -> bool:
        """Kiểm tra trạng thái đã được duyệt chưa."""
        return trang_thai in self.tap_hop_trang_thai

    def them(self, trang_thai: Tuple[int, ...]):
        """Thêm trạng thái vào danh sách đã duyệt."""
        self.tap_hop_trang_thai.add(trang_thai)

def tim_kiem(bai_toan: Dict[str, Tuple[int, ...]], loai_tim_kiem: str) -> Optional[NutTimKiem]:
    """Thực hiện tìm kiếm theo loại được chỉ định (BFS, DFS, UCS, A*, Greedy)."""
    danh_sach_mo = DanhSachMo(loai_tim_kiem)
    danh_sach_dong = DanhSachDong()
    nut_ban_dau = NutTimKiem(None, None, bai_toan['trang_thai_ban_dau'])
    danh_sach_mo.them(nut_ban_dau)

    while not danh_sach_mo.la_rong():
        nut_hien_tai = danh_sach_mo.lay_phan_tu()
        if nut_hien_tai.trang_thai == trang_thai_muc_tieu:
            return nut_hien_tai
        if not danh_sach_dong.tra_cuu(nut_hien_tai.trang_thai):
            danh_sach_dong.them(nut_hien_tai.trang_thai)
            for hanh_dong in lay_danh_sach_hanh_dong_hop_le(nut_hien_tai.trang_thai):
                trang_thai_moi = di_chuyen_o(nut_hien_tai.trang_thai, hanh_dong)
                if not danh_sach_dong.tra_cuu(trang_thai_moi):
                    nut_moi = NutTimKiem(nut_hien_tai, hanh_dong, trang_thai_moi)
                    danh_sach_mo.them(nut_moi)
    return None

def trich_xuat_duong_di(nut: Optional[NutTimKiem]) -> List[Tuple[int, ...]]:
    """Trích xuất lộ trình từ nút mục tiêu về nút ban đầu."""
    duong_di = []
    while nut:
        duong_di.append(nut.trang_thai)
        nut = nut.cha
    return duong_di[::-1]

def in_bang(bang: Tuple[int, ...]):
    """In trạng thái bài toán ra console."""
    for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
        print(list(bang[i:i + KICH_THUOC_LUOI]))
    print()

class GiaiDo8So(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Giải Đố 8 Số - Tìm Kiếm Thông Minh")
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
        self.thuat_toan = ttk.Combobox(khung_dieu_khien, values=["BFS", "DFS", "UCS", "A*", "Greedy"], state="readonly")
        self.thuat_toan.grid(row=0, column=1, padx=5)
        self.thuat_toan.set("A*")

        ttk.Label(khung_dieu_khien, text="Tốc Độ Mỗi Bước (giây):").grid(row=0, column=2, padx=5)
        self.o_toc_do = ttk.Entry(khung_dieu_khien, width=10)
        self.o_toc_do.grid(row=0, column=3, padx=5)
        self.o_toc_do.insert(0, "1.0")

        ttk.Label(khung_dieu_khien, text="Bước:").grid(row=0, column=4, padx=5)
        self.o_buoc = ttk.Entry(khung_dieu_khien, width=5, state="readonly")
        self.o_buoc.grid(row=0, column=5, padx=5)

        ttk.Label(khung_dieu_khien, text="Tổng Số Bước:").grid(row=0, column=6, padx=5)
        self.o_tong_buoc = ttk.Entry(khung_dieu_khien, width=5, state="readonly")
        self.o_tong_buoc.grid(row=0, column=7, padx=5)

        ttk.Label(khung_dieu_khien, text="Thời Gian Giải:").grid(row=0, column=8, padx=5)
        self.o_thoi_gian_giai = ttk.Entry(khung_dieu_khien, width=15, state="readonly")
        self.o_thoi_gian_giai.grid(row=0, column=9, padx=5)

        ttk.Button(khung_dieu_khien, text="Giải", command=self.xu_ly_nut_giai).grid(row=0, column=10, padx=5)
        ttk.Button(khung_dieu_khien, text="Tải Giá Trị", command=self.tai_gia_tri).grid(row=0, column=11, padx=5)

        # Khu vực kết quả
        self.o_ket_qua = tk.Text(khung_ket_qua, height=15, width=60)
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
            
            trang_thai_ban_dau = tuple(ban_dau)
            trang_thai_muc_tieu = tuple(muc_tieu)
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
        bai_toan = {'trang_thai_ban_dau': trang_thai_ban_dau}
        loai_tim_kiem = self.thuat_toan.get()
        nut_muc_tieu = tim_kiem(bai_toan, loai_tim_kiem)

        print("Trạng thái ban đầu:", trang_thai_ban_dau)
        print("Trạng thái mục tiêu:", trang_thai_muc_tieu)
        print("Thuật toán:", loai_tim_kiem)

        self.o_ket_qua.delete(1.0, tk.END)
        if nut_muc_tieu:
            lo_trinh_giai_phap = trich_xuat_duong_di(nut_muc_tieu)
            print("Lộ trình giải pháp:")
            for buoc in lo_trinh_giai_phap:
                in_bang(buoc)
                for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
                    self.o_ket_qua.insert(tk.END, f"{list(buoc[i:i + KICH_THUOC_LUOI])}\n")
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