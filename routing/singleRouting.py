from simanneal import Annealer
import random
import math
import sys
sys.path.append("../../field")
from field.node import Node
from field.map import Map
from model.multicopter import Multi
from model.vtol import Vtol

class TravellingSalesmanProblem(Annealer):
    
    def __init__(self, state, drone):
        self.drone = drone
        self.battery_consumption = float('inf')
        self.flight_time = 0
        self.keeping_payload = 0
        super(TravellingSalesmanProblem,self).__init__(state)
        
    def move(self):
        initial_energy = self.energy()
        """
        R = random.randint(0,1)
    
        if R == 0 :#移動
            a = random.randint(1,len(self.state)-2)# ルートの中で最初と最後のデポを除いた範囲でランダムに得る
            b = random.randint(1,len(self.state)-2)
            
            while a == b:
                a = random.randint(1,len(self.state)-2)# ルートの中で最初と最後のデポを除いた範囲でランダムに得る
                b = random.randint(1,len(self.state)-2)
            
            self.state.insert(a,self.state[b])
            del self.state[b]
            
        else:#交換
            a = random.randint(1,len(self.state)-2)# ルートの中で最初と最後のデポを除いた範囲でランダムに得る
            b = random.randint(1,len(self.state)-2)
            
            while a == b:
                a = random.randint(1,len(self.state)-2)# ルートの中で最初と最後のデポを除いた範囲でランダムに得る
                b = random.randint(1,len(self.state)-2)
                
            self.state[a] ,self.state[b] = self.state[b],self.state[a]
        """
        a = random.randint(1,len(self.state)-2)# ルートの中で最初と最後のデポを除いた範囲でランダムに得る
        b = random.randint(1,len(self.state)-2)
        
        while a == b:
            a = random.randint(1,len(self.state)-2)# ルートの中で最初と最後のデポを除いた範囲でランダムに得る
            b = random.randint(1,len(self.state)-2)
            
        self.state[a] ,self.state[b] = self.state[b],self.state[a]
        # 変更前と後の差をreturn するかも
        return self.energy() - initial_energy
    
    def energy(self):
        payload = 0
        sum_BC = 0
        sum_FT = 0
        for i in reversed(range(1,len(self.state))):
            distance = math.sqrt((self.state[i].x - self.state[i-1].x)**2 + (self.state[i].y - self.state[i-1].y)**2)
            time = self.drone.calcFlightTime(distance)
            bc = self.drone.consum_f(payload)*time + self.drone.consum_h(payload)
            sum_FT += time + self.drone.takeOffTime_m
            sum_BC += bc
            payload += self.state[i-1].demand
        
        if self.battery_consumption > sum_BC:
            self.battery_consumption = sum_BC
            self.flight_time = sum_FT
            self.keeping_payload = payload
        
        return sum_BC
    
