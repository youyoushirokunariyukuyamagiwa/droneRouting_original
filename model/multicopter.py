from . import airframe

class Multi(airframe.Airframe):

    def __init__(self):
        super().__init__()
        self.battery_w = 460000  #機体として正しい値は321120
        self.takeOffTime_s = 60
    
    def consum_f_high(self,payload_kg):
        payload_lb = payload_kg * 2.205 
        return (2.297 * payload_lb + 3.879) / 100 / 60 * 321120 *9/1.4

    def consum_f_low(self,payload_kg):
        payload_lb = payload_kg * 2.205 
        return (2.297 * payload_lb + 3.879) / 100 / 60 * 321120 *9/1.4

    def consum_h(self,payload_kg):
        payload_lb = payload_kg * 2.205 
        return self.takeOffTime_s*(2.297 * payload_lb + 3.879) / 100 / 60 * 321120 *9/1.4