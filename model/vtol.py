from . import airframe

class Vtol(airframe.Airframe):

    def __init__(self):
        super().__init__()
        self.battery_j = 1118880  # 機体として正しい値は1118880(maxの7割)
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

    def calcBattery_f(self,distance,payload_kg):
        if distance < 200:
            battery = self.consum_f_low(payload_kg)*distance/self.speed_m_s
        else:
            battery = self.consum_f_low(payload_kg)*200/self.speed_m_s + self.consum_f_high(payload_kg)*(distance-200)/self.speed_m_s

        return battery

    def addPayloadBC(self,distance,payload_kg):
        if distance < 200:
            battery = 385 * payload_kg * distance/self.speed_m_s
        else:
            if payload_kg < 0.4:
                battery = 385*payload_kg*200/self.speed_m_s+ 495 * (distance-200)/self.speed_m_s
            elif payload_kg >= 0.4:
                battery = 385*payload_kg*200/self.speed_m_s + 59.167 * payload_kg * (distance-200)/self.speed_m_s

        return battery

    #マルチコプターモードでの離着陸の消費電力(J)
    def consum_h(self,payload_kg):
        return self.takeOffTime_s * (385 * payload_kg + 2211.8)
    
    