from . import airframe

class Vtol(airframe.Airframe):

    def __init__(self):
        super().__init__()
        self.battery_j = 460000  # 機体として正しい値は1118880
        self.takeOffTime_s = 60  # 離着陸にかかる時間
        self.speed_m_s = 13.89  # 機体速度50km/h
    
    #固定翼モードでの1秒あたりの消費電力(J)
    def consum_f_high(self,payload_kg):
        if payload_kg < 0.4:
            return 495
        elif payload_kg >= 0.4:
            return 59.167 * payload_kg + 475.67

    #マルチコプターモードでの1秒あたりの消費電力(J)
    def consum_f_low(self,payload_kg):
        return 385 * payload_kg + 2211.8

    #マルチコプターモードでの離着陸の消費電力(J)
    def consum_h(self,payload_kg):
        return self.takeOffTime_s * (385 * payload_kg + 2211.8)
    
    