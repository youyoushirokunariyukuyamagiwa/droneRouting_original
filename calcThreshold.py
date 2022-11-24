import model.multicopter as multi
import model.vtol as vtol

v = vtol.Vtol()
m = multi.Multi()

for payload_g in range(0,1100,100):
    payload_kg = payload_g / 1000
    time = (v.consum_h(payload_kg) - m.consum_h(payload_kg+7.6))/(m.consum_f_high(payload_kg+7.6) - v.consum_f_high(payload_kg))
    print("payload", payload_kg, ": vtol_h:",v.consum_h(payload_kg),": multi_h:",m.consum_h(payload_kg+7.6),
    ": multi_f:",m.consum_f_high(payload_kg+7.6),": vtol_f:",v.consum_f_high(payload_kg),":time :", time)