import random
from field.node import Node
from routing.travellingSalesmanProblem import TravellingSalesmanProblem
from routing import calcThreshold
from routing.singleDP import SingleDP
from routing.doubleDroneRouting import DoubleDR
from routing.vrp import VRP
from model.multicopter import Multi
from model.vtol import Vtol
from field.map import Map
import openpyxl
from matplotlib import pyplot
from routing.vrpState import VrpState
from routing.singleRouting import SingleRouting

# map criate
def main0(path,N):
    Map.criateMapFile(N,path)
    
# battery consumption in 1 minute with 0.1kg~1.0kg payload
def main01():
    drone1 = Multi()
    for i in range(11):
        BCof1m = drone1.consum_f(i/10)
        print(i/10,BCof1m)
    
#mapのみ表示
def main02(path):
    map = Map(path)
    map.showMap()
    
#分析用
def main03(mapPath,drone):
    drone = drone
    routing = SingleDP(drone,mapPath)
    routing.criateTBobjectB()
    routing.printBestRouteObjectB()
    
    routing.plotAnalysis()
    routing.plotRouteFig()
    
#閾値を求める
def main04():
    m = Multi()
    v = Vtol()
    
    calcThreshold.calcThreshold(m,v)
    
# ルートプロット
def main05(nodeList):
    fig = pyplot.figure()
    ax = fig.add_subplot(111)

    ax.plot(*[0,0], 'o', color="blue") #  デポのプロット
    for p in nodeList: #  ノードのプロット
        ax.plot(*[p.x,p.y], 'o', color="red")
        ax.text(p.x, p.y,p.demand)
    
    for i in range(len(nodeList)-1): #  矢印のプロット
        fromNode = nodeList[i]
        toNode = nodeList[i+1]
        ax.annotate('', xy=[toNode.x,toNode.y], xytext=[fromNode.x,fromNode.y],
                    arrowprops=dict(shrink=0, width=1, headwidth=8, 
                                    headlength=10, connectionstyle='arc3',
                                    facecolor='gray', edgecolor='gray')
                    )

    pyplot.show()
    
# 広いマップ作成
def main06(path,N):
    Map.criateLargeMapFile(45,path)
    
# 制限の範囲内での1機体でのルーティング
def main1(mapPath):
    drone1 = Multi()
    drone2 = Vtol()
    routing1 = SingleDP(drone1,mapPath)
    routing2 = SingleDP(drone2,mapPath)

    routing1.criateTBobjectB()
    print("multi")
    routing1.printBestRouteObjectB()
    #print(routing1.goalFlag)
    #routing1.plotRouteFig()

    routing2.criateTBobjectB()
    print("vtol")
    routing2.printBestRouteObjectB()
    #print(routing2.goalFlag)
    #routing2.plotRouteFig()
    
    if routing1.goalFlag == 1 and routing2.goalFlag == 1 :
        ddr = DoubleDR(drone1,drone2,mapPath)
        ddr.flightDrone1List = routing1.bestRoute
        ddr.flightDrone2List = routing2.bestRoute
        ddr.plotFig()
    elif routing1.goalFlag == 1 and routing2.goalFlag == 0:
        routing1.plotRouteFig()
    elif routing1.goalFlag == 0 and routing2.goalFlag == 1:
        routing2.plotRouteFig()
    
def main2(mapPath):
    drone1 = Multi()
    drone2 = Vtol()
    #DDR1 = DoubleDR(drone1,drone1,mapPath)
    #DDR1.findMinBC2flight()
    #print(drone1.__class__.__name__,"(blue):",DDR1.flightDrone1List,"ft ",DDR1.drone1FT,"BC ",DDR1.drone1BC)
    #print(drone1.__class__.__name__,"(green):",DDR1.flightDrone2List,"ft ",DDR1.drone2FT,"BC ",DDR1.drone2BC)
    #print(drone1.__class__.__name__,drone1.__class__.__name__,"BC ",DDR1.drone1BC+DDR1.drone2BC)
    #DDR1.plotFig() #  青矢印がdrone1, 緑矢印がdrone2
    #print()
    
    #DDR2 = DoubleDR(drone2,drone2,mapPath)
    #DDR2.findMinBC2flight()
    #print(drone2.__class__.__name__,"(blue):",DDR2.flightDrone1List,"ft ",DDR2.drone1FT,"BC ",DDR2.drone1BC)
    #print(drone2.__class__.__name__,"(green):",DDR2.flightDrone2List,"ft ",DDR2.drone2FT,"BC ",DDR2.drone2BC)
    #print(drone2.__class__.__name__,drone2.__class__.__name__,"BC ",DDR2.drone1BC+DDR2.drone2BC)
    #DDR2.plotFig() #  青矢印がdrone1, 緑矢印がdrone2
    #print()
    
    DDR3 = DoubleDR(drone1,drone2,mapPath)
    DDR3.findMinBC2flight()
    print(drone1.__class__.__name__,"(blue):",DDR3.flightDrone1List,"ft ",DDR3.drone1FT,"BC ",DDR3.drone1BC)
    print(drone2.__class__.__name__,"(green):",DDR3.flightDrone2List,"ft ",DDR3.drone2FT,"BC ",DDR3.drone2BC)
    
    #print(drone1.__class__.__name__,drone2.__class__.__name__,"BC ",DDR3.drone1BC+DDR3.drone2BC)
    DDR3.plotFig() #  青矢印がdrone1, 緑矢印がdrone2
    
    #if DDR1.drone1BC+DDR1.drone2BC < DDR2.drone1BC+DDR2.drone2BC and DDR1.drone1BC+DDR1.drone2BC < DDR3.drone1BC+DDR3.drone2BC:
    #    print("multi+multi")
    #elif DDR2.drone1BC+DDR2.drone2BC < DDR1.drone1BC+DDR1.drone2BC and DDR2.drone1BC+DDR2.drone2BC < DDR3.drone1BC+DDR3.drone2BC:
    #    print("vtol+vtol")
    #elif DDR3.drone1BC+DDR3.drone2BC < DDR1.drone1BC+DDR1.drone2BC and DDR3.drone1BC+DDR3.drone2BC < DDR2.drone1BC+DDR2.drone2BC:
    #    print("multi+vtol")
    
# simannelを利用したsingleRoutingを実行実験する
def main3(drone1,mapFilePath):
    map = Map(mapFilePath)
    state = map.nodeList
    state.append(Node(0,0,0,0))
    tsp = TravellingSalesmanProblem(state,drone1)
    state = tsp.anneal()
    print()
    #print("長さ",len(state[0]))
    #for node in state[0]:
    #    print(node.nodeNum)
    print(state[1])
    main05(state[0])
    
# 動的計画法のsingleRouting
def main4(mapFilePath):
    miniMap = Map(mapFilePath)
    drone =Multi()
    allCustomerNum = miniMap.CN
    tsp = SingleRouting(miniMap.customerList,drone,allCustomerNum+3)
    tsp.criateTBobjectB()
    tsp.searchBestRouteObjectB()
    for n in tsp.bestRoute:
        print(n.nodeNum,end=" , ")
    print()
    print("BC",tsp.BC,"FT",tsp.FT)
    
#3機以上のドローンで
def main5(mapFilePath,droneNum):
    map = Map(mapFilePath)
    customerList = map.customerList
    #初期解作成
    initial_state = VrpState(droneNum,map.CN)
    for c in customerList:
        initial_state.miniCustomerMap[random.randint(0,droneNum-1)].append(c)
    for i in range(droneNum):
        initial_state.calcCost(i)
    
    vrp = VRP(initial_state)
    state = vrp.anneal()
    print()
    for i in range(droneNum):
        for n in state[0].eachFlights[i]:
            print(n.nodeNum,end=" , ")
        print(state[0].cost_list[i][0].type,"flight time",state[0].cost_list[i][1],"battery consumption",state[0].cost_list[i][2],"delivery payload",state[0].cost_list[i][3])
    
    state[0].plotRouteFig()

if __name__ == "__main__":
    drone1 = Multi()
    drone2 = Vtol()
    main06('data/large1.txt',15)
    #main02('data/large1.txt')
    
    main5('data/large1.txt',5)
    
    #main4('data/double8.txt')
