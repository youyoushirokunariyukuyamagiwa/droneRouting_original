import sys
import os
sys.path.append(os.path.abspath(".."))

from model import multicopter as m
from model import vtol as v
from model import airframe

v = v.Vtol()
m = m.Multi()
mSpeed_m_s = 13.89  # 機体速度50km/h
vSpeed_m_s = 13.89  # 機体速度50km/h

def calcThreshold(A1:airframe,A2:airframe):
    for payload_g in range(0,1100,100):
        payload_kg = payload_g / 1000
        A1h = A1.consum_h(payload_kg) #  VTOL機の離着陸にかかるB消費量
        A1f = A1.consum_f_high(payload_kg) #  VTOL機の前進飛行にかかるB消費量
        A2h = A2.consum_h(payload_kg) #  マルチコプターの離着陸にかかるB消費量
        A2f = A2.consum_f_high(payload_kg) #  マルチコプターの前進飛行にかかるB消費量
        distance = (A1h - A2h)/(A2f/A2.speed_m_s - A1f/A1.peed_m_s) #  それぞれの機体速度を決めたときのB消費量が等しくなる飛行距離（閾値）
        print("payload", payload_kg, ": vtol_h:",A1h,": multi_h:",A2h,
        ": multi_f:",A2f,": vtol_f:",A1f,":threshold :", distance)
    #print("payload : ", payload_kg, "kg ,threshold : ", distance, "m")
    

    