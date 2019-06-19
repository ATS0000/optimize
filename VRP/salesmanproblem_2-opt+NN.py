#巡回セールスマン問題を局所探索法（特に2-opt法）を用いて解く。
#reference: http://codecrafthouse.jp/p/2016/08/traveling-salesman-problem/

import numpy as np
import matplotlib.pyplot as plt
import time
import xlrd

plt.style.use('ggplot')

N = 50
MAP_SIZE = 10

#city_xy = np.random.rand(N, 2) * MAP_SIZE #行列を生成。rand(行, 列)

#plt.figure(figsize=(4, 4))
#plt.plot(city_xy[:, 0], city_xy[:, 1], 'o')
#plt.show()

#エクセルデータから配送先の位置データを持ってくる-------------------------
book = xlrd.open_workbook('city_position2.xlsx')
sheet = book.sheet_by_name('Sheet1')
def get_list(sheet):
    return [sheet.row_values(row) for row in range(sheet.nrows)]
city_xy = get_list(sheet)
city_xy = np.array(city_xy) #リストをnumpyに変換

x = city_xy[:, 0] #すべての行の0列目
y = city_xy[:, 1] #すべての行の1列目

#cp = sheet.nrows #都市数

#print(cp)
print(x)
print(y)
#-------------------------------------------------------------------

#x = city_xy[:, 0] #すべての行の0列目
#y = city_xy[:, 1] #すべての行の1列目

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

'''
#確認print-----------------------------------------------------
print(np.array(test_order[0])) #start位置（スカラー）
print(np.array(test_order[1:])) #start位置以外（リスト）
print(np.array([test_order[0]])) #start位置を要素に持つ1×1のリスト
print(np.array(test_order[1:] + [test_order[0]])) #start位置が最後の位置に行った形になる。つまり、順序をずらす。
print(np.round(distance_matrix))
print(distance_matrix[np.array(test_order), np.array(test_order[1:] + [test_order[0]])])
#--------------------------------------------------------------
'''
#図を作ってプロットを出す関数
def visualize_visit_order(order, city_xy):
    """Visualize traveling path for given visit order"""
    route = np.array(order + [order[0]])  # add point of departure
    x_arr = city_xy[:, 0][route] #順序に並び替え
    y_arr = city_xy[:, 1][route] #順序に並び替え

    plt.figure(figsize=(4, 4))
    plt.plot(x_arr, y_arr, 'o-') #入力の順番に注意
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
            if i == 0 and j == n_cities - 1: #最初と最後の順番は入れ替えない？？→違う。
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
    cost_total = calculate_total_distance(visit_order, distance_matrix)

    while True:
        improved = improve_func(visit_order, distance_matrix)
        if not improved: #改善できないならbreak #わからない
            break

        visit_order = improved

    return visit_order


'''
# 適当に初期解を生成
test_order = list(np.random.permutation(N)) #N個の順番を並び替えたリスト。これが初期順序になる
visualize_visit_order(test_order, city_xy)
total_distance = calculate_total_distance(test_order, distance_matrix)
print('初期解の総移動距離 = {}'.format(total_distance))
print('訪問順序 = {}'.format(test_order)) #print(np.array(test_order))と同じ
'''

#Nearest Neighbour
def NN_method(N, distance_matrix0):
    first_order = []
    i0 = np.random.choice(N) #出発点をランダムに決める
    point = i0 #注目している点
    first_order.append(point)
    distance_improve = distance_matrix0
    for i in range(N):
        distance_improve[i][i] = np.inf

    for i in range(N-1):
        #注目点から一番近い点を探す
        #distance_nonpoint_list = np.delete(distance_improve[point], point) #注目点を除いたリスト(numpy)
        next_point = np.argmin(distance_improve[point]) #注目点から一番近いところ(番号)
        distance_improve[point,:] = np.inf #一度通ったところは取れないようにする
        distance_improve[:,point] = np.inf

        first_order.append(next_point) #並び順に加える
        #first_order = first_order.tolist() #numpyをリストに変換
        point = next_point

    return first_order



#print(test_order)

starttime = time.time()

print(distance_matrix)


first_order = NN_method(N, distance_matrix)
visualize_visit_order(first_order, city_xy)

#なぜか改めてdistance_matrixを定義しなければならない
distance_matrix = np.sqrt((x[:, np.newaxis] - x[np.newaxis, :]) ** 2 +
                          (y[:, np.newaxis] - y[np.newaxis, :]) ** 2)

total_distance = calculate_total_distance(first_order, distance_matrix)
print('初期解の総移動距離 = {}'.format(total_distance))
print('初期の訪問順序 = {}'.format(first_order))

print(distance_matrix)


# 近傍を計算
improved = local_search(first_order, distance_matrix, improve_with_2opt)
#結果を表示
finishtime = time.time()
visualize_visit_order(improved, city_xy)
total_distance = calculate_total_distance(improved, distance_matrix)
print('近傍探索適用後の総移動距離 = {}'.format(total_distance))
print('訪問順序 = {}'.format(improved)) #print(np.array(test_order))と同じ
print(f'計算時間：{finishtime - starttime}')
