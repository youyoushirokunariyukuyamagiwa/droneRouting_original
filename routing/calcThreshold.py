import sys
import os

from matplotlib import pyplot
sys.path.append(os.path.abspath(".."))

from model import airframe
from model import vtol
from model import multicopter

mSpeed_m_s = 13.89  # 機体速度50km/h
vSpeed_m_s = 13.89  # 機体速度50km/h

def calcThreshold(A1:airframe,A2:airframe): #  同じバッテリ消費量で飛べる距離計算式
    x_payload_list = []
    y_distance_list = []
    
    for payload_g in range(0,1100,100):
        payload_kg = payload_g / 1000
        x_payload_list.append(payload_kg)
        
        A1h = A1.consum_h(payload_kg) #  VTOL機の離着陸にかかるB消費量
        A1f = A1.consum_f(payload_kg) #  VTOL機の前進飛行にかかるB消費量
        A2h = A2.consum_h(payload_kg) #  マルチコプターの離着陸にかかるB消費量
        A2f = A2.consum_f(payload_kg) #  マルチコプターの前進飛行にかかるB消費量
        distance = (A1h - A2h)/(A2f/A2.speed_km_m - A1f/A1.speed_km_m) #  それぞれの機体速度を決めたときのB消費量が等しくなる飛行距離（閾値）
        y_distance_list.append(distance)
        
        print("payload", payload_kg, ": multi_h:",round(A1h,2),": vtol_h:",round(A2h,2),
        ": vtol_f:",round(A2f,2),": multi_f:",round(A1f,2),":threshold :", round(distance,2))
    #print("payload : ", payload_kg, "kg ,threshold : ", distance, "m")
    
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    ax.plot(x_payload_list,y_distance_list,marker="o", markersize=6,markerfacecolor="blue")
    pyplot.xlabel("payload")
    pyplot.ylabel("distance(km)")
    pyplot.grid(True)
    
    pyplot.show()

if __name__ == "__main__":
    v1 = vtol.Vtol()
    m1 = multicopter.Multi()
    calcThreshold(m1,v1)

    #print(m1.calcBattery_f(100,1))
    #print(v1.calcBattery_f(100,1))