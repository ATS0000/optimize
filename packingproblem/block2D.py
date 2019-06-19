from pulp import *
import xlrd
import random
import matplotlib.pyplot as plt
#import numpy as np
import matplotlib.cm as cm
import matplotlib.animation as animation
import time

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)

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
n = 8
w = []
h = []
for i in range(n):
      w.append(random.uniform(1, 8))
      h.append(random.uniform(1, 8))

print(w)
print(h)

m = LpProblem( sense= LpMinimize)
x = [LpVariable("x%d" %i, lowBound =0) for i in range(n)]
y = [LpVariable("y%d" %i, lowBound =0) for i in range(n)]
u = [[LpVariable("u%d%d" %(i,j),cat= LpBinary ) for j in range(n)] for i in range(n)]
v = [[LpVariable("v%d%d" %(i,j),cat= LpBinary ) for j in range(n)] for i in range(n)]
H = LpVariable("H")
m += H

W = 26
UB = 80
for i in range(n):
    for j in range(n):
        m += x[i]+w[i] <= x[j]+W*(1-u[i][j])
        m += y[i]+h[i] <= y[j]+UB*(1-v[i][j])

        if i < j:
            m += u[i][j]+u[j][i] + v[i][j]+v[j][i] >= 1

for i in range(n):
    m += x[i] <= W-w[i]
    m += y[i] <= H-h[i]

status = m.solve()
print(pulp.LpStatus[status])
print("目的関数値 = {}".format(pulp.value(m.objective)))
finishtime = time.time()

#ims = []
#im = ax.add_patch(plt.Rectangle(xy=(0, 0), width=0, height=0, angle=0))
def plot(i):
    #plt.cla()
    #plt.plot(pulp.value(x[i]), pulp.value(y[i]), 'o')
    x[i] = pulp.value(x[i])
    y[i] = pulp.value(y[i])
    rect = plt.Rectangle((x[i],y[i]),w[i],h[i], fc=cm.hsv(i/10.0), ec="black")
    #im = plt.plot(rect)
    ax.add_patch(rect)

    #ims.append([im])

    ax.set_xlim([0,W])
    ax.set_ylim([0,pulp.value(m.objective)+1])





#plt.show()
print(f'計算時間：{finishtime - starttime}')

#ax.add_patch(rect)
#ani = animation.ArtistAnimation(fig, ims, interval=300,repeat_delay=10)
ani = animation.FuncAnimation(fig, plot, interval=200)
plt.show()
ani.save('block2D.gif')
