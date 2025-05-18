from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow
from tkinter import messagebox
import time
import random
from Cau_truc import *
from search_in_complex_environment import giai_tim_kiem_moi_truong_phuc_tap, CAC_BUOC_DI_CHUYEN_MTK as CAC_HANH_DONG_DI_CHUYEN_MT_PHUC_TAP

import os
DUONG_DAN_THU_MUC_HIEN_TAI = os.path.dirname(__file__) 

tuple_trang_thai_bat_dau_1 = tuple([0,0,0,0,0,0,0,0,0])
tuple_trang_thai_bat_dau_2 = tuple([0,0,0,0,0,0,0,0,0])
tuple_trang_thai_bat_dau_3 = tuple([0,0,0,0,0,0,0,0,0])
tuple_trang_thai_bat_dau_4 = tuple([0,0,0,0,0,0,0,0,0])

tuple_trang_thai_ket_thuc_1 = tuple([0,0,0,0,0,0,0,0,0])
tuple_trang_thai_ket_thuc_2 = tuple([0,0,0,0,0,0,0,0,0])
tuple_trang_thai_ket_thuc_3 = tuple([0,0,0,0,0,0,0,0,0])
tuple_trang_thai_ket_thuc_4 = tuple([0,0,0,0,0,0,0,0,0])

so_luong_trang_thai_da_mo = None

def in_trang_thai_ra_console(trang_thai):
    for i in range(0, 9, 3):
        print(trang_thai[i], trang_thai[i+1], trang_thai[i+2])
    print("-" * 10)

def ghi_chuoi_hanh_dong_vao_file(chuoi_hanh_dong):
    global so_luong_trang_thai_da_mo
    with open(DUONG_DAN_THU_MUC_HIEN_TAI + "/ket_qua_mt_phuc_tap.txt", "w", encoding="utf-8") as tep:
        tep.write("Chuỗi hành động giải pháp: ")
        if chuoi_hanh_dong is None:
            tep.write("\nKhông có giải pháp")
        else:
            tep.write(f"\n{chuoi_hanh_dong}")
        
        tep.write("\nSố lượng belief state đã mở: ")
        if so_luong_trang_thai_da_mo is None:
            tep.write("\nChưa có thông tin")
        else:
            tep.write(f"\n{so_luong_trang_thai_da_mo}")
        messagebox.showinfo("Thông tin", "Ghi vào file thành công")

def la_di_chuyen_hop_le(vi_tri_so_khong, huong):
    if huong == 'Up' and vi_tri_so_khong < 3:
        return False
    if huong == 'Down' and vi_tri_so_khong > 5:
        return False
    if huong == 'Left' and vi_tri_so_khong % 3 == 0:
        return False
    if huong == 'Right' and vi_tri_so_khong % 3 == 2:
        return False
    return True
        
def ap_dung_hanh_dong_cho_trang_thai(huong: str, trang_thai_hien_tai: tuple):
    vi_tri_so_khong = trang_thai_hien_tai.index(0)
    if la_di_chuyen_hop_le(vi_tri_so_khong, huong):
        do_doi_vi_tri = CAC_HANH_DONG_DI_CHUYEN_MT_PHUC_TAP[huong]
        trang_thai_hien_tai_list = list(trang_thai_hien_tai)
        trang_thai_hien_tai_list[vi_tri_so_khong], trang_thai_hien_tai_list[vi_tri_so_khong + do_doi_vi_tri] = \
            trang_thai_hien_tai_list[vi_tri_so_khong + do_doi_vi_tri], trang_thai_hien_tai_list[vi_tri_so_khong]
        return tuple(trang_thai_hien_tai_list)
    return trang_thai_hien_tai

def la_o_nhap_lieu_rong(bien_qplaintextedit) -> bool:
    return not bien_qplaintextedit.toPlainText().strip()

class UngDungMoiTruongPhucTap(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(DUONG_DAN_THU_MUC_HIEN_TAI + "/complex_environment_GUI.ui", self)
        
        self.btnRandomInput.clicked.connect(self.nhap_lieu_ngau_nhien)  
        self.cbbAlgorithm.addItems(["Tìm kiếm không quan sát", "Tìm kiếm quan sát một phần"])  
        self.btnSolve.clicked.connect(self.xu_ly_nhan_nut_giai)  
        self.txtSolveSpeedPerStep.setPlainText("1")  
        self.toc_do_moi_buoc_ms = 1000
        
        self.chuoi_hanh_dong_giai_phap = None 
        self.btnWriteToFile.clicked.connect(lambda: ghi_chuoi_hanh_dong_vao_file(self.chuoi_hanh_dong_giai_phap))  
        
        self.tap_trang_thai_niem_tin_hien_tai = []
        self.tap_trang_thai_dich_hien_tai = []
        self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau = []

    def nhap_lieu_ngau_nhien(self):
        global tuple_trang_thai_bat_dau_1, tuple_trang_thai_bat_dau_2, tuple_trang_thai_bat_dau_3, tuple_trang_thai_bat_dau_4
        global tuple_trang_thai_ket_thuc_1, tuple_trang_thai_ket_thuc_2, tuple_trang_thai_ket_thuc_3, tuple_trang_thai_ket_thuc_4
        
        cac_so_ngau_nhien = random.sample(range(9), 9)
        tuple_trang_thai_bat_dau_1 = tuple(cac_so_ngau_nhien)
        self.cell1_start1.setPlainText(str(tuple_trang_thai_bat_dau_1[0]))  
        self.cell2_start1.setPlainText(str(tuple_trang_thai_bat_dau_1[1]))  
        self.cell3_start1.setPlainText(str(tuple_trang_thai_bat_dau_1[2]))  
        self.cell4_start1.setPlainText(str(tuple_trang_thai_bat_dau_1[3]))  
        self.cell5_start1.setPlainText(str(tuple_trang_thai_bat_dau_1[4]))  
        self.cell6_start1.setPlainText(str(tuple_trang_thai_bat_dau_1[5]))  
        self.cell7_start1.setPlainText(str(tuple_trang_thai_bat_dau_1[6]))  
        self.cell8_start1.setPlainText(str(tuple_trang_thai_bat_dau_1[7]))  
        self.cell9_start1.setPlainText(str(tuple_trang_thai_bat_dau_1[8]))  
        
        cac_so_ngau_nhien = random.sample(range(9), 9)
        tuple_trang_thai_bat_dau_2 = tuple(cac_so_ngau_nhien)
        self.cell1_start2.setPlainText(str(tuple_trang_thai_bat_dau_2[0]))  
        self.cell2_start2.setPlainText(str(tuple_trang_thai_bat_dau_2[1]))  
        self.cell3_start2.setPlainText(str(tuple_trang_thai_bat_dau_2[2]))  
        self.cell4_start2.setPlainText(str(tuple_trang_thai_bat_dau_2[3]))  
        self.cell5_start2.setPlainText(str(tuple_trang_thai_bat_dau_2[4]))  
        self.cell6_start2.setPlainText(str(tuple_trang_thai_bat_dau_2[5]))  
        self.cell7_start2.setPlainText(str(tuple_trang_thai_bat_dau_2[6]))  
        self.cell8_start2.setPlainText(str(tuple_trang_thai_bat_dau_2[7]))  
        self.cell9_start2.setPlainText(str(tuple_trang_thai_bat_dau_2[8]))  
        
        cac_so_ngau_nhien = random.sample(range(9), 9)
        tuple_trang_thai_bat_dau_3 = tuple(cac_so_ngau_nhien)
        self.cell1_start3.setPlainText(str(tuple_trang_thai_bat_dau_3[0]))  
        self.cell2_start3.setPlainText(str(tuple_trang_thai_bat_dau_3[1]))  
        self.cell3_start3.setPlainText(str(tuple_trang_thai_bat_dau_3[2]))  
        self.cell4_start3.setPlainText(str(tuple_trang_thai_bat_dau_3[3]))  
        self.cell5_start3.setPlainText(str(tuple_trang_thai_bat_dau_3[4]))  
        self.cell6_start3.setPlainText(str(tuple_trang_thai_bat_dau_3[5]))  
        self.cell7_start3.setPlainText(str(tuple_trang_thai_bat_dau_3[6]))  
        self.cell8_start3.setPlainText(str(tuple_trang_thai_bat_dau_3[7]))  
        self.cell9_start3.setPlainText(str(tuple_trang_thai_bat_dau_3[8]))  
        
        cac_so_ngau_nhien = random.sample(range(9), 9)
        tuple_trang_thai_bat_dau_4 = tuple(cac_so_ngau_nhien)
        self.cell1_start4.setPlainText(str(tuple_trang_thai_bat_dau_4[0]))  
        self.cell2_start4.setPlainText(str(tuple_trang_thai_bat_dau_4[1]))  
        self.cell3_start4.setPlainText(str(tuple_trang_thai_bat_dau_4[2]))  
        self.cell4_start4.setPlainText(str(tuple_trang_thai_bat_dau_4[3]))  
        self.cell5_start4.setPlainText(str(tuple_trang_thai_bat_dau_4[4]))  
        self.cell6_start4.setPlainText(str(tuple_trang_thai_bat_dau_4[5]))  
        self.cell7_start4.setPlainText(str(tuple_trang_thai_bat_dau_4[6]))  
        self.cell8_start4.setPlainText(str(tuple_trang_thai_bat_dau_4[7]))  
        self.cell9_start4.setPlainText(str(tuple_trang_thai_bat_dau_4[8]))  
        
        cac_so_ngau_nhien = random.sample(range(9), 9)
        tuple_trang_thai_ket_thuc_1 = tuple(cac_so_ngau_nhien)
        self.cell1_end1.setPlainText(str(tuple_trang_thai_ket_thuc_1[0]))  
        self.cell2_end1.setPlainText(str(tuple_trang_thai_ket_thuc_1[1]))  
        self.cell3_end1.setPlainText(str(tuple_trang_thai_ket_thuc_1[2]))  
        self.cell4_end1.setPlainText(str(tuple_trang_thai_ket_thuc_1[3]))  
        self.cell5_end1.setPlainText(str(tuple_trang_thai_ket_thuc_1[4]))  
        self.cell6_end1.setPlainText(str(tuple_trang_thai_ket_thuc_1[5]))  
        self.cell7_end1.setPlainText(str(tuple_trang_thai_ket_thuc_1[6]))  
        self.cell8_end1.setPlainText(str(tuple_trang_thai_ket_thuc_1[7]))  
        self.cell9_end1.setPlainText(str(tuple_trang_thai_ket_thuc_1[8]))  
        
        cac_so_ngau_nhien = random.sample(range(9), 9)
        tuple_trang_thai_ket_thuc_2 = tuple(cac_so_ngau_nhien)
        self.cell1_end2.setPlainText(str(tuple_trang_thai_ket_thuc_2[0]))  
        self.cell2_end2.setPlainText(str(tuple_trang_thai_ket_thuc_2[1]))  
        self.cell3_end2.setPlainText(str(tuple_trang_thai_ket_thuc_2[2]))  
        self.cell4_end2.setPlainText(str(tuple_trang_thai_ket_thuc_2[3]))  
        self.cell5_end2.setPlainText(str(tuple_trang_thai_ket_thuc_2[4]))  
        self.cell6_end2.setPlainText(str(tuple_trang_thai_ket_thuc_2[5]))  
        self.cell7_end2.setPlainText(str(tuple_trang_thai_ket_thuc_2[6]))  
        self.cell8_end2.setPlainText(str(tuple_trang_thai_ket_thuc_2[7]))  
        self.cell9_end2.setPlainText(str(tuple_trang_thai_ket_thuc_2[8]))  

        cac_so_ngau_nhien = random.sample(range(9), 9)
        tuple_trang_thai_ket_thuc_3 = tuple(cac_so_ngau_nhien)
        self.cell1_end3.setPlainText(str(tuple_trang_thai_ket_thuc_3[0]))  
        self.cell2_end3.setPlainText(str(tuple_trang_thai_ket_thuc_3[1]))  
        self.cell3_end3.setPlainText(str(tuple_trang_thai_ket_thuc_3[2]))  
        self.cell4_end3.setPlainText(str(tuple_trang_thai_ket_thuc_3[3]))  
        self.cell5_end3.setPlainText(str(tuple_trang_thai_ket_thuc_3[4]))  
        self.cell6_end3.setPlainText(str(tuple_trang_thai_ket_thuc_3[5]))  
        self.cell7_end3.setPlainText(str(tuple_trang_thai_ket_thuc_3[6]))  
        self.cell8_end3.setPlainText(str(tuple_trang_thai_ket_thuc_3[7]))  
        self.cell9_end3.setPlainText(str(tuple_trang_thai_ket_thuc_3[8]))  

        cac_so_ngau_nhien = random.sample(range(9), 9)
        tuple_trang_thai_ket_thuc_4 = tuple(cac_so_ngau_nhien)
        self.cell1_end4.setPlainText(str(tuple_trang_thai_ket_thuc_4[0]))  
        self.cell2_end4.setPlainText(str(tuple_trang_thai_ket_thuc_4[1]))  
        self.cell3_end4.setPlainText(str(tuple_trang_thai_ket_thuc_4[2]))  
        self.cell4_end4.setPlainText(str(tuple_trang_thai_ket_thuc_4[3]))  
        self.cell5_end4.setPlainText(str(tuple_trang_thai_ket_thuc_4[4]))  
        self.cell6_end4.setPlainText(str(tuple_trang_thai_ket_thuc_4[5]))  
        self.cell7_end4.setPlainText(str(tuple_trang_thai_ket_thuc_4[6]))  
        self.cell8_end4.setPlainText(str(tuple_trang_thai_ket_thuc_4[7]))  
        self.cell9_end4.setPlainText(str(tuple_trang_thai_ket_thuc_4[8]))  


    def xu_ly_nhan_nut_giai(self):
        global so_luong_trang_thai_da_mo 
        loai_thuat_toan = self.cbbAlgorithm.currentText()  
        
        global tuple_trang_thai_bat_dau_1, tuple_trang_thai_bat_dau_2, tuple_trang_thai_bat_dau_3, tuple_trang_thai_bat_dau_4
        global tuple_trang_thai_ket_thuc_1, tuple_trang_thai_ket_thuc_2, tuple_trang_thai_ket_thuc_3, tuple_trang_thai_ket_thuc_4
        
        self.tap_trang_thai_niem_tin_hien_tai.clear()
        self.tap_trang_thai_dich_hien_tai.clear()

        try:
            if all(not la_o_nhap_lieu_rong(o_nhap) for o_nhap in [
                self.cell1_start1, self.cell4_start1, self.cell7_start1,  
                self.cell2_start1, self.cell5_start1, self.cell8_start1,  
                self.cell3_start1, self.cell6_start1, self.cell9_start1]):  
                tuple_trang_thai_bat_dau_1 = tuple([
                    int(self.cell1_start1.toPlainText()), int(self.cell2_start1.toPlainText()), int(self.cell3_start1.toPlainText()),
                    int(self.cell4_start1.toPlainText()), int(self.cell5_start1.toPlainText()), int(self.cell6_start1.toPlainText()),
                    int(self.cell7_start1.toPlainText()), int(self.cell8_start1.toPlainText()), int(self.cell9_start1.toPlainText())
                ])
                self.tap_trang_thai_niem_tin_hien_tai.append(tuple_trang_thai_bat_dau_1)
            
            if all(not la_o_nhap_lieu_rong(o_nhap) for o_nhap in [
                self.cell1_start2, self.cell4_start2, self.cell7_start2,  
                self.cell2_start2, self.cell5_start2, self.cell8_start2,  
                self.cell3_start2, self.cell6_start2, self.cell9_start2]):  
                tuple_trang_thai_bat_dau_2 = tuple([
                    int(self.cell1_start2.toPlainText()), int(self.cell2_start2.toPlainText()), int(self.cell3_start2.toPlainText()),
                    int(self.cell4_start2.toPlainText()), int(self.cell5_start2.toPlainText()), int(self.cell6_start2.toPlainText()),
                    int(self.cell7_start2.toPlainText()), int(self.cell8_start2.toPlainText()), int(self.cell9_start2.toPlainText())
                ])
                self.tap_trang_thai_niem_tin_hien_tai.append(tuple_trang_thai_bat_dau_2)

            if all(not la_o_nhap_lieu_rong(o_nhap) for o_nhap in [
                self.cell1_start3, self.cell4_start3, self.cell7_start3,  
                self.cell2_start3, self.cell5_start3, self.cell8_start3,  
                self.cell3_start3, self.cell6_start3, self.cell9_start3]):  
                tuple_trang_thai_bat_dau_3 = tuple([
                    int(self.cell1_start3.toPlainText()), int(self.cell2_start3.toPlainText()), int(self.cell3_start3.toPlainText()),
                    int(self.cell4_start3.toPlainText()), int(self.cell5_start3.toPlainText()), int(self.cell6_start3.toPlainText()),
                    int(self.cell7_start3.toPlainText()), int(self.cell8_start3.toPlainText()), int(self.cell9_start3.toPlainText())
                ])
                self.tap_trang_thai_niem_tin_hien_tai.append(tuple_trang_thai_bat_dau_3)

            if all(not la_o_nhap_lieu_rong(o_nhap) for o_nhap in [
                self.cell1_start4, self.cell4_start4, self.cell7_start4, 
                self.cell2_start4, self.cell5_start4, self.cell8_start4,
                self.cell3_start4, self.cell6_start4, self.cell9_start4]): 
                tuple_trang_thai_bat_dau_4 = tuple([
                    int(self.cell1_start4.toPlainText()), int(self.cell2_start4.toPlainText()), int(self.cell3_start4.toPlainText()),
                    int(self.cell4_start4.toPlainText()), int(self.cell5_start4.toPlainText()), int(self.cell6_start4.toPlainText()),
                    int(self.cell7_start4.toPlainText()), int(self.cell8_start4.toPlainText()), int(self.cell9_start4.toPlainText())
                ])
                self.tap_trang_thai_niem_tin_hien_tai.append(tuple_trang_thai_bat_dau_4)
                
            if all(not la_o_nhap_lieu_rong(o_nhap) for o_nhap in [
                self.cell1_end1, self.cell2_end1, self.cell3_end1, 
                self.cell4_end1, self.cell5_end1, self.cell6_end1, 
                self.cell7_end1, self.cell8_end1, self.cell9_end1]):
                tuple_trang_thai_ket_thuc_1 = tuple([
                    int(self.cell1_end1.toPlainText()), int(self.cell2_end1.toPlainText()), int(self.cell3_end1.toPlainText()),
                    int(self.cell4_end1.toPlainText()), int(self.cell5_end1.toPlainText()), int(self.cell6_end1.toPlainText()),
                    int(self.cell7_end1.toPlainText()), int(self.cell8_end1.toPlainText()), int(self.cell9_end1.toPlainText())
                ])
                self.tap_trang_thai_dich_hien_tai.append(tuple_trang_thai_ket_thuc_1)

            if all(not la_o_nhap_lieu_rong(o_nhap) for o_nhap in [
                self.cell1_end2, self.cell2_end2, self.cell3_end2,
                self.cell4_end2, self.cell5_end2, self.cell6_end2, 
                self.cell7_end2, self.cell8_end2, self.cell9_end2]):
                tuple_trang_thai_ket_thuc_2 = tuple([
                    int(self.cell1_end2.toPlainText()), int(self.cell2_end2.toPlainText()), int(self.cell3_end2.toPlainText()),
                    int(self.cell4_end2.toPlainText()), int(self.cell5_end2.toPlainText()), int(self.cell6_end2.toPlainText()),
                    int(self.cell7_end2.toPlainText()), int(self.cell8_end2.toPlainText()), int(self.cell9_end2.toPlainText())
                ])
                self.tap_trang_thai_dich_hien_tai.append(tuple_trang_thai_ket_thuc_2)
                
            if all(not la_o_nhap_lieu_rong(o_nhap) for o_nhap in [
                self.cell1_end3, self.cell2_end3, self.cell3_end3,
                self.cell4_end3, self.cell5_end3, self.cell6_end3, 
                self.cell7_end3, self.cell8_end3, self.cell9_end3]):
                tuple_trang_thai_ket_thuc_3 = tuple([
                    int(self.cell1_end3.toPlainText()), int(self.cell2_end3.toPlainText()), int(self.cell3_end3.toPlainText()),
                    int(self.cell4_end3.toPlainText()), int(self.cell5_end3.toPlainText()), int(self.cell6_end3.toPlainText()),
                    int(self.cell7_end3.toPlainText()), int(self.cell8_end3.toPlainText()), int(self.cell9_end3.toPlainText())
                ])
                self.tap_trang_thai_dich_hien_tai.append(tuple_trang_thai_ket_thuc_3)
                
            if all(not la_o_nhap_lieu_rong(o_nhap) for o_nhap in [
                self.cell1_end4, self.cell2_end4, self.cell3_end4,  
                self.cell4_end4, self.cell5_end4, self.cell6_end4, 
                self.cell7_end4, self.cell8_end4, self.cell9_end4]):
                tuple_trang_thai_ket_thuc_4 = tuple([
                    int(self.cell1_end4.toPlainText()), int(self.cell2_end4.toPlainText()), int(self.cell3_end4.toPlainText()),
                    int(self.cell4_end4.toPlainText()), int(self.cell5_end4.toPlainText()), int(self.cell6_end4.toPlainText()),
                    int(self.cell7_end4.toPlainText()), int(self.cell8_end4.toPlainText()), int(self.cell9_end4.toPlainText())
                ])
                self.tap_trang_thai_dich_hien_tai.append(tuple_trang_thai_ket_thuc_4)
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị nhập vào không hợp lệ!")
            return
              
        thoi_gian_bat_dau = time.perf_counter()
        if not self.tap_trang_thai_niem_tin_hien_tai:
            messagebox.showerror("Lỗi", "Tập trạng thái niềm tin ban đầu rỗng!")
            return
        if not self.tap_trang_thai_dich_hien_tai:
            messagebox.showerror("Lỗi", "Tập trạng thái đích ban đầu rỗng!")
            return
        
        try:
            if int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000) >= 1:  
                self.toc_do_moi_buoc_ms = int(float(self.txtSolveSpeedPerStep.toPlainText()) * 1000)  
            else:
                messagebox.showerror("Lỗi", "Tốc độ mỗi bước phải lớn hơn hoặc bằng 0.001s")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Tốc độ mỗi bước không hợp lệ")
            return

        chuoi_hanh_dong_ket_qua = None
        bien_dem_trang_thai_mo = [0] 
        quan_sat_mot_phan = (loai_thuat_toan == "Tìm kiếm quan sát một phần")
        
        bien_dem_trang_thai_mo_list = [0] 
        quan_sat_mot_phan = (loai_thuat_toan == "Tìm kiếm quan sát một phần") 
        
        chuoi_hanh_dong_ket_qua = giai_tim_kiem_moi_truong_phuc_tap(
            self.tap_trang_thai_niem_tin_hien_tai,      
            self.tap_trang_thai_dich_hien_tai,         
            bien_dem_trang_thai_mo_list,                 
            la_quan_sat_mot_phan_giai_mtk=quan_sat_mot_phan 
        )
        
        so_luong_trang_thai_da_mo = bien_dem_trang_thai_mo_list[0]
        self.chuoi_hanh_dong_giai_phap = chuoi_hanh_dong_ket_qua

        thoi_gian_ket_thuc = time.perf_counter()
        thoi_gian_thuc_thi = thoi_gian_ket_thuc - thoi_gian_bat_dau
        self.txtSolveTime.setPlainText(f"{thoi_gian_thuc_thi:.10f}(s)") 
        print(f"Thời gian thực thi: {thoi_gian_thuc_thi}")
        print(f"Loại thuật toán: {loai_thuat_toan}")
        print(f"Số lượng belief state đã mở: {so_luong_trang_thai_da_mo}")

        if chuoi_hanh_dong_ket_qua is None:
            messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")
            self.txtTotalStep.setPlainText("0") 
            self.txtStep.setPlainText("0") 
            self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau.clear()
            print("Kích thước chuỗi hành động: 0")
        else:
            print(f"Kích thước chuỗi hành động: {len(chuoi_hanh_dong_ket_qua)}")
            
            self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau.clear()
            cac_trang_thai_niem_tin_ban_dau = [
                ttbd for ttbd in [tuple_trang_thai_bat_dau_1, tuple_trang_thai_bat_dau_2, tuple_trang_thai_bat_dau_3, tuple_trang_thai_bat_dau_4]
                if ttbd != tuple([0,0,0,0,0,0,0,0,0]) # Chỉ xử lý các trạng thái thực sự được nhập
            ]

            for trang_thai_bd in cac_trang_thai_niem_tin_ban_dau:
                duong_di_cho_tt = [trang_thai_bd]
                trang_thai_hien_tai_cua_duong_di = trang_thai_bd
                for hanh_dong in chuoi_hanh_dong_ket_qua:
                    trang_thai_hien_tai_cua_duong_di = ap_dung_hanh_dong_cho_trang_thai(hanh_dong, trang_thai_hien_tai_cua_duong_di)
                    duong_di_cho_tt.append(trang_thai_hien_tai_cua_duong_di)
                self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau.append(duong_di_cho_tt)
            
            self.chay_giai_phap_da_tim_duoc()
        
    def chay_giai_phap_da_tim_duoc(self):
        self.buoc_hien_tai_chay = 0
        self.bo_hen_gio = QtCore.QTimer()
        print("Các đường đi kết quả cho từng trạng thái ban đầu:")
        for dd in self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau:
            print(dd)
        self.bo_hen_gio.timeout.connect(self.cap_nhat_cac_buoc_chay_ket_qua)
        self.bo_hen_gio.start(self.toc_do_moi_buoc_ms)

    def cap_nhat_o_hien_thi_ket_qua(self, widget_o, gia_tri):
        if gia_tri == 0:
            widget_o.setPlainText(" ")
        else:
            widget_o.setPlainText(str(gia_tri))

    def cap_nhat_cac_buoc_chay_ket_qua(self):
        duong_di_ket_qua_dau_tien_hop_le = None
        for duong_di_con in self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau:
            if duong_di_con: 
                duong_di_ket_qua_dau_tien_hop_le = duong_di_con
                break
        
        if not duong_di_ket_qua_dau_tien_hop_le:
            self.bo_hen_gio.stop()
            return

        self.txtTotalStep.setPlainText(str(len(duong_di_ket_qua_dau_tien_hop_le) -1 )) 
        
        if self.buoc_hien_tai_chay < len(duong_di_ket_qua_dau_tien_hop_le):
            if len(self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau) > 0 and self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau[0]:
                trang_thai_hien_tai_dd1 = self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau[0][self.buoc_hien_tai_chay]
                self.cap_nhat_o_hien_thi_ket_qua(self.cell1_result1, trang_thai_hien_tai_dd1[0]) 
                self.cap_nhat_o_hien_thi_ket_qua(self.cell2_result1, trang_thai_hien_tai_dd1[1]) 
                self.cap_nhat_o_hien_thi_ket_qua(self.cell3_result1, trang_thai_hien_tai_dd1[2])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell4_result1, trang_thai_hien_tai_dd1[3])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell5_result1, trang_thai_hien_tai_dd1[4])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell6_result1, trang_thai_hien_tai_dd1[5])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell7_result1, trang_thai_hien_tai_dd1[6])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell8_result1, trang_thai_hien_tai_dd1[7])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell9_result1, trang_thai_hien_tai_dd1[8])

            if len(self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau) > 1 and self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau[1]:
                trang_thai_hien_tai_dd2 = self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau[1][self.buoc_hien_tai_chay]
                self.cap_nhat_o_hien_thi_ket_qua(self.cell1_result2, trang_thai_hien_tai_dd2[0]) 
                self.cap_nhat_o_hien_thi_ket_qua(self.cell2_result2, trang_thai_hien_tai_dd2[1])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell3_result2, trang_thai_hien_tai_dd2[2])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell4_result2, trang_thai_hien_tai_dd2[3])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell5_result2, trang_thai_hien_tai_dd2[4])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell6_result2, trang_thai_hien_tai_dd2[5])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell7_result2, trang_thai_hien_tai_dd2[6])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell8_result2, trang_thai_hien_tai_dd2[7])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell9_result2, trang_thai_hien_tai_dd2[8])
            
            if len(self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau) > 2 and self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau[2]:
                trang_thai_hien_tai_dd3 = self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau[2][self.buoc_hien_tai_chay]
                self.cap_nhat_o_hien_thi_ket_qua(self.cell1_result3, trang_thai_hien_tai_dd3[0]) 
                self.cap_nhat_o_hien_thi_ket_qua(self.cell2_result3, trang_thai_hien_tai_dd3[1])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell3_result3, trang_thai_hien_tai_dd3[2])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell4_result3, trang_thai_hien_tai_dd3[3])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell5_result3, trang_thai_hien_tai_dd3[4])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell6_result3, trang_thai_hien_tai_dd3[5])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell7_result3, trang_thai_hien_tai_dd3[6])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell8_result3, trang_thai_hien_tai_dd3[7])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell9_result3, trang_thai_hien_tai_dd3[8])
            if len(self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau) > 3 and self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau[3]:
                trang_thai_hien_tai_dd4 = self.cac_duong_di_ket_qua_cho_moi_trang_thai_ban_dau[3][self.buoc_hien_tai_chay]              
                self.cap_nhat_o_hien_thi_ket_qua(self.cell1_result4, trang_thai_hien_tai_dd4[0])  
                self.cap_nhat_o_hien_thi_ket_qua(self.cell2_result4, trang_thai_hien_tai_dd4[1])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell3_result4, trang_thai_hien_tai_dd4[2])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell4_result4, trang_thai_hien_tai_dd4[3])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell5_result4, trang_thai_hien_tai_dd4[4])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell6_result4, trang_thai_hien_tai_dd4[5])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell7_result4, trang_thai_hien_tai_dd4[6])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell8_result4, trang_thai_hien_tai_dd4[7])
                self.cap_nhat_o_hien_thi_ket_qua(self.cell9_result4, trang_thai_hien_tai_dd4[8])

            self.buoc_hien_tai_chay += 1
            self.txtStep.setPlainText(str(self.buoc_hien_tai_chay)) 
        else:
            self.bo_hen_gio.stop()

ung_dung_qt = QApplication([])
cua_so_chinh = UngDungMoiTruongPhucTap()
cua_so_chinh.show()
ung_dung_qt.exec()