import numpy as np
import matplotlib.pyplot as plt
import time
import math
import random


vn = 3 #vehicle number
cp = 6 #collection place+1(include depot)
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


def initial_solution(cp_list, vn, order):
    #初期順番を作製する.各車両に一つずつ数字を入れていく。
    random.shuffle(cp_list)
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

#以下、局所探索法、特に2-opt法-------------------------------------------------------------
def local_search(order, d_matrix)
#ここまで改善法-----------------------------------------------------------------------------------------

#初期順番を適当に作成
initial_solution(cp_list, vn, order)
print('initial_order = ',order)
total_distance = calculate_total_distance(order, d_matrix)
print(d_matrix)
print('total_distance = ',total_distance)

#ある程度改善する
improve_order = local_search(order, d_matrix, improve_with_2opt, i, j)

'''
def 2opt_method():
def calculate_total_distance():
'''
