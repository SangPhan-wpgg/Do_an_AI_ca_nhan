from collections import deque
from Cau_truc import NutTimKiem 

CAC_BUOC_DI_CHUYEN_MTK = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

do_sau_toi_da_mtk = 100000

def kiem_tra_di_chuyen_hop_le_mtk(vi_tri_so_khong_mtk, huong_mtk):
    if huong_mtk == 'Up' and vi_tri_so_khong_mtk < 3:
        return False
    if huong_mtk == 'Down' and vi_tri_so_khong_mtk > 5:
        return False
    if huong_mtk == 'Left' and vi_tri_so_khong_mtk % 3 == 0:
        return False
    if huong_mtk == 'Right' and vi_tri_so_khong_mtk % 3 == 2:
        return False
    return True

def thuc_hien_di_chuyen_mtk(trang_thai_mtk: tuple, huong_mtk: str):
    vi_tri_so_khong_mtk = trang_thai_mtk.index(0)
    if not kiem_tra_di_chuyen_hop_le_mtk(vi_tri_so_khong_mtk, huong_mtk):
        return None
    vi_tri_moi_mtk = vi_tri_so_khong_mtk + CAC_BUOC_DI_CHUYEN_MTK[huong_mtk]
    trang_thai_moi_list_mtk = list(trang_thai_mtk)
    trang_thai_moi_list_mtk[vi_tri_so_khong_mtk], trang_thai_moi_list_mtk[vi_tri_moi_mtk] = trang_thai_moi_list_mtk[vi_tri_moi_mtk], trang_thai_moi_list_mtk[vi_tri_so_khong_mtk]
    return tuple(trang_thai_moi_list_mtk)

def ap_dung_hanh_dong_cho_tap_niem_tin_mtk(tap_niem_tin_mtk: list, hanh_dong_mtk: str, tap_trang_thai_dich_mtk: list, la_quan_sat_mot_phan_mtk: bool = False):
    tap_ket_qua_mtk = []
    cac_trang_thai_da_tham_trong_tap_mtk = set()
    for trang_thai_trong_niem_tin_mtk in tap_niem_tin_mtk:
        trang_thai_moi_sau_hanh_dong_mtk = thuc_hien_di_chuyen_mtk(trang_thai_trong_niem_tin_mtk, hanh_dong_mtk)
        if trang_thai_moi_sau_hanh_dong_mtk is None:
            trang_thai_moi_sau_hanh_dong_mtk = trang_thai_trong_niem_tin_mtk
        
        if trang_thai_moi_sau_hanh_dong_mtk not in cac_trang_thai_da_tham_trong_tap_mtk:
            cac_trang_thai_da_tham_trong_tap_mtk.add(trang_thai_moi_sau_hanh_dong_mtk)
            if la_quan_sat_mot_phan_mtk:
                if kiem_tra_gan_dich_mtk(trang_thai_moi_sau_hanh_dong_mtk, tap_trang_thai_dich_mtk):                  
                    tap_ket_qua_mtk.append(trang_thai_moi_sau_hanh_dong_mtk)
            else:                
                tap_ket_qua_mtk.append(trang_thai_moi_sau_hanh_dong_mtk)
    return tap_ket_qua_mtk

def kiem_tra_tap_niem_tin_la_dich_mtk(tap_niem_tin_mtk: list, tap_trang_thai_dich_mtk: list) -> bool:
    if not tap_niem_tin_mtk : return False 
    return all(trang_thai_trong_niem_tin in tap_trang_thai_dich_mtk for trang_thai_trong_niem_tin in tap_niem_tin_mtk)

def kiem_tra_gan_dich_mtk(trang_thai_mtk:tuple, tap_trang_thai_dich_mtk:list) -> bool:
    if not tap_trang_thai_dich_mtk: return False 
    return trang_thai_mtk[:3] == tap_trang_thai_dich_mtk[0][:3] # Giả định so sánh 3 phần tử đầu

def in_trang_thai_mtk(trang_thai_de_in_mtk):
    for i_mtk in range(0, 9, 3):
        print(trang_thai_de_in_mtk[i_mtk], trang_thai_de_in_mtk[i_mtk+1], trang_thai_de_in_mtk[i_mtk+2])

def tim_kiem_trong_moi_truong_phuc_tap(tap_niem_tin_ban_dau_mtk: list, tap_trang_thai_dich_mtk: list, danh_sach_so_trang_thai_da_mo_mtk: list, la_quan_sat_mot_phan_mtk: bool = False) -> list:
    hang_doi_mtk = deque()
    cac_tap_niem_tin_da_tham_mtk = set()
    hang_doi_mtk.append((tap_niem_tin_ban_dau_mtk, []))
    do_sau_hien_tai_mtk = 0
    
    while hang_doi_mtk and do_sau_hien_tai_mtk < do_sau_toi_da_mtk:
        tap_niem_tin_hien_tai_mtk, cac_hanh_dong_hien_tai_mtk = hang_doi_mtk.popleft()
        
        tap_niem_tin_dong_bang_mtk = frozenset(map(tuple, tap_niem_tin_hien_tai_mtk)) # Đảm bảo các phần tử bên trong là tuple
        if tap_niem_tin_dong_bang_mtk in cac_tap_niem_tin_da_tham_mtk:
            continue
        cac_tap_niem_tin_da_tham_mtk.add(tap_niem_tin_dong_bang_mtk)
        
        if kiem_tra_tap_niem_tin_la_dich_mtk(tap_niem_tin_hien_tai_mtk, tap_trang_thai_dich_mtk):
            danh_sach_so_trang_thai_da_mo_mtk[0] = len(cac_tap_niem_tin_da_tham_mtk)
            return cac_hanh_dong_hien_tai_mtk
            
        for hanh_dong_duyet_mtk in CAC_BUOC_DI_CHUYEN_MTK:
            tap_niem_tin_moi_mtk = ap_dung_hanh_dong_cho_tap_niem_tin_mtk(tap_niem_tin_hien_tai_mtk, hanh_dong_duyet_mtk, tap_trang_thai_dich_mtk, la_quan_sat_mot_phan_mtk)
            if tap_niem_tin_moi_mtk: # Chỉ thêm nếu tập niềm tin mới không rỗng
                tap_niem_tin_moi_dong_bang_mtk = frozenset(map(tuple, tap_niem_tin_moi_mtk))
                if tap_niem_tin_moi_dong_bang_mtk not in cac_tap_niem_tin_da_tham_mtk:
                     hang_doi_mtk.append((tap_niem_tin_moi_mtk, cac_hanh_dong_hien_tai_mtk + [hanh_dong_duyet_mtk]))
        do_sau_hien_tai_mtk += 1
        
    danh_sach_so_trang_thai_da_mo_mtk[0] = len(cac_tap_niem_tin_da_tham_mtk)
    return None

def giai_tim_kiem_moi_truong_phuc_tap(tap_niem_tin_ban_dau_giai_mtk: list, tap_trang_thai_dich_giai_mtk: list, danh_sach_so_trang_thai_da_mo_giai_mtk: list, la_quan_sat_mot_phan_giai_mtk: bool = False) -> list:
    ke_hoach_mtk = tim_kiem_trong_moi_truong_phuc_tap(tap_niem_tin_ban_dau_giai_mtk, tap_trang_thai_dich_giai_mtk, danh_sach_so_trang_thai_da_mo_giai_mtk, la_quan_sat_mot_phan_giai_mtk)
    return ke_hoach_mtk