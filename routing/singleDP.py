import sys
import os
sys.path.append(os.path.abspath(".."))

from field import map
from field import node
from model import airframe
from model import vtol
from model import multicopter

#  visited2の状態でnode_numがすでに訪問済みかどうか
def checkVisited(visited2, node_num:int, N:int):
    if visited2[-node_num] == '1': #後ろから数えてnode_num番目
        return True
    else:
        return False

def criateNewVisited(visited2:str, nextNode_num:int, N:int):
    vislst = list(visited2)
    vislst[-nextNode_num] = "1"
    new_vis = "".join(vislst)

    return new_vis

def criateMinusVisited(visited2:str, minusNode_num):
    vislst = list(visited2)
    vislst[-minusNode_num] = "0"
    minusVis = "".join(vislst)

    return minusVis

def calcBatteryCons(TB,cList,airframe:airframe,now_node:node,next_node:node,now_vis:str):
    
    now_value = TB.get((now_vis,now_node.node_num))
    if now_value == None:
        return None #  このvisとこのnow_nodeの組み合わせは存在していないのでcontinue
    else:
        BC = now_value.BC + airframe.calcBattery_f(map.Map.distance(now_node,next_node),next_node.demand)
    
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
    m.readMapFile("../data/map2.txt")
    N = len(m.cList)
    drone = multicopter.Multi()
    #drone = vtol.Vtol()
    depo = node.Node(0,0,0,0)

    visited = [] #  2進数string
    TB = {} #辞書 key:(visited , LastNode_num) value:Value}
    
    s='0'+str(N)+'b'
    zero_vis = format(0,s) #  どこにも訪れていない状態の

    for first in m.cList: #  始めのデポ→各ノードまで
        newVis = criateNewVisited(zero_vis,first.node_num,N)
        
        d = m.distance(depo,first) #  デポ→nextまでの距離
        ft = d/drone.speed_m_s + drone.takeOffTime_s
        payload = first.demand #  nextに行くときのpayload
        
        BC = drone.calcBattery_f(d,payload)
        value = Value(0,ft,BC)
        TB[newVis,first.node_num] = value
        visited.append(newVis)
    

    for vis in visited:
        for next_node in m.cList:
            if checkVisited(vis,next_node.node_num,N) == False:
                for now_node in m.cList:
                    if checkVisited(vis,now_node.node_num,N) == True:

                        new_BC = calcBatteryCons(TB,m.cList,drone,now_node,next_node,vis)
                        if new_BC != None and new_BC + drone.calcBattery_f(map.Map.distance(next_node,depo),0) <= drone.battery_j: #  now→nextに行くことが確定
                            #print(vis,next_node.node_num)
                            new_vis = criateNewVisited(vis,next_node.node_num,N)
                            if new_vis not in visited:
                                visited.append(new_vis)
                            new_FT = m.distance(now_node,next_node)/drone.speed_m_s + TB[vis,now_node.node_num].flightTime + drone.takeOffTime_s
                            if (new_vis,next_node.node_num) not in TB.keys() or TB[new_vis,next_node.node_num].flightTime > new_FT:
                                TB[new_vis,next_node.node_num] = Value(now_node.node_num,new_FT,new_BC)

#    for key,tb in TB.items():
#        print(key[0],key[1],tb.flightTime,tb.BC)

    for key,tb in TB.items():
        vis = key[0]
        last_node_num = key[1]
        
        last_distance = map.Map.distance(m.cList[last_node_num-1],depo)
        last_flightTime = last_distance/drone.speed_m_s + drone.takeOffTime_s
        last_BC = drone.calcBattery_f(last_distance,0)
        TB[vis,last_node_num] = Value(tb.previous, tb.flightTime+last_flightTime, tb.BC+last_BC)

    print("-------------------------------")
    for key,tb in TB.items():
        print(key[0],key[1],tb.flightTime,tb.BC)


    all_vis = "1"*N
    best_root = [0] 
    best_time = 9999999999999
    goal_flag = 0
    for key,tb in TB.items():
        vis = key[0]
        last_node_num = key[1]
        
        if vis == all_vis :
            goal_flag = 1
            if tb.flightTime < best_time:
                best_last_node_num = last_node_num
                best_time = tb.flightTime
    
    if goal_flag == 1:
        best_root.append(best_last_node_num)
        now_node_num = best_last_node_num
        now_vis = all_vis
        while True:
            if now_node_num == 0:
                break

            if(TB[now_vis,now_node_num].previous == 0): #  デポだけcListに入ってないので、番号で識別して場合分け
                previous_node_num = 0 #デポ
            else:
                previous_node_num = TB[now_vis,now_node_num].previous

            best_root.append(previous_node_num)
        
            now_vis = criateMinusVisited(now_vis,now_node_num)
            now_node_num = previous_node_num

        best_root.reverse()
        print(best_root)
        print("flight time :",TB[all_vis,best_last_node_num].flightTime,"battery consumption :",TB[all_vis,best_last_node_num].BC)
    elif goal_flag == 0:
        print("We can't visit all victim.\n")
            






    
