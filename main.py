from routing.singleDP import SingleDP
from model.multicopter import Multi
from model.vtol import Vtol


def main():
    drone = Vtol()
    routing = SingleDP(drone,"data/map2.txt")

    routing.criateTB()
    routing.printBestRoute()
    routing.plotRouteFig()

if __name__ == "__main__":
    main()