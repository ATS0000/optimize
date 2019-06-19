import pulp
import pandas as pd
import numpy as np
import networkx as nx
import itertools
import matplotlib.pyplot as plt
num_client = 15 #顧客数（id=0,1,2,...14と番号が振られていると考える。id=0はデポ。）
capacity = 50 #トラックの容量
randint = np.random.randint

seed = 10
# 各顧客のx,y座標と需要（どのくらいの商品が欲しいか）をDataFrameとして作成
df = pd.DataFrame({"x":randint(0,100,num_client),
                   "y":randint(0,100,num_client),
                   "d":randint(5,40,num_client)})
#0番目の顧客はデポ（拠点）とみなす。なので、需要=0, 可視化の時に真ん中に来るよう、
#x,yを50に。
df.ix[0].x = 50
df.ix[0].y = 50
df.ix[0].d = 0

print(df)
print(df.ix[3].x)
# costは顧客数✖️顧客数の距離テーブル。np.arrayで保持。
#cost = create_cost()

#cost = np.sqrt((df.ix[i].x - df.ix[j].x) ** 2 + (df.ix[i].y - df.ix[j].y) ** 2)
#cost = np.array([[np.sqrt(df.ix[i].x - df.ix[j].x) ** 2 + (df.ix[i].y - df.ix[j].y) ** 2 for i in range(num_client)] for j in range(num_client)])

cost = np.array([[ 0 for i in range(num_client)] for j in range(num_client)])

for i in range(num_client):
    for j in range(num_client):
        cost[i][j] = np.sqrt((df.ix[i].x - df.ix[j].x) ** 2 + (df.ix[i].y - df.ix[j].y) ** 2)


print(cost)
