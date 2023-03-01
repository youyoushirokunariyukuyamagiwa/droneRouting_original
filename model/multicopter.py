from . import airframe

class Multi(airframe.Airframe):

    def __init__(self):
        super().__init__()
        self.battery_j = 11188800000  # 機体として正しい値は321120*9/1.4
        self.takeOffTime_s = 120  # 離着陸にかかる時間
        self.speed_m_s = 13.89  # 機体速度50km/h
        self.maxPayload_kg = 10000000
    
    # 高速前進飛行での1秒あたりの消費電力（J)
    def consum_f_high(self,payload_kg):
        return 1742.6*payload_kg + 1334.6

    # 低速前進飛行での1秒あたりの消費電力（J)
    def consum_f_low(self,payload_kg):
        return 1742.6*payload_kg + 1334.6

    def calcBattery_f(self, distance, payload_kg):
        return (1742.6*payload_kg + 1334.6)*distance/self.speed_m_s + self.consum_h(payload_kg)

    def addPayloadBC(self,distance,payload_kg):
        return 1742.6*payload_kg * distance/self.speed_m_s + 1742.6*payload_kg * self.takeOffTime_s

    # 離着陸でのバッテリー消費量（J）
    def consum_h(self,payload_kg):
        return self.takeOffTime_s * (1742.6*payload_kg + 1334.6)