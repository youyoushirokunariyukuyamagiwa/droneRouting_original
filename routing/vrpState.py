import random
from routing.singleRouting import TravellingSalesmanProblem
from model.multicopter import Multi
from model.vtol import Vtol
from field.node import Node

class VrpState():
    
    def __init__(self,droneNum) -> None:
        self.droneNum = droneNum
        self.miniCustomerMap = []
        self.cost_list = [] #各フライトのdrone type, flight time, battery consumptionをタプルで保持
        for i in range(droneNum):
            self.miniCustomerMap.append([])
            self.cost_list.append((None,None,None))
        self.change_flight_1 = None
        self.change_flight_2 = None
        
    def move(self):
        a1 = random.randint(0,self.droneNum-1) # randint(a,b)はa,b含む範囲内の整数をランダムで返す。ミニマップリストのインデックスと対応させるため0~droneNum-1
        b1 = random.randint(0,self.droneNum-1)
            
        while a1 == b1:
            a1 = random.randint(0,self.droneNum-1) # randint(a,b)はa,b含む範囲内の整数をランダムで返す。ミニマップリストのインデックスと対応させるため0~droneNum-1
            b1 = random.randint(0,self.droneNum-1)
        a2 = random.randint(1,len(self.miniCustomerMap[a1])-1)
            
        self.miniCustomerMap[b1].append(self.miniCustomerMap[a1][a2])
        del self.miniCustomerMap[a1][a2]
            
        self.change_flight_1 = a1
        self.change_flight_2 = b1
    
    def exchange(self):
        a1 = random.randint(0,self.droneNum-1) # randint(a,b)はa,b含む範囲内の整数をランダムで返す。ミニマップリストのインデックスと対応させるため0~droneNum-1
        b1 = random.randint(0,self.droneNum-1)
            
        while a1 == b1:
            a1 = random.randint(0,self.droneNum-1) # randint(a,b)はa,b含む範囲内の整数をランダムで返す。ミニマップリストのインデックスと対応させるため0~droneNum-1
            b1 = random.randint(0,self.droneNum-1)
        a2 = random.randint(1,len(self.miniCustomerMap[a1])-1)
        b2 = random.randint(1,len(self.miniCustomerMap[b1])-1)
            
        self.miniCustomerMap[a1][a2] ,self.miniCustomerMap[b1][b2] = self.miniCustomerMap[b1][b2],self.miniCustomerMap[a1][a2]
        
        self.change_flight_1 = a1
        self.change_flight_2 = b1
    
    def change(self):
        R = random.randint(0,1)
        if R == 0:#移動
            self.move()
        else:
            self.exchange()
        
        self.calcCost(self.change_flight_1)
        self.calcCost(self.change_flight_2)
    
    def calcScore(self):
        sum_BC = 0
        for n in self.cost_list:
            sum_BC += n[2]
        
        return sum_BC
    
    def calcCost(self,map_id):
        depo = Node(0,0,0,0)
        initial_flight = [depo]
        initial_flight.extend(self.miniCustomerMap[map_id])
        initial_flight.append(depo)
        tsp1 = TravellingSalesmanProblem(initial_flight,Multi())
        tsp1.updates = 50
        tsp1.steps = 2500
        ans1 = tsp1.anneal()
        tsp2 = TravellingSalesmanProblem(initial_flight,Vtol())
        tsp2.updates = 50
        tsp2.steps = 2500
        ans2 = tsp2.anneal()
        
        if ans1[1] > ans2[1]:
            self.cost_list[map_id] = (Vtol(),tsp2.flight_time,tsp2.battery_consumption)
        else :
            self.cost_list[map_id] = (Multi(),tsp1.flight_time,tsp1.battery_consumption)