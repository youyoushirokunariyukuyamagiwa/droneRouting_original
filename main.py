from routing.singleDP import SingleDP
from routing.doubleDroneRouting import DoubleDR
from model.multicopter import Multi
from model.vtol import Vtol
from field.map import Map
import openpyxl

def main0():
    Map.criateMapFile(6)
    
def main01():
    drone1 = Multi()
    for i in range(11):
        BCof1m = drone1.consum_f(i/10)
        print(i/10,BCof1m)
    
    
def main1():
    drone1 = Multi()
    drone2 = Vtol()
    routing1 = SingleDP(drone1,"data/map2.txt")
    routing2 = SingleDP(drone2,"data/map2.txt")

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
        ddr = DoubleDR(drone1,drone2,"data/map2.txt")
        ddr.flightDrone1List = routing1.bestRoute
        ddr.flightDrone2List = routing2.bestRoute
        ddr.plotFig()
    elif routing1.goalFlag == 1 and routing2.goalFlag == 0:
        routing1.plotRouteFig()
    elif routing1.goalFlag == 0 and routing2.goalFlag == 1:
        routing2.plotRouteFig()
    

def main2():
    drone1 = Multi()
    drone2 = Vtol()
    DDR = DoubleDR(drone1,drone2,"data/map2.txt")
    DDR.findMinFT2flight()
    print("multi:",DDR.flightDrone1List,"ft ",DDR.drone1FT,"BC ",DDR.drone1BC)
    print("vtol2:",DDR.flightDrone2List,"ft ",DDR.drone2FT,"BC ",DDR.drone2BC)

    DDR.plotFig() #  青矢印がdrone1, 緑矢印がdrone2

if __name__ == "__main__":
    main0()
    main1()

