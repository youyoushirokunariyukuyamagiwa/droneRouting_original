import sys
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
        self.route1.criateTBobjectB()
        self.route2.criateTBobjectB()
        self.bestLastNodeEachVis1 = {}
        self.bestLastNodeEachVis2 = {}
        self.flightDrone1 = None#  drone1の担当フライトの最後のvistedとlastNodeNumのタプル
        self.flightDrone2 = None
        self.flightDrone1List = [0]
        self.flightDrone2List = [0]
        self.drone1FT = None
        self.drone1BC = None
        self.drone2FT = None
        self.drone2BC = None

    #各visitedの中でFT最短のルートを見つけ、そのlast_node_numを辞書に格納
    def findMinTimeLastNodeEachVis(self):
        sort1 = sorted(self.route1.TB.items())
        sort2 = sorted(self.route2.TB.items())  # TBをkey（vis,lastNode）で00001から始まるソート
        #for key,tb in sort1:
        #    print(key[0],key[1])
        
        s='0'+str(self.route1.map.CN)+'b'
        lastVis = format(1,s)
        minFTlastNode = 1
        for key,tb in sort1:
            vis = key[0]
            last_node_num = key[1]
            if lastVis == vis :# 一緒の間は値を比べて最短を保持
                if tb.FT < self.route1.TB[vis,minFTlastNode].FT:
                    minFTlastNode = last_node_num
            else: # 変わったら変わる前のvisとそのvisの最短のlast_node_numを辞書に登録
                self.bestLastNodeEachVis1[lastVis] = minFTlastNode
                lastVis = vis
                minFTlastNode = last_node_num
        
        s='0'+str(self.route1.map.CN)+'b'
        lastVis = format(1,s)
        minFTlastNode = 1
        for key,tb in sort2:
            vis = key[0]
            last_node_num = key[1]
            if lastVis == vis :# 一緒の間は値を比べて最短を保持
                if tb.FT < self.route2.TB[vis,minFTlastNode].FT:
                    minFTlastNode = last_node_num
            else: # 変わったら変わる前のvisとそのvisの最短のlast_node_numを辞書に登録
                self.bestLastNodeEachVis2[lastVis] = minFTlastNode
                lastVis = vis
                minFTlastNode = last_node_num
        #for vis,last_node_num in self.bestLastNodeEachVis.items():
        #    print("vis",vis,"  last node",last_node_num)

    def findMinBCLastNodeEachVis(self):
        sort1 = sorted(self.route1.TB.items())
        sort2 = sorted(self.route2.TB.items())  # TBをkey（vis,lastNode）で00001から始まるソート
        #for key,tb in sort1:
        #    print(key[0],key[1])
        
        s='0'+str(self.route1.map.CN)+'b'
        lastVis = format(1,s)
        minBClastNode = 1
        for key,tb in sort1:
            vis = key[0]
            last_node_num = key[1]
            if lastVis == vis :# 一緒の間は値を比べて最短を保持
                if tb.BC < self.route1.TB[vis,minBClastNode].BC:
                    minBClastNode = last_node_num
            else: # 変わったら変わる前のvisとそのvisの最短のlast_node_numを辞書に登録
                self.bestLastNodeEachVis1[lastVis] = minBClastNode
                lastVis = vis
                minBClastNode = last_node_num
        
        #同じことをroute2にも
        s='0'+str(self.route2.map.CN)+'b'
        lastVis = format(1,s)
        minBClastNode = 1
        for key,tb in sort2:
            vis = key[0]
            last_node_num = key[1]
            if lastVis == vis :# 一緒の間は値を比べて最短を保持
                if tb.BC < self.route2.TB[vis,minBClastNode].BC:
                    minBClastNode = last_node_num
            else: # 変わったら変わる前のvisとそのvisの最短のlast_node_numを辞書に登録
                self.bestLastNodeEachVis2[lastVis] = minBClastNode
                lastVis = vis
                minBClastNode = last_node_num
        
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

    def findMinFT2flight(self):
        self.findMinTimeLastNodeEachVis()
        minFT = None
        minSumFT = None
        
        bestFlight1 = (None,None)
        bestFlight2 = (None,None)
        
        for vis,lastNode in self.bestLastNodeEachVis1.items():
            opposeVis = self.criateOpposeVis(vis)

            if opposeVis == False:
                return False
            if opposeVis not in self.bestLastNodeEachVis2:
                continue

            opposeLastNode = self.bestLastNodeEachVis2[opposeVis]
            if minFT == None or minFT >= max(self.route1.TB[vis,lastNode].FT,self.route2.TB[opposeVis,opposeLastNode].FT):
                if minFT == max(self.route1.TB[vis,lastNode].FT,self.route2.TB[opposeVis,opposeLastNode].FT):
                    if minSumFT > self.route1.TB[vis,lastNode].FT + self.route2.TB[opposeVis,opposeLastNode].FT:
                        bestFlight1 = (vis,lastNode)
                        bestFlight2 = (opposeVis,opposeLastNode)
                        #minFT = max(self.route1.TB[vis,lastNode].FT,self.route2.TB[opposeVis,opposeLastNode].FT)
                        minSumFT = self.route1.TB[vis,lastNode].FT + self.route2.TB[opposeVis,opposeLastNode].FT
                bestFlight1 = (vis,lastNode)
                bestFlight2 = (opposeVis,opposeLastNode)
                minFT = max(self.route1.TB[vis,lastNode].FT,self.route2.TB[opposeVis,opposeLastNode].FT)
                minSumFT = self.route1.TB[vis,lastNode].FT + self.route2.TB[opposeVis,opposeLastNode].FT
        
        #FTのMAX値が同じ場合FTの合計値も比べたほうがいいかも。(FT1,FT2)=(5,4),(5,2)が同じ評価になってるから。
        if bestFlight1 == (None,None) and bestFlight2 == (None,None):
            print("we can't visit all victim with 2 flight.")
            sys.exit()
        else:
            self.flightDrone1 = bestFlight1
            self.flightDrone2 = bestFlight2
        """
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
        """
        
        self.flightDrone1 = bestFlight1
        self.flightDrone2 = bestFlight2

        self.drone1FT = self.route1.TB[self.flightDrone1[0],self.flightDrone1[1]].FT
        self.drone1BC = self.route1.TB[self.flightDrone1[0],self.flightDrone1[1]].BC
        self.drone2FT = self.route2.TB[self.flightDrone2[0],self.flightDrone2[1]].FT
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
    
    def findMinBC2flight(self):
        self.findMinBCLastNodeEachVis()
        minFT = None

        bestFlight1 = (None,None)
        bestFlight2 = (None,None)
        
        for vis,lastNode in self.bestLastNodeEachVis1.items():
            opposeVis = self.criateOpposeVis(vis)

            if opposeVis == False:
                return False
            if opposeVis not in self.bestLastNodeEachVis2:
                continue

            opposeLastNode = self.bestLastNodeEachVis2.get(opposeVis)
            
            #こっちは評価基準MAXじゃなくて合計値
            if minFT == None or minFT > self.route1.TB[vis,lastNode].BC + self.route2.TB[opposeVis,opposeLastNode].BC:
                bestFlight1 = (vis,lastNode)
                bestFlight2 = (opposeVis,opposeLastNode)
                
                minFT = self.route1.TB[vis,lastNode].BC + self.route2.TB[opposeVis,opposeLastNode].BC
        
        if bestFlight1 == (None,None) and bestFlight2 == (None,None):
            print("we can't visit all victim with 2 flight.")
            sys.exit()
        else:
            self.flightDrone1 = bestFlight1
            self.flightDrone2 = bestFlight2
        """
        #これはfindMinFT2flight()でしかいらんはず
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
        """

        self.drone1FT = self.route1.TB[self.flightDrone1[0],self.flightDrone1[1]].FT
        self.drone1BC = self.route1.TB[self.flightDrone1[0],self.flightDrone1[1]].BC
        self.drone2FT = self.route2.TB[self.flightDrone2[0],self.flightDrone2[1]].FT
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


