from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow
from tkinter import messagebox 
import time
import random
import math
from dataStructures import * 
import os

CHIEU_RONG_CUA_SO_MAC_DINH = 840 
CHIEU_CAO_CUA_SO_MAC_DINH = 611 
DUONG_DAN_THU_MUC_HIEN_TAI = os.path.dirname(__file__) 

tuple_trang_thai_bat_dau = tuple([0,0,0,0,0,0,0,0,0]) 
tuple_trang_thai_ket_thuc = tuple([0,0,0,0,0,0,0,0,0]) 
duong_di_ket_qua = None 

def la_trang_thai_dich(trang_thai): 
    return trang_thai == tuple_trang_thai_ket_thuc

def tim_vi_tri_o_trong(trang_thai):
    chi_so = trang_thai.index(0) 
    return chi_so // 3, chi_so % 3

def di_chuyen(trang_thai, huong): 
    hang, cot = tim_vi_tri_o_trong(trang_thai)
    chi_so_o_trong = hang * 3 + cot 
    trang_thai_moi_list = list(trang_thai)

    if huong == 'up' and hang > 0:
        chi_so_hoan_doi = (hang - 1) * 3 + cot 
    elif huong == 'down' and hang < 2:
        chi_so_hoan_doi = (hang + 1) * 3 + cot
    elif huong == 'left' and cot > 0:
        chi_so_hoan_doi = hang * 3 + (cot - 1)
    elif huong == 'right' and cot < 2:
        chi_so_hoan_doi = hang * 3 + (cot + 1)
    else:
        return trang_thai 

    trang_thai_moi_list[chi_so_o_trong], trang_thai_moi_list[chi_so_hoan_doi] = trang_thai_moi_list[chi_so_hoan_doi], trang_thai_moi_list[chi_so_o_trong]
    return tuple(trang_thai_moi_list)

def cac_hanh_dong_hop_le(trang_thai): 
    hang, cot = tim_vi_tri_o_trong(trang_thai) 
    cac_huong_di_chuyen = [] 
    if hang > 0: cac_huong_di_chuyen.append('up')
    if hang < 2: cac_huong_di_chuyen.append('down')
    if cot > 0: cac_huong_di_chuyen.append('left')
    if cot < 2: cac_huong_di_chuyen.append('right')
    return cac_huong_di_chuyen

def cac_trang_thai_ket_qua(trang_thai, hanh_dong):
    ket_qua = [di_chuyen(trang_thai, hanh_dong)]
    if random.random() < 0.5:
        ket_qua.append(trang_thai)  
    return ket_qua

def TIM_KIEM_AND_OR(bai_toan):
    bo_nho_trung_gian = {} 
    return TIM_KIEM_OR(bai_toan['initial'], bai_toan, [], 0, bo_nho_trung_gian)

def TIM_KIEM_OR(trang_thai, bai_toan, duong_di_hien_tai, do_sau, bo_nho_trung_gian):
    if la_trang_thai_dich(trang_thai):
        return []
    if trang_thai in duong_di_hien_tai:
        return 'that_bai' 
    if do_sau > CHIEU_RONG_CUA_SO_MAC_DINH:
        return 'that_bai'
    if trang_thai in bo_nho_trung_gian:
        return bo_nho_trung_gian[trang_thai]

    for hanh_dong_hien_tai in cac_hanh_dong_hop_le(trang_thai):
        cac_trang_thai_con = cac_trang_thai_ket_qua(trang_thai, hanh_dong_hien_tai) 
        ke_hoach_con = TIM_KIEM_AND(cac_trang_thai_con, bai_toan, duong_di_hien_tai + [trang_thai], do_sau + 1, bo_nho_trung_gian) 
        if ke_hoach_con != 'that_bai':
            ke_hoach_day_du = [hanh_dong_hien_tai, ke_hoach_con] 
            bo_nho_trung_gian[trang_thai] = ke_hoach_day_du
            return ke_hoach_day_du
    bo_nho_trung_gian[trang_thai] = 'that_bai'
    return 'that_bai'

def TIM_KIEM_AND(danh_sach_trang_thai, bai_toan, duong_di_hien_tai, do_sau, bo_nho_trung_gian): 
    danh_sach_ke_hoach = [] 
    for trang_thai_con in danh_sach_trang_thai: 
        ke_hoach_cho_trang_thai_con = TIM_KIEM_OR(trang_thai_con, bai_toan, duong_di_hien_tai, do_sau + 1, bo_nho_trung_gian) 
        if ke_hoach_cho_trang_thai_con == 'that_bai':
            return 'that_bai'
        danh_sach_ke_hoach.append(ke_hoach_cho_trang_thai_con)
    return danh_sach_ke_hoach

def in_cay_ke_hoach(ke_hoach, khoang_cach_thut_le=0): 
    if ke_hoach == 'that_bai':
        print(' ' * khoang_cach_thut_le + 'thất bại')
    elif ke_hoach == []:
        print(' ' * khoang_cach_thut_le + 'ĐÍCH')
    elif isinstance(ke_hoach, list):
        hanh_dong = ke_hoach[0]
        ke_hoach_con_tong_hop = ke_hoach[1] 
        print(' ' * khoang_cach_thut_le + f'-> {hanh_dong}')
        if isinstance(ke_hoach_con_tong_hop, list): 
            for ke_hoach_con_don in ke_hoach_con_tong_hop:
                in_cay_ke_hoach(ke_hoach_con_don, khoang_cach_thut_le + 4)
        else: 
             in_cay_ke_hoach(ke_hoach_con_tong_hop, khoang_cach_thut_le + 4)
    else:
        print(' ' * khoang_cach_thut_le + str(ke_hoach))

def in_trang_thai_ra_console(trang_thai): 
    for i in range(0, 9, 3):
        print(trang_thai[i], trang_thai[i+1], trang_thai[i+2])
    print("-" * 10)

def ghi_duong_di_vao_file(giai_phap): 
    with open( DUONG_DAN_THU_MUC_HIEN_TAI + "/ket_qua.txt", "w", encoding="utf-8") as tep: 
        tep.write("Giải pháp: ")
        if giai_phap is None: 
            tep.write("\nKhông có giải pháp")
        else:
            for trang_thai_trong_duong_di in giai_phap: 
                tep.write(f"\n{trang_thai_trong_duong_di}")
        messagebox.showinfo("Thông tin", "Ghi vào file thành công")

def trich_xuat_chuoi_trang_thai(ke_hoach, trang_thai_hien_tai): 
    if ke_hoach == 'that_bai' or ke_hoach == []:
        return [trang_thai_hien_tai]
    
    chuoi_trang_thai = [trang_thai_hien_tai] 
    if isinstance(ke_hoach, list):
        hanh_dong = ke_hoach[0]
        cac_ke_hoach_con = ke_hoach[1] 
        trang_thai_sau_hanh_dong_duoc_chon = None
        for trang_thai_ket_qua_tiem_nang in cac_trang_thai_ket_qua(trang_thai_hien_tai, hanh_dong):
            if trang_thai_ket_qua_tiem_nang != trang_thai_hien_tai:
                trang_thai_sau_hanh_dong_duoc_chon = trang_thai_ket_qua_tiem_nang
                break
        if trang_thai_sau_hanh_dong_duoc_chon is None: 
            trang_thai_sau_hanh_dong_duoc_chon = trang_thai_hien_tai

        if isinstance(cac_ke_hoach_con, list) and all(isinstance(kh_con, list) for kh_con in cac_ke_hoach_con):
            if cac_ke_hoach_con: 
                 chuoi_trang_thai += trich_xuat_chuoi_trang_thai(cac_ke_hoach_con[0], trang_thai_sau_hanh_dong_duoc_chon)
        else:
            chuoi_trang_thai += trich_xuat_chuoi_trang_thai(cac_ke_hoach_con, trang_thai_sau_hanh_dong_duoc_chon)
            
    return chuoi_trang_thai


class UngDungTimKiemANDOR(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi( DUONG_DAN_THU_MUC_HIEN_TAI + "/AND_OR_graph_search_GUI.ui", self) 
        self.setFixedSize(CHIEU_RONG_CUA_SO_MAC_DINH, CHIEU_CAO_CUA_SO_MAC_DINH)
        self.btnRandomInput.clicked.connect(self.nhap_lieu_ngau_nhien)    
        self.btnSolve.clicked.connect(self.xu_ly_nhan_nut_giai) 
        self.txtSolveSpeedPerStep.setPlainText("1") 
        self.toc_do_moi_buoc_ms = 1000 
        self.btnWriteToFile.clicked.connect(lambda: ghi_duong_di_vao_file(duong_di_ket_qua)) 
        self.txt_plan_tree.setReadOnly(True) 

    def nhap_lieu_ngau_nhien(self): 
        global tuple_trang_thai_bat_dau, tuple_trang_thai_ket_thuc
        cac_so_ngau_nhien = random.sample(range(9), 9)
        tuple_trang_thai_bat_dau = tuple(cac_so_ngau_nhien)
        self.cell1.setPlainText(str(tuple_trang_thai_bat_dau[0]))
        self.cell2.setPlainText(str(tuple_trang_thai_bat_dau[1]))
        self.cell3.setPlainText(str(tuple_trang_thai_bat_dau[2]))
        self.cell4.setPlainText(str(tuple_trang_thai_bat_dau[3]))
        self.cell5.setPlainText(str(tuple_trang_thai_bat_dau[4]))
        self.cell6.setPlainText(str(tuple_trang_thai_bat_dau[5]))
        self.cell7.setPlainText(str(tuple_trang_thai_bat_dau[6]))
        self.cell8.setPlainText(str(tuple_trang_thai_bat_dau[7]))
        self.cell9.setPlainText(str(tuple_trang_thai_bat_dau[8]))
        
        cac_so_ngau_nhien = random.sample(range(9), 9)
        tuple_trang_thai_ket_thuc = tuple(cac_so_ngau_nhien)
        self.cell1_end.setPlainText(str(tuple_trang_thai_ket_thuc[0]))
        self.cell2_end.setPlainText(str(tuple_trang_thai_ket_thuc[1]))
        self.cell3_end.setPlainText(str(tuple_trang_thai_ket_thuc[2]))
        self.cell4_end.setPlainText(str(tuple_trang_thai_ket_thuc[3]))
        self.cell5_end.setPlainText(str(tuple_trang_thai_ket_thuc[4]))
        self.cell6_end.setPlainText(str(tuple_trang_thai_ket_thuc[5]))
        self.cell7_end.setPlainText(str(tuple_trang_thai_ket_thuc[6]))
        self.cell8_end.setPlainText(str(tuple_trang_thai_ket_thuc[7]))
        self.cell9_end.setPlainText(str(tuple_trang_thai_ket_thuc[8]))

    def dinh_dang_chuoi_cay_ke_hoach(self, ke_hoach, khoang_cach_thut_le=0): 
        if ke_hoach == 'that_bai':
            return ' ' * khoang_cach_thut_le + 'thất bại\n'
        elif ke_hoach == []:
            return ' ' * khoang_cach_thut_le + 'ĐÍCH\n'
        elif isinstance(ke_hoach, list):
            hanh_dong = ke_hoach[0]
            ke_hoach_con_tong_hop = ke_hoach[1]
            chuoi_ket_qua = ' ' * khoang_cach_thut_le + f'→ {hanh_dong}\n' 
            if isinstance(ke_hoach_con_tong_hop, list):
                for ke_hoach_con_don in ke_hoach_con_tong_hop: # sp
                    chuoi_ket_qua += self.dinh_dang_chuoi_cay_ke_hoach(ke_hoach_con_don, khoang_cach_thut_le + 4)
            else:
                chuoi_ket_qua += self.dinh_dang_chuoi_cay_ke_hoach(ke_hoach_con_tong_hop, khoang_cach_thut_le + 4)
            return chuoi_ket_qua
        else:
            return ' ' * khoang_cach_thut_le + str(ke_hoach) + '\n'

    def xu_ly_nhan_nut_giai(self): 
        thoi_gian_bat_dau = time.time() 
        global tuple_trang_thai_bat_dau, tuple_trang_thai_ket_thuc, duong_di_ket_qua
        
        try:
            tuple_trang_thai_bat_dau = tuple([
                int(self.cell1.toPlainText()), int(self.cell2.toPlainText()), int(self.cell3.toPlainText()),
                int(self.cell4.toPlainText()), int(self.cell5.toPlainText()), int(self.cell6.toPlainText()),
                int(self.cell7.toPlainText()), int(self.cell8.toPlainText()), int(self.cell9.toPlainText())]
            )
            tuple_trang_thai_ket_thuc = tuple([
                int(self.cell1_end.toPlainText()), int(self.cell2_end.toPlainText()), int(self.cell3_end.toPlainText()),
                int(self.cell4_end.toPlainText()), int(self.cell5_end.toPlainText()), int(self.cell6_end.toPlainText()),
                int(self.cell7_end.toPlainText()), int(self.cell8_end.toPlainText()), int(self.cell9_end.toPlainText())]
            )
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị nhập vào không hợp lệ!")
            return
        
        try:

            if int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000) >= 1: #ms
                self.toc_do_moi_buoc_ms = int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000)
            else:
                messagebox.showerror("Lỗi", "Tốc độ mỗi bước phải lớn hơn hoặc bằng 0.001s") 
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Tốc độ mỗi bước không hợp lệ")
            return

        bai_toan_hien_tai = {'initial': tuple_trang_thai_bat_dau} 
        ke_hoach_tim_duoc = TIM_KIEM_AND_OR(bai_toan_hien_tai) 
        
        print("Trạng thái bắt đầu:", tuple_trang_thai_bat_dau) 
        print("Trạng thái kết thúc:", tuple_trang_thai_ket_thuc)
        print("Kế hoạch tìm được:", ke_hoach_tim_duoc)
                   
        if ke_hoach_tim_duoc == 'that_bai':
            messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")
            self.txtTotalStep.setPlainText("0") 
            self.txtStep.setPlainText("0")         
        else:          
            duong_di_ket_qua = trich_xuat_chuoi_trang_thai(ke_hoach_tim_duoc, tuple_trang_thai_bat_dau) 
            print("Đường đi kết quả:", duong_di_ket_qua) 
            self.chay_giai_phap(duong_di_ket_qua) 
            self.txtTotalStep.setPlainText(str(len(duong_di_ket_qua))) 
        
        thoi_gian_ket_thuc = time.time() 
        thoi_gian_thuc_thi = thoi_gian_ket_thuc - thoi_gian_bat_dau 
        self.txtSolveTime.setPlainText(f"{thoi_gian_thuc_thi:.9f}(s)")
        self.txt_plan_tree.setPlainText(self.dinh_dang_chuoi_cay_ke_hoach(ke_hoach_tim_duoc)) 

    def chay_giai_phap(self, giai_phap_de_chay): 
        self.buoc_hien_tai = 0 
        self.bo_hen_gio = QtCore.QTimer() 
        self.bo_hen_gio.timeout.connect(self.cap_nhat_buoc_chay) 
        self.giai_phap_dang_chay = giai_phap_de_chay
        self.bo_hen_gio.start(self.toc_do_moi_buoc_ms)
        
    def cap_nhat_o_hien_thi(self, widget_o, gia_tri): 
        if gia_tri == 0:
            widget_o.setPlainText(" ")
        else:
            widget_o.setPlainText(str(gia_tri))
            
    def cap_nhat_buoc_chay(self): 
        if self.buoc_hien_tai < len(self.giai_phap_dang_chay):
            trang_thai_buoc = self.giai_phap_dang_chay[self.buoc_hien_tai] # e
            self.buoc_hien_tai += 1
            self.txtStep.setPlainText(str(self.buoc_hien_tai))
            self.cap_nhat_o_hien_thi(self.cell1_3, trang_thai_buoc[0])
            self.cap_nhat_o_hien_thi(self.cell2_3, trang_thai_buoc[1])
            self.cap_nhat_o_hien_thi(self.cell3_3, trang_thai_buoc[2])
            self.cap_nhat_o_hien_thi(self.cell4_3, trang_thai_buoc[3])
            self.cap_nhat_o_hien_thi(self.cell5_3, trang_thai_buoc[4])
            self.cap_nhat_o_hien_thi(self.cell6_3, trang_thai_buoc[5])
            self.cap_nhat_o_hien_thi(self.cell7_3, trang_thai_buoc[6])
            self.cap_nhat_o_hien_thi(self.cell8_3, trang_thai_buoc[7])
            self.cap_nhat_o_hien_thi(self.cell9_3, trang_thai_buoc[8])
        else:
            self.bo_hen_gio.stop()

    def tai_gia_tri_tu_o_nhap(self): 
        global tuple_trang_thai_bat_dau, tuple_trang_thai_ket_thuc 
        try:
            tuple_trang_thai_bat_dau = tuple([
                int(self.cell1.toPlainText()), int(self.cell2.toPlainText()), int(self.cell3.toPlainText()),
                int(self.cell4.toPlainText()), int(self.cell5.toPlainText()), int(self.cell6.toPlainText()),
                int(self.cell7.toPlainText()), int(self.cell8.toPlainText()), int(self.cell9.toPlainText())]
            )
            tuple_trang_thai_ket_thuc = tuple([
                int(self.cell1_end.toPlainText()), int(self.cell2_end.toPlainText()), int(self.cell3_end.toPlainText()),
                int(self.cell4_end.toPlainText()), int(self.cell5_end.toPlainText()), int(self.cell6_end.toPlainText()),
                int(self.cell7_end.toPlainText()), int(self.cell8_end.toPlainText()), int(self.cell9_end.toPlainText())]
            )
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị nhập vào không hợp lệ!") 
            return
        else: 
            messagebox.showinfo("Thông báo", "Tải giá trị thành công!") 
            return 

ung_dung_qt = QApplication([]) # app
cua_so_chinh = UngDungTimKiemANDOR() # window
cua_so_chinh.show()
ung_dung_qt.exec()