#Khai báo và sử dụng module
from Cau_truc import DanhSachMo
import random

def tao_cac_trang_thai_puzzle_duy_nhat_sl(so_luong_trang_thai_sl):   
    danh_sach_ket_qua_sl = []
    while len(danh_sach_ket_qua_sl) < so_luong_trang_thai_sl:
        cac_so_sl = list(range(9))
        random.shuffle(cac_so_sl)
        trang_thai_tuple_sl = tuple(cac_so_sl)
        if trang_thai_tuple_sl not in danh_sach_ket_qua_sl:          
            danh_sach_ket_qua_sl.append(trang_thai_tuple_sl)
    return danh_sach_ket_qua_sl

tap_niem_tin_ban_dau_sl = [(1,2,3,4,5,6,0,8,7),(1,2,3,4,5,6,0,8,7),(8,7,6,5,4,3,2,1,0),(7,8,0,1,2,3,5,6,4),(8,7,6,5,4,3,0,1,2)]
trang_thai_dich_toan_cuc_sl = (1,2,3,4,5,6,7,8,0)

def la_vi_tri_hop_le_sl(chi_so_de_kiem_tra_sl):
    return chi_so_de_kiem_tra_sl >= 0 and chi_so_de_kiem_tra_sl < 9
       
def ap_dung_hanh_dong_len_tap_niem_tin_sl(tap_niem_tin_hien_tai_sl):
       CAC_HUONG_DI_CHUYEN_CHO_SL = {"U": -3, "D": 3, "L": -1, "R": 1}
       tap_niem_tin_ket_qua_sl = []
       cac_trang_thai_da_them_sl = set()

       for hanh_dong_trong_sl in CAC_HUONG_DI_CHUYEN_CHO_SL.keys():
              tap_niem_tin_sau_hanh_dong_sl = set()
              for trang_thai_trong_tap_sl in tap_niem_tin_hien_tai_sl:
                    vi_tri_o_trong_sl = trang_thai_trong_tap_sl.index(0)
                    vi_tri_can_hoan_doi_sl = vi_tri_o_trong_sl + CAC_HUONG_DI_CHUYEN_CHO_SL[hanh_dong_trong_sl]    
                    if la_vi_tri_hop_le_sl(vi_tri_can_hoan_doi_sl):
                        trang_thai_moi_dang_list_sl = list(trang_thai_trong_tap_sl)
                        trang_thai_moi_dang_list_sl[vi_tri_o_trong_sl], trang_thai_moi_dang_list_sl[vi_tri_can_hoan_doi_sl] = trang_thai_moi_dang_list_sl[vi_tri_can_hoan_doi_sl], trang_thai_moi_dang_list_sl[vi_tri_o_trong_sl]
                        trang_thai_moi_dang_tuple_sl = tuple(trang_thai_moi_dang_list_sl)
                        tap_niem_tin_sau_hanh_dong_sl.add(trang_thai_moi_dang_tuple_sl)
                    else:
                        tap_niem_tin_sau_hanh_dong_sl.add(trang_thai_trong_tap_sl) 
              
              if tap_niem_tin_sau_hanh_dong_sl:
                  tap_niem_tin_ket_qua_sl.append(list(tap_niem_tin_sau_hanh_dong_sl))
       
       return tap_niem_tin_ket_qua_sl 
       
def kiem_tra_tap_niem_tin_la_dich_sl(tap_niem_tin_kiem_tra_sl):
    if not tap_niem_tin_kiem_tra_sl:
        return False
    for trang_thai_trong_tap_kt_sl in tap_niem_tin_kiem_tra_sl:
        if trang_thai_trong_tap_kt_sl != trang_thai_dich_toan_cuc_sl:
            return False
    return True

def tim_kiem_khong_thong_tin_cho_sensorless(tap_niem_tin_ban_dau_cho_ktt_sl: list, loai_tim_kiem_de_chon_sl: str):
    hang_doi_mo_sl = DanhSachMo(loai_tim_kiem_de_chon_sl)
    hang_doi_mo_sl.them((tap_niem_tin_ban_dau_cho_ktt_sl, [])) 
    
    danh_sach_dong_cac_tap_niem_tin_sl = set() 
    
    while not hang_doi_mo_sl.la_rong():
        tap_niem_tin_hien_tai_de_xet_sl, cac_hanh_dong_da_thuc_hien_sl = hang_doi_mo_sl.lay_phan_tu()
        
        tap_niem_tin_hien_tai_fset_sl = frozenset(map(tuple, tap_niem_tin_hien_tai_de_xet_sl))
        if tap_niem_tin_hien_tai_fset_sl in danh_sach_dong_cac_tap_niem_tin_sl:
            continue
            
        danh_sach_dong_cac_tap_niem_tin_sl.add(tap_niem_tin_hien_tai_fset_sl)
        
        if kiem_tra_tap_niem_tin_la_dich_sl(tap_niem_tin_hien_tai_de_xet_sl):
            return cac_hanh_dong_da_thuc_hien_sl
        
        cac_tap_niem_tin_ke_tiep_sl = ap_dung_hanh_dong_len_tap_niem_tin_sl(tap_niem_tin_hien_tai_de_xet_sl)

        CAC_HUONG_DI_CHUYEN_CHO_SL_KEYS = list( {"U": -3, "D": 3, "L": -1, "R": 1}.keys())

        for i_sl in range(len(cac_tap_niem_tin_ke_tiep_sl)):
            tap_niem_tin_moi_de_them_sl = cac_tap_niem_tin_ke_tiep_sl[i_sl]
            hanh_dong_tuong_ung_sl = CAC_HUONG_DI_CHUYEN_CHO_SL_KEYS[i_sl] 
            
            tap_niem_tin_moi_fset_sl = frozenset(map(tuple, tap_niem_tin_moi_de_them_sl))
            if tap_niem_tin_moi_fset_sl not in danh_sach_dong_cac_tap_niem_tin_sl:
                hang_doi_mo_sl.them((tap_niem_tin_moi_de_them_sl, cac_hanh_dong_da_thuc_hien_sl + [hanh_dong_tuong_ung_sl]))
    return None

giai_phap_tim_duoc_sl = tim_kiem_khong_thong_tin_cho_sensorless(tap_niem_tin_ban_dau_sl, "BFS")
if giai_phap_tim_duoc_sl:
    print("Tìm thấy giải pháp (chuỗi hành động):", giai_phap_tim_duoc_sl)
else:
    print("Không tìm thấy giải pháp")