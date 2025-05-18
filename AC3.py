from collections import deque

def rang_buoc_khac_biet(x: int, y: int): 
    return x != y

def thuat_toan_ac3(cac_mien_gia_tri, cac_hang_xom):
    hang_doi_cung = deque([(bien_i, bien_j) for bien_i in cac_mien_gia_tri for bien_j in cac_hang_xom[bien_i]]) 
    # queue chứa các cạnh (cung), khởi tạo là tất cả các cạnh
    while hang_doi_cung:
        bien_i, bien_j = hang_doi_cung.popleft()
        if xem_xet_lai_mien(cac_mien_gia_tri, bien_i, bien_j): # revise -> xem_xet_lai_mien
            if not cac_mien_gia_tri[bien_i]:
                return False # Miền giá trị rỗng -> không hợp lệ -> dừng (tìm thấy sự không nhất quán)
            for bien_k in cac_hang_xom[bien_i]: # Xk -> bien_k
                if bien_k != bien_j:
                    hang_doi_cung.append((bien_k, bien_i))
    return True

def xem_xet_lai_mien(cac_mien_gia_tri: dict, bien_i, bien_j): # revise -> xem_xet_lai_mien, domains -> cac_mien_gia_tri
    da_dieu_chinh = False # revised -> da_dieu_chinh
    # biến ghi nhận có sửa đổi hay không
    for gia_tri_x in cac_mien_gia_tri[bien_i][:]: # x -> gia_tri_x
        # Không có gia_tri_y nào trong mien_gia_tri_j cho phép (gia_tri_x, gia_tri_y) thỏa mãn ràng buộc (khác nhau) giữa mien_gia_tri_i và mien_gia_tri_j
        if all(not rang_buoc_khac_biet(gia_tri_x, gia_tri_y) for gia_tri_y in cac_mien_gia_tri[bien_j]): # y -> gia_tri_y
            cac_mien_gia_tri[bien_i].remove(gia_tri_x)
            da_dieu_chinh = True
    return da_dieu_chinh

danh_sach_bien = [] # variables -> danh_sach_bien
# Danh sách các ô
for i in range(9):
    danh_sach_bien.append(f'X{i}')

# Khởi tạo miền giá trị ban đầu: mọi ô có thể là 0..8
cac_mien_gia_tri_ban_dau = {} # domains -> cac_mien_gia_tri_ban_dau
for bien in danh_sach_bien: # var -> bien
    cac_mien_gia_tri_ban_dau[bien] = list(range(9))
cac_mien_gia_tri_ban_dau['X0'] = [1]
cac_mien_gia_tri_ban_dau['X1'] = [2]

cac_hang_xom_ban_dau = {} # neighbors -> cac_hang_xom_ban_dau
for bien in danh_sach_bien: # var -> bien
    cac_hang_xom_ban_dau[bien] = [v for v in danh_sach_bien if v != bien]

ban_sao_mien_gia_tri = cac_mien_gia_tri_ban_dau.copy() # domains_copy -> ban_sao_mien_gia_tri
co_ket_qua = thuat_toan_ac3(ban_sao_mien_gia_tri, cac_hang_xom_ban_dau) # has_result -> co_ket_qua

if co_ket_qua:
    print("Kết quả thuật toán AC3:")
    for bien in sorted(ban_sao_mien_gia_tri): # var -> bien
        print(f"{bien}: {ban_sao_mien_gia_tri[bien]}")
else:
    print("Không tìm ra lời giải")