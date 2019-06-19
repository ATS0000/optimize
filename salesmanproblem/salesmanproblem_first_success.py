#巡回セールスマン問題
#2019/4/11 巡回路がつながっている.同じ道を通ってしまっている模様。uの値、更新が悪い？u0以外全部1．．．非対称コスト行列ならOK


import pulp as pp
import numpy as np
import xlrd
import matplotlib.pyplot as plt
# 最適化モデルの定義
problem = pp.LpProblem("tsp_mip", pp.LpMinimize)


#excelからデータを持ってくる。縦軸にテーマ(i)、横軸に人（j)
book = xlrd.open_workbook('costlist.xlsx')
sheet = book.sheet_by_name('Sheet1')
def get_list(sheet):
    return [sheet.row_values(row) for row in range(sheet.nrows)]
c = get_list(sheet)
c = np.array(c) #リストをnumpyに変換


#コスト行列

N = sheet.nrows
MAP_SIZE = 100

#np.random.seed(10)
z = np.random.rand(N, 2) * MAP_SIZE



y1 = z[:, 0]
y2 = z[:, 1]
'''
c = np.sqrt((y1[:, np.newaxis] - y1[np.newaxis, :]) ** 2 +
                          (y2[:, np.newaxis] - y2[np.newaxis, :]) ** 2)
'''

print('points', z)

print('cost matrix')
print(c)

# 変数の定義
x = {(i,j):pp.LpVariable(name='x_{}_{}'.format(i, j), cat='Binary') for i in range(N) for j in range(N) if i != j}


u = {(i):pp.LpVariable(name='u_{}'.format(i), cat="Continuous", lowBound=1.0, upBound=(N - 1.0)) for i in range(N)}

u[0] = 0.0


#目的関数
problem += pp.lpSum(c[i, j] * x[i, j] for i in range(N) for j in range(N) if i != j)

#　条件式(2)の登録
for i in range(N):
    problem += pp.lpSum(x[i, j] for j in range(N) if i != j) == 1

# 条件式(3)の登録
for i in range(N):
    problem += pp.lpSum(x[j, i] for j in range(N) if i != j) == 1


'''
#行ったり来たり禁止
for i in range(N):
    for j in range(N):
            problem += pp.value(x[i,j]) != pp.value(x[j,i])
'''


# 制約条件 (MTZ制約)
BigM = 10.0e15
for i in range(N):
    for j in range(N):
        if i != j:
            problem += u[i] + 1.0 - BigM*(1.0 - x[i, j]) <= u[j]


'''
for k in range(N):
    print(pp.value(u[k]))


for i in range(N):
    for j in range(N):
        if i != j:
            print(pp.value(x[i,j]))
'''

# 最適化の実行
status = problem.solve()

# 結果の把握
print("Status: {}".format(pp.LpStatus[status]))
print("目的関数値 = {}".format(pp.value(problem.objective)))

'''
print('u')
for k in range(N):
    print(pp.value(u[k]))

print('x')
for i in range(N):
    for j in range(N):
        if i != j:
            print(pp.value(x[i,j]))
'''

plt.figure(figsize=(5, 5))



for i in range(N):
    for j in range(N):
        if i != j:
            if pp.value(x[i,j]) > 0:
                plt.plot([y1[i],y1[j]],[y2[i],y2[j]], 'o-')


#plt.plot(z[:,0], z[:, 1], 'o')
plt.show()
