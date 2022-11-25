import random


f = open('map1.txt','w')

# 任意マップ作成 
# node = 'x座標, y座標, demand 'のリスト作成

"""
nodelist = ['1000, 200, 0.1 \n','1200, 800, 0.1 \n','500, 900, 0.1 \n','300, 700, 0.1 \n',]

f.writelines(nodelist)

f.close()
"""

#ランダムマップ作成

N = 4  # ノード数
for i in range(N) :
    x = random.randint(100,1500)
    y = random.randint(100,1500)
    demand = random.randint(1,3)/10
    print("node_num : ", i, ", x : ", x, ", y : ", y, ", demand : ", demand,)
    nodeStr = str(x)+","+str(y)+","+str(demand)+"\n"
    f.write(nodeStr)
    

f.close()

#ファイル出力