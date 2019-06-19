import numpy as np
import matplotlib.pyplot as plt
import time
import math
import random
import copy

vn = 4 #vehicle number
cp = 15 #collection place+1(include depot)
cp_list = [i for i in range(1,cp)]
MAP_SIZE = 10
cp_xy = np.random.rand(cp, 2) * MAP_SIZE #行列を生成。rand(行, 列)
x = cp_xy[:, 0] #すべての行の0列目
y = cp_xy[:, 1] #すべての行の1列目
d_matrix = np.sqrt((x[:, np.newaxis] - x[np.newaxis, :]) ** 2 +
                          (y[:, np.newaxis] - y[np.newaxis, :]) ** 2) #distance matrix

order = [[] for i in range(vn)] #各車両の順番情報が入っている。2番目の車両の１番目に訪れる番号はtotal_order[1][0]



print(cp_list)
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
def move_point_improve(order, d_matrix):
    #preorder = order #保存用order.改善されないときはこれに戻す
    '''
    #iとjを選ぶ
    i = random.randint(0,vn-1)
    j = random.choice(0,vn-1)
    '''

    for i in range(vn):
        v_list = [i for i in range(vn)]
        print('i = ', i, '--------------------------')
        v_list.pop(i)
        for j in v_list:
            print('j = ', j, '--------------------------')
            #iとj内の距離の合計を計算
            i_d = calculate_each_distance(i, order, d_matrix)
            j_d = calculate_each_distance(j, order, d_matrix)
            i_j_d = i_d + j_d
            l = 0
            for k in range(1, len(order[i])):
                l += 1
                preorder = copy.deepcopy(order) #保存用order.改善されないときはこれに戻す
                print(order[i][l])
                #iからjへ移す
                order[j].append(order[i][l])
                order[i].pop(l)
                #iとj内の距離の合計を計算
                i_d = calculate_each_distance(i, order, d_matrix)
                j_d = calculate_each_distance(j, order, d_matrix)
                exchange_i_j_d = i_d + j_d #配送先移動後の車両iとjに対しての移動距離の合計
                print('d = ', i_j_d)
                print('e_d = ', exchange_i_j_d)
                l -= 1
                if i_j_d < exchange_i_j_d:
                    print('no_exchange')
                    order = preorder #改善されないなら変更前のorderに戻す
                    l += 1

                print('l = ',l)
                print(preorder, '-->', order)
                print('--------------------')
    return order



    #改善されたなら入れ替え

#def all_separation():




'''
#以下、局所探索法、特に2-opt法-------------------------------------------------------------

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
def improve_with_2opt(visit_order, distance_matrix, i, j):
    """Check all 2-opt neighbors and improve the visit order"""
    n_cities = len(visit_order)
    cost_diff_best = 0.0
    i_best, j_best = None, None

    #すべての組み合わせの中で一番ベスト（一番効果のある）な入れ替えを決定するforloop
    for i in range(0, n_cities - 2):
        for j in range(i + 2, n_cities):
            if i < s and j < g: #条件を満たすものは入れ替えない？？
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


def local_search(visit_order, d_matrix, improve_func, i, j): #improve_func = improve_with_2opt
    """Main procedure of local search"""
    cost_total = calculate_total_distance(visit_order, d_matrix)
    while True:
        improved = improve_func(visit_order, d_matrix, i, j)
        if not improved: #改善できないならbreak
            break
        visit_order = improved

    return visit_order
#ここまで改善法-----------------------------------------------------------------------------------------
'''

#初期順番を適当に作成
separate_solution(cp_list, vn, order)
print('initial_order = ',order)
total_distance = calculate_total_distance(order, d_matrix)
print(d_matrix)
print('total_distance = ',total_distance)

'''
broken_down_list = []
for i in range(vn):
    broken_down_list += order[i]

print(broken_down_list)
'''
#ある程度改善する
improve_order = move_point_improve(order, d_matrix)
print('order = ' ,improve_order)
t = calculate_total_distance(improve_order, d_matrix)
print(total_distance, '-->', t)
#improve_order = local_search(improve_order, d_matrix, improve_with_2opt, i, j)

'''
def 2opt_method():
def calculate_total_distance():
'''
