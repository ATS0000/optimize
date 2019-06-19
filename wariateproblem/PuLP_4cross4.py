import pulp
import random
import numpy as np

def main():
    n = 4
    seat = n
    W = np.zeros([seat,n])

    #値を入れる
    for j in range(n):
        p = random.randint(0,n-1)
        q = random.randint(0,n-1)
        W[p,j] = 2
        W[q,j] = 1



    # 各行を割合に変換
    # sumbox = W.sum(axis=0, dtype='float')
    # W /= sumbox


    # 問題の宣言
    problem = pulp.LpProblem(name='change seat', sense=pulp.LpMaximize)

    # 変数の宣言
    x = {(i,j):pulp.LpVariable(name='x_{}_{}'.format(i, j), cat='Binary') for i in range(seat) for j in range(n)}

    # 目的関数
    problem += pulp.lpSum([W[i,j]*x[i,j] for i in range(seat) for j in range(n)])

    #一つのテーマには2人
    for i in range(seat):
        problem.addConstraint((pulp.lpSum([x[i,j] for j in range(n)]) <= 3),"seat_limitation_{}".format(i))
        problem.addConstraint((pulp.lpSum([x[i,j] for j in range(n)]) >= 2),"seat_limitation2_{}".format(i))
    #ユーザーは２つのテーマを選ぶ
    for j in range(n):
        problem.addConstraint((pulp.lpSum([x[i,j] for i in range(seat)]) == 2),"user_gets_onlyoneseat_{}".format(j))

    status = problem.solve()
    print(pulp.LpStatus[status])
    print("目的関数値 = {}".format(pulp.value(problem.objective)))


    for j in range(n):
        for i in range(seat):
            if pulp.value(x[i,j]) > 0:
                print(f'user {j} seat {i} : {pulp.value(x[i,j])}')

    for i in range(seat):
        for j in range(n):
            print(W[i,j])



if __name__ == '__main__':
    main()
