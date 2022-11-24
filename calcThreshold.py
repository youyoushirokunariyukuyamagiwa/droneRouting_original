import model.multicopter as multi
import model.vtol as vtol

v = vtol.Vtol()
m = multi.Multi()

for payload_g in range(0,1100,100):
    payload_kg = payload_g / 1000
    vh = v.consum_h(payload_kg)
    vf = v.consum_f_low(payload_kg)
    mh = m.consum_h(payload_kg)
    mf = m.consum_f_low(payload_kg)
    time = (vh - mh)/(mf/m.speed_m_s - vf)
    print("payload", payload_kg, ": vtol_h:",vh,": multi_h:",mh,
    ": multi_f:",mf,": vtol_f:",vf,":time :", time)
    #print("payload : ", payload_kg, "kg ,time : ", time, "s")
    