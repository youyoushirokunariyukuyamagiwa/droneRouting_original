import sys
import os
sys.path.append(os.path.abspath(".."))
from matplotlib import pyplot

from field.map import Map
from field.node import Node
from model.airframe import Airframe
from .value import Value

class SingleDP:
    
    def __init__(self,drone,mapFilePath) -> None:
        self.drone = drone
        self.map = Map(mapFilePath)
        self.visitedList = []
        self.TB = {} #  TB[状態(vis),最後に訪れたノード番号] = value(最後から2番目に訪れたノード番号,この状態(vis)でこのlastnodeのときの最短時間,それにかかるバッテリー消費量)
        self.goalFlag = 0
        self.bestRoute = [0]

    #  visited2の状態でnode_numがすでに訪問済みかどうか
    def checkVisited(self,visited:str, nodeNum:int):
        if visited[-nodeNum] == '1':  # 後ろから数えてnode_num番目
            return True
        else:
            return False

    #  現visitedから未訪問ノードを追加訪問した新visitedを作成
    def criatePlusVisited(self,visited:str, plusNodeNum:int):
        vislst = list(visited)
        vislst[-plusNodeNum] = "1"
        plsVis = "".join(vislst)

        return plsVis

    #  現visitedから訪問済みノードを削除した新visitedを作成
    def criateMinusVisited(self,visited:str, minusNodeNum):
        vislst = list(visited)
        vislst[-minusNodeNum] = "0"
        minusVis = "".join(vislst)

        return minusVis

    #  未訪問ノードnextNodeを訪問する際かかるバッテリー消費量
    def calcPlusBC(self,nowNodeNum:int,nextNodeNum:int,nowVis:str):
        nowValue = self.TB.get((nowVis,nowNodeNum))
        if nowValue == None:
            return None #  このvisとこのnow_nodeの組み合わせは存在していないのでcontinue
        else:
            distance = self.map.dMatrix[nowNodeNum][nextNodeNum]
            demand = self.map.nodeList[nextNodeNum].demand
            BC = nowValue.BC + self.drone.calcBattery_f(distance,demand)

        tmpNodeNum = nowNodeNum
        tmpVis = nowVis
        bc =  0
        while True:#過去のルートで発生するto_nodeに届ける荷物の分のB消費量
            if tmpNodeNum == 0:
                break

            previousNodeNum = self.TB[tmpVis,tmpNodeNum].previous

            d = self.map.dMatrix[previousNodeNum][tmpNodeNum]
            bc += self.drone.calcBattery_f(d,demand)
            tmpVis = self.criateMinusVisited(tmpVis,tmpNodeNum)
            tmpNodeNum = previousNodeNum

        return BC+bc

    def checkVisitable(self,fromNodeNum:Node,toNodeNum:Node,nowVis:str,payload):
        if payload + self.map.nodeList[toNodeNum].demand > self.drone.maxPayload_kg: #  現在の出発時搭載ペイロード量＋toNode需要量が機体の搭載可能量を超えているならfalse
            return False
        plsBC = self.calcPlusBC(fromNodeNum,toNodeNum,nowVis)
        if plsBC == None:
            return False
        elif plsBC + self.drone.calcBattery_f(self.map.dMatrix[toNodeNum][0],0) <= self.drone.battery_j:
            return plsBC
        else:
            return False

    def criateTBobjectT(self):
        s='0'+str(self.map.CN)+'b'
        zeroVis = format(0,s) #  どこにも訪れていない状態のvisited作成

        for first in self.map.customerList: #  始めのデポ→各ノードまで
            newVis = self.criatePlusVisited(zeroVis,first.nodeNum)

            d = self.map.dMatrix[0][first.nodeNum] #  デポ→nextまでの距離
            ft = d/self.drone.speed_m_s + self.drone.takeOffTime_s
            payload = first.demand #  nextに行くときのpayload

            BC = self.drone.calcBattery_f(d,payload)
            if BC < self.drone.battery_j and payload < self.drone.maxPayload_kg : #  バッテリー制限とペイロード制限
                value = Value(0,ft,BC,payload)
                self.TB[newVis,first.nodeNum] = value
                self.visitedList.append(newVis)

        for vis in self.visitedList:
            for next_node in self.map.customerList:
                if self.checkVisited(vis,next_node.nodeNum) == False:
                    for now_node in self.map.customerList:
                        if self.checkVisited(vis,now_node.nodeNum) == True:

                            payload = self.TB[vis,now_node.nodeNum].DP
                            new_BC = self.checkVisitable(now_node.nodeNum,next_node.nodeNum,vis,payload)
                            if new_BC :#  now→nextに行くことが確定
                                #print(vis,next_node.nodeNum)
                                new_vis = self.criatePlusVisited(vis,next_node.nodeNum)
                                if new_vis not in self.visitedList:
                                    self.visitedList.append(new_vis)
                                new_FT = self.map.dMatrix[now_node.nodeNum][next_node.nodeNum]/self.drone.speed_m_s + self.TB[vis,now_node.nodeNum].FT + self.drone.takeOffTime_s
                                if (new_vis,next_node.nodeNum) not in self.TB.keys() or self.TB[new_vis,next_node.nodeNum].FT > new_FT:
                                    self.TB[new_vis,next_node.nodeNum] = Value(now_node.nodeNum,new_FT,new_BC,payload+next_node.demand)

        for key,tb in self.TB.items():
            vis = key[0]
            last_node_num = key[1]

            last_distance = self.map.dMatrix[last_node_num][0]
            last_flightTime = last_distance/self.drone.speed_m_s + self.drone.takeOffTime_s
            last_BC = self.drone.calcBattery_f(last_distance,0)
            self.TB[vis,last_node_num] = Value(tb.previous, tb.FT+last_flightTime, tb.BC+last_BC,tb.DP)

    def criateTBobjectB(self):
        s='0'+str(self.map.CN)+'b'
        zeroVis = format(0,s) #  どこにも訪れていない状態のvisited作成

        for first in self.map.customerList: #  始めのデポ→各ノードまで
            newVis = self.criatePlusVisited(zeroVis,first.nodeNum)

            d = self.map.dMatrix[0][first.nodeNum] #  デポ→nextまでの距離
            ft = d/self.drone.speed_m_s + self.drone.takeOffTime_s
            payload = first.demand #  nextに行くときのpayload

            BC = self.drone.calcBattery_f(d,payload)
            if BC < self.drone.battery_j and payload < self.drone.maxPayload_kg : #  バッテリー制限とペイロード制限
                value = Value(0,ft,BC,payload)
                self.TB[newVis,first.nodeNum] = value
                self.visitedList.append(newVis)

        for vis in self.visitedList:
            for next_node in self.map.customerList:
                if self.checkVisited(vis,next_node.nodeNum) == False:
                    for now_node in self.map.customerList:
                        if self.checkVisited(vis,now_node.nodeNum) == True:

                            payload = self.TB[vis,now_node.nodeNum].DP
                            new_BC = self.checkVisitable(now_node.nodeNum,next_node.nodeNum,vis,payload)
                            if new_BC :#  now→nextに行くことが確定
                                #print(vis,next_node.nodeNum)
                                new_vis = self.criatePlusVisited(vis,next_node.nodeNum)
                                if new_vis not in self.visitedList:
                                    self.visitedList.append(new_vis)
                                new_FT = self.map.dMatrix[now_node.nodeNum][next_node.nodeNum]/self.drone.speed_m_s + self.TB[vis,now_node.nodeNum].FT + self.drone.takeOffTime_s
                                if (new_vis,next_node.nodeNum) not in self.TB.keys() or self.TB[new_vis,next_node.nodeNum].BC > new_BC:
                                    self.TB[new_vis,next_node.nodeNum] = Value(now_node.nodeNum,new_FT,new_BC,payload+next_node.demand)

        for key,tb in self.TB.items():
            vis = key[0]
            last_node_num = key[1]

            last_distance = self.map.dMatrix[last_node_num][0]
            last_flightTime = last_distance/self.drone.speed_m_s + self.drone.takeOffTime_s
            last_BC = self.drone.calcBattery_f(last_distance,0)
            self.TB[vis,last_node_num] = Value(tb.previous, tb.FT+last_flightTime, tb.BC+last_BC,tb.DP)

    def printBestRoute(self):
        all_vis = "1"*self.map.CN
        best_time = 9999999999999
        for key,tb in self.TB.items():
            vis = key[0]
            last_node_num = key[1]

            if vis == all_vis :
                self.goalFlag = 1
                if tb.FT < best_time:
                    best_last_node_num = last_node_num
                    best_time = tb.FT

        if self.goalFlag == 1:
            self.bestRoute.append(best_last_node_num)
            now_node_num = best_last_node_num
            now_vis = all_vis
            while True:
                if now_node_num == 0:
                    break

                previous_node_num = self.TB[now_vis,now_node_num].previous
                self.bestRoute.append(previous_node_num)

                now_vis = self.criateMinusVisited(now_vis,now_node_num)
                now_node_num = previous_node_num

            self.bestRoute.reverse()
            print(self.bestRoute)
            print("flight time :",self.TB[all_vis,best_last_node_num].FT,"battery consumption :",self.TB[all_vis,best_last_node_num].BC,"departure payload:",self.TB[all_vis,best_last_node_num].DP)
        elif self.goalFlag == 0:
            print("We can't visit all victim.\n")

    def plotRouteFig(self):
        if self.goalFlag == 0 or len(self.bestRoute) <= 1:
            return False
        fig = pyplot.figure()
        ax = fig.add_subplot(111)

        ax.plot(*[0,0], 'o', color="blue") #  デポのプロット
        for p in self.map.customerList: #  ノードのプロット
            ax.plot(*[p.x,p.y], 'o', color="red")

        for i in range(len(self.bestRoute)-1): #  矢印のプロット
            fromNode = self.map.nodeList[self.bestRoute[i]]
            toNode = self.map.nodeList[self.bestRoute[i+1]]
            ax.annotate('', xy=[toNode.x,toNode.y], xytext=[fromNode.x,fromNode.y],
                        arrowprops=dict(shrink=0, width=1, headwidth=8, 
                                        headlength=10, connectionstyle='arc3',
                                        facecolor='gray', edgecolor='gray')
                        )

        ax.set_xlim([0, 1.2*self.map.maxXY])
        ax.set_ylim([0, 1.2*self.map.maxXY])

        pyplot.show()
        

if __name__ == "__main__":
    map.readMapFile("../data/map2.txt")

    