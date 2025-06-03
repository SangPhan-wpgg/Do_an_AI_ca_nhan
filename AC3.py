from collections import deque
from typing import Dict, List, Set

def rang_buoc_khac_biet(x: int, y: int) -> bool:
    return x != y

def xem_xet_lai_mien(mien_gia_tri: Dict[str, Set[int]], bien_i: str, bien_j: str) -> bool:

    da_dieu_chinh = False
    mien_i = mien_gia_tri[bien_i].copy() 
    for gia_tri_x in mien_i:
        if all(not rang_buoc_khac_biet(gia_tri_x, gia_tri_y) for gia_tri_y in mien_gia_tri[bien_j]):
            mien_gia_tri[bien_i].remove(gia_tri_x)
            da_dieu_chinh = True
    return da_dieu_chinh

def thuat_toan_ac3(mien_gia_tri: Dict[str, Set[int]], hang_xom: Dict[str, List[str]]) -> bool:
    hang_doi_cung = deque((bien_i, bien_j) for bien_i in mien_gia_tri for bien_j in hang_xom[bien_i])
    
    while hang_doi_cung:
        bien_i, bien_j = hang_doi_cung.popleft()
        if xem_xet_lai_mien(mien_gia_tri, bien_i, bien_j):
            if not mien_gia_tri[bien_i]:  
                return False
            for bien_k in hang_xom[bien_i]:
                if bien_k != bien_j:
                    hang_doi_cung.append((bien_k, bien_i))
    return True

def khoi_tao_puzzle() -> tuple[List[str], Dict[str, Set[int]], Dict[str, List[str]]]:

    danh_sach_bien = [f'X{i}' for i in range(9)]
    mien_gia_tri = {bien: set(range(9)) for bien in danh_sach_bien}
    mien_gia_tri['X0'] = {1}
    mien_gia_tri['X1'] = {2}
    hang_xom = {
        bien: [v for v in danh_sach_bien if v != bien]
        for bien in danh_sach_bien
    }
    
    return danh_sach_bien, mien_gia_tri, hang_xom

def main():
    danh_sach_bien, mien_gia_tri, hang_xom = khoi_tao_puzzle()
    for bien in mien_gia_tri:
        if not mien_gia_tri[bien]:
            print(f"Lỗi: Miền giá trị của {bien} rỗng ngay từ đầu!")
            return
    co_ket_qua = thuat_toan_ac3(mien_gia_tri, hang_xom)
    if co_ket_qua:
        print("Kết quả thuật toán AC-3:")
        for bien in sorted(danh_sach_bien):
            print(f"{bien}: {sorted(mien_gia_tri[bien])}")
    else:
        print("Không tìm ra lời giải")

if __name__ == "__main__":
    main()