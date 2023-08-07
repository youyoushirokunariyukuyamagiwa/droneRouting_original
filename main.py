from routing import calcThreshold
from routing.singleDP import SingleDP
from routing.doubleDroneRouting import DoubleDR
from model.multicopter import Multi
from model.vtol import Vtol
from field.map import Map
import openpyxl

def main0(path,N):
    Map.criateMapFile(N,path)
    
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
    
if __name__ == "__main__":
    drone1 = Multi()
    drone2 = Vtol()
    #main0('data/double10.txt',8)
    #main03('data/analysis3.txt',drone1)
    #main03('data/analysis3.txt',drone2)
    main2('data/double4.txt')
    main02('data/double4.txt')
    #main2('data/double3.txt')
    #main2('data/double4.txt')
    #main2('data/double5.txt')
    #main2('data/double6.txt')
    #main2('data/double7.txt')
    #main2('data/double8.txt')
    #main2('data/double9.txt')
    #main2('data/double10.txt')

