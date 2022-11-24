import model.multicopter as multi
import model.vtol as vtol

v = vtol.Vtol()
m = multi.Multi()
mSpeed_m_s = 13.89  # 機体速度50km/h
vSpeed_m_s = 13.89  # 機体速度50km/h

for payload_g in range(0,1100,100):
    payload_kg = payload_g / 1000
    vh = v.consum_h(payload_kg)
    vf = v.consum_f_high(payload_kg)
    mh = m.consum_h(payload_kg)
    mf = m.consum_f_high(payload_kg)
    distance = (vh - mh)/(mf/mSpeed_m_s - vf/vSpeed_m_s)
    print("payload", payload_kg, ": vtol_h:",vh,": multi_h:",mh,
    ": multi_f:",mf,": vtol_f:",vf,":threshold :", distance)
    #print("payload : ", payload_kg, "kg ,threshold : ", distance, "m")
    