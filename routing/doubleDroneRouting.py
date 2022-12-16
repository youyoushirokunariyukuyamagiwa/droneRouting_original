from matplotlib import pyplot
from field.map import Map
from routing.singleDP import SingleDP
from model.multicopter import Multi
from model.vtol import Vtol

class DoubleDR:

    def __init__(self,drone1,drone2,mapFilePath) -> None:
        self.drone1 = drone1
        self.drone2 = drone2
        self.route1 = SingleDP(drone1,mapFilePath)
        self.route2 = SingleDP(drone2,mapFilePath)
        self.route1.criateTB()
        self.route2.criateTB()
        self.bestLastNodeEachVis = {}
        self.flightDrone1 = None#  drone1の担当フライトの最後のvistedとlastNodeNumのタプル
        self.flightDrone2 = None
        self.flightDrone1List = [0]
        self.flightDrone2List = [0]
        self.drone1FT = None
        self.drone1BC = None
        self.drone2FT = None
        self.drone2BC = None

    #各visitedの中で最短のルートを見つけ、そのlast_node_numを辞書に格納
    def findBestLastNodeEachVis(self):
        sort1 = sorted(self.route1.TB.items())
        #sort2 = sorted(self.route2.TB.items())
        #for key,tb in sort:
        #    print(key[0],key[1])
        
        s='0'+str(self.route1.map.CN)+'b'
        lastVis = format(1,s)
        minFTlastNode = 1
        for key,tb in sort1:
            vis = key[0]
            last_node_num = key[1]
            if lastVis == vis :# 一緒の間は値を比べて最短を保持
                if tb.flightTime < self.route1.TB[vis,minFTlastNode].flightTime:
                    minFTlastNode = last_node_num
            else: # 変わったら変わる前のvisとそのvisの最短のlast_node_numを辞書に登録
                self.bestLastNodeEachVis[lastVis] = minFTlastNode
                lastVis = vis
                minFTlastNode = last_node_num
        
        #for vis,last_node_num in self.bestLastNodeEachVis.items():
        #    print("vis",vis,"  last node",last_node_num)

    def criateOpposeVis(self,vis:str):
        vislst = list(vis)
        for i in range(len(vislst)):
            if vislst[i] == "0":
                vislst[i] = "1"
            elif vislst[i] == "1":
                vislst[i] = "0"
            else:
                print("visitedeが正しくありません")
                return False

        opposeVis = "".join(vislst)
        return opposeVis

    def findBest2flight(self):
        self.findBestLastNodeEachVis()
        minTime = None
        for vis,lastNode in self.bestLastNodeEachVis.items():
            opposeVis = self.criateOpposeVis(vis)
            if opposeVis == False:
                return False
            opposeLastNode = self.bestLastNodeEachVis[opposeVis]
            if minTime == None or minTime > max(self.route1.TB[vis,lastNode].flightTime,self.route2.TB[opposeVis,opposeLastNode].flightTime):
                bestFlight1 = (vis,lastNode)
                bestFlight2 = (opposeVis,opposeLastNode)
                minTime = max(self.route1.TB[vis,lastNode].flightTime,self.route2.TB[opposeVis,opposeLastNode].flightTime)
        
        if self.route1.TB[bestFlight1[0],bestFlight1[1]].BC > self.route2.TB[bestFlight1[0],bestFlight1[1]].BC:
            diff1 = self.route1.TB[bestFlight1[0],bestFlight1[1]].BC - self.route2.TB[bestFlight1[0],bestFlight1[1]].BC
            if self.route1.TB[bestFlight2[0],bestFlight2[1]].BC > self.route2.TB[bestFlight2[0],bestFlight2[1]].BC:
                diff2 = self.route1.TB[bestFlight2[0],bestFlight2[1]].BC - self.route2.TB[bestFlight2[0],bestFlight2[1]].BC
                if diff1 < diff2 :
                    self.flightDrone2 = bestFlight1
                    self.flightDrone1 = bestFlight2
                else:
                    self.flightDrone2 = bestFlight2
                    self.flightDrone1 = bestFlight1
            else:
                self.flightDrone1 = bestFlight2
                self.flightDrone2 = bestFlight1
        else:
            diff1 = self.route2.TB[bestFlight1[0],bestFlight1[1]].BC - self.route1.TB[bestFlight1[0],bestFlight1[1]].BC
            if self.route1.TB[bestFlight2[0],bestFlight2[1]].BC < self.route2.TB[bestFlight2[0],bestFlight2[1]].BC:
                diff2 = self.route2.TB[bestFlight2[0],bestFlight2[1]].BC - self.route1.TB[bestFlight2[0],bestFlight2[1]].BC
                if diff2 < diff1 :
                    self.flightDrone2 = bestFlight1
                    self.flightDrone1 = bestFlight2
                else:
                    self.flightDrone2 = bestFlight2
                    self.flightDrone1 = bestFlight1
            else:
                self.flightDrone1 = bestFlight1
                self.flightDrone2 = bestFlight2

        self.drone1FT = self.route1.TB[self.flightDrone1[0],self.flightDrone1[1]].flightTime
        self.drone1BC = self.route1.TB[self.flightDrone1[0],self.flightDrone1[1]].BC
        self.drone2FT = self.route2.TB[self.flightDrone2[0],self.flightDrone2[1]].flightTime
        self.drone2BC = self.route2.TB[self.flightDrone2[0],self.flightDrone2[1]].BC

        # drone1のフライトをリストに格納
        self.flightDrone1List.append(self.flightDrone1[1])# 最後のカスタマーを追加
        now_vis = self.flightDrone1[0]
        now_node_num = self.flightDrone1[1]
        while True:
            if now_node_num == 0:
                break

            previous_node_num = self.route1.TB[now_vis,now_node_num].previous
            self.flightDrone1List.append(previous_node_num)

            now_vis = self.route1.criateMinusVisited(now_vis,now_node_num)
            now_node_num = previous_node_num
        self.flightDrone1List.reverse()

        # drone2のフライトをリストに格納
        self.flightDrone2List.append(self.flightDrone2[1])# 最後のカスタマーを追加
        now_vis = self.flightDrone2[0]
        now_node_num = self.flightDrone2[1]
        while True:
            if now_node_num == 0:
                break

            previous_node_num = self.route2.TB[now_vis,now_node_num].previous
            self.flightDrone2List.append(previous_node_num)

            now_vis = self.route2.criateMinusVisited(now_vis,now_node_num)
            now_node_num = previous_node_num
        self.flightDrone2List.reverse()

    def plotFig(self):

        if len(self.flightDrone1List) <= 1 or len(self.flightDrone2List) <= 1 :
            return False
        fig = pyplot.figure()
        ax = fig.add_subplot(111)

        ax.plot(*[0,0], 'o', color="black") #  デポのプロット
        for p in self.route1.map.customerList: #  ノードのプロット
            ax.plot(*[p.x,p.y], 'o', color="red")

        for i in range(len(self.flightDrone1List)-1): #  drone1の矢印のプロット
            fromNode = self.route1.map.nodeList[self.flightDrone1List[i]]
            toNode = self.route1.map.nodeList[self.flightDrone1List[i+1]]
            ax.annotate('', xy=[toNode.x,toNode.y], xytext=[fromNode.x,fromNode.y],
                        arrowprops=dict(shrink=0, width=1, headwidth=8, 
                                        headlength=10, connectionstyle='arc3',
                                        facecolor='blue', edgecolor='blue')
                        )

        for i in range(len(self.flightDrone2List)-1): #  drone2の矢印のプロット
            fromNode = self.route2.map.nodeList[self.flightDrone2List[i]]
            toNode = self.route2.map.nodeList[self.flightDrone2List[i+1]]
            ax.annotate('', xy=[toNode.x,toNode.y], xytext=[fromNode.x,fromNode.y],
                        arrowprops=dict(shrink=0, width=1, headwidth=8, 
                                        headlength=10, connectionstyle='arc3',
                                        facecolor='green', edgecolor='green')
                        )

        ax.set_xlim([0, 1.2*self.route1.map.maxXY])
        ax.set_ylim([0, 1.2*self.route1.map.maxXY])

        pyplot.show()


