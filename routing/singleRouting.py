import sys
import os
import math
sys.path.append(os.path.abspath(".."))
from matplotlib import pyplot

from field.map import Map
from field.node import Node
from model.airframe import Airframe
from .value import Value

class SingleRouting():
    
    def __init__(self,custmerMap,drone,allCustomerNum) -> None:
        self.drone = drone
        self.allCustomerNum = allCustomerNum
        self.custmerMap = custmerMap
        self.visitedList = []#訪問済みノードの集合visを格納。visは各customerに訪問済みかどうかを1 or 0で評価し、リストに格納
        # 例 vis:001101 となる場合、顧客は全部で６カ所あり、ノード番号1,3,4の顧客が訪問済みを表している。これはvis[-(ノード番号)]=1 or 0で確認できる
        self.TB = {}#  TB[状態(vis),最後に訪れたノード番号] = value(最後から2番目に訪れたノード番号,この状態(vis)でこのlastnodeのときの最短時間,それにかかるバッテリー消費量)
        self.bestRoute = [0]
        self.FT = None
        self.BC = None
        self.depo = Node(0,0,0,0)
        self.all_vis = self.makeAllvisFromCustomerList(self.custmerMap,allCustomerNum)
    
    def checkSumDemand(self,custmerMap):
        sumDemand = 0
        for c in custmerMap:
            sumDemand += c.demand
        
        return sumDemand

    #  2進数visitedの状態でnode_numがすでに訪問済みかどうか
    def checkVisited(self,visited:str, nodeNum:int):
        if visited[-nodeNum] == '1':  # 後ろから数えてnode_num番目
            return True
        else:
            return False

    #  現visitedから未訪問ノードを追加訪問した新visitedを作成
    def criatePlusVisited(self,vis:str, plusNodeNum:int):
        vislst = list(vis)
        vislst[-plusNodeNum] = "1"
        plsVis = "".join(vislst)

        return plsVis

    #  現visitedから任意の訪問済みノードを１つ削除した新visitedを作成
    def criateMinusVisited(self,vis:str, minusNodeNum):
        vislst = list(vis)
        vislst[-minusNodeNum] = "0"
        minusVis = "".join(vislst)

        return minusVis

    #  未訪問ノードnextNodeを訪問する際かかるバッテリー消費量
    def calcPlusBC(self,nowNode:Node,nextNode:Node,nowVis:str):
        nowValue = self.TB.get((nowVis,nowNode))
        if nowValue == None:
            return None #  このvisとこのnow_nodeの組み合わせは存在していないのでcontinue
        else:
            distance = self.calcDistance(nowNode,nextNode)
            demand = nextNode.demand
            BC = nowValue.BC + self.drone.calcBattery_f(distance,demand)
        
        tmpNode = nowNode
        tmpVis = nowVis
        bc =  0
        while True:#過去のルートで発生するto_nodeに届ける荷物の分のB消費量
            if tmpNode.nodeNum == 0:
                break

            previousNode = self.TB[tmpVis,tmpNode].previous

            d = self.calcDistance(previousNode,tmpNode)
            bc += self.drone.addPayloadBC(d,demand)
            tmpVis = self.criateMinusVisited(tmpVis,tmpNode.nodeNum)
            tmpNode = previousNode

        return BC+bc

    """
    def checkVisitable(self,fromNodeNum:Node,toNodeNum:Node,nowVis:str,payload):
        if payload + self.map.nodeList[toNodeNum].demand > self.drone.maxPayload_kg: #  現在の出発時搭載ペイロード量＋toNode需要量が機体の搭載可能量を超えているならfalse
            return False
        plsBC = self.calcPlusBC(fromNodeNum,toNodeNum,nowVis)

        if plsBC == None:
            return False
        elif plsBC + self.drone.calcBattery_f(self.map.dMatrix[toNodeNum][0],0) <= self.drone.battery_p:
            return plsBC
        else: #toNode → depo まで帰ってこれない
            return False
    """
    
    def calcDistance(self,fromNode,toNode):
        d = math.sqrt((fromNode.x-toNode.x)**2 + (fromNode.y-toNode.y)**2)
        return d
    
    def makeAllvisFromCustomerList(self,customerList,allCustomerNum):
        #s='0'+str(allCustomerNum)+'b' # s = "04b" みたいになってる
        #zeroVis = format(0,s) #組み込み関数format()
        zeroVis = "0".zfill(allCustomerNum)
        for n in customerList:
            zeroVis = self.criatePlusVisited(zeroVis,n.nodeNum)
        
        return zeroVis
    
    """
    def criateTBobjectT(self):
        s='0'+str(self.map.CN)+'b'
        zeroVis = format(0,s) #  どこにも訪れていない状態のvisited作成

        for first in self.map.customerList: #  始めのデポ→各ノードまで
            newVis = self.criatePlusVisited(zeroVis,first.nodeNum)

            d_km = self.map.dMatrix[0][first.nodeNum] #  デポ→nextまでの距離
            ft_m = self.drone.calcFlightTime(d_km)
            payload_kg = first.demand #  nextに行くときのpayload

            BCP = self.drone.calcBattery_f(d_km,payload_kg)

            if BCP < self.drone.battery_p and payload_kg < self.drone.maxPayload_kg : #  バッテリー制限とペイロード制限
                value = Value(0,ft_m,BCP,payload_kg)
                self.TB[newVis,first.nodeNum] = value
                self.visitedList.append(newVis)

        for vis in self.visitedList:
            for next_node in self.map.customerList:
                if self.checkVisited(vis,next_node.nodeNum) == False:
                    for now_node in self.map.customerList:
                        if self.checkVisited(vis,now_node.nodeNum) == True:

                            
                            if self.TB.get((vis,now_node.nodeNum)) != None:
                                payload_kg = self.TB.get((vis,now_node.nodeNum)).DP
                            else:
                                continue
                            #payload_kg = self.TB[vis,now_node.nodeNum].DP
                            
                            new_BC = self.checkVisitable(now_node.nodeNum,next_node.nodeNum,vis,payload_kg)
                            if new_BC != False :#  now→nextに行くことが確定
                                #print(vis,next_node.nodeNum)
                                new_vis = self.criatePlusVisited(vis,next_node.nodeNum)
                                if new_vis not in self.visitedList:
                                    self.visitedList.append(new_vis)
                                new_FT = self.drone.calcFlightTime(self.map.dMatrix[now_node.nodeNum][next_node.nodeNum]) + self.TB[vis,now_node.nodeNum].FT
                                if (new_vis,next_node.nodeNum) not in self.TB.keys() or self.TB[new_vis,next_node.nodeNum].FT > new_FT:
                                    self.TB[new_vis,next_node.nodeNum] = Value(now_node.nodeNum,new_FT,new_BC,payload_kg+next_node.demand)

        for key,tb in self.TB.items():
            vis = key[0]
            last_node_num = key[1]

            last_distance = self.map.dMatrix[last_node_num][0]
            last_flightTime = self.drone.calcFlightTime(last_distance)
            last_BC = self.drone.calcBattery_f(last_distance,0)
            self.TB[vis,last_node_num] = Value(tb.previous, tb.FT+last_flightTime, tb.BC+last_BC,tb.DP)
    """

    def criateTBobjectB(self):
        #s='0'+str(len(self.custmerMap))+'b'
        #zeroVis = format(0,s) #  どこにも訪れていない状態のvisited作成
        zeroVis = "0".zfill(self.allCustomerNum)
        
        for first in self.custmerMap: #  始めのデポ→各ノードまで
            newVis = self.criatePlusVisited(zeroVis,first.nodeNum)

            d_km = math.sqrt((first.x)**2 + (first.y)**2) #  デポ→nextまでの距離
            ft_m = self.drone.calcFlightTime(d_km)
            payload_kg = first.demand #  nextに行くときのpayload

            BCP = self.drone.calcBattery_f(d_km,payload_kg)
            value = Value(self.depo,ft_m,BCP,payload_kg)
            self.TB[newVis,first] = value
            self.visitedList.append(newVis)

        for vis in self.visitedList:
            for next_node in self.custmerMap:
                if self.checkVisited(vis,next_node.nodeNum) == False:
                    for now_node in self.custmerMap:
                        if self.checkVisited(vis,now_node.nodeNum) == True:

                            currentValue = self.TB.get((vis,now_node))
                            if currentValue != None:
                                payload_kg = currentValue.DP
                            else:
                                continue
                            
                            new_BC = self.calcPlusBC(now_node,next_node,vis)
                            new_vis = self.criatePlusVisited(vis,next_node.nodeNum)
                            if new_vis not in self.visitedList:
                                self.visitedList.append(new_vis)
                            new_FT = self.drone.calcFlightTime(self.calcDistance(now_node,next_node)) + self.TB[vis,now_node].FT
                            if (new_vis,next_node) not in self.TB.keys() or self.TB[new_vis,next_node].BC > new_BC:
                                self.TB[new_vis,next_node] = Value(now_node,new_FT,new_BC,payload_kg+next_node.demand)

        for key,tb in self.TB.items():
            vis = key[0]
            last_node = key[1]
            if vis == self.all_vis:
                last_distance = self.calcDistance(last_node,self.depo)
                last_flightTime = self.drone.calcFlightTime(last_distance)
                last_BC = self.drone.calcBattery_f(last_distance,0)
                self.TB[vis,last_node] = Value(tb.previous, tb.FT+last_flightTime, tb.BC+last_BC,tb.DP)

    """
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
    """
    
    """
    def completeRouting(self):
        compFlightDict = {}
        TBkeyList = self.TB.keys()
        TBkeyList.sort(reverse=True) #  visが埋まっているものから決定する
        for key in TBkeyList:
            vis = key[0]
            compFlightDict[vis] = []
            opposeVis = self.criateOpposeVis(vis)
            while True:
                if opposeVis in compFlightDict.keys(): #  すでに記録されたフライトの組み合わせなら
                    break
                if opposeVis in self.TB.keys  ここ正しくない。理想はTBを最適にしたkeyがvisだけの状態のものを使うこと
                    compFlightDict[vis].append(opposeVis)
                    break
                else:
                    while True:
                        num = opposeVisを十進数に
                        num -= 1
                        newVis = numを2進数に
                        if newVis in self.TB.keys ここもうえと同様
                            compFlightDict[vis].append(newVis)
                            opposeVis = opposeVisからnewVisを引いたvisを出す関数
                            break
        if opposeVis == False:
            return False
    """

#全てのノードを通ったかどうかでstrVisの111...を探すのは間違い
    """
    def printBestRouteObjectT(self):
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
            self.FT = self.TB[all_vis,best_last_node_num].FT
            self.BC = self.TB[all_vis,best_last_node_num].BC
            
        elif self.goalFlag == 0:
            print("We can't visit all victim.\n")
            self.map.showMap()
    """
    
    def searchBestRouteObjectB(self):
        best_BC = float('inf')
        
        for key,tb in self.TB.items():
            vis = key[0]
            last_node = key[1]

            if vis == self.all_vis :
                if tb.BC < best_BC:
                    best_last_node = last_node
                    best_BC = tb.BC

        self.bestRoute.append(best_last_node)
        now_node = best_last_node
        now_vis = self.all_vis
        while True:
            if now_node.nodeNum == 0:
                break

            previous_node = self.TB[now_vis,now_node].previous
            self.bestRoute.append(previous_node)

            now_vis = self.criateMinusVisited(now_vis,now_node.nodeNum)
            now_node = previous_node

        self.bestRoute.reverse()
        #print(self.bestRoute)
        #print("flight time :",self.TB[all_vis,best_last_node].FT,"battery consumption :",self.TB[all_vis,best_last_node].BC,"departure payload:",self.TB[all_vis,best_last_node].DP)
        self.FT = self.TB[self.all_vis,best_last_node].FT
        self.BC = self.TB[self.all_vis,best_last_node].BC


    def plotRouteFig(self):
        if self.goalFlag == 0 or len(self.bestRoute) <= 1:
            return False
        fig = pyplot.figure()
        ax = fig.add_subplot(111)

        ax.plot(*[0,0], 'o', color="blue") #  デポのプロット
        for p in self.map.customerList: #  ノードのプロット
            ax.plot(*[p.x,p.y], 'o', color="red")
            ax.text(p.x, p.y,p.demand)

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

    def plotAnalysis(self):
        if self.goalFlag == 0:
            print("This routing is not completed yet")
            return False
        
        x_d_list = []
        y_b_list = []
        payload_list = []
        
        index = 0
        sumDistance = 0
        x_d_list.append(sumDistance)
        remainBattery = 100
        y_b_list.append(remainBattery)
        payload = self.map.calcSumDemand()
        payload_list.append(payload)
        
        while True:
            node1_num = self.bestRoute[index]
            node2_num = self.bestRoute[index+1]
            
            d = self.map.dMatrix[node1_num][node2_num]
            b = self.drone.calcBattery_f(d,payload)
            
            sumDistance += d
            remainBattery -= b
            x_d_list.append(sumDistance)
            y_b_list.append(remainBattery)
            
            payload -= self.map.nodeList[node2_num].demand
            payload_list.append(payload)
            
            if node2_num == 0:
                break
            
            index += 1
            
        
        fig = pyplot.figure()
        ax = fig.add_subplot(111)
        
        ax.plot(x_d_list,y_b_list,marker="o", markersize=6,markerfacecolor="blue")
        for i in range(len(self.bestRoute)):
            ax.text(x_d_list[i], y_b_list[i],self.map.nodeList[self.bestRoute[i]].demand)
        
        #ax.bar(x_d_list,payload_list)#加えて棒グラフで機体の積載量を載せたい
        #ax.set_ylabel('Axis for bar')
        
        
        ax.set_ylim([0, 100])
        pyplot.xlabel("distance(km)")
        pyplot.ylabel("remain Battery(%)")
        pyplot.grid(True)
        pyplot.show()
        
