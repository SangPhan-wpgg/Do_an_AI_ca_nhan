from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow
from tkinter import messagebox
import time
import random
from collections import deque
from copy import deepcopy
from dataStructures import NutTimKiem, DanhSachMo, DanhSachDong
import os

CHIEU_RONG_CUA_SO_MAC_DINH = 840 
CHIEU_CAO_CUA_SO_MAC_DINH = 611 
DUONG_DAN_THU_MUC_HIEN_TAI = os.path.dirname(__file__) 

tuple_trang_thai_dich_csp_module = None
cac_muc_da_tham_csp_module = []
duong_di_giai_phap_csp_module = None

def la_trang_thai_dich_cho_csp(trang_thai:tuple) -> bool:
    global tuple_trang_thai_dich_csp_module
    return trang_thai == tuple_trang_thai_dich_csp_module

def in_trang_thai_ra_console_cho_csp(trang_thai):
    for i in range(0, 9, 3):
        print(trang_thai[i], trang_thai[i+1], trang_thai[i+2])
    print("-" * 10)                         

def ghi_giai_phap_csp_ra_file(giai_phap_csp):
    global cac_muc_da_tham_csp_module
    with open(DUONG_DAN_THU_MUC_HIEN_TAI + "/ket_qua_csp.txt", "w", encoding="utf-8") as tep_ghi:
        tep_ghi.write("Giải pháp CSP: ")
        if giai_phap_csp is None:
            tep_ghi.write("\nKhông có giải pháp")
        else:
            if isinstance(giai_phap_csp, dict):
                for bien_csp, gia_tri_csp in giai_phap_csp.items():
                    tep_ghi.write(f"\n{bien_csp}: {gia_tri_csp}")
            elif isinstance(giai_phap_csp, list):
                 for trang_thai_trong_giai_phap in giai_phap_csp:
                      tep_ghi.write(f"\n{trang_thai_trong_giai_phap}")
        
        tep_ghi.write("\nCác mục đã duyệt (trạng thái hoặc bước gán): ")
        if not cac_muc_da_tham_csp_module:
            tep_ghi.write("\nKhông có")
        else:
            for muc_da_duyet in cac_muc_da_tham_csp_module:
                tep_ghi.write(f"\n{muc_da_duyet}")
        messagebox.showinfo("Thông tin", "Ghi vào file thành công")

def kiem_tra_vi_pham_rang_buoc_csp(trang_thai_tuple_csp):
    if not all(0 <= phan_tu_trong_tuple <= 8 for phan_tu_trong_tuple in trang_thai_tuple_csp):
        return True
    if len(set(trang_thai_tuple_csp)) != 9:
        return True
    return False

def tao_trang_thai_ngau_nhien_cho_csp():      
    return tuple(random.randint(0, 8) for _ in range(9))      

def kiem_tra_rang_buoc_khac_biet_csp(x_csp: int, y_csp: int):
    return x_csp != y_csp

def chay_thuat_toan_ac3_cho_csp(cac_mien_gt_hien_tai_ac3, cac_bien_ke_can_ac3):
    hang_doi_cung_cho_ac3 = deque([(b_i, b_j) for b_i in cac_mien_gt_hien_tai_ac3 for b_j in cac_bien_ke_can_ac3[b_i]])
    while hang_doi_cung_cho_ac3:
        b_i, b_j = hang_doi_cung_cho_ac3.popleft()
        if dieu_chinh_mien_gt_cho_ac3(cac_mien_gt_hien_tai_ac3, b_i, b_j):
            if not cac_mien_gt_hien_tai_ac3[b_i]:
                return False
            for b_k in cac_bien_ke_can_ac3[b_i]:
                if b_k != b_j:
                    hang_doi_cung_cho_ac3.append((b_k, b_i))
    return True

def dieu_chinh_mien_gt_cho_ac3(cac_mien_gt_hien_tai_ac3: dict, b_i, b_j):
    da_thuc_hien_dieu_chinh_mien = False
    for gia_tri_x_ac3 in cac_mien_gt_hien_tai_ac3[b_i][:]:
        if all(not kiem_tra_rang_buoc_khac_biet_csp(gia_tri_x_ac3, gia_tri_y_ac3) for gia_tri_y_ac3 in cac_mien_gt_hien_tai_ac3[b_j]):
            cac_mien_gt_hien_tai_ac3[b_i].remove(gia_tri_x_ac3)
            da_thuc_hien_dieu_chinh_mien = True
    return da_thuc_hien_dieu_chinh_mien

def dinh_dang_mien_gia_tri_thanh_chuoi(cac_mien_gt_hien_tai_dd: dict):
    chuoi_ket_qua_dinh_dang = ""
    for bien_dd, mien_gt_dd in cac_mien_gt_hien_tai_dd.items():
        chuoi_ket_qua_dinh_dang += f"{bien_dd}: {mien_gt_dd}" + "\n"
    return chuoi_ket_qua_dinh_dang

cac_mien_gia_tri_csp_toan_cuc_cua_module = {}

class UngDungBaiToanThoaManRangBuoc(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(DUONG_DAN_THU_MUC_HIEN_TAI + "/constrainSatisfactionProblemGUI.ui", self)
        self.setFixedSize(CHIEU_RONG_CUA_SO_MAC_DINH, CHIEU_CAO_CUA_SO_MAC_DINH)
        self.btnSolve.clicked.connect(self.thuc_hien_giai_csp)
        self.cbbAlgorithm.addItems(["Backtracking", "Thử nghiệm ngẫu nhiên", "AC3 + Backtracking"])
        self.cbbAlgorithm.setCurrentText("Backtracking")
        self.txtSolveSpeedPerStep.setPlainText("1")
        self.toc_do_hien_thi_moi_buoc_ms_csp = 1000
        self.btnWriteToFile.clicked.connect(lambda: ghi_giai_phap_csp_ra_file(duong_di_giai_phap_csp_module))
    
    def cap_nhat_o_hien_thi_ket_qua_csp(self, widget_o_hien_thi, gia_tri_hien_thi):
        if gia_tri_hien_thi == -1:
            widget_o_hien_thi.setPlainText(" ")
        else:
            widget_o_hien_thi.setPlainText(str(gia_tri_hien_thi))
        
    def thuc_hien_giai_csp(self):
        global duong_di_giai_phap_csp_module, cac_muc_da_tham_csp_module, cac_mien_gia_tri_csp_toan_cuc_cua_module
        
        duong_di_giai_phap_csp_module = [] 
        cac_muc_da_tham_csp_module = []    
        
        loai_thuat_toan_duoc_chon_csp = self.cbbAlgorithm.currentText()
        
        danh_sach_bien_cho_csp = []
        for chi_so_i in range(1, 10):
            danh_sach_bien_cho_csp.append(f'X{chi_so_i}')

        cac_mien_gia_tri_csp_toan_cuc_cua_module.clear()
        danh_sach_gia_tri_min_moi_bien_csp = [
            self.spinBox_minX1.value(), self.spinBox_minX2.value(), self.spinBox_minX3.value(),
            self.spinBox_minX4.value(), self.spinBox_minX5.value(), self.spinBox_minX6.value(),
            self.spinBox_minX7.value(), self.spinBox_minX8.value(), self.spinBox_minX9.value()
        ]
        danh_sach_gia_tri_max_moi_bien_csp = [
            self.spinBox_maxX1.value(), self.spinBox_maxX2.value(), self.spinBox_maxX3.value(),
            self.spinBox_maxX4.value(), self.spinBox_maxX5.value(), self.spinBox_maxX6.value(),
            self.spinBox_maxX7.value(), self.spinBox_maxX8.value(), self.spinBox_maxX9.value()
        ]
        chi_so_bien_de_gan_mien = 0
        for bien_trong_danh_sach in danh_sach_bien_cho_csp:
            cac_mien_gia_tri_csp_toan_cuc_cua_module[bien_trong_danh_sach] = list(range(danh_sach_gia_tri_min_moi_bien_csp[chi_so_bien_de_gan_mien], danh_sach_gia_tri_max_moi_bien_csp[chi_so_bien_de_gan_mien] + 1))
            chi_so_bien_de_gan_mien += 1
        
        cac_bien_ke_can_cho_csp = { }
        for bien_trong_danh_sach in danh_sach_bien_cho_csp:
            cac_bien_ke_can_cho_csp[bien_trong_danh_sach] = [bien_v for bien_v in danh_sach_bien_cho_csp if bien_v != bien_trong_danh_sach]

        danh_sach_so_lan_thu_gan_csp = [0]
        
        def chon_bien_chua_duoc_gan_csp(ds_bien_csp, phep_gan_csp_ht):
            for b_duyet in ds_bien_csp:
                if b_duyet not in phep_gan_csp_ht:
                    return b_duyet
            return None 
            
        def kiem_tra_tinh_nhat_quan_cua_phep_gan_csp(gt_kiem_tra:int, phep_gan_csp_ht: dict) -> bool:
            for b_khac_trong_phep_gan in phep_gan_csp_ht:
                if phep_gan_csp_ht[b_khac_trong_phep_gan] == gt_kiem_tra:
                    return False
            return True
            
        def chuyen_doi_phep_gan_sang_trang_thai_csp(phep_gan_csp_ht: dict) -> tuple:
            trang_thai_tu_phep_gan_csp = [-1] * 9
            for b_trong_phep_gan, gt_b in phep_gan_csp_ht.items():
                chi_so_tt_csp = int(b_trong_phep_gan.strip("X"))
                trang_thai_tu_phep_gan_csp[chi_so_tt_csp - 1] = gt_b
            return tuple(trang_thai_tu_phep_gan_csp)
            
        def thuc_hien_tim_kiem_quay_lui_csp(phep_gan_hien_tai_cua_bt, so_lan_thu_gan_cua_bt: list):
            global cac_muc_da_tham_csp_module
            if len(phep_gan_hien_tai_cua_bt) == len(danh_sach_bien_cho_csp):
                return phep_gan_hien_tai_cua_bt
            
            bien_can_gan_cho_bt = chon_bien_chua_duoc_gan_csp(danh_sach_bien_cho_csp, phep_gan_hien_tai_cua_bt)
            if bien_can_gan_cho_bt is None: 
                return None 

            for gia_tri_de_thu_gan_bt in cac_mien_gia_tri_csp_toan_cuc_cua_module[bien_can_gan_cho_bt]:
                so_lan_thu_gan_cua_bt[0] += 1
                if kiem_tra_tinh_nhat_quan_cua_phep_gan_csp(gia_tri_de_thu_gan_bt, phep_gan_hien_tai_cua_bt):
                    phep_gan_hien_tai_cua_bt[bien_can_gan_cho_bt] = gia_tri_de_thu_gan_bt
                    cac_muc_da_tham_csp_module.append(chuyen_doi_phep_gan_sang_trang_thai_csp(deepcopy(phep_gan_hien_tai_cua_bt)))
                    ket_qua_de_quy_bt = thuc_hien_tim_kiem_quay_lui_csp(phep_gan_hien_tai_cua_bt, so_lan_thu_gan_cua_bt)
                    if ket_qua_de_quy_bt:
                        return ket_qua_de_quy_bt
                    del phep_gan_hien_tai_cua_bt[bien_can_gan_cho_bt]
                    cac_muc_da_tham_csp_module.append(chuyen_doi_phep_gan_sang_trang_thai_csp(deepcopy(phep_gan_hien_tai_cua_bt)))
            return [] 
            
        def thuc_hien_tim_kiem_thu_nghiem_ngau_nhien_csp():
            global cac_muc_da_tham_csp_module
            duong_di_tim_duoc_tu_thu_nghiem = []
            trang_thai_moi_khi_thu_nghiem = tuple([-1]*9)
            so_lan_lap_toi_da_thu_nghiem = 100000 
            dem_lap_thu_nghiem = 0
            while kiem_tra_vi_pham_rang_buoc_csp(trang_thai_moi_khi_thu_nghiem) and dem_lap_thu_nghiem < so_lan_lap_toi_da_thu_nghiem:
                trang_thai_moi_khi_thu_nghiem = tao_trang_thai_ngau_nhien_cho_csp()
                duong_di_tim_duoc_tu_thu_nghiem.append(trang_thai_moi_khi_thu_nghiem)
                dem_lap_thu_nghiem +=1
                if not kiem_tra_vi_pham_rang_buoc_csp(trang_thai_moi_khi_thu_nghiem):
                    cac_muc_da_tham_csp_module = duong_di_tim_duoc_tu_thu_nghiem[:]
                    return duong_di_tim_duoc_tu_thu_nghiem 
            cac_muc_da_tham_csp_module = duong_di_tim_duoc_tu_thu_nghiem[:]
            return [] 
            
        thoi_gian_bat_dau_xu_ly_csp = time.perf_counter()       
        try:
            if int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000) >= 1:
                self.toc_do_hien_thi_moi_buoc_ms_csp  = int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000)
            else:
                messagebox.showerror("Lỗi", "Tốc độ mỗi bước phải lớn hơn hoặc bằng 0.001s")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Tốc độ mỗi bước không hợp lệ")
            return
            
        duong_di_giai_phap_csp_module = [] 
        if loai_thuat_toan_duoc_chon_csp == "Thử nghiệm ngẫu nhiên":
            duong_di_giai_phap_csp_module = thuc_hien_tim_kiem_thu_nghiem_ngau_nhien_csp()
            danh_sach_so_lan_thu_gan_csp[0] = len(duong_di_giai_phap_csp_module) if duong_di_giai_phap_csp_module else 0
        elif loai_thuat_toan_duoc_chon_csp == "AC3 + Backtracking":
            if not chay_thuat_toan_ac3_cho_csp(cac_mien_gia_tri_csp_toan_cuc_cua_module, cac_bien_ke_can_cho_csp):
                messagebox.showerror("Lỗi", "Tìm thấy sự không nhất quán sau AC3. Không có giải pháp.")
                duong_di_giai_phap_csp_module = []
            else:
                duong_di_giai_phap_csp_module = thuc_hien_tim_kiem_quay_lui_csp({}, danh_sach_so_lan_thu_gan_csp)
        else:           
            duong_di_giai_phap_csp_module = thuc_hien_tim_kiem_quay_lui_csp({}, danh_sach_so_lan_thu_gan_csp)
            
        thoi_gian_ket_thuc_xu_ly_csp = time.perf_counter()
        thoi_gian_thuc_thi_cua_csp = thoi_gian_ket_thuc_xu_ly_csp - thoi_gian_bat_dau_xu_ly_csp
        self.txtSolveTime.setPlainText(f"{thoi_gian_thuc_thi_cua_csp:.10f}(s)")
        
        if not duong_di_giai_phap_csp_module:
            messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")
            self.txtTotalStep.setPlainText("0")
            self.txtStep.setPlainText("0")
        else:         
            self.chay_hien_thi_giai_phap_csp(cac_muc_da_tham_csp_module)        
            self.txtTotalStep.setPlainText(str(len(cac_muc_da_tham_csp_module)))
            
        self.output_domain.setPlainText(dinh_dang_mien_gia_tri_thanh_chuoi(cac_mien_gia_tri_csp_toan_cuc_cua_module))
                
    def chay_hien_thi_giai_phap_csp(self, danh_sach_buoc_de_chay_csp):
        self.buoc_hien_tai_khi_chay_csp = 0
        self.bo_hen_gio_hien_thi_csp = QtCore.QTimer()
        self.bo_hen_gio_hien_thi_csp.timeout.connect(self.cap_nhat_buoc_hien_thi_csp)
        self.giai_phap_dang_duoc_chay_hien_thi_csp = danh_sach_buoc_de_chay_csp
        self.bo_hen_gio_hien_thi_csp.start(self.toc_do_hien_thi_moi_buoc_ms_csp)

    def cap_nhat_buoc_hien_thi_csp(self):
        if self.buoc_hien_tai_khi_chay_csp < len(self.giai_phap_dang_duoc_chay_hien_thi_csp):
            trang_thai_cua_buoc_hien_thi_csp = self.giai_phap_dang_duoc_chay_hien_thi_csp[self.buoc_hien_tai_khi_chay_csp]
            self.buoc_hien_tai_khi_chay_csp += 1
            self.txtStep.setPlainText(str(self.buoc_hien_tai_khi_chay_csp))
            if isinstance(trang_thai_cua_buoc_hien_thi_csp, tuple) and len(trang_thai_cua_buoc_hien_thi_csp) == 9:
                self.cap_nhat_o_hien_thi_ket_qua_csp(self.cell1_3, trang_thai_cua_buoc_hien_thi_csp[0])
                self.cap_nhat_o_hien_thi_ket_qua_csp(self.cell2_3, trang_thai_cua_buoc_hien_thi_csp[1])
                self.cap_nhat_o_hien_thi_ket_qua_csp(self.cell3_3, trang_thai_cua_buoc_hien_thi_csp[2])
                self.cap_nhat_o_hien_thi_ket_qua_csp(self.cell4_3, trang_thai_cua_buoc_hien_thi_csp[3])
                self.cap_nhat_o_hien_thi_ket_qua_csp(self.cell5_3, trang_thai_cua_buoc_hien_thi_csp[4])
                self.cap_nhat_o_hien_thi_ket_qua_csp(self.cell6_3, trang_thai_cua_buoc_hien_thi_csp[5])
                self.cap_nhat_o_hien_thi_ket_qua_csp(self.cell7_3, trang_thai_cua_buoc_hien_thi_csp[6])
                self.cap_nhat_o_hien_thi_ket_qua_csp(self.cell8_3, trang_thai_cua_buoc_hien_thi_csp[7])
                self.cap_nhat_o_hien_thi_ket_qua_csp(self.cell9_3, trang_thai_cua_buoc_hien_thi_csp[8])
        else:
            self.bo_hen_gio_hien_thi_csp.stop()
                
ung_dung_qt_cho_csp = QApplication([])
cua_so_chinh_cho_csp = UngDungBaiToanThoaManRangBuoc()
cua_so_chinh_cho_csp.show()
ung_dung_qt_cho_csp.exec()