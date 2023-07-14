from routing.singleDP import SingleDP
from routing.doubleDroneRouting import DoubleDR
from model.multicopter import Multi
from model.vtol import Vtol
from field.map import Map
import openpyxl

def main0(path):
    Map.criateMapFile(5,path)
    
def main01():
    drone1 = Multi()
    for i in range(11):
        BCof1m = drone1.consum_f(i/10)
        print(i/10,BCof1m)
    
def main02(path):
    map = Map(path)
    map.showMap()
    
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
    DDR = DoubleDR(drone1,drone2,mapPath)
    DDR.findMinBC2flight()
    print("multi(blue):",DDR.flightDrone1List,"ft ",DDR.drone1FT,"BC ",DDR.drone1BC)
    print("vtol(green):",DDR.flightDrone2List,"ft ",DDR.drone2FT,"BC ",DDR.drone2BC)

    DDR.plotFig() #  青矢印がdrone1, 緑矢印がdrone2

if __name__ == "__main__":
    main0('data/map7.txt')
    main1('data/map7.txt')

