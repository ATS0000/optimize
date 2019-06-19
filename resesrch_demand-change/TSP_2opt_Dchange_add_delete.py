#巡回セールスマン問題を局所探索法（特に2-opt法）を用いて解く。
#reference: http://codecrafthouse.jp/p/2016/08/traveling-salesman-problem/
#animation付き。

import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation

plt.style.use('ggplot')
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)


N = 20
MAP_SIZE = 100

city_xy = np.random.rand(N, 2) * MAP_SIZE #行列を生成。rand(行, 列)

#plt.figure(figsize=(4, 4))
#plt.plot(city_xy[:, 0], city_xy[:, 1], 'o')
#plt.show()

x = city_xy[:, 0] #すべての行の0列目
y = city_xy[:, 1] #すべての行の1列目

for i in range(N):
    ax.scatter(x[i], y[i], c='black')

#わからない
distance_matrix = np.sqrt((x[:, np.newaxis] - x[np.newaxis, :]) ** 2 +
                          (y[:, np.newaxis] - y[np.newaxis, :]) ** 2)

# 見やすくするために10都市分だけ出力。
# distance_matrix[i, j]が都市iと都市jの距離。
#print(np.round(distance_matrix[:10, :10])) #１０行目１０列目まで

def calculate_total_distance(order, distance_matrix):
    """Calculate total distance traveled for given visit order"""
    idx_from = np.array(order) #訪問順
    idx_to = np.array(order[1:] + [order[0]]) #訪問順をひとつずらしたリスト
    distance_arr = distance_matrix[idx_from, idx_to] #idx_toのk番目が行、idx_fromのk番目が列を指定する行列

    return np.sum(distance_arr)

ims = []
#図を作ってプロットを出す関数
def visualize_visit_order(order, distance_matrix, improve_with_2opt, city_xy, reserve_list):
    """Visualize traveling path for given visit order"""

    print(order)
    for i in range(len(order)):

        if i == 3: #この条件の時、需要が変わる（キャンセルされる）
            t = Delete_demand(order, i)
            #im1 = ax.scatter(x[order[t-1]], y[order[t-1]], s=50, c='black', marker='x')
            reCalculation(order, distance_matrix, improve_with_2opt, city_xy)
            print('--->')
            print(order)

        if i == 5: #この条件の時、需要が変わる（予約が増える）
            s = Add_demand(order, reserve_list, i)
            im1 = ax.scatter(x[order[s]], y[order[s]], s=200, c='red', marker='*')
            reCalculation(order, distance_matrix, improve_with_2opt, city_xy)
            print('--->')
            print(order)

        route = np.array(order + [order[0]])  # add point of departure
        x_arr = city_xy[:, 0][route] #順序に並び替え
        y_arr = city_xy[:, 1][route] #順序に並び替え

        im1 = ax.plot(x_arr, y_arr, 'k' '--')
        #im2 = ax.scatter(x_arr[i], y_arr[i], c='red') #入力の順番に注意
        if i < len(order):
            im2 = ax.plot([x_arr[i], x_arr[i+1]], [y_arr[i], y_arr[i+1]], 'b' '-')

        ims.append(im1+im2)

        if i == len(order)+1:
            break

    ani = animation.ArtistAnimation(fig, ims, interval=500, repeat_delay=1500)
    #ani.save('')
    plt.show()



#以下、局所探索法、特に2-opt法

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
def local_search(visit_order, distance_matrix, improve_func, city_xy): #improve_func = improve_with_2opt
    """Main procedure of local search"""
    cost_total = calculate_total_distance(visit_order, distance_matrix)

    while True:

        improved = improve_func(visit_order, distance_matrix)
        if not improved: #改善できないならbreak #わからない
            break

        visit_order = improved

    return visit_order


def Delete_demand(order, i):
    t = np.random.randint(i+1, len(order)) #delete point
    order.pop(t) #delete_demand
    return t

def Add_demand(order, reserve_list, i):
    s = np.random.randint(i+1, len(order)) #add point
    order.insert(s, reserve_list[np.random.randint(len(reserve_list))])
    return s


def reCalculation(order, distance_matrix, improve_with_2opt, city_xy):
    order = local_search(order, distance_matrix, improve_with_2opt, city_xy)


def somedelete_demand(order):
    M = 10 #最初に需要を消しておく点の数
    reserve_list = []
    for j in range(M):
        t = np.random.randint(len(order))
        reserve_list.append(order[t])
        order.pop(t)

    print('reserve_list = ', reserve_list)
    return reserve_list



# 適当に初期解を生成
test_order = list(np.random.permutation(N)) #N個の順番を並び替えたリスト。これが初期順序になる
#visualize_visit_order(test_order, city_xy)
#total_distance = calculate_total_distance(test_order, distance_matrix)
#print('初期解の総移動距離 = {}'.format(total_distance))
#print('訪問順序 = {}'.format(test_order)) #print(np.array(test_order))と同じ

reserve_list = somedelete_demand(test_order)

print('test_order = ' ,test_order)

for i in range(len(test_order)): #予約済み（reserve_list以外の点）のみ赤く塗る
    ax.scatter(x[test_order[i]], y[test_order[i]], c='red')

#starttime = time.time()

# 近傍を計算
improved = local_search(test_order, distance_matrix, improve_with_2opt, city_xy)

#finishtime = time.time()
#結果を表示



visualize_visit_order(improved, distance_matrix, improve_with_2opt, city_xy, reserve_list)
total_distance = calculate_total_distance(improved, distance_matrix)
#print('近傍探索適用後の総移動距離 = {}'.format(total_distance))
#print('訪問順序 = {}'.format(improved)) #print(np.array(test_order))と同じ
    #print(f'計算時間：{finishtime - starttime}')
