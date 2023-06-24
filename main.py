from routing.singleDP import SingleDP
from routing.doubleDroneRouting import DoubleDR
from model.multicopter import Multi
from model.vtol import Vtol
from field.map import Map

def main0():
    Map.criateMapFile(6)
    
def main1():
    drone1 = Multi()
    drone2 = Vtol()
    routing1 = SingleDP(drone1,"data/map2.txt")
    routing2 = SingleDP(drone2,"data/map2.txt")

    routing2.criateTBobjectT()
    routing2.printBestRouteObjectT()
    routing2.plotRouteFig()
    
    routing1.criateTBobjectT()
    routing1.printBestRouteObjectT()
    routing1.plotRouteFig()
    

def main2():
    drone1 = Vtol()
    drone2 = Vtol()
    DDR = DoubleDR(drone1,drone2,"data/map2.txt")
    DDR.findMinBC2flight()
    print("multi:",DDR.flightDrone1List,"ft ",DDR.drone1FT,"BC ",DDR.drone1BC)
    print("vtol2:",DDR.flightDrone2List,"ft ",DDR.drone2FT,"BC ",DDR.drone2BC)

    DDR.plotFig() #  青矢印がdrone1, 緑矢印がdrone2

if __name__ == "__main__":
    #main0()
    main2()

