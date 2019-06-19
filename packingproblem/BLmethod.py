import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import numpy as np


fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)

def bl_candidates(i,x,y,w,h):
    cand=[(0,0)]
    for j in range(i):
        for k in range(j):
            cand += [(x[j]+ w[j],y[k]+h[k])]
            cand += [(x[k]+ w[k],y[j]+h[j])]
    for j in range(i):
        cand += [(0,y[j]+h[j])]
        cand += [(x[j]+w[j] ,0)]
    return cand


def is_feas(i,p,x,y,w,h,W):
    if p[0] < 0 or W < p[0]+w[i]:
        return False
    for j in range(i):
        if max(p[0],x[j]) < min(p[0]+w[i],x[j]+w[j]):
            if max(p[1],y[j]) < min(p[1]+h[i],y[j]+h[j]):
                return False
    return True


def BL_method(w,h,W):
    x,y=[],[]
    for i in range(len(w)):
        blfp=[]
        cand = bl_candidates(i,x,y,w,h)
        for p in cand:
            if is_feas(i,p,x,y,w,h,W):
                blfp += [p]
        min_p = min(blfp ,key= lambda v:(v[1],v[0]))
        x += [min_p[0]]
        y += [min_p[1]]
    return x,y

n = 230
W=130 #容器の幅
w=[]
h=[]

for i in range(n):
      w.append(random.uniform(1, 12))
      h.append(random.uniform(1, 12))

x,y=BL_method(w,h,W)
#print(x,y)

for i in range(n):
    rect = plt.Rectangle((x[i],y[i]),w[i],h[i], fc=cm.hsv(i/230.0), ec="black")
    ax.add_patch(rect)

ax.set_xlim([0,W])
ax.set_ylim([0,W])
plt.show()
