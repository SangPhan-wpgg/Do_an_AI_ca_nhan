def tim_kiem_quay_lui(bang_hien_tai: list, vi_tri_dang_xet: int, cac_so_da_dung: list, trang_thai_dich: list, duong_di_hien_tai: list):
    if vi_tri_dang_xet == 9:
        if bang_hien_tai == trang_thai_dich:
            print("Đã tìm thấy trạng thái đích:")
            for buoc_di in duong_di_hien_tai:
                in_bang(buoc_di)
        return

    for so_de_thu in range(9):
        if not cac_so_da_dung[so_de_thu]:
            bang_hien_tai[vi_tri_dang_xet] = so_de_thu
            cac_so_da_dung[so_de_thu] = True
            duong_di_hien_tai.append(bang_hien_tai[:])
            tim_kiem_quay_lui(bang_hien_tai, vi_tri_dang_xet + 1, cac_so_da_dung, trang_thai_dich, duong_di_hien_tai)
            duong_di_hien_tai.pop()
            cac_so_da_dung[so_de_thu] = False
            bang_hien_tai[vi_tri_dang_xet] = -1

def in_bang(bang_can_in: list):
    for i in range(0, 9, 3):
        print(bang_can_in[i:i+3])
    print()
    print("--------------------")
    print()

bang_khoi_tao = [-1] * 9
cac_so_da_su_dung_ban_dau = [False] * 9
trang_thai_dich_muc_tieu = [6, 7, 8, 0, 1, 2, 3, 4, 5]
duong_di_tim_kiem = []

tim_kiem_quay_lui(bang_khoi_tao, 0, cac_so_da_su_dung_ban_dau, trang_thai_dich_muc_tieu, duong_di_tim_kiem)