import random
from collections import defaultdict
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

cac_hanh_dong_n2 = ['Up', 'Down', 'Left', 'Right']

CAC_BUOC_DI_CHUYEN_N2 = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

def kiem_tra_trang_thai_dich_n2(trang_thai_n2: tuple, tuple_trang_thai_dich_n2: tuple) -> bool:
    return trang_thai_n2 == tuple_trang_thai_dich_n2

def kiem_tra_di_chuyen_hop_le_n2(vi_tri_so_khong_n2: int, huong_di_chuyen_n2: str) -> bool:
    if huong_di_chuyen_n2 == 'Up' and vi_tri_so_khong_n2 < 3:
        return False
    if huong_di_chuyen_n2 == 'Down' and vi_tri_so_khong_n2 > 5:
        return False
    if huong_di_chuyen_n2 == 'Left' and vi_tri_so_khong_n2 % 3 == 0:
        return False
    if huong_di_chuyen_n2 == 'Right' and vi_tri_so_khong_n2 % 3 == 2:
        return False
    return True

def thuc_hien_di_chuyen_n2(trang_thai_n2: tuple, huong_di_chuyen_n2: str):
    vi_tri_so_khong_n2 = trang_thai_n2.index(0)
    if not kiem_tra_di_chuyen_hop_le_n2(vi_tri_so_khong_n2, huong_di_chuyen_n2):
        return None
    vi_tri_moi_n2 = vi_tri_so_khong_n2 + CAC_BUOC_DI_CHUYEN_N2[huong_di_chuyen_n2]
    trang_thai_moi_list_n2 = list(trang_thai_n2)
    trang_thai_moi_list_n2[vi_tri_so_khong_n2], trang_thai_moi_list_n2[vi_tri_moi_n2] = trang_thai_moi_list_n2[vi_tri_moi_n2], trang_thai_moi_list_n2[vi_tri_so_khong_n2]
    return tuple(trang_thai_moi_list_n2)

def tinh_heuristic_n2(trang_thai_n2: tuple, tuple_trang_thai_dich_n2: tuple) -> int:
    gia_tri_h_n2 = 0
    for i_n2 in range(1, 9):
        vi_tri_x1_n2, vi_tri_y1_n2 = divmod(trang_thai_n2.index(i_n2), 3)
        vi_tri_x2_n2, vi_tri_y2_n2 = divmod(tuple_trang_thai_dich_n2.index(i_n2), 3)
        gia_tri_h_n2 += abs(vi_tri_x1_n2 - vi_tri_x2_n2) + abs(vi_tri_y1_n2 - vi_tri_y2_n2)
    return gia_tri_h_n2

def giai_bang_hoc_tang_cuong_n2(tuple_trang_thai_bat_dau_n2: tuple, tuple_trang_thai_dich_n2: tuple, danh_sach_q_n2: list)->list:
    alpha_n2 = 0.1
    gamma_n2 = 0.8
    epsilon_n2 = 0.4
    so_luong_episodes_n2 = 10000

    cac_phan_thuong_moi_episode_n2 = []
    cac_buoc_moi_episode_n2 = []
    cac_lan_thanh_cong_n2 = []
    dem_thanh_cong_n2 = 0
    
    bang_q_n2 = defaultdict(lambda: {a_n2: 0.0 for a_n2 in cac_hanh_dong_n2})
    for episode_idx_n2 in range(so_luong_episodes_n2):
        trang_thai_hien_tai_n2 = deepcopy(tuple_trang_thai_bat_dau_n2)
        so_buoc_n2 = 0
        tong_phan_thuong_n2 = 0
        SO_BUOC_TOI_DA_N2 = 20000
        while not kiem_tra_trang_thai_dich_n2(trang_thai_hien_tai_n2, tuple_trang_thai_dich_n2) and so_buoc_n2 < SO_BUOC_TOI_DA_N2:
            if random.uniform(0, 1) < epsilon_n2:
                hanh_dong_duoc_chon_n2 = random.choice(cac_hanh_dong_n2)
            else:
                hanh_dong_duoc_chon_n2 = max(bang_q_n2[trang_thai_hien_tai_n2], key=bang_q_n2[trang_thai_hien_tai_n2].get)
            
            trang_thai_ke_tiep_n2 = thuc_hien_di_chuyen_n2(trang_thai_hien_tai_n2, hanh_dong_duoc_chon_n2)
            
            if trang_thai_ke_tiep_n2 is None:
                phan_thuong_n2 = -50 
                gia_tri_q_moi_toi_da_n2 = 0
                xac_suat_chuyen_trang_thai_n2 = 0.0001
            else:
                phan_thuong_n2 = 100 if kiem_tra_trang_thai_dich_n2(trang_thai_ke_tiep_n2, tuple_trang_thai_dich_n2) else -1
                if trang_thai_ke_tiep_n2 not in bang_q_n2:
                    bang_q_n2[trang_thai_ke_tiep_n2] = {a_n2: 0 for a_n2 in cac_hanh_dong_n2}
                gia_tri_q_moi_toi_da_n2 = max(bang_q_n2[trang_thai_ke_tiep_n2].values())
                heuristic_val = tinh_heuristic_n2(trang_thai_ke_tiep_n2, tuple_trang_thai_dich_n2)
                xac_suat_chuyen_trang_thai_n2 = 1 - heuristic_val / 41 if heuristic_val < 41 else 0.0001
            
            tong_phan_thuong_n2 += phan_thuong_n2
            
            bang_q_n2[trang_thai_hien_tai_n2][hanh_dong_duoc_chon_n2] += alpha_n2 * (phan_thuong_n2 + gamma_n2 * xac_suat_chuyen_trang_thai_n2 * gia_tri_q_moi_toi_da_n2 - bang_q_n2[trang_thai_hien_tai_n2][hanh_dong_duoc_chon_n2])
            
            if trang_thai_ke_tiep_n2 is None:
                break
            trang_thai_hien_tai_n2 = trang_thai_ke_tiep_n2
            so_buoc_n2 += 1
            
        if kiem_tra_trang_thai_dich_n2(trang_thai_hien_tai_n2, tuple_trang_thai_dich_n2):
            cac_buoc_moi_episode_n2.append(so_buoc_n2)
            dem_thanh_cong_n2 += 1
        else:
            cac_buoc_moi_episode_n2.append(SO_BUOC_TOI_DA_N2)
        cac_phan_thuong_moi_episode_n2.append(tong_phan_thuong_n2)
        
        if (episode_idx_n2 + 1) % 100 == 0:
            cac_lan_thanh_cong_n2.append(dem_thanh_cong_n2 / 100)
            dem_thanh_cong_n2 = 0
            
    for trang_thai_q_n2 in bang_q_n2.keys():
        danh_sach_q_n2.append(f"{trang_thai_q_n2}: {bang_q_n2[trang_thai_q_n2]}")
        
    trang_thai_hien_tai_n2 = deepcopy(tuple_trang_thai_bat_dau_n2)
    so_buoc_giai_n2 = 1
    giai_phap_n2 = []
    while not kiem_tra_trang_thai_dich_n2(trang_thai_hien_tai_n2, tuple_trang_thai_dich_n2) and so_buoc_giai_n2 < SO_BUOC_TOI_DA_N2:
        giai_phap_n2.append(trang_thai_hien_tai_n2)
        if trang_thai_hien_tai_n2 not in bang_q_n2:
            break
        hanh_dong_duoc_chon_n2 = max(bang_q_n2[trang_thai_hien_tai_n2], key=bang_q_n2[trang_thai_hien_tai_n2].get)
        trang_thai_hien_tai_n2 = thuc_hien_di_chuyen_n2(trang_thai_hien_tai_n2, hanh_dong_duoc_chon_n2)
        if trang_thai_hien_tai_n2 is None:
             break
        so_buoc_giai_n2 += 1
        
    cac_phan_thuong_trung_binh_n2 = [np.mean(cac_phan_thuong_moi_episode_n2[i_n2:i_n2+100]) for i_n2 in range(0, len(cac_phan_thuong_moi_episode_n2), 100)]
    plt.figure(figsize=(14, 6))
    plt.plot(range(100, len(cac_phan_thuong_moi_episode_n2)+1, 100), cac_phan_thuong_trung_binh_n2, color='green', label='Phần thưởng trung bình mỗi 100 episode')
    plt.xlabel("Episode")
    plt.ylabel("Phần thưởng")
    plt.title("Phần thưởng trung bình mỗi 100 episode (Nháp 2)")
    plt.grid(True)
    plt.legend()
    plt.show()

    cac_buoc_trung_binh_n2 = [np.mean(cac_buoc_moi_episode_n2[i_n2:i_n2+100]) for i_n2 in range(0, len(cac_buoc_moi_episode_n2), 100)]
    plt.figure(figsize=(14, 6))
    plt.plot(range(100, len(cac_buoc_moi_episode_n2)+1, 100), cac_buoc_trung_binh_n2, color='orange', label='Số bước trung bình mỗi 100 episode')
    plt.xlabel("Episode")
    plt.ylabel("Số bước đến đích")
    plt.title("Số bước trung bình mỗi 100 episode (Nháp 2)")
    plt.grid(True)
    plt.legend()
    plt.show()
    
    plt.figure(figsize=(10, 4))
    plt.plot(range(100, len(cac_lan_thanh_cong_n2)*100 + 1, 100), cac_lan_thanh_cong_n2)
    plt.title('Tỷ lệ thành công mỗi 100 episode (Nháp 2)')
    plt.xlabel('Episode')
    plt.ylabel('Tỷ lệ thành công')
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    if kiem_tra_trang_thai_dich_n2(trang_thai_hien_tai_n2, tuple_trang_thai_dich_n2):
        giai_phap_n2.append(tuple_trang_thai_dich_n2)
        return giai_phap_n2
    else:
        return None