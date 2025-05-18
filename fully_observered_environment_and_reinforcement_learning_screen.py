from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow
from tkinter import messagebox
import time
import random
import numpy
import math
import heapq
import os

from Cau_truc import NutTimKiem, DanhSachMo, DanhSachDong, tao_nut_tim_kiem, trich_xuat_duong_di
from reinforcement_learning import giai_bang_hoc_tang_cuong


CHIEU_RONG_CUA_SO_MAC_DINH = 840 
CHIEU_CAO_CUA_SO_MAC_DINH = 611 
DUONG_DAN_THU_MUC_HIEN_TAI = os.path.dirname(__file__) 

tuple_trang_thai_bat_dau_fo = tuple([0,0,0,0,0,0,0,0,0])
tuple_trang_thai_ket_thuc_fo = tuple([0,0,0,0,0,0,0,0,0])
nut_goc_fo = None
duong_di_ket_qua_fo = None
danh_sach_dong_fo = None

def ham_heuristic_fo(trang_thai: tuple) -> int:
    global tuple_trang_thai_ket_thuc_fo
    gia_tri_h = 0
    for so_i in range(1, 9):
        try:
            vi_tri_so_i_tt = trang_thai.index(so_i)
            vi_tri_so_i_dich = tuple_trang_thai_ket_thuc_fo.index(so_i)
            hang1_tt, cot1_tt = divmod(vi_tri_so_i_tt, 3)
            hang2_dich, cot2_dich = divmod(vi_tri_so_i_dich, 3)
            gia_tri_h += abs(hang1_tt - hang2_dich) + abs(cot1_tt - cot2_dich)
        except ValueError:
            pass
    return gia_tri_h

def kiem_tra_trang_thai_dich_fo(trang_thai:tuple) -> bool:
    global tuple_trang_thai_ket_thuc_fo
    return trang_thai == tuple_trang_thai_ket_thuc_fo

def tim_cac_trang_thai_ke_tiep_fo(trang_thai: tuple) -> list:
    danh_sach_con = []
    vi_tri_so_khong = trang_thai.index(0)
    hang_hien_tai, cot_hien_tai = vi_tri_so_khong//3, vi_tri_so_khong%3

    cac_hanh_dong_tiem_nang = {
        'UP': (-1, 0), 'DOWN': (1, 0),
        'LEFT': (0, -1), 'RIGHT': (0, 1)
    }

    for hanh_dong, (delta_hang, delta_cot) in cac_hanh_dong_tiem_nang.items():
        hang_moi, cot_moi = hang_hien_tai + delta_hang, cot_hien_tai + delta_cot
        if 0 <= hang_moi < 3 and 0 <= cot_moi < 3:
            vi_tri_moi = hang_moi * 3 + cot_moi
            trang_thai_moi_list = list(trang_thai)           
            trang_thai_moi_list[vi_tri_so_khong], trang_thai_moi_list[vi_tri_moi] = trang_thai_moi_list[vi_tri_moi], trang_thai_moi_list[vi_tri_so_khong]
            danh_sach_con.append((hanh_dong, tuple(trang_thai_moi_list)))
    return danh_sach_con

def tim_kiem_khong_thong_tin_fo(nut_goc_ktt: NutTimKiem, loai_tim_kiem: str):
    global danh_sach_dong_fo
    danh_sach_mo_ktt = DanhSachMo(loai_tim_kiem)
    danh_sach_mo_ktt.them(nut_goc_ktt)
    danh_sach_dong_fo = DanhSachDong()
    
    while not danh_sach_mo_ktt.la_rong():
        nut_hien_tai_ktt = danh_sach_mo_ktt.lay_phan_tu()
        if danh_sach_dong_fo.tra_cuu(nut_hien_tai_ktt.trang_thai):
            continue
            
        danh_sach_dong_fo.them(nut_hien_tai_ktt.trang_thai)
        
        if kiem_tra_trang_thai_dich_fo(nut_hien_tai_ktt.trang_thai):
            return trich_xuat_duong_di(nut_hien_tai_ktt)
        
        for hanh_dong_ktt, trang_thai_moi_ktt in tim_cac_trang_thai_ke_tiep_fo(nut_hien_tai_ktt.trang_thai):
            if not danh_sach_dong_fo.tra_cuu(trang_thai_moi_ktt):
                nut_moi_ktt = tao_nut_tim_kiem(nut_hien_tai_ktt, hanh_dong_ktt, trang_thai_moi_ktt)
                danh_sach_mo_ktt.them(nut_moi_ktt)
    return None

def tim_kiem_do_sau_gioi_han_fo(nut_hien_tai_dls: NutTimKiem, gioi_han_do_sau_dls: int):
    global danh_sach_dong_fo
    ngan_xep_dls = [(nut_hien_tai_dls, [nut_hien_tai_dls.trang_thai])] 
    danh_sach_dong_tam_thoi_dls = DanhSachDong() 
    
    while ngan_xep_dls:
        nut_dang_xet_dls, duong_di_tam_thoi_dls = ngan_xep_dls.pop()        
        if kiem_tra_trang_thai_dich_fo(nut_dang_xet_dls.trang_thai):
            danh_sach_dong_fo = danh_sach_dong_tam_thoi_dls 
            return trich_xuat_duong_di(nut_dang_xet_dls) # Hoặc trả về duong_di_tam_thoi_dls nếu muốn
        
        if danh_sach_dong_tam_thoi_dls.tra_cuu(nut_dang_xet_dls.trang_thai) and len(duong_di_tam_thoi_dls) > 1 : # tránh thêm nút gốc nhiều lần
             continue
        danh_sach_dong_tam_thoi_dls.them(nut_dang_xet_dls.trang_thai)
        
        if len(duong_di_tam_thoi_dls) -1 < gioi_han_do_sau_dls:
            for hanh_dong_dls, trang_thai_moi_dls in reversed(tim_cac_trang_thai_ke_tiep_fo(nut_dang_xet_dls.trang_thai)):
                if not danh_sach_dong_tam_thoi_dls.tra_cuu(trang_thai_moi_dls):
                    nut_moi_dls = tao_nut_tim_kiem(nut_dang_xet_dls, hanh_dong_dls, trang_thai_moi_dls)
                    ngan_xep_dls.append((nut_moi_dls, duong_di_tam_thoi_dls + [trang_thai_moi_dls]))
    danh_sach_dong_fo = danh_sach_dong_tam_thoi_dls
    return None
       
def tim_kiem_do_sau_lap_fo(nut_goc_ids: NutTimKiem):
    do_sau_toi_da_ids = 100 
    for do_sau_hien_tai_ids in range(do_sau_toi_da_ids + 1):
        giai_phap_ids = tim_kiem_do_sau_gioi_han_fo(nut_goc_ids, do_sau_hien_tai_ids)
        if giai_phap_ids is not None:
            return giai_phap_ids
    return None
    
def tim_kiem_chi_phi_dong_nhat_fo(nut_goc_ucs: NutTimKiem):
    global danh_sach_dong_fo
    danh_sach_mo_ucs = DanhSachMo("UCS")
    danh_sach_mo_ucs.them(nut_goc_ucs)
    danh_sach_dong_fo = DanhSachDong()
    
    while not danh_sach_mo_ucs.la_rong():
        nut_hien_tai_ucs = danh_sach_mo_ucs.lay_phan_tu()
        if kiem_tra_trang_thai_dich_fo(nut_hien_tai_ucs.trang_thai):
            return trich_xuat_duong_di(nut_hien_tai_ucs)
        
        if danh_sach_dong_fo.tra_cuu(nut_hien_tai_ucs.trang_thai):
            continue
        danh_sach_dong_fo.them(nut_hien_tai_ucs.trang_thai)
        
        for hanh_dong_ucs, trang_thai_moi_ucs in tim_cac_trang_thai_ke_tiep_fo(nut_hien_tai_ucs.trang_thai):
            if not danh_sach_dong_fo.tra_cuu(trang_thai_moi_ucs):
                nut_moi_ucs = tao_nut_tim_kiem(nut_hien_tai_ucs, hanh_dong_ucs, trang_thai_moi_ucs)
                danh_sach_mo_ucs.them(nut_moi_ucs) 
    return None

def tim_kiem_tham_lam_fo(nut_goc_greedy: NutTimKiem):
    global danh_sach_dong_fo
    danh_sach_mo_greedy = DanhSachMo("Greedy")
    nut_goc_greedy.chi_phi_h = ham_heuristic_fo(nut_goc_greedy.trang_thai)
    danh_sach_mo_greedy.them(nut_goc_greedy)
    danh_sach_dong_fo = DanhSachDong()
    
    while not danh_sach_mo_greedy.la_rong():
        nut_hien_tai_greedy = danh_sach_mo_greedy.lay_phan_tu()
        
        if kiem_tra_trang_thai_dich_fo(nut_hien_tai_greedy.trang_thai):
            return trich_xuat_duong_di(nut_hien_tai_greedy)
        
        if danh_sach_dong_fo.tra_cuu(nut_hien_tai_greedy.trang_thai):
            continue
        danh_sach_dong_fo.them(nut_hien_tai_greedy.trang_thai)
        
        for hanh_dong_greedy, trang_thai_moi_greedy in tim_cac_trang_thai_ke_tiep_fo(nut_hien_tai_greedy.trang_thai):
            if not danh_sach_dong_fo.tra_cuu(trang_thai_moi_greedy):
                nut_moi_greedy = tao_nut_tim_kiem(nut_hien_tai_greedy, hanh_dong_greedy, trang_thai_moi_greedy)
                nut_moi_greedy.chi_phi_h = ham_heuristic_fo(nut_moi_greedy.trang_thai)
                danh_sach_mo_greedy.them(nut_moi_greedy)
    return None

def tim_kiem_a_sao_fo(nut_goc_astar: NutTimKiem):
    global danh_sach_dong_fo
    danh_sach_mo_astar = DanhSachMo("A*")
    nut_goc_astar.chi_phi_h = ham_heuristic_fo(nut_goc_astar.trang_thai)
    danh_sach_mo_astar.them(nut_goc_astar)
    danh_sach_dong_fo = DanhSachDong()
    
    while not danh_sach_mo_astar.la_rong():  
        nut_hien_tai_astar = danh_sach_mo_astar.lay_phan_tu()
        
        if kiem_tra_trang_thai_dich_fo(nut_hien_tai_astar.trang_thai):
            return trich_xuat_duong_di(nut_hien_tai_astar)
        
        if danh_sach_dong_fo.tra_cuu(nut_hien_tai_astar.trang_thai):
            continue
        danh_sach_dong_fo.them(nut_hien_tai_astar.trang_thai)
        
        for hanh_dong_astar, trang_thai_moi_astar in tim_cac_trang_thai_ke_tiep_fo(nut_hien_tai_astar.trang_thai):
            if not danh_sach_dong_fo.tra_cuu(trang_thai_moi_astar):
                nut_moi_astar = tao_nut_tim_kiem(nut_hien_tai_astar, hanh_dong_astar, trang_thai_moi_astar)
                nut_moi_astar.chi_phi_h = ham_heuristic_fo(nut_moi_astar.trang_thai)
                danh_sach_mo_astar.them(nut_moi_astar)
    return None

def tim_kiem_ida_sao_fo(nut_goc_idastar: NutTimKiem):
    def tim_kiem_trong_nguong_idastar(nut_idastar: NutTimKiem, duong_di_hien_tai_idastar: set, nguong_idastar: int):
        global danh_sach_dong_fo 
        chi_phi_f_idastar = nut_idastar.chi_phi_g + ham_heuristic_fo(nut_idastar.trang_thai)
        if chi_phi_f_idastar > nguong_idastar:
            return chi_phi_f_idastar, None
        if kiem_tra_trang_thai_dich_fo(nut_idastar.trang_thai):
            return None, trich_xuat_duong_di(nut_idastar)
        
        nguong_toi_thieu_moi_idastar = float("inf")
        danh_sach_dong_fo.them(nut_idastar.trang_thai) 

        for hanh_dong_idastar, trang_thai_moi_idastar in tim_cac_trang_thai_ke_tiep_fo(nut_idastar.trang_thai):
            if trang_thai_moi_idastar in duong_di_hien_tai_idastar : 
                continue  
            if trang_thai_moi_idastar in danh_sach_dong_fo.tap_hop_trang_thai and nut_idastar.trang_thai != nut_goc_idastar.trang_thai :
                 continue

            nut_moi_idastar = tao_nut_tim_kiem(nut_idastar, hanh_dong_idastar, trang_thai_moi_idastar)
            duong_di_hien_tai_idastar.add(trang_thai_moi_idastar)
            ket_qua_nguong_idastar, duong_di_tim_thay_idastar = tim_kiem_trong_nguong_idastar(nut_moi_idastar, duong_di_hien_tai_idastar, nguong_idastar)
            if duong_di_tim_thay_idastar:
                return None, duong_di_tim_thay_idastar
            nguong_toi_thieu_moi_idastar = min(nguong_toi_thieu_moi_idastar, ket_qua_nguong_idastar)
            duong_di_hien_tai_idastar.remove(trang_thai_moi_idastar)
        return nguong_toi_thieu_moi_idastar, None

    global danh_sach_dong_fo
    danh_sach_dong_fo = DanhSachDong()
    nguong_hien_tai_idastar = nut_goc_idastar.chi_phi_g + ham_heuristic_fo(nut_goc_idastar.trang_thai)
    while True:
        danh_sach_dong_fo.tap_hop_trang_thai.clear() 
        nguong_moi_idastar, duong_di_ket_qua_idastar = tim_kiem_trong_nguong_idastar(nut_goc_idastar, {nut_goc_idastar.trang_thai}, nguong_hien_tai_idastar)
        if duong_di_ket_qua_idastar:
            return duong_di_ket_qua_idastar
        if nguong_moi_idastar == float("inf"):
            return None
        nguong_hien_tai_idastar = nguong_moi_idastar
 
def tim_kiem_leo_doi_don_gian_fo(nut_goc_shc: NutTimKiem):
    global danh_sach_dong_fo
    danh_sach_dong_fo = DanhSachDong()
    nut_hien_tai_shc = nut_goc_shc
    danh_sach_dong_fo.them(nut_hien_tai_shc.trang_thai)
    while True:
        if kiem_tra_trang_thai_dich_fo(nut_hien_tai_shc.trang_thai):
            return trich_xuat_duong_di(nut_hien_tai_shc)
        cac_hang_xom_shc = tim_cac_trang_thai_ke_tiep_fo(nut_hien_tai_shc.trang_thai)
        if not cac_hang_xom_shc:
            return None 
        
        da_tim_thay_tot_hon_shc = False
        for hanh_dong_shc, trang_thai_shc in cac_hang_xom_shc:
            if ham_heuristic_fo(trang_thai_shc) < ham_heuristic_fo(nut_hien_tai_shc.trang_thai):
                nut_hien_tai_shc = tao_nut_tim_kiem(nut_hien_tai_shc, hanh_dong_shc, trang_thai_shc)
                danh_sach_dong_fo.them(nut_hien_tai_shc.trang_thai)
                da_tim_thay_tot_hon_shc = True
                break
        if not da_tim_thay_tot_hon_shc:
            return None

def tim_kiem_leo_doi_doc_nhat_fo(nut_goc_sahc: NutTimKiem):
    global danh_sach_dong_fo
    danh_sach_dong_fo = DanhSachDong()
    nut_hien_tai_sahc = nut_goc_sahc
    danh_sach_dong_fo.them(nut_hien_tai_sahc.trang_thai)
    while True:
        if kiem_tra_trang_thai_dich_fo(nut_hien_tai_sahc.trang_thai):
            return trich_xuat_duong_di(nut_hien_tai_sahc)
        cac_hang_xom_sahc = tim_cac_trang_thai_ke_tiep_fo(nut_hien_tai_sahc.trang_thai)
        if not cac_hang_xom_sahc:
            return None
        
        nut_tot_nhat_trong_hang_xom_sahc = None
        heuristic_tot_nhat_sahc = ham_heuristic_fo(nut_hien_tai_sahc.trang_thai)

        for hanh_dong_sahc, trang_thai_sahc in cac_hang_xom_sahc:
            h_trang_thai_sahc = ham_heuristic_fo(trang_thai_sahc)
            if h_trang_thai_sahc < heuristic_tot_nhat_sahc:
                heuristic_tot_nhat_sahc = h_trang_thai_sahc
                nut_tot_nhat_trong_hang_xom_sahc = tao_nut_tim_kiem(nut_hien_tai_sahc, hanh_dong_sahc, trang_thai_sahc)
        
        if nut_tot_nhat_trong_hang_xom_sahc is None:
            return None
        nut_hien_tai_sahc = nut_tot_nhat_trong_hang_xom_sahc
        danh_sach_dong_fo.them(nut_hien_tai_sahc.trang_thai)

def tim_kiem_leo_doi_ngau_nhien_stochastic_fo(nut_goc_stohc: NutTimKiem):
    global danh_sach_dong_fo
    danh_sach_dong_fo = DanhSachDong()
    nut_hien_tai_stohc = nut_goc_stohc
    danh_sach_dong_fo.them(nut_hien_tai_stohc.trang_thai)
    max_lap_stohc = 1000
    so_lan_lap_stohc = 0
    while so_lan_lap_stohc < max_lap_stohc :
        so_lan_lap_stohc+=1
        if kiem_tra_trang_thai_dich_fo(nut_hien_tai_stohc.trang_thai):
            return trich_xuat_duong_di(nut_hien_tai_stohc)
        cac_hang_xom_stohc = tim_cac_trang_thai_ke_tiep_fo(nut_hien_tai_stohc.trang_thai)
        if not cac_hang_xom_stohc:
            return None
        
        random.shuffle(cac_hang_xom_stohc)
        da_tim_thay_tot_hon_stohc = False
        for hanh_dong_stohc, trang_thai_stohc in cac_hang_xom_stohc:
            if ham_heuristic_fo(trang_thai_stohc) < ham_heuristic_fo(nut_hien_tai_stohc.trang_thai):
                nut_hien_tai_stohc = tao_nut_tim_kiem(nut_hien_tai_stohc, hanh_dong_stohc, trang_thai_stohc)
                danh_sach_dong_fo.them(nut_hien_tai_stohc.trang_thai)
                da_tim_thay_tot_hon_stohc = True
                break
        if not da_tim_thay_tot_hon_stohc : # Nếu không có hàng xóm nào tốt hơn, có thể bị kẹt
             if cac_hang_xom_stohc : # Chọn ngẫu nhiên một hàng xóm để thoát khỏi local optimum
                 hanh_dong_ngau_nhien, trang_thai_ngau_nhien = random.choice(cac_hang_xom_stohc)
                 nut_hien_tai_stohc = tao_nut_tim_kiem(nut_hien_tai_stohc, hanh_dong_ngau_nhien, trang_thai_ngau_nhien)
                 danh_sach_dong_fo.them(nut_hien_tai_stohc.trang_thai)
             else: # Không còn hàng xóm
                 return None
    return None


def tim_kiem_luyen_kim_mo_phong_fo(nut_goc_sa: NutTimKiem):
    global danh_sach_dong_fo
    danh_sach_dong_fo = DanhSachDong()
    so_lan_lap_toi_da_sa = 10000
    nut_hien_tai_sa = nut_goc_sa
    danh_sach_dong_fo.them(nut_hien_tai_sa.trang_thai)
    lan_lap_hien_tai_sa = 0
    nhiet_do_sa = random.uniform(pow(10, 2), pow(10, 3)) 
    
    giai_phap_tot_nhat_sa = nut_hien_tai_sa

    while lan_lap_hien_tai_sa < so_lan_lap_toi_da_sa and nhiet_do_sa > 1e-3:
        lan_lap_hien_tai_sa += 1
        if kiem_tra_trang_thai_dich_fo(nut_hien_tai_sa.trang_thai):
            return trich_xuat_duong_di(nut_hien_tai_sa)
        
        cac_hang_xom_sa = tim_cac_trang_thai_ke_tiep_fo(nut_hien_tai_sa.trang_thai)
        if not cac_hang_xom_sa:
            return trich_xuat_duong_di(giai_phap_tot_nhat_sa) 

        hanh_dong_ngau_nhien_sa, trang_thai_ngau_nhien_sa = random.choice(cac_hang_xom_sa)
        nut_ke_tiep_sa = tao_nut_tim_kiem(nut_hien_tai_sa, hanh_dong_ngau_nhien_sa, trang_thai_ngau_nhien_sa)
        
        delta_e_sa = ham_heuristic_fo(nut_ke_tiep_sa.trang_thai) - ham_heuristic_fo(nut_hien_tai_sa.trang_thai)
        
        if delta_e_sa < 0:
            nut_hien_tai_sa = nut_ke_tiep_sa
            danh_sach_dong_fo.them(nut_hien_tai_sa.trang_thai)
            if ham_heuristic_fo(nut_hien_tai_sa.trang_thai) < ham_heuristic_fo(giai_phap_tot_nhat_sa.trang_thai):
                 giai_phap_tot_nhat_sa = nut_hien_tai_sa
        else:
            try:
                xac_suat_chuyen_sa = math.exp(-delta_e_sa / nhiet_do_sa)
                if random.random() < xac_suat_chuyen_sa:
                    nut_hien_tai_sa = nut_ke_tiep_sa
                    danh_sach_dong_fo.them(nut_hien_tai_sa.trang_thai)
            except OverflowError: # Trường hợp delta_E quá lớn, math.exp lỗi
                pass # Bỏ qua bước chuyển xấu này

        alpha_sa = random.uniform(0.85, 0.99) 
        nhiet_do_sa *= alpha_sa
            
    return trich_xuat_duong_di(giai_phap_tot_nhat_sa) if giai_phap_tot_nhat_sa else None


def tim_kiem_chum_tia_fo(nut_goc_beam: NutTimKiem, do_rong_chum_beam: int = 2):
    global danh_sach_dong_fo
    danh_sach_mo_beam = DanhSachMo("Beam search")
    nut_goc_beam.chi_phi_h = ham_heuristic_fo(nut_goc_beam.trang_thai)
    danh_sach_mo_beam.them(nut_goc_beam)
    danh_sach_dong_fo = DanhSachDong() 
    
    while not danh_sach_mo_beam.la_rong():
        cac_nut_tot_nhat_trong_chum_beam = []
        for _ in range(do_rong_chum_beam):
            if danh_sach_mo_beam.la_rong():
                break
            nut_xet_beam = danh_sach_mo_beam.lay_phan_tu()
            if kiem_tra_trang_thai_dich_fo(nut_xet_beam.trang_thai):
                return trich_xuat_duong_di(nut_xet_beam)
            
            if not danh_sach_dong_fo.tra_cuu(nut_xet_beam.trang_thai):
                danh_sach_dong_fo.them(nut_xet_beam.trang_thai)
                cac_nut_tot_nhat_trong_chum_beam.append(nut_xet_beam)

        danh_sach_mo_beam.hang_doi_kep.clear() 
        heapq.heapify(danh_sach_mo_beam.hang_doi_kep)


        for nut_cha_beam in cac_nut_tot_nhat_trong_chum_beam:
            for hanh_dong_beam, trang_thai_moi_beam in tim_cac_trang_thai_ke_tiep_fo(nut_cha_beam.trang_thai):
                if not danh_sach_dong_fo.tra_cuu(trang_thai_moi_beam):
                    nut_moi_beam = tao_nut_tim_kiem(nut_cha_beam, hanh_dong_beam, trang_thai_moi_beam)
                    nut_moi_beam.chi_phi_h = ham_heuristic_fo(nut_moi_beam.trang_thai)
                    danh_sach_mo_beam.them(nut_moi_beam)
    return None


def lai_ghep_thu_tu_fo(cha1: tuple, cha2: tuple) -> tuple:
    kich_thuoc = len(cha1)
    cha1_list = list(cha1)
    cha2_list = list(cha2)
    
    diem_bat_dau_lai, diem_ket_thuc_lai = sorted(random.sample(range(kich_thuoc), 2))
    
    con1 = [None] * kich_thuoc
    con2 = [None] * kich_thuoc
    
    con1[diem_bat_dau_lai : diem_ket_thuc_lai + 1] = cha1_list[diem_bat_dau_lai : diem_ket_thuc_lai + 1]
    con2[diem_bat_dau_lai : diem_ket_thuc_lai + 1] = cha2_list[diem_bat_dau_lai : diem_ket_thuc_lai + 1]
    
    chi_so_cha2 = 0
    for i in range(kich_thuoc):
        if con1[i] is None:
            while cha2_list[chi_so_cha2] in con1:
                chi_so_cha2 += 1
            con1[i] = cha2_list[chi_so_cha2]
    
    chi_so_cha1 = 0
    for i in range(kich_thuoc):
        if con2[i] is None:
            while cha1_list[chi_so_cha1] in con2:
                chi_so_cha1 += 1
            con2[i] = cha1_list[chi_so_cha1]
            
    return tuple(con1), tuple(con2)

def dot_bien_hoan_vi_fo(ca_the:tuple)->tuple:
    ca_the_list = list(ca_the)
    if len(ca_the_list) < 2: return ca_the # Không thể hoán vị nếu ít hơn 2 phần tử
    vi_tri1, vi_tri2 = random.sample(range(len(ca_the_list)), 2)
    ca_the_list[vi_tri1], ca_the_list[vi_tri2] = ca_the_list[vi_tri2], ca_the_list[vi_tri1]
    return tuple(ca_the_list)

def giai_thuat_di_truyen_fo(nut_goc_ga: NutTimKiem, kich_thuoc_quan_the_ga: int = 50, so_the_he_ga: int = 100, ti_le_dot_bien_ga: float = 0.1):
    global danh_sach_dong_fo
    danh_sach_dong_fo = DanhSachDong() 

    quan_the_hien_tai_ga = []
    
    trang_thai_ban_dau_ga = nut_goc_ga.trang_thai
    if kiem_tra_trang_thai_dich_fo(trang_thai_ban_dau_ga):
        danh_sach_dong_fo.them(trang_thai_ban_dau_ga)
        return [trang_thai_ban_dau_ga] 

    # Tạo quần thể ban đầu từ các trạng thái lân cận của trạng thái gốc
    cac_trang_thai_lan_can_ga = tim_cac_trang_thai_ke_tiep_fo(trang_thai_ban_dau_ga)
    for _, trang_thai_lc_ga in cac_trang_thai_lan_can_ga:
        if len(quan_the_hien_tai_ga) < kich_thuoc_quan_the_ga and trang_thai_lc_ga not in {tt for tt, _ in quan_the_hien_tai_ga}:
            quan_the_hien_tai_ga.append((trang_thai_lc_ga, ham_heuristic_fo(trang_thai_lc_ga)))
            danh_sach_dong_fo.them(trang_thai_lc_ga)
    
    # Nếu không đủ từ lân cận, tạo ngẫu nhiên cho đến khi đủ kích thước quần thể
    while len(quan_the_hien_tai_ga) < kich_thuoc_quan_the_ga:
        trang_thai_ngau_nhien_ga = list(range(9))
        random.shuffle(trang_thai_ngau_nhien_ga)
        trang_thai_ngau_nhien_ga = tuple(trang_thai_ngau_nhien_ga)
        if trang_thai_ngau_nhien_ga not in {tt for tt, _ in quan_the_hien_tai_ga}:
             quan_the_hien_tai_ga.append((trang_thai_ngau_nhien_ga, ham_heuristic_fo(trang_thai_ngau_nhien_ga)))
             danh_sach_dong_fo.them(trang_thai_ngau_nhien_ga)


    for the_he_idx_ga in range(so_the_he_ga):
        quan_the_hien_tai_ga.sort(key=lambda x: x[1]) 

        if quan_the_hien_tai_ga[0][1] == 0: 
            trang_thai_dich_tim_thay_ga = quan_the_hien_tai_ga[0][0]
            # Cần cơ chế truy vết đường đi nếu muốn trả về đường đi hoàn chỉnh
            # Hiện tại chỉ trả về trạng thái đích
            return [trang_thai_dich_tim_thay_ga]

        quan_the_moi_ga = quan_the_hien_tai_ga[:2] # Giữ lại 2 cá thể tốt nhất (Elitism)

        while len(quan_the_moi_ga) < kich_thuoc_quan_the_ga:
            cha1_ga, cha2_ga = random.choices(quan_the_hien_tai_ga[:len(quan_the_hien_tai_ga)//2], k=2) # Chọn cha mẹ từ nửa tốt nhất
            
            con1_ga, con2_ga = lai_ghep_thu_tu_fo(cha1_ga[0], cha2_ga[0])
            
            if random.random() < ti_le_dot_bien_ga:
                con1_ga = dot_bien_hoan_vi_fo(con1_ga)
            if random.random() < ti_le_dot_bien_ga:
                con2_ga = dot_bien_hoan_vi_fo(con2_ga)

            if con1_ga not in {tt for tt, _ in quan_the_moi_ga}:
                quan_the_moi_ga.append((con1_ga, ham_heuristic_fo(con1_ga)))
                danh_sach_dong_fo.them(con1_ga)
            if len(quan_the_moi_ga) < kich_thuoc_quan_the_ga and con2_ga not in {tt for tt, _ in quan_the_moi_ga}:
                 quan_the_moi_ga.append((con2_ga, ham_heuristic_fo(con2_ga)))
                 danh_sach_dong_fo.them(con2_ga)
        
        quan_the_hien_tai_ga = quan_the_moi_ga
        
    quan_the_hien_tai_ga.sort(key=lambda x: x[1])
    # Có thể trả về cá thể tốt nhất tìm được nếu không đạt đích
    # return [quan_the_hien_tai_ga[0][0]]
    return None 


def ghi_duong_di_vao_file_fo(giai_phap_fo):
    global danh_sach_dong_fo
    with open(DUONG_DAN_THU_MUC_HIEN_TAI + "/ket_qua_fo.txt", "w", encoding="utf-8") as tep_fo:
        tep_fo.write("Giải pháp: ")
        if giai_phap_fo is None:
            tep_fo.write("\nKhông có giải pháp")
        else:
            for trang_thai_gp_fo in giai_phap_fo:
                tep_fo.write(f"\n{trang_thai_gp_fo}")
        
        tep_fo.write("\nDanh sách đóng (các trạng thái đã duyệt): ")
        if danh_sach_dong_fo is None or not danh_sach_dong_fo.tap_hop_trang_thai:
            tep_fo.write("\nKhông có")
        else:
            for trang_thai_dd_fo in danh_sach_dong_fo.tap_hop_trang_thai:
                tep_fo.write(f"\n{trang_thai_dd_fo}")
        messagebox.showinfo("Thông tin", "Ghi vào file thành công")
        
class UngDungTimKiemTongQuat(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(DUONG_DAN_THU_MUC_HIEN_TAI + "/GUI.ui", self)
        self.setFixedSize(CHIEU_RONG_CUA_SO_MAC_DINH, CHIEU_CAO_CUA_SO_MAC_DINH)
        self.btnRandomInput.clicked.connect(self.nhap_lieu_ngau_nhien_fo)
        self.cbbAlgorithm.addItems(["BFS", "DFS", "UCS", "IDS", "Greedy", "A*", "IDA*", 
                                    "Leo đồi đơn giản", "Leo đồi dốc nhất", "Leo đồi ngẫu nhiên Stochastic", 
                                    "Luyện kim mô phỏng", "Tìm kiếm chùm tia", "Giải thuật di truyền", 
                                    "Học tăng cường"])
        self.btnSolve.clicked.connect(self.xu_ly_giai_fo)
        self.txtSolveSpeedPerStep.setPlainText("1")
        self.toc_do_moi_buoc_ms_fo = 1000
        self.btnWriteToFile.clicked.connect(lambda: ghi_duong_di_vao_file_fo(duong_di_ket_qua_fo))
        
    def nhap_lieu_ngau_nhien_fo(self):
        global tuple_trang_thai_bat_dau_fo, tuple_trang_thai_ket_thuc_fo
        cac_so_ngau_nhien_bd_fo = random.sample(range(9), 9)
        tuple_trang_thai_bat_dau_fo = tuple(cac_so_ngau_nhien_bd_fo)
        self.cell1.setPlainText(str(tuple_trang_thai_bat_dau_fo[0]))
        self.cell2.setPlainText(str(tuple_trang_thai_bat_dau_fo[1]))
        self.cell3.setPlainText(str(tuple_trang_thai_bat_dau_fo[2]))
        self.cell4.setPlainText(str(tuple_trang_thai_bat_dau_fo[3]))
        self.cell5.setPlainText(str(tuple_trang_thai_bat_dau_fo[4]))
        self.cell6.setPlainText(str(tuple_trang_thai_bat_dau_fo[5]))
        self.cell7.setPlainText(str(tuple_trang_thai_bat_dau_fo[6]))
        self.cell8.setPlainText(str(tuple_trang_thai_bat_dau_fo[7]))
        self.cell9.setPlainText(str(tuple_trang_thai_bat_dau_fo[8]))
        
        cac_so_ngau_nhien_kt_fo = random.sample(range(9), 9)
        tuple_trang_thai_ket_thuc_fo = tuple(cac_so_ngau_nhien_kt_fo)
        self.cell1_2.setPlainText(str(tuple_trang_thai_ket_thuc_fo[0]))
        self.cell2_2.setPlainText(str(tuple_trang_thai_ket_thuc_fo[1]))
        self.cell3_2.setPlainText(str(tuple_trang_thai_ket_thuc_fo[2]))
        self.cell4_2.setPlainText(str(tuple_trang_thai_ket_thuc_fo[3]))
        self.cell5_2.setPlainText(str(tuple_trang_thai_ket_thuc_fo[4]))
        self.cell6_2.setPlainText(str(tuple_trang_thai_ket_thuc_fo[5]))
        self.cell7_2.setPlainText(str(tuple_trang_thai_ket_thuc_fo[6]))
        self.cell8_2.setPlainText(str(tuple_trang_thai_ket_thuc_fo[7]))
        self.cell9_2.setPlainText(str(tuple_trang_thai_ket_thuc_fo[8]))
        
    def xu_ly_giai_fo(self):
        global tuple_trang_thai_bat_dau_fo, tuple_trang_thai_ket_thuc_fo, nut_goc_fo, duong_di_ket_qua_fo, danh_sach_dong_fo
        loai_thuat_toan_fo = self.cbbAlgorithm.currentText()
        try:
            tuple_trang_thai_bat_dau_fo = tuple([
                int(self.cell1.toPlainText()), int(self.cell2.toPlainText()), int(self.cell3.toPlainText()),
                int(self.cell4.toPlainText()), int(self.cell5.toPlainText()), int(self.cell6.toPlainText()),
                int(self.cell7.toPlainText()), int(self.cell8.toPlainText()), int(self.cell9.toPlainText())]
            )
            tuple_trang_thai_ket_thuc_fo = tuple([
                int(self.cell1_2.toPlainText()), int(self.cell2_2.toPlainText()), int(self.cell3_2.toPlainText()),
                int(self.cell4_2.toPlainText()), int(self.cell5_2.toPlainText()), int(self.cell6_2.toPlainText()),
                int(self.cell7_2.toPlainText()), int(self.cell8_2.toPlainText()), int(self.cell9_2.toPlainText())]
            )
            nut_goc_fo = tao_nut_tim_kiem(None, None, tuple_trang_thai_bat_dau_fo)
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị nhập vào không hợp lệ!")
            return # Thêm return ở đây          
            
        try:
            toc_do_nhap_ms_fo = int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000)
            if toc_do_nhap_ms_fo >= 1:
                self.toc_do_moi_buoc_ms_fo = toc_do_nhap_ms_fo
            else:
                messagebox.showerror("Lỗi", "Tốc độ mỗi bước phải lớn hơn hoặc bằng 0.001s")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Tốc độ mỗi bước không hợp lệ")
            return
        
        giai_phap_tim_duoc_fo = None
        thoi_gian_bat_dau_xu_ly_fo = time.perf_counter()

        if loai_thuat_toan_fo == "BFS" or loai_thuat_toan_fo == "DFS":
            giai_phap_tim_duoc_fo = tim_kiem_khong_thong_tin_fo(nut_goc_fo, loai_thuat_toan_fo)
        elif loai_thuat_toan_fo == "UCS":
            giai_phap_tim_duoc_fo = tim_kiem_chi_phi_dong_nhat_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "IDS":
            giai_phap_tim_duoc_fo = tim_kiem_do_sau_lap_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "A*":
            giai_phap_tim_duoc_fo = tim_kiem_a_sao_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "IDA*":
            giai_phap_tim_duoc_fo = tim_kiem_ida_sao_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "Greedy":
            giai_phap_tim_duoc_fo = tim_kiem_tham_lam_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "Leo đồi đơn giản":
            giai_phap_tim_duoc_fo = tim_kiem_leo_doi_don_gian_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "Leo đồi dốc nhất":
            giai_phap_tim_duoc_fo = tim_kiem_leo_doi_doc_nhat_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "Leo đồi ngẫu nhiên Stochastic":
            giai_phap_tim_duoc_fo = tim_kiem_leo_doi_ngau_nhien_stochastic_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "Luyện kim mô phỏng":
            giai_phap_tim_duoc_fo = tim_kiem_luyen_kim_mo_phong_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "Tìm kiếm chùm tia":
            giai_phap_tim_duoc_fo = tim_kiem_chum_tia_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "Giải thuật di truyền":
            giai_phap_tim_duoc_fo = giai_thuat_di_truyen_fo(nut_goc_fo)
        elif loai_thuat_toan_fo == "Học tăng cường":
            danh_sach_q_value_htc = []
            danh_sach_dong_fo = DanhSachDong() # Khởi tạo lại danh_sach_dong_fo cho học tăng cường
            giai_phap_tim_duoc_fo = giai_bang_hoc_tang_cuong(nut_goc_fo.trang_thai, tuple_trang_thai_ket_thuc_fo, danh_sach_q_value_htc)
            # Đối với học tăng cường, danh_sach_dong_fo có thể cần được xử lý khác
            # Tạm thời gán các trạng thái trong Q_list vào nếu cần
            for muc_q in danh_sach_q_value_htc:
                 # Cần phân tích chuỗi trong muc_q để lấy trạng thái nếu muốn thêm vào danh_sach_dong_fo
                 pass # Hoặc bạn có thể để danh_sach_dong_fo được cập nhật bởi chính hàm giai_bang_hoc_tang_cuong

        thoi_gian_ket_thuc_xu_ly_fo = time.perf_counter()
        thoi_gian_thuc_thi_fo = thoi_gian_ket_thuc_xu_ly_fo - thoi_gian_bat_dau_xu_ly_fo
        self.txtSolveTime.setPlainText(f"{thoi_gian_thuc_thi_fo:.8f}(s)")
        
        print(f"Thời gian thực thi: {thoi_gian_thuc_thi_fo}")
        print(f"Loại thuật toán: {loai_thuat_toan_fo}")
        if danh_sach_dong_fo and hasattr(danh_sach_dong_fo, 'tap_hop_trang_thai'):
            print(f"Số lượng trạng thái đã mở/duyệt: {len(danh_sach_dong_fo.tap_hop_trang_thai)}")
        else:
             print(f"Số lượng trạng thái đã mở/duyệt: Không có thông tin từ danh_sach_dong_fo")


        if giai_phap_tim_duoc_fo is None:
            messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")
            self.txtTotalStep.setPlainText("0")
            self.txtStep.setPlainText("0")
            duong_di_ket_qua_fo = None
        else:
            if loai_thuat_toan_fo == "Giải thuật di truyền":
                # Giải thuật di truyền có thể chỉ trả về trạng thái đích, không phải đường đi
                 if isinstance(giai_phap_tim_duoc_fo, list) and len(giai_phap_tim_duoc_fo) > 0 and kiem_tra_trang_thai_dich_fo(giai_phap_tim_duoc_fo[-1]):
                    messagebox.showinfo("Thông báo", f"Tìm thấy trạng thái đích: {giai_phap_tim_duoc_fo[-1]}")
                    self.chay_hien_thi_giai_phap_fo(giai_phap_tim_duoc_fo) 
                    duong_di_ket_qua_fo = giai_phap_tim_duoc_fo
                    self.txtTotalStep.setPlainText(str(len(giai_phap_tim_duoc_fo)))
                 else:
                    messagebox.showinfo("Thông báo", "Giải thuật di truyền kết thúc, không chắc chắn đạt đích hoặc không có đường đi rõ ràng.")
                    self.txtTotalStep.setPlainText("N/A")
                    self.txtStep.setPlainText("N/A")


            elif loai_thuat_toan_fo == "And Or graph search": # Tên này không có trong combobox
                messagebox.showinfo("Thông báo", f"Kế hoạch điều kiện: {giai_phap_tim_duoc_fo}")
            else:
                self.chay_hien_thi_giai_phap_fo(giai_phap_tim_duoc_fo)
                duong_di_ket_qua_fo = giai_phap_tim_duoc_fo
                self.txtTotalStep.setPlainText(str(len(giai_phap_tim_duoc_fo)))
                
    def chay_hien_thi_giai_phap_fo(self, giai_phap_de_chay_fo):
        if not giai_phap_de_chay_fo or not isinstance(giai_phap_de_chay_fo, list) :
            messagebox.showerror("Lỗi", "Không có giải pháp hợp lệ để chạy hiển thị.")
            return

        self.buoc_hien_tai_fo = 0
        self.bo_hen_gio_fo = QtCore.QTimer()
        self.bo_hen_gio_fo.timeout.connect(self.cap_nhat_buoc_hien_thi_fo)
        self.giai_phap_dang_chay_fo = giai_phap_de_chay_fo
        self.bo_hen_gio_fo.start(self.toc_do_moi_buoc_ms_fo)

    def cap_nhat_o_hien_thi_fo(self, o_widget_fo, gia_tri_fo):
        if gia_tri_fo == 0:
            o_widget_fo.setPlainText(" ")
        else:
            o_widget_fo.setPlainText(str(gia_tri_fo))

    def cap_nhat_buoc_hien_thi_fo(self):
        if self.buoc_hien_tai_fo < len(self.giai_phap_dang_chay_fo):
            trang_thai_buoc_fo = self.giai_phap_dang_chay_fo[self.buoc_hien_tai_fo]
            self.buoc_hien_tai_fo += 1
            self.txtStep.setPlainText(str(self.buoc_hien_tai_fo))
            self.cap_nhat_o_hien_thi_fo(self.cell1_3, trang_thai_buoc_fo[0])
            self.cap_nhat_o_hien_thi_fo(self.cell2_3, trang_thai_buoc_fo[1])
            self.cap_nhat_o_hien_thi_fo(self.cell3_3, trang_thai_buoc_fo[2])
            self.cap_nhat_o_hien_thi_fo(self.cell4_3, trang_thai_buoc_fo[3])
            self.cap_nhat_o_hien_thi_fo(self.cell5_3, trang_thai_buoc_fo[4])
            self.cap_nhat_o_hien_thi_fo(self.cell6_3, trang_thai_buoc_fo[5])
            self.cap_nhat_o_hien_thi_fo(self.cell7_3, trang_thai_buoc_fo[6])
            self.cap_nhat_o_hien_thi_fo(self.cell8_3, trang_thai_buoc_fo[7])
            self.cap_nhat_o_hien_thi_fo(self.cell9_3, trang_thai_buoc_fo[8])
        else:
            self.bo_hen_gio_fo.stop()              

ung_dung_qt_fo = QApplication([])
cua_so_chinh_fo = UngDungTimKiemTongQuat()
cua_so_chinh_fo.show()
ung_dung_qt_fo.exec()