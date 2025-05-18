import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel
)
from PyQt6.QtCore import QTimer
import copy

danh_sach_bien_n = ["X", "Y", "Z"]

cac_mien_gia_tri_n = {
    "X": [0,1,2,3,4,5,6,7,8],
    "Y": [0,1,2,3,4,5,6,7,8],
    "Z": [0,1,2,3,4,5,6,7,8]
}

def kiem_tra_nhat_quan_n(bien_n, gia_tri_n, phep_gan_n):
    for bien_khac_n in phep_gan_n:
        if phep_gan_n[bien_khac_n] == gia_tri_n:
            return False
    return True

def chon_bien_chua_gan_n(danh_sach_bien_trong_n, phep_gan_trong_n):
    for bien_trong_n in danh_sach_bien_trong_n:
        if bien_trong_n not in phep_gan_trong_n:
            return bien_trong_n
    return None

def quay_lui_n(phep_gan_n):
    if len(phep_gan_n) == len(danh_sach_bien_n):
        return phep_gan_n

    bien_duoc_chon_n = chon_bien_chua_gan_n(danh_sach_bien_n, phep_gan_n)
    if bien_duoc_chon_n is None:
        return None 

    for gia_tri_duyet_n in cac_mien_gia_tri_n[bien_duoc_chon_n]:
        if kiem_tra_nhat_quan_n(bien_duoc_chon_n, gia_tri_duyet_n, phep_gan_n):
            phep_gan_n[bien_duoc_chon_n] = gia_tri_duyet_n
            ket_qua_n = quay_lui_n(phep_gan_n)
            if ket_qua_n:
                return ket_qua_n
            del phep_gan_n[bien_duoc_chon_n]
    return None

giai_phap_n = quay_lui_n({})
print("Lời giải cho nhap.py:", giai_phap_n)

trang_thai_dich_puzzle_n = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
trang_thai_bat_dau_puzzle_n = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
cac_buoc_di_chuyen_puzzle_n = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class UngDungPuzzleN(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("8 Puzzle Quay Lui - PyQt")
        self.setGeometry(100, 100, 300, 350)

        self.layout_chinh = QVBoxLayout()
        self.setLayout(self.layout_chinh)

        self.bang_hien_thi = QTableWidget(3, 3)
        self.layout_chinh.addWidget(self.bang_hien_thi)

        self.layout_nut_bam = QHBoxLayout()
        self.nut_buoc_tiep = QPushButton("Bước Tiếp")
        self.nut_tu_dong_chay = QPushButton("Tự Động")
        self.nut_dat_lai = QPushButton("Đặt Lại")
        self.layout_nut_bam.addWidget(self.nut_buoc_tiep)
        self.layout_nut_bam.addWidget(self.nut_tu_dong_chay)
        self.layout_nut_bam.addWidget(self.nut_dat_lai)
        self.layout_chinh.addLayout(self.layout_nut_bam)

        self.nhan_trang_thai = QLabel("Đang chờ...")
        self.layout_chinh.addWidget(self.nhan_trang_thai)

        self.nut_buoc_tiep.clicked.connect(self.thuc_hien_buoc_tiep)
        self.nut_tu_dong_chay.clicked.connect(self.thuc_hien_tu_dong_chay)
        self.nut_dat_lai.clicked.connect(self.thuc_hien_dat_lai)

        self.bo_hen_gio_n = QTimer()
        self.bo_hen_gio_n.timeout.connect(self.thuc_hien_buoc_tiep)

        self.thuc_hien_dat_lai()

    def thuc_hien_dat_lai(self):
        self.cac_trang_thai_da_tham_n = set()
        self.duong_di_hien_tai_n = []
        self.ngan_xep_trang_thai_n = [(copy.deepcopy(trang_thai_bat_dau_puzzle_n), [])]
        self.cap_nhat_bang_hien_thi(trang_thai_bat_dau_puzzle_n)
        self.nhan_trang_thai.setText("Đã đặt lại.")
        self.bo_hen_gio_n.stop()

    def cap_nhat_bang_hien_thi(self, trang_thai_bang_n):
        for hang_n in range(3):
            for cot_n in range(3):
                gia_tri_o_n = trang_thai_bang_n[hang_n][cot_n]
                muc_bang_n = QTableWidgetItem("" if gia_tri_o_n == 0 else str(gia_tri_o_n))
                self.bang_hien_thi.setItem(hang_n, cot_n, muc_bang_n)

    def thuc_hien_buoc_tiep(self):
        if not self.ngan_xep_trang_thai_n:
            self.nhan_trang_thai.setText("Không tìm được lời giải.")
            self.bo_hen_gio_n.stop()
            return

        trang_thai_hien_tai_puzzle_n, duong_di_puzzle_n = self.ngan_xep_trang_thai_n.pop()
        khoa_trang_thai_n = tuple(map(tuple, trang_thai_hien_tai_puzzle_n))
        if khoa_trang_thai_n in self.cac_trang_thai_da_tham_n:
            return 
        self.cac_trang_thai_da_tham_n.add(khoa_trang_thai_n)

        self.cap_nhat_bang_hien_thi(trang_thai_hien_tai_puzzle_n)
        self.duong_di_hien_tai_n = duong_di_puzzle_n

        if trang_thai_hien_tai_puzzle_n == trang_thai_dich_puzzle_n:
            self.nhan_trang_thai.setText(f"Đã giải xong sau {len(duong_di_puzzle_n)} bước.")
            self.bo_hen_gio_n.stop()
            return

        vi_tri_x_so_khong_n, vi_tri_y_so_khong_n = next((h, c) for h in range(3) for c in range(3) if trang_thai_hien_tai_puzzle_n[h][c] == 0)

        for delta_x_n, delta_y_n in cac_buoc_di_chuyen_puzzle_n:
            vi_tri_x_moi_n, vi_tri_y_moi_n = vi_tri_x_so_khong_n + delta_x_n, vi_tri_y_so_khong_n + delta_y_n
            if 0 <= vi_tri_x_moi_n < 3 and 0 <= vi_tri_y_moi_n < 3:
                trang_thai_moi_puzzle_n = copy.deepcopy(trang_thai_hien_tai_puzzle_n)
                trang_thai_moi_puzzle_n[vi_tri_x_so_khong_n][vi_tri_y_so_khong_n], trang_thai_moi_puzzle_n[vi_tri_x_moi_n][vi_tri_y_moi_n] = trang_thai_moi_puzzle_n[vi_tri_x_moi_n][vi_tri_y_moi_n], trang_thai_moi_puzzle_n[vi_tri_x_so_khong_n][vi_tri_y_so_khong_n]
                khoa_trang_thai_moi_n = tuple(map(tuple, trang_thai_moi_puzzle_n))
                if khoa_trang_thai_moi_n not in self.cac_trang_thai_da_tham_n:
                    self.ngan_xep_trang_thai_n.append((trang_thai_moi_puzzle_n, duong_di_puzzle_n + [trang_thai_moi_puzzle_n]))
        
        self.nhan_trang_thai.setText(f"Đang duyệt {len(self.cac_trang_thai_da_tham_n)} trạng thái...")


    def thuc_hien_tu_dong_chay(self):
        self.bo_hen_gio_n.start(500)

if __name__ == "__main__":
    ung_dung_chay_n = QApplication(sys.argv)
    cua_so_n = UngDungPuzzleN()
    cua_so_n.show()
    sys.exit(ung_dung_chay_n.exec())