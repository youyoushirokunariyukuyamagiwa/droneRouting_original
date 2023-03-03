from routing.singleDP import SingleDP
from routing.doubleDroneRouting import DoubleDR
from model.multicopter import Multi
from model.vtol import Vtol


def main1():
    drone = Vtol()
    routing = SingleDP(drone,"data/map2.txt")

    routing.criateTBobjectB()
    routing.printBestRoute()
    routing.plotRouteFig()

def main2():
    drone1 = Multi()
    drone2 = Vtol()
    DDR = DoubleDR(drone1,drone2,"data/map2.txt")
    DDR.findBest2flight()
    print(DDR.flightDrone1List,"ft ",DDR.drone1FT,"BC ",DDR.drone1BC)
    print(DDR.flightDrone2List,"ft ",DDR.drone2FT,"BC ",DDR.drone2BC)

    DDR.plotFig()

if __name__ == "__main__":
    main1()

