from map import node

f = open('map/map1.txt','r')
next(f) #  ファイルの2行目から読み込み
node_num = 0
cList = []

while True: #  マップのファイルから顧客リストを作成
  nodeStr = f.readline() #  ファイルから1行読む
  if nodeStr == '': #  EOFになったら終了
    break
  nodeList = nodeStr.split(',') #  カンマで分割してx座標,y座標,demandを取得
  x = int(nodeList[0])
  y = int(nodeList[1])
  demand = float(nodeList[2])
  n = node.Node(node_num,x,y,demand) #  nodeクラスに変換
  cList.append(n) #  顧客リストに追加
  print("node_num : ", node_num, ", x : ", x, ", y : ", y, ", demand : ", demand)
  node_num += 1

