import random
from routing.travellingSalesmanProblem import TravellingSalesmanProblem
from routing.singleRouting import SingleRouting
from model.multicopter import Multi
from model.vtol import Vtol
from field.node import Node
from matplotlib import pyplot

class VrpState():
    
    def __init__(self,droneNum,allCustomerNum) -> None:
        self.droneNum = droneNum
        self.allCustomerNum = allCustomerNum
        self.miniCustomerMap = []
        self.cost_list = [] #各フライトのdrone type, flight time, battery consumptionをタプルで保持
        self.eachFlights = [] #最終的な各ドローンのルーティング
        for i in range(droneNum):
            self.miniCustomerMap.append([])
            self.cost_list.append((None,None,None))
            self.eachFlights.append([])
        self.change_flight_1 = None
        self.change_flight_2 = None
        
        
        
    def move(self):
        a1 = random.randint(0,self.droneNum-1) # randint(a,b)はa,b含む範囲内の整数をランダムで返す。ミニマップリストのインデックスと対応させるため0~droneNum-1
        b1 = random.randint(0,self.droneNum-1)
            
        while a1 == b1 or len(self.miniCustomerMap[a1]) < 2:#１だと移動したあと空のフライトができてしまうので、最低でもカスタマーは２必要
            a1 = random.randint(0,self.droneNum-1) # randint(a,b)はa,b含む範囲内の整数をランダムで返す。ミニマップリストのインデックスと対応させるため0~droneNum-1
            b1 = random.randint(0,self.droneNum-1)
        a2 = random.randint(0,len(self.miniCustomerMap[a1])-1)
            
        self.miniCustomerMap[b1].append(self.miniCustomerMap[a1][a2])
        del self.miniCustomerMap[a1][a2]
            
        self.change_flight_1 = a1
        self.change_flight_2 = b1
    
    def exchange(self):
        a1 = random.randint(0,self.droneNum-1) # randint(a,b)はa,b含む範囲内の整数をランダムで返す。ミニマップリストのインデックスと対応させるため0~droneNum-1
        b1 = random.randint(0,self.droneNum-1)
            
        while a1 == b1 or len(self.miniCustomerMap[a1]) < 1 or len(self.miniCustomerMap[b1]) < 1:
            a1 = random.randint(0,self.droneNum-1) # randint(a,b)はa,b含む範囲内の整数をランダムで返す。ミニマップリストのインデックスと対応させるため0~droneNum-1
            b1 = random.randint(0,self.droneNum-1)
        a2 = random.randint(0,len(self.miniCustomerMap[a1])-1)
        b2 = random.randint(0,len(self.miniCustomerMap[b1])-1)
            
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
        for touple in self.cost_list:
            sum_BC += touple[2]
        
        return sum_BC
    
    def calcCost(self,map_id):
        
        multiRouting = SingleRouting(self.miniCustomerMap[map_id],Multi(),self.allCustomerNum)
        multiRouting.criateTBobjectB()
        multiRouting.searchBestRouteObjectB()
        vtolRouting = SingleRouting(self.miniCustomerMap[map_id],Vtol(),self.allCustomerNum)
        vtolRouting.criateTBobjectB()
        vtolRouting.searchBestRouteObjectB()
        
        if multiRouting.BC > vtolRouting.BC:
            self.cost_list[map_id] = (Vtol(),vtolRouting.FT,vtolRouting.BC)
            self.eachFlights[map_id] = vtolRouting.bestRoute
        else :
            self.cost_list[map_id] = (Multi(),multiRouting.FT,multiRouting.FT)
            self.eachFlights[map_id] = multiRouting.bestRoute
    
    def plotRouteFig(self):
        fig = pyplot.figure()
        ax = fig.add_subplot(111)

        ax.plot(*[0,0], 'o', color="blue") #  デポのプロット
        for map in self.miniCustomerMap:
            for n in map:
                ax.plot(*[n.x,n.y], 'o', color="red")
                ax.text(n.x, n.y,n.demand)

        for flight in self.eachFlights:
            for i in range(len(flight)-1): #  矢印のプロット
                fromNode = flight[i]
                toNode = flight[i+1]
                ax.annotate('', xy=[toNode.x,toNode.y], xytext=[fromNode.x,fromNode.y],
                            arrowprops=dict(shrink=0, width=1, headwidth=8, 
                                            headlength=10, connectionstyle='arc3',
                                            facecolor='gray', edgecolor='gray')
                            )

        pyplot.show()