import sys
import os
sys.path.append(os.path.abspath(".."))

from model import airframe
from model import vtol
from model import multicopter

mSpeed_m_s = 13.89  # 機体速度50km/h
vSpeed_m_s = 13.89  # 機体速度50km/h

def calcThresholdU200(A1:airframe,A2:airframe): #  距離200m以下の時の閾値計算式
    for payload_g in range(0,1100,100):
        payload_kg = payload_g / 1000
        A1h = A1.consum_h(payload_kg) #  VTOL機の離着陸にかかるB消費量
        A1f = A1.consum_f_high(payload_kg) #  VTOL機の前進飛行にかかるB消費量
        A2h = A2.consum_h(payload_kg) #  マルチコプターの離着陸にかかるB消費量
        A2f = A2.consum_f_high(payload_kg) #  マルチコプターの前進飛行にかかるB消費量
        distance = (A1h - A2h)/(A2f/A2.speed_m_s - A1f/A1.speed_m_s) #  それぞれの機体速度を決めたときのB消費量が等しくなる飛行距離（閾値）
        print("payload", payload_kg, ": vtol_h:",round(A1h,2),": multi_h:",round(A2h,2),
        ": multi_f:",round(A2f,2),": vtol_f:",round(A1f,2),":threshold :", round(distance,2))
    #print("payload : ", payload_kg, "kg ,threshold : ", distance, "m")

def calcThresholdA200(A1:airframe,A2:airframe):
    for payload_g in range(0,1100,100):
        payload_kg = payload_g / 1000
        A1h = A1.consum_h(payload_kg)
        A1fh = A1.consum_f_high(payload_kg)
        A1fl = A1.consum_f_low(payload_kg)
        A2h = A2.consum_h(payload_kg)
        A2fh = A2.consum_f_high(payload_kg)
        A2fl = A2.consum_f_low(payload_kg)
        d = (200/A2.speed_m_s*(A2fl-A2fh)+A2h+200/A1.speed_m_s*(A1fh-A1fl)-A1h)/(A1fh/A1.speed_m_s-A2fh/A2.speed_m_s)
        print("payload : ", payload_kg, "kg ,threshold : ", d, "m")

if __name__ == "__main__":
    v1 = vtol.Vtol()
    m1 = multicopter.Multi()
    """
    for payload_g in range(0,1100,100):
        payload_kg = payload_g / 1000
        A1h = v1.consum_h(payload_kg) #  VTOL機の離着陸にかかるB消費量
        A1f = v1.consum_f_high(payload_kg) #  VTOL機の前進飛行にかかるB消費量
        A2h = m1.consum_h(payload_kg) #  マルチコプターの離着陸にかかるB消費量
        A2f = m1.consum_f_high(payload_kg) #  マルチコプターの前進飛行にかかるB消費量
        distance = (A1h - A2h)/(A2f/m1.speed_m_s - A1f/v1.speed_m_s) #  それぞれの機体速度を決めたときのB消費量が等しくなる飛行距離（閾値）
        print("payload", payload_kg, ": vtol_h:",A1h,": multi_h:",A2h,
        ": multi_f:",A2f,": vtol_f:",A1f,":threshold :", distance)
    """
    #calcThresholdA200(m1,v1)
    #calcThresholdU200(m1,v1)
    print(m1.calcBattery_f(100,1))
    print(v1.calcBattery_f(100,1))