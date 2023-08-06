import sys
import os
import time

import regex as re
import numpy as np


paAEON1 = r"^T[RH][uU]NG\W*T[AÂ]M\W*TH[UƯư][OƠơ]NG\W*[\w]?M[AẠ]I"
paAEON2 = r"^MUA HÀNG TRỰC TUYẾN"
paAEON3 = r"^SỐ LƯỢNG MẶT HÀNG"
paAEON4 = r"^PHƯƠNG THỨC THANH TOÁN"
paAEON5 = r"^TỔNG THANH TOÁN"

paBigC1 = r"^Cty TNHH TMQT-DV Sthi Big C"
paBigC2 = r"^PHIEU TINH TIEN"
paBigC3 = r"^=\s*TONG CONG"
paBigC4 = r"^=\s*Tong Tien Hang"

paCoopMart1 = r"^Co gia tri xuat Hoa don GTGT trong ngay"
paCoopMart2 = r"^PHIEU TINH TIEN"
paCoopMart3 = r"^Tong so tien thanh toan"
paCoopMart4 = r"^THONG TIN KHACH HANG THAN THIET"

paVinCommerce1 = r"^H[OÓ][AÁ] ĐƠN BÁN HÀNG"
paVinCommerce2 = r"^\d{12,13}"
paVinCommerce3 = r"^[T]?ỔNG TIỀN PHẢI T\.TOÁN"
paVinCommerce4 = r"^Tax invoice will be issued within same day"
paVinCommerce5 = r"^Chỉ xuất hoá đơn trong ngày"

paLotteMart1 = r"^LOTTE[\.]{1,2}MART"
paLotteMart2 = r"^CTY CO PHAN TTT[MN] LOTTE"
paLotteMart3 = r"^LOTTE Mart \w+"
paLotteMart4 = r"^\d{12,13}$"
paLotteMart5 = r"^So tien da nhan"
paLotteMart6 = r"^TIET KIEM HON KHI SU DUNG THE THANH VIEN"

paBachHoaXanh1 = r"^BÁCH HOÁ XANH"
paBachHoaXanh2 = r"^PHIẾU THANH TOÁN"
paBachHoaXanh3 = r"^\(Giá trên đã bao gồm thuế GTGT\)"

paEMart1 = r"^Hoạt động từ\s*[:]?\s*\d+"
paEMart2 = r"^Số tiền sẽ nhận"
paEMart3 = r"^\d{12,13}$"
paEMart4 = r"^Thuế giá trị gia tăng"
paEMart5 = r"^Tổng số hàng Số lượng"

paLMart1 = r"^Hệ thống Siêu Thị L-MART"
paLMart2 = r"^HOÁ ĐƠN BÁN HÀNG"
paLMart3 = r"^Tổng tiền hàng\s*[:]?"

class PatternBill():

  def __init__(self, pattern, rateL, rateR, rateH):
    
    self.pattern = pattern
    self.rateL = rateL
    self.rateR = rateR
    self.rateH = rateH

def getLines(lines, boxes, L1, R1, L2, R2, L3, R3, H, rate1, rate2, rate3):

  lLines = []
  lBoxes = []
  for i in range(len(boxes)):
    item = boxes[i]
    l_t = item[0][0]
    t_l = item[0][1]
    r_t = item[1][0]
    t_r = item[1][1]
    r_b = item[2][0]
    b_r = item[2][1]
    l_b = item[3][0]
    b_l = item[3][1]
    ocr = lines[i]
    l = len(boxes)
    
    if b_l - t_l >= H / 2 and b_l - t_l <= 4 * H:
      if i < l / 3 and l_t >= L1 and r_t <= R1:
        lBoxes.append(item)
        lLines.append(ocr)
      if i >= l / 3 and i < 2 * l / 3 and l_t >= L2 and r_t <= R2:
        lBoxes.append(item)
        lLines.append(ocr)
      if i >= 2 * l / 3 and l_t >= L3 and r_t <= R3:
        lBoxes.append(item)
        lLines.append(ocr)

  return L1, L2, L3, R1, R2, R3, H, rate1, rate2, rate3, lLines, lBoxes

def cropBill(lines, boxes, patterns):

  L1 = 10000
  L2 = 10000
  L3 = 10000
  R1 = 0
  R2 = 0
  R3 = 0
  H1 = 0
  H2 = 0
  H3 = 0
  H = 0
  rate1 = 0
  rate2 = 0
  rate3 = 0
  
  n = len(boxes)
  for i in range(len(boxes)):
    item = boxes[i]
    l_t = item[0][0]
    t_l = item[0][1]
    r_t = item[1][0]
    t_r = item[1][1]
    r_b = item[2][0]
    b_r = item[2][1]
    l_b = item[3][0]
    b_l = item[3][1]
    ocr = lines[i]

    if H1 == 0 and i < n / 3:
      for pa in patterns:
        pattern = pa.pattern
        rateL = pa.rateL
        rateR = pa.rateR
        if re.search(pattern, ocr):
          L1 = l_t
          R1 = r_t
          d = R1 - L1
          L1 = (int)(L1 - rateL * d)
          R1 = (int)(R1 + rateR * d)
          H1 = b_l - t_l
          rate1 = (t_r - t_l) / d 
          break
    
    if H2 == 0 and i >= n / 3 and i < 2 * n / 3:
      for pa in patterns:
        pattern = pa.pattern
        rateL = pa.rateL
        rateR = pa.rateR
        if re.search(pattern, ocr):
          L2 = l_t
          R2 = r_t
          d = R2 - L2
          L2 = (int)(L2 - rateL * d)
          R2 = (int)(R2 + rateR * d)
          H2 = b_l - t_l
          rate2 = (t_r - t_l) / d 
          break
    
    if H3 == 0 and i >= 2 * n / 3:
      for pa in patterns:
        pattern = pa.pattern
        rateL = pa.rateL
        rateR = pa.rateR
        if re.search(pattern, ocr):
          L3 = l_t
          R3 = r_t
          d = R3 - L3
          L3 = (int)(L3 - rateL * d)
          R3 = (int)(R3 + rateR * d)
          H3 = b_l - t_l
          rate3 = (t_r - t_l) / d 
          break

  if H2 == 0: 
    H2 = H1
    L2 = L1
    R2 = R1
    rate2 = rate1
  if H3 == 0: 
    H3 = H2
    L3 = L2
    R3 = R2
    rate3 = rate2
  if H1 == 0: 
    H1 = H2
    L1 = L2
    R1 = R2
    rate1 = rate2

  H = (H1 + H2 + H3) / 2
  H = (int)(H - H/4)
  if L1 < 0: L1 = 0
  if L2 < 0: L2 = 0
  if L3 < 0: L3 = 0

  return getLines(lines, boxes, L1, R1, L2, R2, L3, R3, H, rate1, rate2, rate3)

def cropAEON(lines, boxes):

  rule1 = PatternBill(paAEON1, 0.2, 0.4, 1.0)
  rule2 = PatternBill(paAEON2, 0.8, 0.8, 1.0)
  rule3 = PatternBill(paAEON3, 0.2, 1.7, 1.0)
  rule4 = PatternBill(paAEON4, 0.2, 1.5, 1.0)
  rule5 = PatternBill(paAEON5, 0.2, 2.5, 1.0)
  patterns = [rule1, rule2, rule3, rule4, rule5]

  return cropBill(lines, boxes, patterns)

def cropBigC(lines, boxes):

  rule1 = PatternBill(paBigC1, 0.1, 0.1, 1.0)
  rule2 = PatternBill(paBigC2, 1.2, 1.2, 1.0)
  rule3 = PatternBill(paBigC3, 0.3, 2.0, 1.0)
  rule4 = PatternBill(paBigC4, 0.3, 2.0, 1.0)
  patterns = [rule1, rule2, rule3, rule4]

  return cropBill(lines, boxes, patterns)

def cropCoopMart(lines, boxes):

  rule1 = PatternBill(paCoopMart1, 0.2, 0.2, 1.0)
  rule2 = PatternBill(paCoopMart2, 1.0, 1.0, 1.0)
  rule3 = PatternBill(paCoopMart3, 0.1, 1.0, 1.0)
  rule4 = PatternBill(paCoopMart4, 0.1, 0.4, 1.0)
  patterns = [rule1, rule2, rule3, rule4]

  return cropBill(lines, boxes, patterns)

def cropVinCommerce(lines, boxes):

  rule1 = PatternBill(paVinCommerce1, 1.1, 1.1, 1.0)
  rule2 = PatternBill(paVinCommerce2, 0.1, 3.1, 1.0)
  rule3 = PatternBill(paVinCommerce3, 0.1, 1.1, 1.0)
  rule4 = PatternBill(paVinCommerce4, 0.1, 0.1, 1.0)
  patterns = [rule1, rule2, rule3, rule4]

  return cropBill(lines, boxes, patterns)

def cropLotteMart(lines, boxes):

  rule1 = PatternBill(paLotteMart1, 0.2, 0.1, 1.0)
  rule2 = PatternBill(paLotteMart2, 0.1, 0.5, 1.0)
  rule3 = PatternBill(paLotteMart3, 0.1, 2.0, 1.0)
  rule4 = PatternBill(paLotteMart4, 0.1, 2.5, 1.0)
  rule5 = PatternBill(paLotteMart5, 0.1, 0.4, 1.0)
  rule6 = PatternBill(paLotteMart6, 0.1, 0.4, 1.0)
  patterns = [rule1, rule2, rule3, rule4, rule5]

  return cropBill(lines, boxes, patterns)

def cropBachHoaXanh(lines, boxes):

  rule1 = PatternBill(paBachHoaXanh1, 0.6, 0.6, 1.0)
  rule2 = PatternBill(paBachHoaXanh2, 0.5, 0.5, 1.0)
  rule3 = PatternBill(paBachHoaXanh3, 0.3, 0.3, 1.0)
  patterns = [rule1, rule2, rule3]

  return cropBill(lines, boxes, patterns)

def cropLMart(lines, boxes):

  rule1 = PatternBill(paLMart1, 0.2, 0.2, 0.8)
  rule2 = PatternBill(paLMart2, 0.5, 0.5, 0.6)
  rule3 = PatternBill(paLMart3, 1.3, 1.1, 1.0)
  patterns = [rule1, rule2, rule3]

  return cropBill(lines, boxes, patterns)

def cropEMart(lines, boxes):

  rule1 = PatternBill(paEMart1, 0.2, 1.7, 1.0)
  rule2 = PatternBill(paEMart2, 0.1, 2.5, 0.6)
  rule3 = PatternBill(paEMart3, 0.1, 3.1, 1.0)
  rule4 = PatternBill(paEMart4, 0.1, 2.1, 1.0)
  rule5 = PatternBill(paEMart5, 0.1, 2.1, 1.0)
  patterns = [rule1, rule2, rule3, rule4, rule5]

  return cropBill(lines, boxes, patterns)


def getXY(item):

  l_t = int(item[0][0])
  t_l = int(item[0][1])
  r_t = int(item[1][0])
  t_r = int(item[1][1])
  r_b = int(item[2][0])
  b_r = int(item[2][1])
  l_b = int(item[3][0])
  b_l = int(item[3][1])
  
  return l_t, t_l, r_t, t_r, r_b, b_r, l_b, b_l 

def normalShop(info):

  info = re.sub(r"\s*\|\s*", " ", info)

  info = re.sub(r"T[RH]UNG T[AÂ]M", "TRUNG TÂM", info)
  info = re.sub(r"THƯƠNG\W*[\w]?M[AẠ]I", "THƯƠNG MẠI", info)

  info = re.sub(r"AEON[G]", "AEON", info)

  return info

def normalDiachi(info):

  info = re.sub(r"HCH", "HCM", info)

  return info

def normalSDT(info):

  info = re.sub(r"^S[oO]", "So", info)
  info = re.sub(r",", ".", info)
  return info

def normalSanPham(info):

  info = re.sub(r"\d+\s*\|\s*", "", info)
  return info

def normalSLMH(info):

  info = re.sub(r"S[ốỐ] LƯỢNG MẶT HÀNG\s*[:]?", "SỐ LƯỢNG MẶT HÀNG:", info)
  
  return info

def normalTongTien(info):

  info = re.sub(r"[T]?[ÔỔỐ]NG THANH TOÁ[N]?\s*[:]?", "TỔNG THANH TOÁN:", info)
  
  return info

def normalTienThoiLai(info):

  info = re.sub(r"[T]?I[EÈÉỀẾ]N TH[OỐ]I L[AẠ]I\s*[:]?", "TIỀN THỐI LẠI:", info)

  return info

def normalThuNgan(info):

  info = re.sub(r"[T]?H[uU] NG[AÂ]N\s*[:]?", "THU NGÂN:", info)

  return info

def normalQuay(info):

  info = re.sub(r"Q[uU][AÀÂẦ][yY]\s*[:]?", "QUẦY:", info)

  return info

def check2Lines(x1, y1, x2, y2, rate, d):

  if abs(rate) > 0.03:
    y2N = y1 + rate * (x2 - x1)
    #print(str(y2N) + "\t" + str(y2))
    if abs(y2 - y2N) < d:
      return abs(y2 - y2N)
  
  elif abs(y2 - y1) < 2 * d:
    return abs(y2 - y1)

  return -1

def checkDiachi(ocr):
  
  paDiachi1 = r"^[DĐ][cC]\s*[:]"
  paDiachi2 = r"(Binh Duong|DN|Ha Noi|HC[MH]|H[oồ] Ch[ií] Minh|Tan Phu|Thu Dau Mot|Việt Nam|[0Q]\.(\d+|\w+(\s\w+)*))$"
  paDiachi3 = r"[\W]([pP][\.]\d{1,2}|([pP]hường|[qQ]uận|[tT]ầng|[tT]hành [pP]hố|[xX]ã) \w+(\s+\w+)*)[\W]"

  if re.search(paDiachi1, ocr) or re.search(paDiachi2, ocr) or re.search(paDiachi3, ocr):
    return True

  return False

def checkGia(ocr):

  paGia = r"^[-]?\d+([\.,]\d{2,3})+(\s\d+([\.,]\d{2,3})+)?(d|đ)?$"
  if re.search(paGia, ocr):
    return True

  return False

def checkSanPham(info):

  if re.search(r"^\d+\s*[xX]?\s*$", info):
    return False
  if re.search(r"^[xX]\s*$", info):
    return False

  return True
  
def searchPatternH(pattern, id, lid, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2):

  lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
  for iS in lid:
    if iS > idB and iS < idE:
      infoS = lLines[iS]
      ltS, tlS, rtS, trS, rbS, brS, lbS, blS = getXY(lBoxes[iS])
      d = check2Lines(ltS, tlS, lt, tl, rate, H)
      #print(infoS + "\t" + str(d))
      if d >= 0 and ltS > d1 and ltS < d2 and re.search(pattern, infoS):
        return infoS, iS

  return "", -1

def searchPatternD(pattern, id, lid, lLines, lBoxes, idB, idE, H, dis):

  lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
  for iS in lid:
    if iS > idB and iS < idE:
      infoS = lLines[iS]
      ltS, tlS, rtS, trS, rbS, brS, lbS, blS = getXY(lBoxes[iS])
      if abs(lt - ltS) < dis and tl < tlS and tl > tlS - H and re.search(pattern, infoS):
        return infoS, iS

  return "", -1

def searchPatternD2(pattern, id, lid, lLines, lBoxes, idB, idE, H, d1, d2):

  lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
  for iS in lid:
    if iS > idB and iS < idE:
      infoS = lLines[iS]
      ltS, tlS, rtS, trS, rbS, brS, lbS, blS = getXY(lBoxes[iS])
      if tl < tlS and tl > tlS - H and ltS > d1 and ltS < d2 and re.search(pattern, infoS):
        return infoS, iS

  return "", -1

def searchPatternU(pattern, id, lid, lLines, lBoxes, idB, idE, H, dis):

  lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
  for iS in lid:
    if iS > idB and iS < idE:
      infoS = lLines[iS]
      ltS, tlS, rtS, trS, rbS, brS, lbS, blS = getXY(lBoxes[iS])
      if abs(lt - ltS) < dis and tl > tlS and tl < tlS + H and re.search(pattern, infoS):
        return infoS, iS

  return "", -1

def searchPatternM(pattern, id, lid, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2):

  min = 1000
  idMin = -1
  infoMin = ""
  lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
  for iS in lid:
    if iS > idB and iS < idE:
      infoS = lLines[iS]
      ltS, tlS, rtS, trS, rbS, brS, lbS, blS = getXY(lBoxes[iS])
      d = check2Lines(rt, tr, ltS, tlS, rate, H)
      if d >= 0 and d < min and ltS > d1 and ltS < d2 and re.search(pattern, infoS):
        min = d
        idMin = iS
        infoMin = infoS
  if min < 1000:
    return infoMin, idMin

  return "", -1


class InfosAEON:

  def __init__(self):
        self.shop = ""
        self.title = ""
        self.diachi = ""
        self.sdt = ""
        self.email = ""
        self.website = ""
        self.masothue = ""
        self.titleGia = ""
        self.sanpham = []
        self.mahang = []
        self.soluong = []
        self.dongia = []
        self.gia = []
        self.soluongmathang = ""
        self.tongtien = ""
        self.tienthoilai = ""
        self.thungan = ""
        self.quay = ""
        self.mathanhvien = ""
        self.sogiaodich = ""
        self.thoigian = ""

  def showInfos(self):
    print(self.shop)
    print(self.title)
    print(self.diachi)
    print(self.sdt)
    print(self.email)
    print(self.website)
    print(self.masothue)
    print(self.soluongmathang)
    print(self.tongtien)
    print(self.tienthoilai)
    print(self.thungan)
    print(self.quay)
    print(self.mathanhvien)
    print(self.sogiaodich)
    print(self.thoigian)
    for i in range(len(self.sanpham)):
      print(self.sanpham[i] + "\t" + self.mahang[i] + "\t" + self.soluong[i] + "\t" + self.dongia[i] + "\t" + self.gia[i])

    return

def extractSanPhamAEON(infos, lLines, lBoxes, idB, idE, H):
  
  paSanPham = r"^\S+(\s+\S+)+"
  paGia = r"[-]?\d+([\.,]\d{2,3})+(d|đ)?$"
  paSoLuong = r"^\d+([\.,]\d{2,3})*"
  paMaHang = r"\d{10,12}$"
  n = len(lLines)
  L = L1
  R = R1
  rate = rate1
  for id in range(idB, idE):
    if id >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif id >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[id]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
    lID1 = [id - 1, id + 1, id - 2, id + 2]
    lID2 = [id + 1, id + 2, id + 3, id + 4]
    ma = re.search(paMaHang, info)
    if ma:
      mahang = ma.group()
      sanpham = ""
      info = re.sub(r"\s*\d+$", "", info)
      if re.search(paSanPham, info):
        sanpham = info
      soluong = "1"
      dongia = ""
      gia = ""
      yGia = 0
      yDonGia = 0

      if sanpham == "":
        dSP1 = L
        dSP2 = lt
        sanpham, iSP = searchPatternM(paSanPham, id, lID1, lLines, lBoxes, idB, idE, L, R, 2 * H, rate, dSP1, dSP2)
        if iSP > 0:
          lLines[iSP] = ""
      
      gia, iGia = searchPatternD(paGia, id, lID2, lLines, lBoxes, idB, idE, 2 * H, 25)
      if iGia > 0:
        lLines[iGia] = ""
        dDG1 = L + (int)((R - L) / 4)
        dDG2 = lt
        lDG = [iGia - 1, iGia + 1, iGia - 2, iGia + 2]
        dongia, iDG = searchPatternM(paGia, iGia, lDG, lLines, lBoxes, idB, idE, L, R, H, rate, dDG1, dDG2)
        
        dSL1 = L
        dSL2 = L + (int)((R - L) / 4)
        if iDG > 0:
          lLines[iDG] = ""
          lSL = [iDG - 1, iDG + 1, iDG - 2, iDG + 2]
        else:
          lSL = [iGia - 1, iGia +1, iGia - 2, iGia + 2]
        soluong, iSL = searchPatternM(paSoLuong, iDG, lSL, lLines, lBoxes, idB, idE, L, R, H, rate, dSL1, dSL2)
        if iSL > 0:
          lLines[iSL] = ""
        else:
          soluong = "1"

      infos.sanpham.append(sanpham)
      infos.mahang.append(mahang)
      infos.soluong.append(soluong)
      infos.dongia.append(dongia)
      infos.gia.append(gia)
    
  return

def extractAEON(lLines, lBoxes):

  infos = InfosAEON()

  idTitle = 0
  idGia = 0
  idTongTien = 0

  paShop = r"^(T[RH]UNG TÂM THƯƠNG\W*[\w]?M[AẠ]I)"
  paTitle = r"^(MUA HÀNG TRỰC TUYẾN)"
  paSDT = r"^[DĐ]T[:\.]\s*\d+([\.,\s]\d+)*"
  paWebsite = r"www\.\S+\.(vn|com)$"
  paEmail = r"^Email\s*:\s*.+\.(vn|com)$"
  paTitleGia = r"^(ĐƠN GIÁ|THÀNH TIỀN)"
  paGia = r"[-]?\d+([\.,]\d{2,3})*(d|đ)?"
  
  paSoLuongMatHang = r"^(S[ốỐ] LƯỢNG MẶT HÀNG)"
  paTongTien = r"^[T]?[ÔỔỐ]NG THANH TOÁ[N]?"
  paTienThoilai = r"^[T]?I[EÈÉỀẾ]N TH[OỐ]I L[AẠ]I"

  paThuNgan = r"^THU NG[AÂ]N\s*[:]?\s*"
  paQuay = r"^Q[uU][AÀÂẦ][yY]\s*[:]?\s*\d+"
  paMaThanhVien = r"^MÃ THÀNH VIÊN\s*[:]?\s*\d+"
  paSoGiaoDich = r"^S[ốỐ] GIAO DỊCH\s*[:]?\s*\d+"
  paThoiGian = r"\d{2}[:]\d{2}\s+\d{2}\/\d{2}\/\d{4}"
  n = len(lLines)
  L = L1
  R = R1
  rate = rate1
  for i in range(len(lLines)):
    if i >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif i >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[i]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[i])
    lID = [i - 1, i + 1, i - 2, i + 2]
    if infos.shop == "" and re.search(paShop, info):
      infos.shop = normalShop(info)
      for j in range(max(0,i - 2), i + 2):
        infoS = lLines[j]
        ltS, tlS, rtS, trS, rbS, brS, lbS, blS = getXY(lBoxes[j])
        if j != i and abs(tlS - tr) < 30 and rt > ltS - 100 and re.search(r"\s*[-]?\s*\w+(\s+\w+)+", infoS):
          infos.shop += " " + infoS
          break

    if infos.title == "" and re.search(paTitle, info):
      infos.title = info
      idTitle = i
    if idGia == 0 and re.search(paTitleGia, info):
      titleGia = info
      idGia = i
      
    if infos.soluongmathang == "" and re.search(paSoLuongMatHang, info):
      infos.soluongmathang = normalSLMH(info)
      idTongTien = i
      d1 = rt
      d2 = rt + 50
      tongSL, iTSL = searchPatternM(r"\d+$", i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTSL > 0:
        lLines[iTSL] = ""
        infos.soluongmathang += " | " + tongSL

      d1 = L2 + (int)(R2 - L2)/3
      d2 = R2
      tongGia, iTG = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTG > 0:
        lLines[iTG] = ""
        infos.soluongmathang += " | " + tongGia

    if infos.tongtien == "" and re.search(paTongTien, info):
      infos.tongtien = normalTongTien(info)
      idTongTien = i
      d1 = rt
      d2 = R2
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongtien += " | " + tongtien
        lLines[iTT] = ""

    if infos.tienthoilai == "" and re.search(paTienThoilai, info):
      infos.tienthoilai = normalTienThoiLai(info)
      d1 = rt
      d2 = R2
      tienthoilai, iTTL = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, 2 * H, rate, d1, d2)
      if iTTL > 0:
        infos.tienthoilai += " | " + tienthoilai
        lLines[iTTL] = ""

    if infos.thungan == "":
      ma = re.search(paThuNgan, info)
      if ma:
        infos.thungan = normalThuNgan(info)
        if idTongTien == 0:
          idTongTien = i

    if infos.quay == "":
      ma = re.search(paQuay, info)
      if ma:
        infos.quay = ma.group()

    if infos.mathanhvien == "":
      ma = re.search(paMaThanhVien, info)
      if ma:
        infos.mathanhvien = ma.group()

    if infos.sogiaodich == "":
      ma = re.search(paSoGiaoDich, info)
      if ma:
        infos.sogiaodich = ma.group()

    if infos.thoigian == "":
      ma = re.search(paThoiGian, info)
      if ma:
        infos.thoigian = ma.group()

  if idGia == 0:
    idGia = idTitle
  if idTongTien == 0:
    idTongTien = len(lLines)

  for i in range(idTitle):
    info = lLines[i]
    
    if infos.sdt == "":
      ma = re.search(paSDT, info)
      if ma != None:
        infos.sdt = normalSDT(ma.group())

    if infos.website == "":
      ma = re.search(paWebsite, info)
      if ma != None:
        infos.website = ma.group()

    if infos.email == "":
      if re.search(paEmail, info):
        infos.email = info

  extractSanPhamAEON(infos, lLines, lBoxes, idGia, idTongTien, H)
    
  return infos


class InfosBigC:

  def __init__(self):
        self.congty = ""
        self.shop = ""
        self.title = ""
        self.diachi = ""
        self.sdt = ""
        self.hotline = ""
        self.website = ""
        self.masothue = ""
        self.sanpham = []
        self.soluong = []
        self.gia = []
        self.tongtienhang = ""
        self.tongcong = ""
        self.soluongmathang = ""
        self.tienmat = ""
        self.tienthoilai = ""
        self.thungan = ""
        self.quay = ""
        self.ticket = ""
        self.thoigian = ""

  def showInfos(self):
    print(self.congty)
    print(self.shop)
    print(self.diachi)
    print(self.masothue)
    print(self.sdt)
    print(self.hotline)
    print(self.website)
    print(self.title)
    print(self.tongtienhang)
    print(self.tongcong)
    print(self.soluongmathang)
    print(self.tienmat)
    print(self.tienthoilai)
    print(self.thungan)
    print(self.quay)
    print(self.ticket)
    print(self.thoigian)
    
    for i in range(len(self.sanpham)):
      print(self.sanpham[i] + "\t" + self.soluong[i] + "\t" + self.gia[i])

    return

def extractSanPhamBigC(infos, lLines, lBoxes, idB, idE):
  
  paSanPham = r"^\S+(\s+\S+)+"
  paGia = r"[-]?\d+([\.,]\d{2,3})+(d|đ)?[vV]?$"
  paSoLuong = r"^\d+([\.,]\d{2,3})*"
  
  n = len(lLines)
  L = L1
  R = R1
  rate = rate1
  for id in range(idB, idE):
    if id >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif id >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[id]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
    if lt > L1 + (int)(3 * (R1 - L1) / 5) and re.search(paGia, info):
      gia = info
      sanpham = ""
      soluong = "1"
      
      lID = [id - 1, id + 1, id - 2, id + 2]
      d1 = L + 100
      d2 = lt
      sanpham, iSP = searchPatternM(paSanPham, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
      if iSP > 0:
        lLines[iSP] = ""
        lID = [iSP - 1, iSP + 1, iSP - 2, iSP + 2]
        d1 = L
        d2 = L + (R - L) / 5
        soluong, iSL = searchPatternM(paSoLuong, iSP, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
        if iSL > 0:
          lLines[iSL] = ""

      infos.sanpham.append(sanpham)
      infos.soluong.append(soluong)
      infos.gia.append(gia)
    
  return

def extractBigC(lLines, lBoxes):

  infos = InfosBigC()

  idTitle = 0
  idGia = 0
  idTongTien = 0

  paCty = r"^B[iI][gG] C \w+(\s+\w+)*"
  paShop = r"^((CN T[pP]HCM\W)?C[tT][yY] TNHH|CN CT CP)"
  paDiachi = r"(Binh Duong|DN|Ha Noi|HC[MH]|Tan Phu|Thu Dau Mot)$"
  paTitle = r"^PHIEU TINH TIEN"
  paMaSoThue = r"Ma so thue[:]?\s*[\W]?\d+"
  paSDT = r"^S[oO] DT[:\.]?\s*[\(]?\d+[\)]?([\.,\s-]\d+)*"
  paHotline = r"^Hotline[:\.]?\s*\d+([\.,\s]\d+)*"
  paWebsite = r"www\.\S+\.(vn|com)$"
  paTitleGia = r"^(VAT|SAN PHAM|GIA TRI)"
  paGia = r"[-]?\d+([\.,]\d{2,3})*(d|đ)?"
  paTongTienHang = r"^[=]?\s*Tong Tien Hang"
  paTongCong = r"^[=]?\s*TONG C[O\s]NG"
  paSoLuongMatHang = r"^So [lL]uong mat hang\s*[:]?(\s*\d+)?"
  paTienMat = r"^TIEN MAT \(VND\)"
  paTienThoiLai = r"^TIEN THOI LAI"
  paThuNgan = r"^Th. ngan\s*[:]?\s*\S+"
  paQuay = r"Quay\s*[:]?\s*\d+"
  paTicket = r"^Ticket\s*[:]?\s*\d+"
  paThoigian = r"\d{2}[\/7]\d{2}[\/7]\d{4}\s*\d{2}[:]\d{2}[:]\d{2}"

  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for i in range(len(lLines)):
    if i >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif i >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[i]
    lID = [i - 1, i + 1, i - 2, i + 2]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[i])

    if infos.congty == "" and re.search(paCty, info):
      infos.congty = info

    if infos.shop == "" and re.search(paShop, info):
      infos.shop = info
      infoS = lLines[i + 1]
      if re.search(paDiachi, infoS):
        infos.diachi = normalDiachi(infoS)
      else:
        infoS = lLines[i + 2]
        if re.search(paDiachi, infoS):
          infos.diachi = normalDiachi(infoS)

    if infos.masothue == "" and re.search(paMaSoThue, info):
      infos.masothue = info

    if infos.sdt == "" and re.search(paSDT, info):
      infos.sdt = normalSDT(info)

    if infos.hotline == "" and re.search(paHotline, info):
      infos.hotline = info

    if infos.title == "" and re.search(paTitle, info):
      infos.title = info
      idTitle = i

    if re.search(paTitleGia, info):
      titleGia = info
      idGia = i
      
    if infos.tongtienhang == "" and re.search(paTongTienHang, info):
      infos.tongtienhang = info
      idTongTien = i
      d1 = L + (int)((R - L)/3)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongtienhang += " | " + tongtien
        lLines[iTT] = ""

    if infos.tongcong == "" and re.search(paTongCong, info):
      infos.tongcong = info
      if idTongTien == 0:
        idTongTien = i
      d1 = L + (int)((R - L)/3)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongcong += " | " + tongtien
        lLines[iTT] = ""

    if infos.soluongmathang == "" and re.search(paSoLuongMatHang, info):
      infos.soluongmathang = info
      d1 = rt
      d2 = R
      soluong, iSL = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iSL > 0:
        infos.soluongmathang += " | " + soluong
        lLines[iSL] = ""

    if infos.tienmat == "" and re.search(paTienMat, info):
      infos.tienmat = info
      d1 = L + (int)((R - L)/3)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tienmat += " | " + tongtien
        lLines[iTT] = ""

    if infos.tienthoilai == "" and re.search(paTienThoiLai, info):
      infos.tienthoilai = info
      d1 = L + (int)((R - L)/3)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tienthoilai += " | " + tongtien
        lLines[iTT] = ""

  if idGia == 0:
    idGia = idTitle
  if idTongTien == 0:
    idTongTien = len(lLines)
  
  for i in range(idTongTien, len(lLines)):
    info = lLines[i]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[i])

    if re.search(paWebsite, info):
      infos.website = info

    ma = re.search(paThuNgan, info)
    if ma:
      infos.thungan = ma.group()
    
    ma = re.search(paQuay, info)
    if ma:
      infos.quay = ma.group()

    ma = re.search(paTicket, info)
    if ma:
      infos.ticket = ma.group()
    
    ma = re.search(paThoigian, info)
    if ma:
      infos.thoigian = ma.group()

  extractSanPhamBigC(infos, lLines, lBoxes, idGia, idTongTien)
    
  return infos

class InfosCoopMart:

  def __init__(self):
        self.shop = ""
        self.title = ""
        self.diachi = ""
        self.sdt = ""
        self.fax = ""
        self.hotline = ""
        self.email = ""
        self.website = ""
        self.masothue = ""
        self.sanpham = []
        self.mahang = []
        self.vat = []
        self.soluong = []
        self.dongia = []
        self.gia = []
        self.tongtienhang = ""
        self.soluongmathang = ""
        self.nhanvien = ""
        self.quay = ""
        self.sohd = ""
        self.thoigian = ""

  def showInfos(self):
    print(self.shop)
    print(self.diachi)
    print(self.masothue)
    print(self.sdt)
    print(self.fax)
    print(self.hotline)
    print(self.email)
    print(self.website)
    print(self.title)
    print(self.tongtienhang)
    print(self.soluongmathang)
    print(self.nhanvien)
    print(self.quay)
    print(self.sohd)
    print(self.thoigian)
    
    for i in range(len(self.sanpham)):
      print(self.mahang[i] + "\t" + self.sanpham[i] + "\t" + self.vat[i] + "\t" + self.soluong[i] + "\t" + self.dongia[i] + "\t" + self.gia[i])

    return

def extractSanPhamCoopMart(infos, lLines, lBoxes, idB, idE):
  
  paVAT = r"^VAT"
  paMaHang = r"^\d{13,15}"
  paGia = r"[-]?\d+([\.,]\d{2,3})+(d|đ)?[vV]?$"
  paSoLuong = r"^\d+([\.,]\d{2,3})*"
  
  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for id in range(idB, idE):
    if id >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif id >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[id]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
    ma = re.search(paMaHang, info)
    if lt < L1 + (int)((R1 - L1) / 5) and ma:
      mahang = ma.group()
      sanpham = re.sub(r"^\d+\s*", "", info)
      if sanpham == "":
        d1 = rt
        d2 = L + (int)((R - L)/2)
        lID = [id - 1, id + 1]
        sanpham, iSP = searchPatternM(r"^\S+(\s\S+)+", id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
        if iSP > 0:
          lLines[iSP] = ""

      soluong = "1"
      vat = ""
      gia = ""
      dongia = ""

      d1 = L
      d2 = L + (int)((R - L)/5)
      lID = [id + 1, id + 2, id + 3, id + 4]
      vat, iV = searchPatternD(paVAT, id, lID, lLines, lBoxes, idB, idE, 2.5 * H, 40)
      if iV > 0:
        lLines[iV] = ""
        ltV, tlV, rtV, trV, rbV, brV, lbV, blV = getXY(lBoxes[iV])
        d1 = rtV
        d2 = L + (int)((R - L)/2)
        lID = [iV - 1, iV + 1, iV - 2, iV + 2]
        dongia, iDG = searchPatternH(paGia, iV, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
        
        d1 = L + (int)((R - L)/2)
        d2 = R
        if iDG > 0:
          lLines[iDG] = ""
          lID = [iDG - 1, iDG + 1, iDG - 2, iDG + 2]
          gia, iGia = searchPatternH(paGia, iDG, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
        else:
          lID = [iV - 1, iV + 1, iV - 2, iV + 2]
          gia, iGia = searchPatternH(paGia, iV, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
        if iGia > 0:
          lLines[iGia] = ""

      infos.mahang.append(mahang)
      infos.sanpham.append(sanpham)
      infos.vat.append(vat)
      infos.soluong.append(soluong)
      infos.dongia.append(dongia)
      infos.gia.append(gia)
    
  return

def extractCoopMart(lLines, lBoxes):

  infos = InfosCoopMart()

  idTitle = 0
  idGia = 0
  idTongTien = 0

  paShop = r"^Co[\.]?op\s*([Mm]art|Food) \w+(\s\w+)+"
  paDiachi = r"(Binh Duong|DN|Ha Noi|HC[MH]|Tan Phu|Thu Dau Mot|Q\.(\d+|\w+(\s\w+)*))$"
  paTitle = r"^PHIEU TINH TIEN"
  paMaSoThue = r"Ma so thue[:]?\s*[\W]?\d+"
  paSDT = r"^DT[:\.]?\s*[\(]?\d+[\)]?([\.,\s-]\d+)*"
  paFax = r"FAX[:\.]?\s*[\(]?\d+[\)]?([\.,\s-]\d+)*"
  paHotline = r"^Hotline[:\.]?\s*\d+([\.,\s]\d+)*"
  paEmail = r"^Email[:\.]?\s*\S+\.(vn|com)$"
  paWebsite = r"^Website[:\.]?\s*www\.\S+\.(vn|com)$"
  paGia = r"[-]?\d+([\.,]\d{2,3})*(d|đ)?"
  paTongTienHang = r"^Tong so tien thanh toan[:]?"
  paSoLuongMatHang = r"^Tong so luong hang\s*[:]?"
  paSoLuong = r"^\d+([\.,]\d{2,3})*"
  paNhanVien = r"^(Nhan vien|NV)\s*[:]?\s*(\w+(\s\w+)*|\d+\S*)"
  paQuay = r"Quay\s*[:]?\s*\d+"
  paSoHD = r"^So HD\s*[:]?\s*\d+"
  paThoigian = r"(Ngay\s*[:]?\s*)?\d{1,2}[\/7]\d{2}[\/7]\d{4}(\s*\d{2}[:]\d{2}([:]\d{2})?)?"

  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for i in range(len(lLines)):
    if i >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif i >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[i]
    lID = [i - 1, i + 1, i - 2, i + 2]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[i])

    if infos.shop == "" and re.search(paShop, info):
      infos.shop = info

    if infos.masothue == "" and re.search(paMaSoThue, info):
      infos.masothue = info
      infoS = lLines[i + 1]
      if re.search(paDiachi, infoS):
        infos.diachi = infoS

    ma = re.search(paSDT, info)
    if ma:
      infos.sdt = ma.group()
      ma = re.search(paFax, info)
      if ma:
        infos.fax = ma.group()

    if infos.hotline == "" and re.search(paHotline, info):
      infos.hotline = info

    if infos.email == "" and re.search(paEmail, info):
      infos.email = info

    if infos.website == "" and re.search(paWebsite, info):
      infos.website = info

    if infos.title == "" and re.search(paTitle, info):
      infos.title = info
      idTitle = i
    
    if idTongTien == 0:
      ma = re.search(paQuay, info)
      if ma:
        infos.quay = ma.group()

      ma = re.search(paThoigian, info)
      if ma:
        infos.thoigian = ma.group()

      ma = re.search(paNhanVien, info)
      if ma:
        infos.nhanvien = ma.group()
        idGia = i

      ma = re.search(paSoHD, info)
      if ma:
        infos.sohd = ma.group()
        if idGia < i:
          idGia = i

    if infos.tongtienhang == "" and re.search(paTongTienHang, info):
      infos.tongtienhang = info
      idTongTien = i
      d1 = L + (int)((R - L)/3)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongtienhang += " | " + tongtien
        lLines[iTT] = ""

    if infos.soluongmathang == "" and re.search(paSoLuongMatHang, info):
      infos.soluongmathang = info
      if idTongTien == 0:
        idTongTien = i
      d1 = rt
      d2 = R
      soluong, iSL = searchPatternM(paSoLuong, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iSL > 0:
        infos.soluongmathang += " | " + soluong
        lLines[iSL] = ""

  if idGia == 0:
    idGia = idTitle
  if idTongTien == 0:
    idTongTien = len(lLines)
  
  extractSanPhamCoopMart(infos, lLines, lBoxes, idGia, idTongTien)
    
  return infos


class InfosVinCommerce:

  def __init__(self):
        self.shop = ""
        self.title = ""
        self.diachi = ""
        self.sdt = ""
        self.hotline = ""
        self.website = ""
        self.sanpham = []
        self.mahang = []
        self.soluong = []
        self.dongia = []
        self.gia = []
        self.tongtienhang = ""
        self.tienkhachtra = ""
        self.nhanvien = ""
        self.quay = ""
        self.sohd = ""
        self.thoigian = ""

  def showInfos(self):
    print(self.shop)
    print(self.diachi)
    print(self.sdt)
    print(self.hotline)
    print(self.website)
    print(self.title)
    print(self.tongtienhang)
    print(self.tienkhachtra)
    print(self.nhanvien)
    print(self.quay)
    print(self.sohd)
    print(self.thoigian)
    
    for i in range(len(self.sanpham)):
      print(self.mahang[i] + "\t" + self.sanpham[i] + "\t" + self.soluong[i] + "\t" + self.dongia[i] + "\t" + self.gia[i])

    return

def extractSanPhamVinCommerce(infos, lLines, lBoxes, idB, idE):
  
  paMaHang = r"^\d{12,13}"
  paGia = r"[-]?\d+([\.,]\d{2,3})+(d|đ)?[vV]?$"
  paSoLuong = r"^\d+([\.,]\d{2,3})"
  
  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for id in range(idB, idE):
    if id >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif id >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[id]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
    lID = [id - 1, id + 1, id - 2, id + 2]
    ma = re.search(paMaHang, info)
    if lt < L + (int)((R - L) / 5) and ma:
      mahang = ma.group()

      lSP = [id - 1, id - 2, id - 3, id - 4, id - 5]
      sanpham, iSP = searchPatternU(r"^[\w\W]+$", id, lSP, lLines, lBoxes, idB, idE, 2 * H, 50)
      #sanpham, idSP = searchSanPhamVinCommerce(id, lLines, lBoxes)
      if iSP > 0:
        lLines[iSP] = ""

      soluong = "1"
      gia = ""
      dongia = ""

      d1 = L + (int)((R - L) / 5)
      d2 = L + (int)(3*(R - L) / 5)
      dongia, iDG = searchPatternH(paGia, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
      if iDG > 0:
        lLines[iDG] = ""
      
      d1 = L + (int)(3*(R - L) / 5)
      d2 = R
      soluong, iSL = searchPatternH(paSoLuong, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
      if iSL > 0:
        lLines[iSL] = ""
      
      d1 = L + (int)(3*(R - L) / 5)
      d2 = R
      gia, iGia = searchPatternH(paGia, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
      if iGia > 0:
        lLines[iGia] = ""

      infos.mahang.append(mahang)
      infos.sanpham.append(sanpham)
      infos.soluong.append(soluong)
      infos.dongia.append(dongia)
      infos.gia.append(gia)
    
  return

def extractVinCommerce(lLines, lBoxes):

  infos = InfosVinCommerce()

  idTitle = 0
  idGia = 0
  idTongTien = 0

  paShop = r"^VM\+"
  paDiachi = r"(Đà Nẵng|Hà Nội,HN)$"
  paTitle = r"^H[OÓ][AÁ] ĐƠN BÁN HÀNG"
  paTitleGia = r"(Mặt hàng|Đơn giá|SL|T\.Tiền)"
  paGia = r"[-]?\d+([\.,]\d{2,3})+(d|đ)?[vV]?$"
  paSDT = r"^\d+{10}$"
  paHotline = r"^Hotline[:\.]?\s*\d+([\.,\s]\d+)*"
  paWebsite = r"(Websi[\s]?te)?[:\.]?\s*[w]?ww\.\S+\.(vn|com)$"
  paTongTienHang = r"^[T]?[ÔỔ]NG TI[ÊỀẾ]N PH[AẢ]I [T1].[\s]?TOÁN[:]?"
  paTienKhachTra = r"^TI[ÊỀẾ]N KH[AÁ]CH TR[ẢAA]\s*[:]?"
  paNhanVien = r"N[:V]BH\s*[:]?\s*(\w+(\s\w+)*|\d+\S*)"
  paQuay = r"Qu[âầấ]y\s*[:]?\s*\d+"
  paSoHD = r"^HĐ\s*[:]?\s*\d+"
  paThoigian = r"Ngày bán\s*[:]?\s*\d{1,2}([:]\d)?[\/]\d{2}[\/]\d{4}\s*(\d{2}[:])?(\d{2}[:]\d{2})?"

  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for i in range(len(lLines)):
    if i >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif i >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[i]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[i])
    lID = [i - 1, i + 1, i - 2, i + 2]

    if infos.shop == "" and re.search(paShop, info):
      infos.shop = info

    if infos.diachi == "" and re.search(paDiachi, info):
      infos.diachi = info

    if infos.title == "" and re.search(paTitle, info):
      infos.title = info
      idTitle = i
    
    if infos.thoigian == "" and re.search(paThoigian, info):
      infos.thoigian = info
    
    if infos.sohd == "" and re.search(paSoHD, info):
      infos.sohd = info

    if infos.quay == "" and re.search(paQuay, info):
      infos.quay = info

    if infos.nhanvien == "" and re.search(paNhanVien, info):
      infos.nhanvien = info
    
    if re.search(paTitleGia, info):
      idGia = i

    if infos.tongtienhang == "" and re.search(paTongTienHang, info):
      infos.tongtienhang = info
      idTongTien = i
      d1 = L + (int)((R - L)/3)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongtienhang += " | " + tongtien
        lLines[iTT] = ""

    if infos.tienkhachtra == "" and re.search(paTienKhachTra, info):
      infos.tienkhachtra = info

      d1 = L + (int)((R - L)/3)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        if idTongTien == 0:
          idTongTien = iTT
        infos.tienkhachtra += " | " + tongtien
        lLines[iTT] = ""
        
    if idTongTien > 0:
      ma = re.search(paHotline, info)
      if infos.hotline == "" and ma:
        infos.hotline = ma.group()

      ma = re.search(paWebsite, info)
      if infos.website == "" and ma:
        infos.website = ma.group()

  if idGia == 0:
    idGia = idTitle
  if idTongTien == 0:
    idTongTien = len(lLines)
  
  extractSanPhamVinCommerce(infos, lLines, lBoxes, idGia, idTongTien)
    
  return infos


class InfosLotteMart:

  def __init__(self):
        self.congty = ""
        self.shop = ""
        self.diachi = ""
        self.sdt = ""
        self.hotline = ""
        self.website = ""
        self.mst = ""
        self.sanpham = []
        self.mahang = []
        self.soluong = []
        self.dongia = []
        self.gia = []
        self.tongtienhang = ""
        self.tienkhachtra = ""
        self.tienthua = ""
        self.nhanvien = ""
        self.quanly = ""
        self.quay = ""
        self.sohd = ""
        self.thoigian = ""

  def showInfos(self):
    print(self.congty)
    print(self.shop)
    print(self.diachi)
    print(self.sdt)
    print(self.hotline)
    print(self.website)
    print(self.mst)
    print(self.tongtienhang)
    print(self.tienkhachtra)
    print(self.tienthua)
    print(self.nhanvien)
    print(self.quanly)
    print(self.quay)
    print(self.sohd)
    print(self.thoigian)
    
    for i in range(len(self.sanpham)):
      print(self.mahang[i] + "\t" + self.sanpham[i] + "\t" + self.soluong[i] + "\t" + self.dongia[i] + "\t" + self.gia[i])

    return

def extractSanPhamLotteMart(infos, lLines, lBoxes, idB, idE):
  
  paMaHang = r"^\d{12,13}"
  paGia = r"^[-]?\d+([\.,]\d{2,3})+(\s\d+([\.,]\d{2,3})+)?(d|đ)?$"
  paSoLuong = r"^\d+$"
  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for id in range(idB, idE):
    if id >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif id >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[id]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])

    ma = re.search(paMaHang, info)
    if lt < L + (int)(2 * (R - L) / 5) and ma:
      mahang = ma.group()
      soluong = "1"
      gia = ""
      dongia = ""
      iDonGia = 0

      dongia = info.replace(mahang, "")
      dongia = re.sub(r"^\s*", "", dongia)

      lID = [id - 1, id - 2, id - 3, id - 4, id - 5]
      sanpham, iSP = searchPatternU(r"^[\w\W]+$", id, lID, lLines, lBoxes, idB, idE, 2 * H, 75) 
      if iSP > 0:
        lLines[iSP] = ""

      if dongia == "":
        d1 = rt
        d2 = L + (int)(3 * (R - L) / 5)
        lID = [id - 1, id + 1, id - 2, id + 2]
        dongia, iDG = searchPatternH(paGia, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
        if iDG > 0:
          lLines[iDG] = ""
      
      d1 = L + (int)(3 * (R - L) / 5)
      d2 = R
      lID = [id - 1, id + 1, id - 2, id + 2]
      soluong, iSL = searchPatternH(paSoLuong, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
      if iSL > 0:
        lLines[iSL] = ""
      
      if gia == "":
        d1 = L + (int)(3 * (R - L) / 5)
        d2 = R
        lID = [id - 1, id + 1, id - 2, id + 2]
        gia, iGia = searchPatternH(paGia, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
        if iGia > 0:
          lLines[iGia] = ""

      infos.mahang.append(mahang)
      infos.sanpham.append(sanpham)
      infos.soluong.append(soluong)
      infos.dongia.append(dongia)
      infos.gia.append(gia)
    
  return

def extractLotteMart(lLines, lBoxes):

  infos = InfosLotteMart()

  idTitle = 0
  idGia = 0
  idTongTien = 0

  paCongty = r"^CTY CO PHAN TTT[MN] LOTTE"
  paShop = r"^LO[TI][TI]E Mart \w+"
  paTitleGia = r"^(Ma so|dgia|sl|so tien)$"
  paGia = r"^[-]?\d+([\.,]\d{2,3})+(\s\d+([\.,]\d{2,3})+)?(d|đ)?$"
  paSDT = r"[DĐ]T[:]?\s*(\(\d+\))?\d+([\.\s]\d+)*"
  paHotline = r"Hotline[:\.]?\s*\d+([\.,\s]\d+)*"
  paWebsite = r"^Website[:\.]?\s*www\.\S+\.(vn|com)$"
  paMST = r"^MST[:]?\s*\d{4}[\s]?\d{3}[\s]?\d{3}$"
  paTongTienHang = r"^Tong cong"
  paTienKhachTra = r"^So tien da nhan\s*[:]?"
  paTienThua = r"^Tien mat thua\s*[:]?"
  paNhanVien = r"^CASHIER\s*[:]?\s*\w*"
  paQuanLy = r"^MANAGER\s*[:]?\s*\w*"
  paSoHD = r"POS\s*[:]?\s*\d+([-]\d+)?"
  paThoigian = r"([\S]?ENT[\S]?\s*)?\d{4}[-]\d{2}[-]\d{2}(\s*\d{2}[:]\d{2}([:]\d{2})?)?"

  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for i in range(len(lLines)):
    if i >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif i >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[i]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[i])
    lID = [i - 1, i + 1, i - 2, i + 2]

    if infos.congty == "" and re.search(paCongty, info):
      infos.congty = info

    if infos.shop == "" and re.search(paShop, info):
      infos.shop = info
      infoS = lLines[i + 1]
      if checkDiachi(infoS):
        infos.diachi = infoS

    ma = re.search(paSDT, info)
    if infos.sdt == "" and ma:
      infos.sdt = ma.group()

    ma = re.search(paHotline, info)
    if infos.hotline == "" and ma:
      infos.hotline = ma.group()
    
    if infos.mst == "" and re.search(paMST, info):
      infos.mst = info

    if infos.nhanvien == "" and re.search(paNhanVien, info):
      infos.nhanvien = info
      d1 = rt
      d2 = rt + 4 * H
      nhanvienS, iNV = searchPatternH(r"^\S+(\s+\S+)*", i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iNV >= 0:
        infos.nhanvien += " " + nhanvienS
        lLines[iNV] = ""

    if infos.quanly == "" and re.search(paQuanLy, info):
      infos.quanly = info
      d1 = rt
      d2 = rt + 4 * H
      quanlyS, iQL = searchPatternH(r"^\S+(\s+\S+)*", i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iQL >= 0:
        infos.quanly += " " + quanlyS
        lLines[iQL] = ""

    ma = re.search(paThoigian, info)
    if infos.thoigian == "" and ma:
      infos.thoigian = ma.group()

    ma = re.search(paSoHD, info)
    if infos.sohd == "" and ma:
      infos.sohd = ma.group()
    
    if idGia == 0 and re.search(paTitleGia, info):
      idGia = i

    if infos.tongtienhang == "" and re.search(paTongTienHang, info):
      infos.tongtienhang = info
      idTongTien = i
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongtienhang += " | " + tongtien
        lLines[iTT] = ""

    if infos.tienkhachtra == "" and re.search(paTienKhachTra, info):
      infos.tienkhachtra = info
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        if idTongTien == 0:
          idTongTien = iTT
        infos.tienkhachtra += " | " + tongtien
        lLines[iTT] = ""
        
    if infos.tienthua == "" and re.search(paTienThua, info):
      infos.tienthua = info
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        if idTongTien == 0:
          idTongTien = iTT
        infos.tienthua += " | " + tongtien
        lLines[iTT] = ""

    if idTongTien > 0:
      if re.search(paWebsite, info):
        infos.website = info

  if idGia == 0:
    idGia = idTitle
  if idTongTien == 0:
    idTongTien = len(lLines)
  
  extractSanPhamLotteMart(infos, lLines, lBoxes, idGia, idTongTien)
    
  return infos


class InfosBachHoaXanh:

  def __init__(self):
        self.diachi = ""
        self.website = ""
        self.title = ""
        self.sanpham = []
        self.soluong = []
        self.dongia = []
        self.gia = []
        self.tongtienhang = ""
        self.tiengiam = ""
        self.nhanvien = ""
        self.sohd = ""
        self.thoigian = ""

  def showInfos(self):
    print(self.diachi)
    print(self.website)
    print(self.title)
    print(self.tongtienhang)
    print(self.tiengiam)
    print(self.nhanvien)
    print(self.sohd)
    print(self.thoigian)
    
    for i in range(len(self.sanpham)):
      print(self.sanpham[i] + "\t" + self.soluong[i] + "\t" + self.dongia[i] + "\t" + self.gia[i])

    return

def extractSanPhamBachHoaXanh(infos, lLines, lBoxes, idB, idE):
  
  paGia = r"^[-]?\d+([\.,]\d{2,3})*(d|đ)?$"

  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for id in range(idB, idE):
    if id >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif id >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[id]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
    lID = [id - 1, id +1, id - 2, id + 2]
    if lt < L + (int)(2 * (R - L) / 5) and re.search(r"\S+(\s+\S+)+", info):
      sanpham = info
      soluong = "1"
      gia = ""
      dongia = ""
      
      if dongia == "":
        d1 = L + (int)((R - L) / 5)
        d2 = L + (int)(3 * (R - L) / 5)
        lDG = [id + 1, id + 2, id + 3, id + 4]
        dongia, iDG = searchPatternD2(paGia, id, lDG, lLines, lBoxes, idB, idE, 2 * H, d1, d2)
        if iDG > 0:
          lLines[iDG] = ""

      if gia == "":
        d1 = L + (int)(3 * (R - L) / 5)
        d2 = R
        lGia = [id + 1, id + 2, id + 3, id + 4]
        gia, iGia = searchPatternD2(paGia, id, lGia, lLines, lBoxes, idB, idE, 2 * H, d1, d2)
        if iGia > 0:
          lLines[iGia] = ""

      infos.sanpham.append(sanpham)
      infos.soluong.append(soluong)
      infos.dongia.append(dongia)
      infos.gia.append(gia)
    
  return

def extractBachHoaXanh(lLines, lBoxes):

  infos = InfosBachHoaXanh()

  idTitle = 0
  idGia = 0
  idTongTien = 0

  paTitle = r"^PHIẾU THANH TOÁN"
  paTitleGia = r"^(SL|Giá bán|T.\s*Tiền)$"
  paGia = r"^[-]?\d+([\.,]\d{2,3})+(\s\d+([\.,]\d{2,3})+)?(d|đ)?$"
  paWebsite = r"^(Website[:\.]?\s*)?www\.\S+\.(vn|com)$"
  paTongTienHang = r"^Tổng t[il]ền\s*[:]?"
  paTienGiam = r"^Đã giảm\s*[:]?"
  paNhanVien = r"^Nhân viên\s*[:]?\s*\w*"
  paSoHD = r"^Số CT\s*[:]?"
  paThoigian = r"^Ngày CT\s*[:]?\s*(\d{2}[-/]\d{2}[-/]\d{4}(\s*\d{2}[:]\d{2}([:]\d{2})?)?)?"
  
  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for i in range(len(lLines)):
    if i >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif i >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[i]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[i])
    lID = [i - 1, i + 1, i - 2, i + 2]

    if re.search(paWebsite, info):
      infos.website = info
      infoS = lLines[i + 1]
      if checkDiachi(infoS):
        infos.diachi = infoS
        infoS2 = lLines[i + 2]
        if checkDiachi(infoS2):
          infos.diachi += " " + infoS2
    
    if re.search(paTitle, info):
      infos.title = info
      idTitle = i
    
    if infos.sohd == "" and re.search(paSoHD, info):
      infos.sohd = info
      d1 = rt
      d2 = rt + 5 * H
      sohdS, iHD = searchPatternH(r"^[\w\W]+$", i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iHD >= 0:
        infos.sohd += " " + sohdS
        lLines[iHD] = ""
    
    if infos.nhanvien == "" and re.search(paNhanVien, info):
      infos.nhanvien = info
      d1 = rt
      d2 = rt + 4 * H
      nhanvienS, iNV = searchPatternH(r"^[\w\W]+$", i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iNV >= 0:
        infos.nhanvien += " " + nhanvienS
        lLines[iNV] = ""
    
    if infos.thoigian == "" and re.search(paThoigian, info):
      infos.thoigian = info
      d1 = rt
      d2 = rt + 4 * H
      thoigianS, iTG = searchPatternH(r"^\S+(\s+\S+)*", i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTG >= 0:
        infos.thoigian += " " + thoigianS
        lLines[iTG] = ""
    
    if idGia == 0 and re.search(paTitleGia, info):
      idGia = i
    
    if infos.tongtienhang == "" and re.search(paTongTienHang, info):
      infos.tongtienhang = info
      idTongTien = i
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongtienhang += " | " + tongtien
        lLines[iTT] = ""
        
    if infos.tiengiam == "" and re.search(paTienGiam, info):
      infos.tiengiam = info
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        if idTongTien == 0:
          idTongTien = iTT
        infos.tiengiam += " | " + tongtien
        lLines[iTT] = ""

  if idGia == 0:
    idGia = idTitle
  if idTongTien == 0:
    idTongTien = len(lLines)
  
  extractSanPhamBachHoaXanh(infos, lLines, lBoxes, idGia, idTongTien)
    
  return infos


class InfosLMart:

  def __init__(self):
        self.congty = ""
        self.diachi = ""
        self.sdt = ""
        self.title = ""
        self.sanpham = []
        self.soluong = []
        self.dongia = []
        self.gia = []
        self.tongtienhang = ""
        self.tongthanhtoan = ""
        self.tienkhachdua = ""
        self.tiengiam = ""
        self.nhanvien = ""
        self.sohd = ""
        self.thoigian = ""

  def showInfos(self):
    print(self.congty)
    print(self.diachi)
    print(self.sdt)
    print(self.title)
    print(self.tongtienhang)
    print(self.tongthanhtoan)
    print(self.tienkhachdua)
    print(self.nhanvien)
    print(self.sohd)
    print(self.thoigian)
    
    for i in range(len(self.sanpham)):
      print(self.sanpham[i] + "\t" + self.soluong[i] + "\t" + self.dongia[i] + "\t" + self.gia[i])

    return

def extractSanPhamLMart(infos, lLines, lBoxes, idB, idE):
  
  paGia = r"^[-]?\d+([\.,]\d{2,3})*(d|đ)?$"

  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for id in range(idB, idE):
    if id >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif id >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[id]
    lID = [id - 1, id + 1, id - 2, id + 2]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
    if lt < L + (int)(3 * (R - L) / 5) and checkGia(info):
      dongia = info
      soluong = "1"
      sanpham = ""
      gia = ""
      
      d1 = L + (int)(3 * (R - L) / 5)
      d2 = R
      lID = [id - 1, id + 1, id - 2, id + 2]
      gia, iGia = searchPatternH(paGia, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
      if iGia > 0:
        lLines[iGia] = ""

      d1 = L
      d2 = L + (int)(3 * (R - L) / 5)
      lID = [id - 2, id - 1, id + 1, id + 2]
      sanpham, iSP = searchPatternH(r"^\S+(\s+\S+)+", id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
      if iSP > 0:
        lLines[iSP] = ""
        lSP = [iSP + 1, iSP + 2, iSP + 3, iSP + 4, iSP + 5]
        sanphamS, iSPs = searchPatternD(r"^[\w\W]+$", iSP, lSP, lLines, lBoxes, idB, idE, 2 * H, 50)
        if iSPs > 0:
          sanpham += " " + sanphamS
          lLines[iSPs] = ""

      infos.sanpham.append(sanpham)
      infos.soluong.append(soluong)
      infos.dongia.append(dongia)
      infos.gia.append(gia)
    
  return

def extractLMart(lLines, lBoxes):

  infos = InfosLMart()

  idTitle = 0
  idGia = 0
  idTongTien = 0

  paCongty = r"Hệ thống Siêu Thị L-MART"
  paTitle = r"^H[OÓ][AÁ] ĐƠN BÁN HÀNG"
  paTitleGia = r"^(Mặt hàng|Giá|S\.L|T\.\s*Tiền)$"
  paGia = r"^[-]?\d+([\.,]\d{2,3})*(d|đ)?$"
  paSDT = r"^[DĐ]T[:\.]?\s*\d+$"
  paTongTienHang = r"^Tổng tiền hàng\s*[:]?"
  paTongThanhToan = r"^Tổng thanh toán\s*[:]?"
  paTienKhachDua = r"^Tiền khách đưa\s*[:]?"
  paNhanVien = r"^Nhân viên\s*[:]?\s*\w*"
  paSoHD = r"^Số HĐ\s*[:]?\s*\w+"
  paThoigian = r"Ngày\s*[:]?\s*(\d{2}[-/]\d{2}[-/]\d{4}(\s*\d{2}[:]\d{2}([:]\d{2})?)?)?"
  
  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for i in range(len(lLines)):
    if i > 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif i > n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[i]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[i])
    lID = [i - 1, i + 1, i - 2, i + 2]

    if re.search(paCongty, info):
      infos.congty = info
      infoS = lLines[i + 1]
      if checkDiachi(infoS):
        infos.diachi = infoS
    
    if re.search(paSDT, info):
      infos.sdt = info

    if re.search(paTitle, info):
      infos.title = info
      idTitle = i
    
    ma = re.search(paSoHD, info)
    if infos.sohd == "" and ma:
      infos.sohd = ma.group()
    
    ma = re.search(paThoigian, info)
    if infos.thoigian == "" and ma:
      infos.thoigian = ma.group()

    if infos.nhanvien == "" and re.search(paNhanVien, info):
      infos.nhanvien = info
      
    if idGia == 0 and re.search(paTitleGia, info):
      idGia = i
    
    if infos.tongtienhang == "" and re.search(paTongTienHang, info):
      infos.tongtienhang = info
      idTongTien = i
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongtienhang += " | " + tongtien
        lLines[iTT] = ""
        
    if infos.tongthanhtoan == "" and re.search(paTongThanhToan, info):
      infos.tongthanhtoan = info
      if idTongTien == 0:
          idTongTien = iTT
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongthanhtoan += " | " + tongtien
        lLines[iTT] = ""

    if infos.tienkhachdua == "" and re.search(paTienKhachDua, info):
      infos.tienkhachdua = info
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tienkhachdua += " | " + tongtien
        lLines[iTT] = ""

  if idGia == 0:
    idGia = idTitle
  if idTongTien == 0:
    idTongTien = len(lLines)
  
  extractSanPhamLMart(infos, lLines, lBoxes, idGia, idTongTien)
    
  return infos


class InfosEMart:

  def __init__(self):
        self.congty = ""
        self.diachi = ""
        self.sdt = ""
        self.mst = ""
        self.mahang = []
        self.sanpham = []
        self.soluong = []
        self.dongia = []
        self.gia = []
        self.tongtienhang = ""
        self.tongthanhtoan = ""
        self.tongluonghang = ""
        self.nhanvien = ""
        self.manv = ""
        self.thoigian = ""
        self.pos = ""

  def showInfos(self):
    print(self.congty)
    print(self.diachi)
    print(self.sdt)
    print(self.mst)
    print(self.tongtienhang)
    print(self.tongthanhtoan)
    print(self.tongluonghang)
    print(self.nhanvien)
    print(self.manv)
    print(self.thoigian)
    print(self.pos)
    
    for i in range(len(self.sanpham)):
      print(self.mahang[i] + "\t" + self.sanpham[i] + "\t" + self.soluong[i] + "\t" + self.dongia[i] + "\t" + self.gia[i])

    return

def extractSanPhamEMart(infos, lLines, lBoxes, idB, idE):
  
  paMaHang = r"^\d{12,13}"
  paGia = r"^[-]?\d+([\.,]\d{2,3})*(d|đ)?$"
  paSoLuong = r"^\d+([\.,]\d{2,3})?"

  L= L1
  R = R1
  rate = rate1
  n = len(lLines)
  for id in range(idB, idE):
    if id >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif id >= n / 3:
      L = L2
      R = R2
      rate = rate2

    info = lLines[id]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[id])
    lID = [id - 1, id + 1, id - 2, id + 2]
    ma = re.search(paMaHang, info)
    if lt < L + (int)((R - L) / 5) and ma:
      mahang = ma.group()
      lSP = [id - 1, id - 2, id - 3, id - 4, id - 5]
      sanpham, iSP = searchPatternU(r"^[\w\W]+$", id, lSP, lLines, lBoxes, idB, idE, 2 * H, 50)
      if iSP > 0:
        lLines[iSP] = ""

      soluong = "1"
      gia = ""
      dongia = ""

      d1 = L + (int)((R - L) / 5)
      d2 = L + (int)(3*(R - L) / 5)
      dongia, iDG = searchPatternH(paGia, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
      if iDG > 0:
        lLines[iDG] = ""
        d1 = L + (int)(3*(R - L) / 4)
        d2 = R
        lGia = [iDG - 1, iDG + 1, iDG - 2, iDG + 2]
        gia, iGia = searchPatternH(paGia, iDG, lGia, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
        if iGia > 0:
          lLines[iGia] = ""

      d1 = L + (int)(3*(R - L) / 5)
      d2 = R
      soluong, iSL = searchPatternH(paSoLuong, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
      if iSL > 0:
        lLines[iSL] = ""
      
      if gia == "":
        d1 = L + (int)(3*(R - L) / 4)
        d2 = R
        gia, iGia = searchPatternH(paGia, id, lID, lLines, lBoxes, idB, idE, L, R, H, rate, d1, d2)
        if iGia > 0:
          lLines[iGia] = ""

      infos.mahang.append(mahang)
      infos.sanpham.append(sanpham)
      infos.soluong.append(soluong)
      infos.dongia.append(dongia)
      infos.gia.append(gia)
    
  return

def extractEMart(lLines, lBoxes):

  infos = InfosEMart()

  idTitle = 0
  idGia = 0
  idTongTien = 0

  paCongty = r"^Emart \w+(\s\w+)+$"
  paTitleGia = r"^(Tên sản phẩm|Đơn giá|S\.L|Số tiền)$"
  paGia = r"^[-]?\d+([\.,]\d{2,3})*(d|đ)?$"
  paSDT = r"^Điện thoại\s*[:\.]?\s*(\(\d+\))?\s*\d+(\s\d+)*"
  paMST = r"^Mã số thuế\s*[:]?\s*\d+"
  paTongTienHang = r"^Tổng số$"
  paTongThanhToan = r"^Số tiền sẽ nhận"
  paTongLuongHang = r"^Tổng số hàng Số lượng\s*[:]?"
  paNhanVien = r"Cashier\s*[:]?\s*[\w\W]+$"
  paMaNV = r"^NO\s*[:]?\s*\d+"
  paThoigian = r"\d{2}[-/]\d{2}[-/]\d{4}(\s*\d{2}[:]\d{2}([:]\d{2})?)?"
  paPOS = r"POS\s*[:]?\s*\d{4}[-]\d{4}"
  
  L = L1
  R = R1
  rate = rate1
  n = len(lLines)
  for i in range(len(lLines)):
    if id >= 2 * n / 3:
      L = L3
      R = R3
      rate = rate3
    elif id >= n / 3:
      L = L2
      R = R2
      rate = rate2
    
    info = lLines[i]
    lt, tl, rt, tr, rb, br, lb, bl = getXY(lBoxes[i])
    lID = [i - 1, i + 1, i - 2, i + 2]
    if re.search(paCongty, info):
      infos.congty = info
    
    if re.search(paSDT, info):
      infos.sdt = info
    if re.search(paMST, info):
      infos.mst = info

    if checkDiachi(info):
      infos.diachi = info
      d1 = L1
      d2 = lt
      diachiS, iDC = searchPatternH(r"^[\w\W]+$", i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iDC > 0:
        infos.diachi = diachiS + " " + infos.diachi
            
    ma = re.search(paThoigian, info)
    if infos.thoigian == "" and ma:
      infos.thoigian = ma.group()
    if re.search(paPOS, info):
      infos.pos = info
    
    ma = re.search(paNhanVien, info)
    if infos.nhanvien == "" and ma:
      infos.nhanvien = ma.group()
    ma = re.search(paMaNV, info)
    if infos.manv == "" and ma:
      infos.manv = ma.group()

    if idGia == 0 and re.search(paTitleGia, info):
      idGia = i
    
    if infos.tongtienhang == "" and re.search(paTongTienHang, info):
      infos.tongtienhang = info
      idTongTien = i
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongtienhang += " | " + tongtien
        lLines[iTT] = ""
        
    if infos.tongthanhtoan == "" and re.search(paTongThanhToan, info):
      infos.tongthanhtoan = info
      if idTongTien == 0:
          idTongTien = iTT
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongthanhtoan += " | " + tongtien
        lLines[iTT] = ""

    if infos.tongluonghang == "" and re.search(paTongLuongHang, info):
      infos.tongluonghang = info
      d1 = L + (int)((R - L)/2)
      d2 = R
      tongtien, iTT = searchPatternM(paGia, i, lID, lLines, lBoxes, 0, n, L, R, H, rate, d1, d2)
      if iTT > 0:
        infos.tongluonghang += " | " + tongtien
        lLines[iTT] = ""

  if idGia == 0:
    idGia = idTitle
  if idTongTien == 0:
    idTongTien = len(lLines)
  
  extractSanPhamEMart(infos, lLines, lBoxes, idGia, idTongTien)
    
  return infos

def crop(pts, image):

    """
    Takes inputs as 8 points
    and Returns cropped, masked image with a white background
    """
    rect = cv2.boundingRect(pts)
    x,y,w,h = rect
    cropped = image[y:y+h, x:x+w].copy()
    pts = pts - pts.min(axis=0)
    mask = np.zeros(cropped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
    dst = cv2.bitwise_and(cropped, cropped, mask=mask)
    bg = np.ones_like(cropped, np.uint8)*255
    cv2.bitwise_not(bg,bg, mask=mask)
    dst2 = bg + dst

    return dst2

def generate_words(image_name, score_bbox, image):

  num_bboxes = len(score_bbox)
  for num in range(num_bboxes):
    bbox_coords = score_bbox[num].split(':')[-1].split(',\n')
    if bbox_coords!=['{}']:
      l_t = float(bbox_coords[0].strip(' array([').strip(']').split(',')[0])
      t_l = float(bbox_coords[0].strip(' array([').strip(']').split(',')[1])
      r_t = float(bbox_coords[1].strip(' [').strip(']').split(',')[0])
      t_r = float(bbox_coords[1].strip(' [').strip(']').split(',')[1])
      r_b = float(bbox_coords[2].strip(' [').strip(']').split(',')[0])
      b_r = float(bbox_coords[2].strip(' [').strip(']').split(',')[1])
      l_b = float(bbox_coords[3].strip(' [').strip(']').split(',')[0])
      b_l = float(bbox_coords[3].strip(' [').strip(']').split(',')[1].strip(']'))
      pts = np.array([[int(l_t), int(t_l)], [int(r_t) ,int(t_r)], [int(r_b) , int(b_r)], [int(l_b), int(b_l)]])
      
      if np.all(pts) > 0:
        
        word = crop(pts, image)
        
        folder = '/'.join( image_name.split('/')[:-1])

        #CHANGE DIR
        dir = '/content/Lines/'

        if os.path.isdir(os.path.join(dir + folder)) == False :
          os.makedirs(os.path.join(dir + folder))

        try:
          file_name = os.path.join(dir + image_name)
          cv2.imwrite(file_name+'_{}.jpg'.format(num), word)
          print('Image saved to '+file_name+'_{}.jpg'.format(num))
        except:
          continue
          
def idHoadon(bboxes):

  idHoadon = -1

  lines = []
  boxes = []

  paAEON1 = r"^T[RH][uU]NG\W*T[AÂ]M\W*TH[UƯư][OƠơ]NG\W*[\w]?M[AẠ]I AEON"
  paAEON2 = r"^MUA HÀNG TRỰC TUYẾN"
  paAEON3 = r"^SỐ LƯỢNG MẶT HÀNG"
  paAEON4 = r"^PHƯƠNG THỨC THANH TOÁN"
  paAEON5 = r"^TỔNG THANH TOÁN"

  paBigC1 = r"^Cty TNHH TMQT-DV Sthi Big C"
  paBigC2 = r"^PHIEU TINH TIEN"
  paBigC3 = r"^=\s*TONG CONG"
  paBigC4 = r"^=\s*Tong Tien Hang"

  paCoopMart1 = r"^Co gia tri xuat Hoa don GTGT trong ngay"
  paCoopMart2 = r"^PHIEU TINH TIEN"
  paCoopMart3 = r"^Tong so tien thanh toan"
  paCoopMart4 = r"^THONG TIN KHACH HANG THAN THIET"
  
  paVinCommerce1 = r"^VinCommerce"
  paVinCommerce2 = r"^[T]?ỔNG TIỀN PHẢI T.TOÁN"
  paVinCommerce3 = r"^Tax invoice will be issued within same day"
  paVinCommerce4 = r"^Chỉ xuất hoá đơn trong ngày"

  paLotteMart1 = r"^LOTTE[\.]{1,2}MART"
  paLotteMart2 = r"^CTY CO PHAN TTT[MN] LOTTE"
  paLotteMart3 = r"^LOTTE Mart"
  paLotteMart4 = r"^So tien da nhan"
  paLotteMart5 = r"^TIET KIEM HON KHI SU DUNG THE THANH VIEN"

  paBachHoaXanh1 = r"^BÁCH HOÁ XANH"
  paBachHoaXanh2 = r"^PHIẾU THANH TOÁN"
  paBachHoaXanh3 = r"^\(Giá trên đã bao gồm thuế GTGT\)"

  paLMart1 = r"^Hệ thống Siêu Thị L-MART"
  paLMart2 = r"^HOÁ ĐƠN BÁN HÀNG"

  paEMart1 = r"^Emart$"
  paEMart2 = r"^Số tiền sẽ nhận"
  paEMart3 = r"^Tổng số hàng Số lượng\s*[:]?"

  for box_num in range(len(bboxes)):
    item = bboxes[box_num]
    l_t = float(item[0][0])
    t_l = float(item[0][1])
    r_t = float(item[1][0])
    t_r = float(item[1][1])
    r_b = float(item[2][0])
    b_r = float(item[2][1])
    l_b = float(item[3][0])
    b_l = float(item[3][1])
    pts = np.array([[int(l_t), int(t_l)], [int(r_t) ,int(t_r)], [int(r_b) , int(b_r)], [int(l_b), int(b_l)]])
    
    if np.all(pts) > 0:
      line = crop(pts, image)
      try:
        imgL = Image.fromarray(line)
        ocr = detector.predict(imgL)
        lines.append(ocr)
        boxes.append(pts)

        if idHoadon < 0 and re.search(paAEON1, ocr) or re.search(paAEON2, ocr) or re.search(paAEON3, ocr):
          idHoadon = 1
        if idHoadon < 0 and re.search(paBigC3, ocr) or re.search(paBigC4, ocr):
          idHoadon = 2
        if idHoadon < 0 and re.search(paCoopMart1, ocr) or re.search(paCoopMart3, ocr) or re.search(paCoopMart4, ocr):
          idHoadon = 3
        if idHoadon < 0 and re.search(paVinCommerce1, ocr) or re.search(paVinCommerce2, ocr) or re.search(paVinCommerce3, ocr) or re.search(paVinCommerce4, ocr):
          idHoadon = 4
        if idHoadon < 0 and re.search(paLotteMart1, ocr) or re.search(paLotteMart2, ocr) or re.search(paLotteMart3, ocr) or re.search(paLotteMart4, ocr) or re.search(paLotteMart5, ocr):
          idHoadon = 5
        if idHoadon < 0 and re.search(paBachHoaXanh1, ocr) or re.search(paBachHoaXanh2, ocr) or re.search(paBachHoaXanh3, ocr):
          idHoadon = 6
        if idHoadon < 0 and re.search(paLMart1, ocr) or re.search(paLMart2, ocr):
          idHoadon = 7
        if idHoadon < 0 and re.search(paEMart1, ocr) or re.search(paEMart2, ocr) or re.search(paEMart3, ocr):
          idHoadon = 8

      except:
        print("Error")
  return idHoadon, lines, boxes

def cropHoadon(idHoadon, lines, boxes):

  lLines = []
  lBoxes = []
  L1 = 0
  L2 = 0
  L3 = 0
  R1 = 0
  R2 = 0
  R3 = 0
  H = 0
  rate1 = 0
  rate2 = 0
  rate3 = 0

  if idHoadon == 1:
    return cropAEON(lines, boxes)
  if idHoadon == 2:
    return cropBigC(lines, boxes)
  if idHoadon == 3:
    return cropCoopMart(lines, boxes)
  if idHoadon == 4:
    return cropVinCommerce(lines, boxes)
  if idHoadon == 5:
    return cropLotteMart(lines, boxes)
  if idHoadon == 6:
    return cropBachHoaXanh(lines, boxes)
  if idHoadon == 7:
    return cropLMart(lines, boxes)
  if idHoadon == 8:
    return cropEMart(lines, boxes)

  return L1, L2, L3, R1, R2, R3, H, rate1, rate2, rate3, lLines, lBoxes

def eiHoadon(idHoadon, L1, L2, L3, R1, R2, R3, H, rate1, rate2, rate3, lLines, lBoxes):

  if idHoadon == 1:
    infos = extractAEON(lLines, lBoxes)
    infos.showInfos()
    return infos

  if idHoadon == 2:
    infos = extractBigC(lLines, lBoxes)
    infos.showInfos()
    return infos

  if idHoadon == 3:
    infos = extractCoopMart(lLines, lBoxes)
    infos.showInfos()
    return infos

  if idHoadon == 4:
    infos = extractVinCommerce(lLines, lBoxes)
    infos.showInfos()
    return infos

  if idHoadon == 5:
    infos = extractLotteMart(lLines, lBoxes)
    infos.showInfos()
    return infos

  if idHoadon == 6:
    infos = extractBachHoaXanh(lLines, lBoxes)
    infos.showInfos()
    return infos

  if idHoadon == 7:
    infos = extractLMart(lLines, lBoxes)
    infos.showInfos()
    return infos

  if idHoadon == 8:
    infos = extractEMart(lLines, lBoxes)
    infos.showInfos()
    return infos

  return null