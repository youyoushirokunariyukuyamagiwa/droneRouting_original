from . import airframe

class Multi(airframe.Airframe):

    def __init__(self):
        super().__init__()
        self.battery_j = 11188800000  # 機体として正しい値は321120*9/1.4 321120が機体そのままのバッテリー量の7割、今回機体を比較するにあたって機体重量を基準に合わせて9/1.4倍してるのでその他のパラメータも9/1.4倍
        # ↑　2064342.,,,
        self.takeOffTime_s = 120  # 離着陸にかかる時間
        self.highSpeed_m_s = 13.89  # 機体速度50km/h
        self.lowSpeed_m_s = 13.89  # 機体速度50km/h
        self.maxPayload_kg = 0.8  #もともとの積載可能量120gの9/1.4倍

    # 高速前進飛行での1秒あたりの消費電力（J)
    def consum_f_high(self,payload_kg):
        return 1742.6*payload_kg + 1334.6

    # 低速前進飛行での1秒あたりの消費電力（J)
    def consum_f_low(self,payload_kg):
        return 1742.6*payload_kg + 1334.6

    def calcBattery_f(self, distance, payload_kg):
        return (1742.6*payload_kg + 1334.6)*distance/self.highSpeed_m_s + self.consum_h(payload_kg)

    def addPayloadBC(self,distance,payload_kg):
        return 1742.6*payload_kg * distance/self.highSpeed_m_s + 1742.6*payload_kg * self.takeOffTime_s

    # 離着陸でのバッテリー消費量（J）
    def consum_h(self,payload_kg):
        return self.takeOffTime_s * (1742.6*payload_kg + 1334.6)
    
    def calcFlightTime(self,distance):
        return distance/self.highSpeed_m_s + self.takeOffTime_s