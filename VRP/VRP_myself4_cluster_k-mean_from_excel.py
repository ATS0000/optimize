import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#matplotlib.use('Agg')
import time
import datetime
import math
import random
import copy
import pandas as pd
#from pandas.tools import plotting # 高度なプロットを行うツールのインポート
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.cluster import KMeans # K-means クラスタリングをおこなう
import xlrd

plt.style.use('ggplot')
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)

vn = 6 #vehicle number
#cp = 50 #collection place+1(include depot)
#cp_list = [i for i in range(1,cp)]
#MAP_SIZE = 10

'''
cp_xy = np.random.rand(cp, 2) * MAP_SIZE #行列を生成。rand(行, 列)
k = 0
for j in range(vn):
    print('!!!',j)
    if j != 0:
        k += math.ceil(cp/vn)-1
    p = 10*MAP_SIZE*np.random.rand()*np.random.choice([-1,1])
    q = 10*MAP_SIZE*np.random.rand()*np.random.choice([-1,1])
    for i in range(math.ceil(cp/vn)-1):
        print(i+k)
        cp_xy[i+k][0] += p
        cp_xy[i+k][1] += q

cp_xy[0][0] = 0.
cp_xy[0][1] = 0.


#print(cp_xy)
'''

#エクセルデータから配送先の位置データを持ってくる-------------------------
book = xlrd.open_workbook('city_position2.xlsx')
sheet = book.sheet_by_name('Sheet1')
def get_list(sheet):
    return [sheet.row_values(row) for row in range(sheet.nrows)]
cp_xy = get_list(sheet)
cp_xy = np.array(cp_xy) #リストをnumpyに変換

x = cp_xy[:, 0] #すべての行の0列目
y = cp_xy[:, 1] #すべての行の1列目

cp = sheet.nrows #都市数

print(cp)
print(x)
print(y)
#-------------------------------------------------------------------

d_matrix = np.sqrt((x[:, np.newaxis] - x[np.newaxis, :]) ** 2 +
                          (y[:, np.newaxis] - y[np.newaxis, :]) ** 2) #distance matrix

order = [[] for i in range(vn)] #各車両の順番情報が入っている。2番目の車両の１番目に訪れる番号はtotal_order[1][0]



#print(cp_list)
#print(cp_list[0:3])


def separate_solution(cp_list, vn, order):
    #初期順番を作製する.各車両に一つずつ数字を入れていく。
    #random.shuffle(cp_list)
    k = 0
    while k != len(cp_list):
        for i in range(vn):
            if k == len(cp_list):
                break
            order[i].append(cp_list[k])
            k += 1
            #print('randam_order = ',t_order)
    for i in range(vn): #depotを加える
        order[i].insert(0, 0)


def calculate_total_distance(order, d_matrix):
    """Calculate total distance traveled for given visit order"""
    total_distance = 0
    for i in range(vn):
        idx_from = np.array(order[i]) #訪問順
        idx_to = np.array(order[i][1:] + [order[i][0]]) #訪問順をひとつずらしたリスト
        distance_arr = d_matrix[idx_from, idx_to] #idx_toのk番目が行、idx_fromのk番目が列を指定する行列
        total_distance += np.sum(distance_arr)

    return total_distance

def calculate_each_distance(i, order, d_matrix):
    """Calculate each distance traveled for given visit order"""
    idx_from = np.array(order[i]) #訪問順
    idx_to = np.array(order[i][1:] + [order[i][0]]) #訪問順をひとつずらしたリスト
    #print(idx_from)
    #print(idx_to)
    distance_arr = d_matrix[idx_from, idx_to] #idx_toのk番目が行、idx_fromのk番目が列を指定する行列

    return np.sum(distance_arr)

#配送先を移してクラスタ的に改善
def k_means_method(order, d_matrix, vn):
    #d_matrix_del = np.delete(d_matrix, [0, 0], 1)
    d_matrix_pd = pd.DataFrame(d_matrix)
    kmeans_model = KMeans(n_clusters=vn, random_state=10).fit(d_matrix_pd.iloc[:, 1:])
    labels = kmeans_model.labels_

    print(labels)

    for i in range(cp):
        order[labels[i]].append(i)

    for i in range(vn): #depotを加える
        order[i].insert(0, 0)

    return order


def visualize_visit_order(order, cp_xy, vn):
    """Visualize traveling path for given visit order"""
    for i in range(vn):
        route = np.array(order[i] + [order[i][0]])  # add point of departure
        x_arr = cp_xy[:, 0][route] #順序に並び替え
        y_arr = cp_xy[:, 1][route] #順序に並び替え

        plt.plot(x_arr, y_arr, 'o-') #入力の順番に注意

    plt.show()
    #plt.savefig('VRP_myself'+str(datetime.datetime.now())+'.png')




#以下、局所探索法、特に2-opt法-------------------------------------------------------------

def calculate_2opt_total_distance(order, distance_matrix):
    """Calculate total distance traveled for given visit order"""
    idx_from = np.array(order) #訪問順
    idx_to = np.array(order[1:] + [order[0]]) #訪問順をひとつずらしたリスト
    distance_arr = distance_matrix[idx_from, idx_to] #idx_toのk番目が行、idx_fromのk番目が列を指定する行列

    return np.sum(distance_arr)

#移動距離の差分を計算する
def calculate_2opt_exchange_cost(visit_order, i, j, distance_matrix):
    """Calculate the difference of cost by applying given 2-opt exchange"""
    n_cities = len(visit_order)
    a, b = visit_order[i], visit_order[(i + 1) % n_cities] #最大のcity番号だけ特殊。それ以外は隣のcity番号。
    c, d = visit_order[j], visit_order[(j + 1) % n_cities]

    cost_before = distance_matrix[a, b] + distance_matrix[c, d]
    cost_after = distance_matrix[a, c] + distance_matrix[b, d]
    return cost_after - cost_before

#交換後の訪問順序を計算
def apply_2opt_exchange(visit_order, i, j):
    """Apply 2-opt exhanging on visit order"""

    tmp = visit_order[i + 1: j + 1]
    tmp.reverse()
    visit_order[i + 1: j + 1] = tmp

    return visit_order

#近傍探索の実装。現状の訪問経路の、各２パスを入れ替える操作を全組み合わせで実施します。
#全通りを計算しておき、もっとも総移動距離を減らせる交換を実際に適用します。これ以上改善できなければNoneを返すことにします。
def improve_with_2opt(visit_order, distance_matrix):
    """Check all 2-opt neighbors and improve the visit order"""
    n_cities = len(visit_order)
    cost_diff_best = 0.0
    i_best, j_best = None, None

    #すべての組み合わせの中で一番ベスト（一番効果のある）な入れ替えを決定するforloop
    for i in range(0, n_cities - 2):
        for j in range(i + 2, n_cities):
            if i == 0 and j == n_cities - 1: #最初と最後の順番は入れ替えない？？
                continue #条件を満たしたら以下をスキップ（条件を満たしてないなら実行）

            cost_diff = calculate_2opt_exchange_cost(
                visit_order, i, j, distance_matrix)
            #costの差分がより小さいならそれをbestにする
            if cost_diff < cost_diff_best:
                cost_diff_best = cost_diff
                i_best, j_best = i, j
    #costの差分が0より小さいなら（少しでも改善されるなら）２点の順番を入れ替える
    if cost_diff_best < 0.0:
        visit_order_new = apply_2opt_exchange(visit_order, i_best, j_best)
        return visit_order_new
    else:
        return None

#改善ができる限り、上の近傍探索を繰り返す
def local_search(visit_order, distance_matrix, improve_func): #improve_func = improve_with_2opt
    """Main procedure of local search"""
    cost_total = calculate_2opt_total_distance(visit_order, distance_matrix)

    while True:
        improved = improve_func(visit_order, distance_matrix)
        if not improved: #改善できないならbreak #わからない
            break

        visit_order = improved

    return visit_order


def opt_improve(vn, improve_order, d_matrix, improve_with_2opt):
    opt_improve_order = [[] for i in range(vn)]
    for i in range(vn):
        opt_improve_order[i] = local_search(improve_order[i], d_matrix, improve_with_2opt)

    return opt_improve_order

#ここまで改善法-----------------------------------------------------------------------------------------


#ある程度改善する--------------------------------------------------------------------
#total_distance = calculate_total_distance(order, d_matrix) #改善前の総距離

#1.クラスタ的に配送先を決める
improve_order = k_means_method(order, d_matrix,vn)
print('order = ' ,improve_order)
t = calculate_total_distance(improve_order, d_matrix)
#print(total_distance, '-->', t)


#2.各車両に対して2optで改善
opt_improve_order = opt_improve(vn, improve_order, d_matrix, improve_with_2opt)
t_opt = calculate_total_distance(opt_improve_order, d_matrix)
print(t, '-->', t_opt)
order = opt_improve_order

visualize_visit_order(order, cp_xy, vn)

'''
#以下で、以上で求めたルートを基に配送（収集）する--------------------------------------

for i in range(cp): #配送先のプロット
    ax.scatter(x[i], y[i], c='red')
ax.scatter(x[0], y[0], marker=',', s=200, c='b')

state = [0 for i in range(vn)] #各車両の居場所を収納する。
next_state = []
for i in range(vn):
    if len(order[i]) > 1:
        next_state.append(order[i][1])
    else:
        next_state.append(0)

ims =[]
for i in range(max([len(order[i]) for i in range(vn)])):

    for j in range(vn):
        if len(order[j]) > i+1:
            state[j] = order[j][i]
            next_state[j] = order[j][i+1]
        else:
            state[j] = next_state[j]
            next_state[j] = 0

    #print('state = ',state,'next_state = ', next_state)

    im1=[0 for i in range(vn)]
    im2=[0 for i in range(vn)]
    each_vn = []
    tot_vn = []
    for k in range(vn):
        im1[k] = ax.plot([x[state[k]], x[next_state[k]]], [y[state[k]], y[next_state[k]]], 'r' '-',lw=7)
        each_vn += im1[k]

        route = np.array(order[k] + [order[k][0]])  # add point of departure
        x_arr = cp_xy[:, 0][route] #順序に並び替え
        y_arr = cp_xy[:, 1][route] #順序に並び替え
        im2[k] = ax.plot(x_arr, y_arr, 'k', '--')
        tot_vn += im2[k]

    ims.append(each_vn + tot_vn)


ani = animation.ArtistAnimation(fig, ims, interval=500, repeat_delay=1500)
#ani.save('')
plt.show()
'''
