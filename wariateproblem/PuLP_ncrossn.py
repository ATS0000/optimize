import pulp
import random
import numpy as np

def main():
    n = 50
    seat = 15
    W = np.zeros([seat,n])

    #値を入れる
    for j in range(n):
        p = random.randint(0,seat-1)
        q = random.randint(0,seat-1)
        r = random.randint(0,seat-1)
        while q == p:
            q = random.randint(0,seat-1)
        while r == p or r == q:
            r = random.randint(0,seat-1)
        W[p,j] = 3
        W[q,j] = 2
        W[r,j] = 1
    '''
    #Wを表示
    for j in range(n):
        print('!!')
        print(j)
        print('!!')
        for i in range(seat):
            print(W[i,j])
    '''


    #GPAを配慮
    for j in range(n):
        k = random.uniform(2.0,4.3)
        for i in range(seat):
            W[i,j] = k*W[i,j]



    # 各行を割合に変換
    # sumbox = W.sum(axis=0, dtype='float')
    # W /= sumbox


    # 問題の宣言
    problem = pulp.LpProblem(name='change seat', sense=pulp.LpMaximize)

    # 変数の宣言
    x = {(i,j):pulp.LpVariable(name='x_{}_{}'.format(i, j), cat='Binary') for i in range(seat) for j in range(n)}

    # 目的関数
    problem += pulp.lpSum([W[i,j]*x[i,j] for i in range(seat) for j in range(n)])

    #一つのテーマには10～11人
    for i in range(seat):
        problem.addConstraint((pulp.lpSum([x[i,j] for j in range(n)]) >= 10),"seat_limitation_{}".format(i))
        problem.addConstraint((pulp.lpSum([x[i,j] for j in range(n)]) <= 11),"seat_limitation2_{}".format(i))
    #ユーザーは3つのテーマを行う
    for j in range(n):
        problem.addConstraint((pulp.lpSum([x[i,j] for i in range(seat)]) == 3),"user_gets_onlyoneseat_{}".format(j))

    status = problem.solve()
    print(pulp.LpStatus[status])
    print("目的関数値 = {}".format(pulp.value(problem.objective)))


    for j in range(n):
        for i in range(seat):
            if pulp.value(x[i,j]) > 0:
                print(f'user {j} seat {i} : {pulp.value(x[i,j])}')

#Wを表示
    '''
    for j in range(n):
        print('!!')
        print(j)
        print('!!')
        for i in range(seat):
            print(W[i,j])
    '''

#1人り当たりのテーマ数を確認
    for j in range(n):
        a = 0 #選んだテーマの数
        for i in range(seat):
            if W[i,j] > 0:
                a += 1
        print(f'user {j} : {a}' )

#テーマごとの人数を確認
    for i in range(seat):
        b = 0
        for j in range(n):
            if pulp.value(x[i,j]) > 0:
                b += 1
        print(f'theme {i} : {b}')





if __name__ == '__main__':
    main()
