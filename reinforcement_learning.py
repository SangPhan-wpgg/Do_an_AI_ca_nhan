import random
from collections import defaultdict
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

cac_hanh_dong_htc = ['Up', 'Down', 'Left', 'Right']

CAC_BUOC_DI_CHUYEN_HTC = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

def kiem_tra_trang_thai_dich_htc(trang_thai_htc: tuple, tuple_trang_thai_dich_htc: tuple) -> bool:
    return trang_thai_htc == tuple_trang_thai_dich_htc

def kiem_tra_di_chuyen_hop_le_htc(vi_tri_so_khong_htc: int, huong_di_chuyen_htc: str) -> bool:
    if huong_di_chuyen_htc == 'Up' and vi_tri_so_khong_htc < 3:
        return False
    if huong_di_chuyen_htc == 'Down' and vi_tri_so_khong_htc > 5:
        return False
    if huong_di_chuyen_htc == 'Left' and vi_tri_so_khong_htc % 3 == 0:
        return False
    if huong_di_chuyen_htc == 'Right' and vi_tri_so_khong_htc % 3 == 2:
        return False
    return True

def thuc_hien_di_chuyen_htc(trang_thai_htc: tuple, huong_di_chuyen_htc: str):
    vi_tri_so_khong_htc = trang_thai_htc.index(0)
    if not kiem_tra_di_chuyen_hop_le_htc(vi_tri_so_khong_htc, huong_di_chuyen_htc):
        return None
    vi_tri_moi_htc = vi_tri_so_khong_htc + CAC_BUOC_DI_CHUYEN_HTC[huong_di_chuyen_htc]
    trang_thai_moi_list_htc = list(trang_thai_htc)
    trang_thai_moi_list_htc[vi_tri_so_khong_htc], trang_thai_moi_list_htc[vi_tri_moi_htc] = trang_thai_moi_list_htc[vi_tri_moi_htc], trang_thai_moi_list_htc[vi_tri_so_khong_htc]
    return tuple(trang_thai_moi_list_htc)

def tinh_heuristic_htc(trang_thai_htc: tuple, tuple_trang_thai_dich_htc: tuple) -> int:
    gia_tri_h_htc = 0
    for i_htc in range(1, 9):
        try:
            vi_tri_x1_htc, vi_tri_y1_htc = divmod(trang_thai_htc.index(i_htc), 3)
            vi_tri_x2_htc, vi_tri_y2_htc = divmod(tuple_trang_thai_dich_htc.index(i_htc), 3)
            gia_tri_h_htc += abs(vi_tri_x1_htc - vi_tri_x2_htc) + abs(vi_tri_y1_htc - vi_tri_y2_htc)
        except ValueError:
            pass #Bỏ qua nếu số không có trong trạng thái (dù 8-puzzle thường có đủ)
    return gia_tri_h_htc

def giai_bang_hoc_tang_cuong(tuple_trang_thai_bat_dau_htc: tuple, tuple_trang_thai_dich_htc: tuple, danh_sach_q_htc: list)->list:
    alpha_htc = 0.1
    gamma_htc = 0.8
    epsilon_htc = 0.4
    so_luong_episodes_htc = 10000

    cac_phan_thuong_moi_episode_htc = []
    cac_buoc_moi_episode_htc = []
    cac_lan_thanh_cong_htc = []
    dem_thanh_cong_htc = 0
    
    bang_q_htc = defaultdict(lambda: {a_htc: 0.0 for a_htc in cac_hanh_dong_htc})
    for episode_idx_htc in range(so_luong_episodes_htc):
        trang_thai_hien_tai_htc = deepcopy(tuple_trang_thai_bat_dau_htc)
        so_buoc_htc = 0
        tong_phan_thuong_htc = 0
        SO_BUOC_TOI_DA_HTC = 20000
        while not kiem_tra_trang_thai_dich_htc(trang_thai_hien_tai_htc, tuple_trang_thai_dich_htc) and so_buoc_htc < SO_BUOC_TOI_DA_HTC:
            if random.uniform(0, 1) < epsilon_htc:
                hanh_dong_duoc_chon_htc = random.choice(cac_hanh_dong_htc)
            else:
                hanh_dong_duoc_chon_htc = max(bang_q_htc[trang_thai_hien_tai_htc], key=bang_q_htc[trang_thai_hien_tai_htc].get)
            
            trang_thai_ke_tiep_htc = thuc_hien_di_chuyen_htc(trang_thai_hien_tai_htc, hanh_dong_duoc_chon_htc)
            
            if trang_thai_ke_tiep_htc is None:
                phan_thuong_htc = -50 
                gia_tri_q_moi_toi_da_htc = 0
                xac_suat_chuyen_trang_thai_htc = 0.0001
            else:
                phan_thuong_htc = 100 if kiem_tra_trang_thai_dich_htc(trang_thai_ke_tiep_htc, tuple_trang_thai_dich_htc) else -1
                if trang_thai_ke_tiep_htc not in bang_q_htc:
                    bang_q_htc[trang_thai_ke_tiep_htc] = {a_htc: 0 for a_htc in cac_hanh_dong_htc}
                gia_tri_q_moi_toi_da_htc = max(bang_q_htc[trang_thai_ke_tiep_htc].values())
                heuristic_val_htc = tinh_heuristic_htc(trang_thai_ke_tiep_htc, tuple_trang_thai_dich_htc)
                xac_suat_chuyen_trang_thai_htc = 1 - heuristic_val_htc / 41 if heuristic_val_htc < 41 else 0.0001 # Giả sử 41 là h tối đa
            
            tong_phan_thuong_htc += phan_thuong_htc
            
            bang_q_htc[trang_thai_hien_tai_htc][hanh_dong_duoc_chon_htc] += alpha_htc * (phan_thuong_htc + gamma_htc * xac_suat_chuyen_trang_thai_htc * gia_tri_q_moi_toi_da_htc - bang_q_htc[trang_thai_hien_tai_htc][hanh_dong_duoc_chon_htc])
            
            if trang_thai_ke_tiep_htc is None:
                break
            trang_thai_hien_tai_htc = trang_thai_ke_tiep_htc
            so_buoc_htc += 1
            
        if kiem_tra_trang_thai_dich_htc(trang_thai_hien_tai_htc, tuple_trang_thai_dich_htc):
            cac_buoc_moi_episode_htc.append(so_buoc_htc)
            dem_thanh_cong_htc += 1
        else:
            cac_buoc_moi_episode_htc.append(SO_BUOC_TOI_DA_HTC)
        cac_phan_thuong_moi_episode_htc.append(tong_phan_thuong_htc)
        
        if (episode_idx_htc + 1) % 100 == 0:
            cac_lan_thanh_cong_htc.append(dem_thanh_cong_htc / 100)
            dem_thanh_cong_htc = 0
            
    for trang_thai_q_htc in bang_q_htc.keys():
        danh_sach_q_htc.append(f"{trang_thai_q_htc}: {bang_q_htc[trang_thai_q_htc]}")
        
    trang_thai_hien_tai_htc = deepcopy(tuple_trang_thai_bat_dau_htc)
    so_buoc_giai_htc = 0 # Sửa lỗi so_buoc_giai_htc = 1 thành 0
    giai_phap_htc = []
    while not kiem_tra_trang_thai_dich_htc(trang_thai_hien_tai_htc, tuple_trang_thai_dich_htc) and so_buoc_giai_htc < SO_BUOC_TOI_DA_HTC:
        giai_phap_htc.append(trang_thai_hien_tai_htc)
        if trang_thai_hien_tai_htc not in bang_q_htc:
            break
        hanh_dong_duoc_chon_htc = max(bang_q_htc[trang_thai_hien_tai_htc], key=bang_q_htc[trang_thai_hien_tai_htc].get)
        trang_thai_ke_tiep_htc = thuc_hien_di_chuyen_htc(trang_thai_hien_tai_htc, hanh_dong_duoc_chon_htc)
        if trang_thai_ke_tiep_htc is None:
             break
        trang_thai_hien_tai_htc = trang_thai_ke_tiep_htc
        so_buoc_giai_htc += 1
        
    cac_phan_thuong_trung_binh_htc = [np.mean(cac_phan_thuong_moi_episode_htc[i_htc:i_htc+100]) for i_htc in range(0, len(cac_phan_thuong_moi_episode_htc), 100)]
    plt.figure(figsize=(14, 6))
    plt.plot(range(100, len(cac_phan_thuong_moi_episode_htc)+1, 100), cac_phan_thuong_trung_binh_htc, color='green', label='Phần thưởng TB mỗi 100 episode')
    plt.xlabel("Episode")
    plt.ylabel("Phần thưởng")
    plt.title("Phần thưởng trung bình mỗi 100 episode")
    plt.grid(True)
    plt.legend()
    plt.show()

    cac_buoc_trung_binh_htc = [np.mean(cac_buoc_moi_episode_htc[i_htc:i_htc+100]) for i_htc in range(0, len(cac_buoc_moi_episode_htc), 100)]
    plt.figure(figsize=(14, 6))
    plt.plot(range(100, len(cac_buoc_moi_episode_htc)+1, 100), cac_buoc_trung_binh_htc, color='orange', label='Số bước TB mỗi 100 episode')
    plt.xlabel("Episode")
    plt.ylabel("Số bước đến đích")
    plt.title("Số bước trung bình mỗi 100 episode")
    plt.grid(True)
    plt.legend()
    plt.show()
    
    plt.figure(figsize=(10, 4))
    plt.plot(range(100, len(cac_lan_thanh_cong_htc)*100 + 1, 100), cac_lan_thanh_cong_htc)
    plt.title('Tỷ lệ thành công mỗi 100 episode')
    plt.xlabel('Episode')
    plt.ylabel('Tỷ lệ thành công')
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    if kiem_tra_trang_thai_dich_htc(trang_thai_hien_tai_htc, tuple_trang_thai_dich_htc):
        giai_phap_htc.append(tuple_trang_thai_dich_htc)
        return giai_phap_htc
    else:
        return None