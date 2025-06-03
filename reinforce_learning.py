import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from typing import Tuple, List, Optional, Dict
from collections import defaultdict

# Hằng số
CHIEU_RONG_CUA_SO = 840
CHIEU_CAO_CUA_SO = 611
KICH_THUOC_LUOI = 3
KICH_THUOC_BAI_TOAN = KICH_THUOC_LUOI * KICH_THUOC_LUOI
CAC_HANH_DONG = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

# Cấu trúc dữ liệu
class NutTimKiem:
    def __init__(self, trang_thai: Tuple[int, ...], cha: Optional['NutTimKiem'] = None,
                 hanh_dong: Optional[str] = None, chi_phi_g: int = 0):
        self.trang_thai = trang_thai
        self.cha = cha
        self.hanh_dong = hanh_dong
        self.chi_phi_g = chi_phi_g
        self.chi_phi_h = 0

class DanhSachMo:
    def __init__(self, loai_tim_kiem: str):
        self.hang_doi = []
        self.loai_tim_kiem = loai_tim_kiem

    def them(self, nut: NutTimKiem):
        if self.loai_tim_kiem == "BFS":
            self.hang_doi.append(nut)
        elif self.loai_tim_kiem == "DFS":
            self.hang_doi.insert(0, nut)
        elif self.loai_tim_kiem in ["UCS", "A*", "Greedy", "Beam search"]:
            self.hang_doi.append((self.tinh_chi_phi(nut), nut))
            self.hang_doi.sort(key=lambda x: x[0])
        else:
            raise ValueError("Loại tìm kiếm không hợp lệ!")

    def lay_phan_tu(self) -> Optional[NutTimKiem]:
        if not self.hang_doi:
            return None
        if self.loai_tim_kiem in ["BFS", "DFS"]:
            return self.hang_doi.pop(0)
        return self.hang_doi.pop(0)[1]

    def la_rong(self) -> bool:
        return len(self.hang_doi) == 0

    def tinh_chi_phi(self, nut: NutTimKiem) -> float:
        if self.loai_tim_kiem == "UCS":
            return nut.chi_phi_g
        elif self.loai_tim_kiem == "Greedy":
            return nut.chi_phi_h
        elif self.loai_tim_kiem == "A*":
            return nut.chi_phi_g + nut.chi_phi_h
        elif self.loai_tim_kiem == "Beam search":
            return nut.chi_phi_h
        return 0

class DanhSachDong:
    def __init__(self):
        self.tap_hop_trang_thai = set()

    def them(self, trang_thai: Tuple[int, ...]):
        self.tap_hop_trang_thai.add(trang_thai)

    def tra_cuu(self, trang_thai: Tuple[int, ...]) -> bool:
        return trang_thai in self.tap_hop_trang_thai

def tao_nut_tim_kiem(cha: Optional[NutTimKiem], hanh_dong: Optional[str],
                      trang_thai: Tuple[int, ...]) -> NutTimKiem:
    chi_phi_g = cha.chi_phi_g + 1 if cha else 0
    return NutTimKiem(trang_thai, cha, hanh_dong, chi_phi_g)

def trich_xuat_duong_di(nut: NutTimKiem) -> List[Tuple[int, ...]]:
    duong_di = []
    while nut:
        duong_di.append(nut.trang_thai)
        nut = nut.cha
    return duong_di[::-1]

# Hàm tiện ích
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

def ham_heuristic(trang_thai: Tuple[int, ...], trang_thai_dich: Tuple[int, ...]) -> int:
    """Tính heuristic kết hợp Manhattan và số ô sai vị trí."""
    manhattan = 0
    sai_vi_tri = 0
    for i in range(1, KICH_THUOC_BAI_TOAN):
        x1, y1 = divmod(trang_thai.index(i), KICH_THUOC_LUOI)
        x2, y2 = divmod(trang_thai_dich.index(i), KICH_THUOC_LUOI)
        manhattan += abs(x1 - x2) + abs(y1 - y2)
        if trang_thai[i - 1] != trang_thai_dich[i - 1]:
            sai_vi_tri += 1
    return manhattan + sai_vi_tri

def kiem_tra_trang_thai_dich(trang_thai: Tuple[int, ...], trang_thai_dich: Tuple[int, ...]) -> bool:
    return trang_thai == trang_thai_dich

def tim_cac_trang_thai_ke_tiep(trang_thai: Tuple[int, ...]) -> List[Tuple[str, Tuple[int, ...]]]:
    danh_sach_con = []
    vi_tri_khong = trang_thai.index(0)
    hang, cot = vi_tri_khong // KICH_THUOC_LUOI, vi_tri_khong % KICH_THUOC_LUOI
    for hanh_dong, (dh, dc) in CAC_HANH_DONG.items():
        h_moi, c_moi = hang + dh, cot + dc
        if 0 <= h_moi < KICH_THUOC_LUOI and 0 <= c_moi < KICH_THUOC_LUOI:
            vi_tri_moi = h_moi * KICH_THUOC_LUOI + c_moi
            trang_thai_moi = list(trang_thai)
            trang_thai_moi[vi_tri_khong], trang_thai_moi[vi_tri_moi] = trang_thai_moi[vi_tri_moi], trang_thai_moi[vi_tri_khong]
            danh_sach_con.append((hanh_dong, tuple(trang_thai_moi)))
    return danh_sach_con

# Thuật toán tìm kiếm
def tim_kiem_khong_thong_tin(nut_goc: NutTimKiem, loai_tim_kiem: str,
                             trang_thai_dich: Tuple[int, ...]) -> Optional[List[Tuple[int, ...]]]:
    danh_sach_mo = DanhSachMo(loai_tim_kiem)
    danh_sach_mo.them(nut_goc)
    danh_sach_dong = DanhSachDong()
    while not danh_sach_mo.la_rong():
        nut_hien_tai = danh_sach_mo.lay_phan_tu()
        if danh_sach_dong.tra_cuu(nut_hien_tai.trang_thai):
            continue
        danh_sach_dong.them(nut_hien_tai.trang_thai)
        if kiem_tra_trang_thai_dich(nut_hien_tai.trang_thai, trang_thai_dich):
            return trich_xuat_duong_di(nut_hien_tai), danh_sach_dong
        for hanh_dong, trang_thai_moi in tim_cac_trang_thai_ke_tiep(nut_hien_tai.trang_thai):
            if not danh_sach_dong.tra_cuu(trang_thai_moi):
                nut_moi = tao_nut_tim_kiem(nut_hien_tai, hanh_dong, trang_thai_moi)
                danh_sach_mo.them(nut_moi)
    return None, danh_sach_dong

def tim_kiem_do_sau_lap(nut_goc: NutTimKiem, trang_thai_dich: Tuple[int, ...]) -> Optional[List[Tuple[int, ...]]]:
    do_sau_toi_da = 100
    for do_sau in range(do_sau_toi_da + 1):
        ngan_xep = [(nut_goc, [nut_goc.trang_thai])]
        danh_sach_dong = DanhSachDong()
        while ngan_xep:
            nut_hien_tai, duong_di = ngan_xep.pop()
            if kiem_tra_trang_thai_dich(nut_hien_tai.trang_thai, trang_thai_dich):
                return duong_di, danh_sach_dong
            if len(duong_di) - 1 < do_sau and not danh_sach_dong.tra_cuu(nut_hien_tai.trang_thai):
                danh_sach_dong.them(nut_hien_tai.trang_thai)
                for hanh_dong, trang_thai_moi in reversed(tim_cac_trang_thai_ke_tiep(nut_hien_tai.trang_thai)):
                    if not danh_sach_dong.tra_cuu(trang_thai_moi):
                        nut_moi = tao_nut_tim_kiem(nut_hien_tai, hanh_dong, trang_thai_moi)
                        ngan_xep.append((nut_moi, duong_di + [trang_thai_moi]))
    return None, DanhSachDong()

def tim_kiem_a_sao(nut_goc: NutTimKiem, trang_thai_dich: Tuple[int, ...]) -> Optional[List[Tuple[int, ...]]]:
    danh_sach_mo = DanhSachMo("A*")
    nut_goc.chi_phi_h = ham_heuristic(nut_goc.trang_thai, trang_thai_dich)
    danh_sach_mo.them(nut_goc)
    danh_sach_dong = DanhSachDong()
    while not danh_sach_mo.la_rong():
        nut_hien_tai = danh_sach_mo.lay_phan_tu()
        if danh_sach_dong.tra_cuu(nut_hien_tai.trang_thai):
            continue
        danh_sach_dong.them(nut_hien_tai.trang_thai)
        if kiem_tra_trang_thai_dich(nut_hien_tai.trang_thai, trang_thai_dich):
            return trich_xuat_duong_di(nut_hien_tai), danh_sach_dong
        for hanh_dong, trang_thai_moi in tim_cac_trang_thai_ke_tiep(nut_hien_tai.trang_thai):
            if not danh_sach_dong.tra_cuu(trang_thai_moi):
                nut_moi = tao_nut_tim_kiem(nut_hien_tai, hanh_dong, trang_thai_moi)
                nut_moi.chi_phi_h = ham_heuristic(nut_moi.trang_thai, trang_thai_dich)
                danh_sach_mo.them(nut_moi)
    return None, danh_sach_dong

def tim_kiem_luyen_kim_mo_phong(nut_goc: NutTimKiem, trang_thai_dich: Tuple[int, ...]) -> Optional[List[Tuple[int, ...]]]:
    danh_sach_dong = DanhSachDong()
    so_lan_lap_toi_da = 5000  # Giảm số lần lặp
    nut_hien_tai = nut_goc
    danh_sach_dong.them(nut_hien_tai.trang_thai)
    lan_lap = 0
    nhiet_do = 1000  # Nhiệt độ ban đầu ổn định
    giai_phap_tot_nhat = nut_hien_tai
    while lan_lap < so_lan_lap_toi_da and nhiet_do > 1e-3:
        lan_lap += 1
        if kiem_tra_trang_thai_dich(nut_hien_tai.trang_thai, trang_thai_dich):
            return trich_xuat_duong_di(nut_hien_tai), danh_sach_dong
        cac_hang_xom = tim_cac_trang_thai_ke_tiep(nut_hien_tai.trang_thai)
        if not cac_hang_xom:
            return trich_xuat_duong_di(giai_phap_tot_nhat), danh_sach_dong
        hanh_dong, trang_thai_moi = random.choice(cac_hang_xom)
        nut_ke_tiep = tao_nut_tim_kiem(nut_hien_tai, hanh_dong, trang_thai_moi)
        delta_e = ham_heuristic(nut_ke_tiep.trang_thai, trang_thai_dich) - ham_heuristic(nut_hien_tai.trang_thai, trang_thai_dich)
        if delta_e < 0 or random.random() < math.exp(-delta_e / nhiet_do):
            nut_hien_tai = nut_ke_tiep
            danh_sach_dong.them(nut_hien_tai.trang_thai)
            if ham_heuristic(nut_hien_tai.trang_thai, trang_thai_dich) < ham_heuristic(giai_phap_tot_nhat.trang_thai, trang_thai_dich):
                giai_phap_tot_nhat = nut_hien_tai
        nhiet_do *= 0.95  # Tỷ lệ làm nguội cố định
    return trich_xuat_duong_di(giai_phap_tot_nhat), danh_sach_dong

def giai_thuat_di_truyen(nut_goc: NutTimKiem, trang_thai_dich: Tuple[int, ...],
                         kich_thuoc_quan_the: int = 30, so_the_he: int = 50, ti_le_dot_bien: float = 0.2) -> Optional[List[Tuple[int, ...]]]:
    danh_sach_dong = DanhSachDong()
    quan_the = []
    trang_thai_ban_dau = nut_goc.trang_thai
    if kiem_tra_trang_thai_dich(trang_thai_ban_dau, trang_thai_dich):
        danh_sach_dong.them(trang_thai_ban_dau)
        return [trang_thai_ban_dau], danh_sach_dong
    cac_trang_thai_lan_can = tim_cac_trang_thai_ke_tiep(trang_thai_ban_dau)
    for _, trang_thai in cac_trang_thai_lan_can:
        if len(quan_the) < kich_thuoc_quan_the:
            quan_the.append((trang_thai, ham_heuristic(trang_thai, trang_thai_dich)))
            danh_sach_dong.them(trang_thai)
    while len(quan_the) < kich_thuoc_quan_the:
        trang_thai_ngau_nhien = tuple(random.sample(range(9), 9))
        if trang_thai_ngau_nhien not in {tt for tt, _ in quan_the}:
            quan_the.append((trang_thai_ngau_nhien, ham_heuristic(trang_thai_ngau_nhien, trang_thai_dich)))
            danh_sach_dong.them(trang_thai_ngau_nhien)
    for _ in range(so_the_he):
        quan_the.sort(key=lambda x: x[1])
        if quan_the[0][1] == 0:
            return [quan_the[0][0]], danh_sach_dong
        quan_the_moi = quan_the[:2]
        while len(quan_the_moi) < kich_thuoc_quan_the:
            cha1, cha2 = random.choices(quan_the[:len(quan_the) // 2], k=2)
            con1, con2 = lai_ghep_thu_tu(cha1[0], cha2[0])
            if random.random() < ti_le_dot_bien:
                con1 = dot_bien_hoan_vi(con1)
            if random.random() < ti_le_dot_bien:
                con2 = dot_bien_hoan_vi(con2)
            if con1 not in {tt for tt, _ in quan_the_moi}:
                quan_the_moi.append((con1, ham_heuristic(con1, trang_thai_dich)))
                danh_sach_dong.them(con1)
            if len(quan_the_moi) < kich_thuoc_quan_the and con2 not in {tt for tt, _ in quan_the_moi}:
                quan_the_moi.append((con2, ham_heuristic(con2, trang_thai_dich)))
                danh_sach_dong.them(con2)
        quan_the = quan_the_moi
    return None, danh_sach_dong

def lai_ghep_thu_tu(cha1: Tuple[int, ...], cha2: Tuple[int, ...]) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    kich_thuoc = KICH_THUOC_BAI_TOAN
    cha1_list, cha2_list = list(cha1), list(cha2)
    diem_bat_dau, diem_ket_thuc = sorted(random.sample(range(kich_thuoc), 2))
    con1, con2 = [None] * kich_thuoc, [None] * kich_thuoc
    con1[diem_bat_dau:diem_ket_thuc + 1] = cha1_list[diem_bat_dau:diem_ket_thuc + 1]
    con2[diem_bat_dau:diem_ket_thuc + 1] = cha2_list[diem_bat_dau:diem_ket_thuc + 1]
    chi_so_cha2 = chi_so_cha1 = 0
    for i in range(kich_thuoc):
        if con1[i] is None:
            while cha2_list[chi_so_cha2] in con1:
                chi_so_cha2 += 1
            con1[i] = cha2_list[chi_so_cha2]
        if con2[i] is None:
            while cha1_list[chi_so_cha1] in con2:
                chi_so_cha1 += 1
            con2[i] = cha1_list[chi_so_cha1]
    return tuple(con1), tuple(con2)

def dot_bien_hoan_vi(ca_the: Tuple[int, ...]) -> Tuple[int, ...]:
    ca_the_list = list(ca_the)
    vi_tri1, vi_tri2 = random.sample(range(len(ca_the_list)), 2)
    ca_the_list[vi_tri1], ca_the_list[vi_tri2] = ca_the_list[vi_tri2], ca_the_list[vi_tri1]
    return tuple(ca_the_list)

def giai_bang_hoc_tang_cuong(trang_thai_bat_dau: Tuple[int, ...], trang_thai_dich: Tuple[int, ...]) -> Optional[List[Tuple[int, ...]]]:
    alpha = 0.1
    gamma = 0.9
    epsilon = 0.5
    epsilon_min = 0.01
    epsilon_decay = 0.995
    so_luong_episodes = 5000
    SO_BUOC_TOI_DA = 1000
    bang_q = defaultdict(lambda: {a: 0.0 for a in CAC_HANH_DONG.keys()})
    danh_sach_dong = DanhSachDong()
    for _ in range(so_luong_episodes):
        trang_thai_hien_tai = trang_thai_bat_dau
        so_buoc = 0
        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        while not kiem_tra_trang_thai_dich(trang_thai_hien_tai, trang_thai_dich) and so_buoc < SO_BUOC_TOI_DA:
            if random.random() < epsilon:
                hanh_dong = random.choice(list(CAC_HANH_DONG.keys()))
            else:
                hanh_dong = max(bang_q[trang_thai_hien_tai], key=bang_q[trang_thai_hien_tai].get)
            for hd, trang_thai_moi in tim_cac_trang_thai_ke_tiep(trang_thai_hien_tai):
                if hd == hanh_dong:
                    break
            else:
                phan_thuong = -50
                gia_tri_q_toi_da = 0
                xac_suat_chuyen = 0.0001
                trang_thai_moi = None
            if trang_thai_moi:
                phan_thuong = 100 if kiem_tra_trang_thai_dich(trang_thai_moi, trang_thai_dich) else -1
                if trang_thai_moi not in bang_q:
                    bang_q[trang_thai_moi] = {a: 0 for a in CAC_HANH_DONG.keys()}
                gia_tri_q_toi_da = max(bang_q[trang_thai_moi].values())
                xac_suat_chuyen = 1 - ham_heuristic(trang_thai_moi, trang_thai_dich) / 41 if ham_heuristic(trang_thai_moi, trang_thai_dich) < 41 else 0.0001
            bang_q[trang_thai_hien_tai][hanh_dong] += alpha * (
                phan_thuong + gamma * xac_suat_chuyen * gia_tri_q_toi_da - bang_q[trang_thai_hien_tai][hanh_dong]
            )
            if trang_thai_moi is None:
                break
            trang_thai_hien_tai = trang_thai_moi
            danh_sach_dong.them(trang_thai_hien_tai)
            so_buoc += 1
    trang_thai_hien_tai = trang_thai_bat_dau
    giai_phap = [trang_thai_hien_tai]
    so_buoc_giai = 0
    while not kiem_tra_trang_thai_dich(trang_thai_hien_tai, trang_thai_dich) and so_buoc_giai < SO_BUOC_TOI_DA:
        if trang_thai_hien_tai not in bang_q:
            return None, danh_sach_dong
        hanh_dong = max(bang_q[trang_thai_hien_tai], key=bang_q[trang_thai_hien_tai].get)
        for hd, trang_thai_moi in tim_cac_trang_thai_ke_tiep(trang_thai_hien_tai):
            if hd == hanh_dong:
                break
        else:
            return None, danh_sach_dong
        trang_thai_hien_tai = trang_thai_moi
        giai_phap.append(trang_thai_hien_tai)
        danh_sach_dong.them(trang_thai_hien_tai)
        so_buoc_giai += 1
    if kiem_tra_trang_thai_dich(trang_thai_hien_tai, trang_thai_dich):
        return giai_phap, danh_sach_dong
    return None, danh_sach_dong

# Giao diện Tkinter
class UngDungPuzzle(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle - Tìm Kiếm Tổng Quát")
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_CAO_CUA_SO}")
        self.resizable(False, False)
        self.toc_do_moi_buoc_ms = 1000
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = []
        self.trang_thai_bat_dau = (1, 2, 3, 4, 0, 6, 7, 5, 8)
        self.trang_thai_dich = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.danh_sach_dong = DanhSachDong()
        self.thiet_lap_giao_dien()

    def thiet_lap_giao_dien(self):
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

        # Lưới nhập liệu
        self.o_nhap_ban_dau = []
        for i in range(KICH_THUOC_LUOI):
            hang_o = []
            for j in range(KICH_THUOC_LUOI):
                o_nhap = ttk.Entry(khung_trang_thai_ban_dau, width=5, justify="center")
                o_nhap.grid(row=i, column=j, padx=2, pady=2)
                o_nhap.insert(0, str(self.trang_thai_bat_dau[i * KICH_THUOC_LUOI + j]))
                hang_o.append(o_nhap)
            self.o_nhap_ban_dau.append(hang_o)

        self.o_nhap_muc_tieu = []
        for i in range(KICH_THUOC_LUOI):
            hang_o = []
            for j in range(KICH_THUOC_LUOI):
                o_nhap = ttk.Entry(khung_trang_thai_muc_tieu, width=5, justify="center")
                o_nhap.grid(row=i, column=j, padx=2, pady=2)
                o_nhap.insert(0, str(self.trang_thai_dich[i * KICH_THUOC_LUOI + j]))
                hang_o.append(o_nhap)
            self.o_nhap_muc_tieu.append(hang_o)

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
        ttk.Label(khung_dieu_khien, text="Thuật Toán:").grid(row=0, column=0, padx=5)
        self.cbb_thuat_toan = ttk.Combobox(khung_dieu_khien, values=[
            "BFS", "DFS", "A*", "IDS", "Luyện kim mô phỏng", "Giải thuật di truyền", "Học tăng cường"])
        self.cbb_thuat_toan.grid(row=0, column=1, padx=5)
        self.cbb_thuat_toan.set("A*")

        ttk.Label(khung_dieu_khien, text="Tốc Độ (giây):").grid(row=0, column=2, padx=5)
        self.o_toc_do = ttk.Entry(khung_dieu_khien, width=10)
        self.o_toc_do.grid(row=0, column=3, padx=5)
        self.o_toc_do.insert(0, "1.0")

        ttk.Label(khung_dieu_khien, text="Bước:").grid(row=0, column=4, padx=5)
        self.o_buoc = ttk.Entry(khung_dieu_khien, width=5, state="readonly")
        self.o_buoc.grid(row=0, column=5, padx=5)

        ttk.Label(khung_dieu_khien, text="Tổng Bước:").grid(row=0, column=6, padx=5)
        self.o_tong_buoc = ttk.Entry(khung_dieu_khien, width=5, state="readonly")
        self.o_tong_buoc.grid(row=0, column=7, padx=5)

        ttk.Label(khung_dieu_khien, text="Thời Gian:").grid(row=0, column=8, padx=5)
        self.o_thoi_gian = ttk.Entry(khung_dieu_khien, width=15, state="readonly")
        self.o_thoi_gian.grid(row=0, column=9, padx=5)

        ttk.Label(khung_dieu_khien, text="Trạng Thái Duyệt:").grid(row=0, column=10, padx=5)
        self.o_trang_thai_duyet = ttk.Entry(khung_dieu_khien, width=10, state="readonly")
        self.o_trang_thai_duyet.grid(row=0, column=11, padx=5)

        ttk.Button(khung_dieu_khien, text="Nhập Ngẫu Nhiên", command=self.nhap_lieu_ngau_nhien).grid(row=0, column=12, padx=5)
        ttk.Button(khung_dieu_khien, text="Giải", command=self.xu_ly_giai).grid(row=0, column=13, padx=5)
        ttk.Button(khung_dieu_khien, text="Đặt Lại", command=self.dat_lai).grid(row=0, column=14, padx=5)

        # Khu vực kết quả
        self.o_ket_qua = tk.Text(khung_ket_qua, height=12, width=60)
        self.o_ket_qua.grid(row=0, column=0, padx=5, pady=5)
        thanh_cuon = ttk.Scrollbar(khung_ket_qua, orient="vertical", command=self.o_ket_qua.yview)
        thanh_cuon.grid(row=0, column=1, sticky="ns")
        self.o_ket_qua.config(yscrollcommand=thanh_cuon.set)

        self.bo_hen_gio = self.after(0, lambda: None)

    def nhap_lieu_ngau_nhien(self):
        """Nhập trạng thái ban đầu và mục tiêu ngẫu nhiên."""
        cac_so_ngau_nhien = random.sample(range(9), 9)
        self.trang_thai_bat_dau = tuple(cac_so_ngau_nhien)
        for i in range(KICH_THUOC_LUOI):
            for j in range(KICH_THUOC_LUOI):
                self.o_nhap_ban_dau[i][j].delete(0, tk.END)
                self.o_nhap_ban_dau[i][j].insert(0, str(cac_so_ngau_nhien[i * KICH_THUOC_LUOI + j]))
        cac_so_ngau_nhien = random.sample(range(9), 9)
        self.trang_thai_dich = tuple(cac_so_ngau_nhien)
        for i in range(KICH_THUOC_LUOI):
            for j in range(KICH_THUOC_LUOI):
                self.o_nhap_muc_tieu[i][j].delete(0, tk.END)
                self.o_nhap_muc_tieu[i][j].insert(0, str(cac_so_ngau_nhien[i * KICH_THUOC_LUOI + j]))
        self.dat_lai()

    def dat_lai(self):
        """Đặt lại trạng thái giao diện."""
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = []
        self.o_buoc.delete(0, tk.END)
        self.o_buoc.insert(0, "0")
        self.o_tong_buoc.delete(0, tk.END)
        self.o_tong_buoc.insert(0, "0")
        self.o_thoi_gian.delete(0, tk.END)
        self.o_trang_thai_duyet.delete(0, tk.END)
        self.o_ket_qua.delete(1.0, tk.END)
        for i in range(KICH_THUOC_LUOI):
            for j in range(KICH_THUOC_LUOI):
                gia_tri = self.trang_thai_bat_dau[i * KICH_THUOC_LUOI + j]
                self.o_hien_thi[i][j].config(text=str(gia_tri) if gia_tri != 0 else "")
        self.after_cancel(self.bo_hen_gio)

    def xu_ly_giai(self):
        """Xử lý giải bài toán với thuật toán được chọn."""
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
            self.trang_thai_bat_dau = tuple(ban_dau)
            self.trang_thai_dich = tuple(muc_tieu)
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
            return

        try:
            toc_do = float(self.o_toc_do.get())
            if toc_do < 0.001:
                raise ValueError("Tốc độ tối thiểu là 0.001 giây!")
            self.toc_do_moi_buoc_ms = int(toc_do * 1000)
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
            return

        loai_thuat_toan = self.cbb_thuat_toan.get()
        nut_goc = tao_nut_tim_kiem(None, None, self.trang_thai_bat_dau)
        thoi_gian_bat_dau = time.perf_counter()

        if loai_thuat_toan in ["BFS", "DFS"]:
            giai_phap, self.danh_sach_dong = tim_kiem_khong_thong_tin(nut_goc, loai_thuat_toan, self.trang_thai_dich)
        elif loai_thuat_toan == "A*":
            giai_phap, self.danh_sach_dong = tim_kiem_a_sao(nut_goc, self.trang_thai_dich)
        elif loai_thuat_toan == "IDS":
            giai_phap, self.danh_sach_dong = tim_kiem_do_sau_lap(nut_goc, self.trang_thai_dich)
        elif loai_thuat_toan == "Luyện kim mô phỏng":
            giai_phap, self.danh_sach_dong = tim_kiem_luyen_kim_mo_phong(nut_goc, self.trang_thai_dich)
        elif loai_thuat_toan == "Giải thuật di truyền":
            giai_phap, self.danh_sach_dong = giai_thuat_di_truyen(nut_goc, self.trang_thai_dich)
        elif loai_thuat_toan == "Học tăng cường":
            giai_phap, self.danh_sach_dong = giai_bang_hoc_tang_cuong(self.trang_thai_bat_dau, self.trang_thai_dich)
        else:
            messagebox.showerror("Lỗi", "Thuật toán không được hỗ trợ!")
            return

        thoi_gian_ket_thuc = time.perf_counter()
        thoi_gian_thuc_thi = thoi_gian_ket_thuc - thoi_gian_bat_dau

        self.o_thoi_gian.delete(0, tk.END)
        self.o_thoi_gian.insert(0, f"{thoi_gian_thuc_thi:.2f} (giây)")
        self.o_trang_thai_duyet.delete(0, tk.END)
        self.o_trang_thai_duyet.insert(0, str(len(self.danh_sach_dong.tap_hop_trang_thai)))

        if giai_phap:
            self.o_ket_qua.delete(1.0, tk.END)
            for trang_thai in giai_phap:
                for i in range(0, KICH_THUOC_BAI_TOAN, KICH_THUOC_LUOI):
                    self.o_ket_qua.insert(tk.END, f"{list(trang_thai[i:i + KICH_THUOC_LUOI])}\n")
                self.o_ket_qua.insert(tk.END, "\n")
            self.chay_hien_thi_giai_phap(giai_phap)
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, str(len(giai_phap) - 1))
        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")
            self.o_tong_buoc.delete(0, tk.END)
            self.o_tong_buoc.insert(0, "0")
            self.o_ket_qua.delete(1.0, tk.END)
            self.o_ket_qua.insert(tk.END, "Không tìm thấy giải pháp!\n")

    def chay_hien_thi_giai_phap(self, giai_phap: List[Tuple[int, ...]]):
        if not giai_phap:
            messagebox.showerror("Lỗi", "Không có giải pháp hợp lệ để hiển thị!")
            return
        self.buoc_hien_tai = 0
        self.giai_phap_dang_chay = giai_phap
        self.after_cancel(self.bo_hen_gio)
        self.cap_nhat_buoc()

    def cap_nhat_buoc(self):
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