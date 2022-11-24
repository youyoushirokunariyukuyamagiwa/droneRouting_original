import model.multicopter as multi
import model.vtol as vtol

v = vtol.Vtol()
m = multi.Multi()
mSpeed_m_s = 13.89  # 機体速度50km/h
vSpeed_m_s = 13.89  # 機体速度50km/h

for payload_g in range(0,1100,100):
    payload_kg = payload_g / 1000
    vh = v.consum_h(payload_kg) #  VTOL機の離着陸にかかるB消費量
    vf = v.consum_f_high(payload_kg) #  VTOL機の前進飛行にかかるB消費量
    mh = m.consum_h(payload_kg) #  マルチコプターの離着陸にかかるB消費量
    mf = m.consum_f_high(payload_kg) #  マルチコプターの前進飛行にかかるB消費量
    distance = (vh - mh)/(mf/mSpeed_m_s - vf/vSpeed_m_s) #  それぞれの機体速度を決めたときのB消費量が等しくなる飛行距離（閾値）
    print("payload", payload_kg, ": vtol_h:",vh,": multi_h:",mh,
    ": multi_f:",mf,": vtol_f:",vf,":threshold :", distance)
    #print("payload : ", payload_kg, "kg ,threshold : ", distance, "m")
    