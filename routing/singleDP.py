import sys
import os
sys.path.append(os.path.abspath(".."))

from field import map
from field import node
from model import airframe
from model import vtol

#  visited2の状態でnode_numがすでに訪問済みかどうか
def checkVisited(visited2:str, node_num:int, N:int):
    if visited2[-1*node_num] == '1': #後ろから数えてnode_num番目
        return True
    else:
        return False

def criateNewVisited(visited2:str, nextNode_num:int, N:int):
    if checkVisited(visited2,nextNode_num,N): #すでに訪問済みなら終わる
        return False
    
    vislst = list(visited2)
    vislst[-nextNode_num] = "1"
    new_vis = "".join(vislst)

    return new_vis

def criateMinusVisited(visited2:str, minusNode_num):
    if visited2[-minusNode_num] == 0: #  そもそも未訪問ならfalseを返す
        return False
    vislst = list(visited2)
    vislst[-minusNode_num] = "0"
    minusVis = "".join(vislst)

    return minusVis

def calcBatteryCons(TB,cList,airframe:airframe,now_node:node,next_node:node,now_vis:str):
    BC = TB[now_vis,now_node.node_num].BC 
    + airframe.calcBattery_f(map.Map.distance(now_node,next_node),next_node.demand)
    + airframe.calcBattery_f(map.Map.distance(next_node,depo),0)
    
    tmp_node = now_node
    tmp_vis = now_vis
    bc =  0
    while True:#過去のルートで発生するto_nodeに届ける荷物の分のB消費量
        
        if tmp_node == depo:
            break

        if(TB[tmp_vis,tmp_node.node_num].previous == 0): #  デポだけcListに入ってないので、番号で識別して場合分け
            previous_node = depo
        else:
            previous_node = cList[TB[tmp_vis,tmp_node.node_num].previous-1]
        
        d = map.Map.distance(previous_node,tmp_node)
        bc += airframe.calcBattery_f(d,next_node.demand)
        tmp_vis = criateMinusVisited(tmp_vis,tmp_node.node_num)
        tmp_node = previous_node
        
    return BC+bc

def checkVisitable(TB,cList,airframe:airframe,from_node:node,to_node:node,now_vis:str):
    if calcBatteryCons(TB,cList,airframe,from_node,to_node,now_vis) <= airframe.battery_j:
        return True
    else:
        return False

class Value:
    def __init__(self):
        self.previous = 0
        self.flightTime = 0
        self.BC = 0

    def __init__(self,previous,flightTime,BC):
        self.previous = previous
        self.flightTime = flightTime
        self.BC = BC

if __name__ == "__main__":
    m = map.Map()
    m.readMapFile("../data/map1.txt")
    N = len(m.cList)
    drone = vtol.Vtol()
    depo = node.Node(0,0,0,0)

    visited = [] #  2進数string
    TB = {} #辞書 key:(visited , LastNode_num) value:Value}
    
    s='0'+str(N)+'b'
    now = format(0,s) #  どこにも訪れていない状態の

    for next in m.cList: #  始めのデポ→各ノードまで
        newVis = criateNewVisited(now,next.node_num,N)
        
        d = m.distance(depo,next) #  デポ→nextまでの距離
        ft = d/drone.speed_m_s
        payload = next.demand #  nextに行くときのpayload
        
        BC = drone.calcBattery_f(d,payload)
        value = Value(0,ft,BC)
        TB[newVis,next.node_num] = value
        visited.append(newVis)
    

    for key,ptb in list(TB.items()):
        print(key[0],key[1],ptb.BC)
        vis = key[0]
        lastNode = key[1]

        for next in m.cList:
            if checkVisited(vis,next.node_num,N) == False:
                for previous in m.cList:
                    if checkVisited(vis,previous.node_num,N) == True:

                        new_BC = calcBatteryCons(TB,m.cList,drone,previous,next,vis)
                        if new_BC <= drone.battery_j: #  prevoius→nextに行くことが確定

                            new_vis = criateNewVisited(vis,next.node_num,N)
                            if new_vis not in visited:
                                visited.append(new_vis)
                            new_FT = m.distance(previous,next)/drone.speed_m_s + ptb.flightTime
                            if (new_vis,next.node_num) not in TB.keys() or TB[new_vis,next.node_num].flightTime > new_FT:
                                TB[new_vis,next.node_num] = Value(previous,new_FT,new_BC)

    

                            
                    





    
