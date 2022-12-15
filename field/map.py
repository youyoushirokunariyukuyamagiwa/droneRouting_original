#import sys
#import os
#sys.path.append(os.path.abspath("."))

import random
import math
from . import node #  singleDPを実行するときはこうしないとエラーでる
#import node #  新しいマップファイルを作成するときはこっちじゃないとエラー出る

class Map:

    def __init__(self,mapFilePass) -> None:
        self.customerList = [] #  配達先のノードリスト
        self.nodeList = [] #  customerList + デポ
        self.dMatrix = [] #  距離の表
        self.CN = 0
        self.N = 0
        self.maxXY = 0
        self.depo = node.Node(0,0,0,0)
        self.nodeList.append(self.depo)
        self.readMapFile(mapFilePass)
        self.criateDmatrix()
    
    #  ランダムマップ作成
    # node = 'x座標, y座標, demand 'のリスト作成
    @staticmethod
    def criateMapFile(N:int):
        f = open('../data/map1.txt','w')
        f.write("x-axis, y-axis, demand")

        for i in range(N) :
            f.write("\n")
            x = random.randint(100,300)
            y = random.randint(100,300)
            demand = random.randint(1,4)/10
            print("node_num : ", i+1, ", x : ", x, ", y : ", y, ", demand : ", demand,)
            nodeStr = str(x)+","+str(y)+","+str(demand)
            f.write(nodeStr)

        f.close()
    

    def readMapFile(self,fileName):
        f = open(fileName,'r')
        next(f) #  ファイルの2行目から読み込み
        nodeNum = 1 #  nodeListのインデックスと対応

        while True: #  マップのファイルから顧客リストを作成
            nodeStr = f.readline() #  ファイルから1行読む
            if nodeStr == '': #  EOFになったら終了
                break
            nodeList = nodeStr.split(',') #  カンマで分割してx座標,y座標,demandを取得
            x = int(nodeList[0])
            if x > self.maxXY:
                self.maxXY = x
            y = int(nodeList[1])
            if y > self.maxXY:
                self.maxXY = y
            demand = float(nodeList[2])
            n = node.Node(nodeNum,x,y,demand) #  nodeクラスに変換
            self.customerList.append(n) #  顧客リストに追加
            self.nodeList.append(n)
            print("node_num : ", nodeNum, ", x : ", x, ", y : ", y, ", demand : ", demand)
            nodeNum += 1
            self.CN += 1
        self.N = nodeNum
        f.close()

    def distance(self,fromNodeNum,toNodeNum):
        fromNode = self.nodeList[fromNodeNum]
        toNode = self.nodeList[toNodeNum]
        return math.sqrt((fromNode.x - toNode.x)**2 + (fromNode.y - toNode.y)**2)

    def criateDmatrix(self):
        for i in range(self.N):
            dList = []
            for j in range(self.N):
                d = self.distance(i,j)
                dList.append(d)
            self.dMatrix.append(dList)

if __name__ == "__main__":
    Map.criateMapFile(5)