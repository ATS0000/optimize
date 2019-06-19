from pulp import *
import xlrd
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
import time



#注意！奥行きがz,高さがy

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')

starttime = time.time()

'''
book = xlrd.open_workbook('block_x_y.xlsx')
sheet = book.sheet_by_name('Sheet1')
def get_list_2d_all(sheet):
    return [sheet.row_values(row) for row in range(sheet.nrows)]
S = get_list_2d_all(sheet)
S = np.array(W)
for i in range(n):
    w[i] = S[i]
    w[j] = S[j]
'''
n = 10
w = []
h = []
s = []
for i in range(n):
      w.append(random.uniform(10, 100))
      h.append(random.uniform(20, 70))
      s.append(random.uniform(10, 30))

print(w)
print(h)
print(s)

m = LpProblem( sense= LpMinimize)
x = [LpVariable("x%d" %i, lowBound =0) for i in range(n)]
y = [LpVariable("y%d" %i, lowBound =0) for i in range(n)]
z = [LpVariable("z%d" %i, lowBound =0) for i in range(n)]
u = [[LpVariable("u%d%d" %(i,j),cat= LpBinary ) for j in range(n)] for i in range(n)]
v = [[LpVariable("v%d%d" %(i,j),cat= LpBinary ) for j in range(n)] for i in range(n)]
l = [[LpVariable("l%d%d" %(i,j),cat= LpBinary ) for j in range(n)] for i in range(n)]
H = LpVariable("H")
m += H

W = 3000
UB = 4000
S = 4000
for i in range(n):
    for j in range(n):
        m += x[i]+w[i] <= x[j]+W*(1-u[i][j])
        m += y[i]+h[i] <= y[j]+UB*(1-v[i][j])
        m += z[i]+s[i] <= z[j]+S*(1-l[i][j])


        if i < j:
            m += u[i][j]+u[j][i] + v[i][j]+v[j][i] >= 1
            m += u[i][j]+u[j][i] + l[i][j]+l[j][i] >= 1
            m += l[i][j]+l[j][i] + v[i][j]+v[j][i] >= 1


for i in range(n):
    m += x[i] <= W-w[i]
    m += y[i] <= H-h[i]
    m += z[i] <= S-h[i]

status = m.solve()
print(pulp.LpStatus[status])
print("目的関数値 = {}".format(pulp.value(m.objective)))
finishtime = time.time()


for i in range(n):
    #plt.plot(pulp.value(x[i]), pulp.value(y[i]), 'o')
    x[i] = pulp.value(x[i])
    y[i] = pulp.value(y[i])
    z[i] = pulp.value(z[i])
    rect = plt.Rectangle((x[i],y[i]),w[i],h[i], fc=cm.hsv(i/10.0), ec="black")
    ax.add_patch(rect)

'''
ax.set_xlim([0,W])
ax.set_ylim([0,UB])
ax.set_zlim([0,S])
'''

plt.show()
print(f'計算時間：{finishtime - starttime}')
