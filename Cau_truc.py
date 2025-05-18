from collections import deque
import heapq

class NutTimKiem:
    def __init__(self, cha=None, hanh_dong=None, trang_thai=(0,0,0,0,0,0,0,0,0)):
        self.cha = cha
        self.hanh_dong = hanh_dong
        self.trang_thai = trang_thai
        if cha is not None:
            self.chi_phi_g = cha.chi_phi_g + self.tinh_chi_phi_g(hanh_dong)
        else:
            self.chi_phi_g = 0
        self.chi_phi_h = 0
        
    def tinh_chi_phi_g(self, hanh_dong_chi_phi_g):
        if hanh_dong_chi_phi_g is None:
            return 0
        return 1
        
    def __lt__(self, nut_khac):
        return self.chi_phi_g < nut_khac.chi_phi_g

def tao_nut_tim_kiem(cha_nut, hanh_dong_nut, trang_thai_nut):
    return NutTimKiem(cha_nut, hanh_dong_nut, trang_thai_nut)

def trich_xuat_duong_di(nut_hien_tai: NutTimKiem) -> list:
    duong_di_ket_qua = []
    if nut_hien_tai: 
        tam_thoi_nut = nut_hien_tai
        while tam_thoi_nut.cha is not None:
            duong_di_ket_qua.append(tam_thoi_nut.trang_thai)
            tam_thoi_nut = tam_thoi_nut.cha
        if tam_thoi_nut:
            duong_di_ket_qua.append(tam_thoi_nut.trang_thai)
        duong_di_ket_qua.reverse()
    return duong_di_ket_qua

class DanhSachMo:
    def __init__(self, loai_danh_sach: str) -> None:
        self.hang_doi_kep = deque()
        self.loai_danh_sach = loai_danh_sach
        if loai_danh_sach == "UCS" or loai_danh_sach == "Beam search" or loai_danh_sach == "Genetic algorithm" or loai_danh_sach == "A*" or loai_danh_sach == "Greedy": # A* và Greedy cũng dùng heapq với f_cost hoặc h_cost
            self.hang_doi_kep = []
            heapq.heapify(self.hang_doi_kep)
            
    def them(self, nut_can_them:NutTimKiem):
        if self.loai_danh_sach == "UCS":
            heapq.heappush(self.hang_doi_kep, (nut_can_them.chi_phi_g, nut_can_them))
        elif self.loai_danh_sach == "A*": 
            heapq.heappush(self.hang_doi_kep, (nut_can_them.chi_phi_g + nut_can_them.chi_phi_h, nut_can_them))
        elif self.loai_danh_sach == "Greedy" or self.loai_danh_sach == "Beam search" or self.loai_danh_sach == "Genetic algorithm": # Các thuật toán này thường ưu tiên h_cost
            heapq.heappush(self.hang_doi_kep, (nut_can_them.chi_phi_h, nut_can_them))
        else:
            self.hang_doi_kep.append(nut_can_them)
            
    def lay_phan_tu(self):
        if self.loai_danh_sach == "BFS":
            return self.hang_doi_kep.popleft()
        elif self.loai_danh_sach in ["UCS", "A*", "Greedy", "Beam search", "Genetic algorithm"]:                
            return heapq.heappop(self.hang_doi_kep)[1] 
        elif self.loai_danh_sach == "DFS":
            return self.hang_doi_kep.pop()
            
    def la_rong(self):
        return len(self.hang_doi_kep) == 0

class DanhSachDong:
    def __init__(self):
        self.tap_hop_trang_thai = set()
        
    def tra_cuu(self, trang_thai_can_tra_cuu:tuple)->bool:
        return trang_thai_can_tra_cuu in self.tap_hop_trang_thai
        
    def them(self, trang_thai_can_them:tuple)->None:
        self.tap_hop_trang_thai.add(trang_thai_can_them)