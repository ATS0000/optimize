#excelから読み込み割り当てる。ランダムデータ数を入力したい場合はPuLP_ncrossn.pyなどを参照。
#第一希望を3,第二希望を2,第三希望を1とし、最大化する。
#テーマをテーマA,B,Cに分類し、学生はA,B,Cから2つ以上の分野を行うようにする。
#reference:https://qiita.com/cheerfularge/items/d1474c4f3ad65a34941c
import pulp
import random
import numpy as np
import xlrd
import xlwt
import matplotlib.animation as animation
import matplotlib.pyplot as plt

plt.style.use('ggplot')
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)

def main():
    #excelからデータを持ってくる。縦軸にテーマ(i)、横軸に人（j)
    book = xlrd.open_workbook('theme_user.xlsx')
    sheet = book.sheet_by_name('Sheet1')
    def get_list(sheet):
        return [sheet.row_values(row) for row in range(sheet.nrows)]
    W = get_list(sheet)
    W = np.array(W) #リストをnumpyに変換

    n = sheet.ncols #人の数
    theme = sheet.nrows #テーマの数

    print('人数',n)
    print('テーマの数',theme)


    #GPAを配慮
    for j in range(n):
        k = random.uniform(2.0,4.3)
        for i in range(theme):
            W[i,j] = k*W[i,j]


    # 各行を割合に変換
    # sumbox = W.sum(axis=0, dtype='float')
    # W /= sumbox


    # 問題の宣言
    problem = pulp.LpProblem(name='allocation theme', sense=pulp.LpMaximize)

    # 変数の宣言
    x = {(i,j):pulp.LpVariable(name='x_{}_{}'.format(i, j), cat='Binary') for i in range(theme) for j in range(n)}

    # 目的関数
    problem += pulp.lpSum([W[i,j]*x[i,j] for i in range(theme) for j in range(n)])


    #テーマジャンルA、B、Cを2つ以上はやることになる
    themeA = 7 #themeAの数
    themeB = 4 #themeBの数
    themeC = theme - themeA - themeB #themeCの数

    #一つのテーマには[3n/theme]人の前後
    for i in range(theme):
        problem.addConstraint((pulp.lpSum([x[i,j] for j in range(n)]) >= 17),"seat_limitation_{}".format(i))
        problem.addConstraint((pulp.lpSum([x[i,j] for j in range(n)]) <= 18),"seat_limitation2_{}".format(i))


    #テーマジャンルA、B、Cを2つ以上はやることになる
    themeA = 7 #themeAの数
    themeB = 4 #themeBの数
    themeC = theme - themeA - themeB #themeCの数
    #ユーザーは3つのテーマを行う
    ims =[]
    for j in range(n):
        problem.addConstraint((pulp.lpSum([x[i,j] for i in range(theme)]) == 3),"user_gets_theme_{}".format(j))

        problem.addConstraint((pulp.lpSum([x[i,j] for i in range(themeA)]) <= 2),"user_gets_themeA_{}".format(j))
        problem.addConstraint((pulp.lpSum([x[i,j] for i in range(themeA,themeA + themeB)]) <= 2),"user_gets_themeB_{}".format(j))
        problem.addConstraint((pulp.lpSum([x[i,j] for i in range(themeA + themeB,theme)]) <= 2),"user_gets_themeC_{}".format(j))

        #print(pulp.value(x[i,j]))


        if pulp.value(x[i,j]) == 1 :
            im = ax.scatter(i, j, c='red', alpha=0.4)
            ims.append([im])


    status = problem.solve()

    print(pulp.LpStatus[status])
    print("目的関数値 = {}".format(pulp.value(problem.objective)))


    for j in range(n):
        for i in range(theme):
            if pulp.value(x[i,j]) > 0:
                print(f'user {j} theme {i} : {pulp.value(x[i,j])}')

#Wを表示
    print('割当完了！！！')
#1人り当たりのテーマ数を確認
    for j in range(n):
        a = 0 #割当された一人当たりのテーマの数
        for i in range(theme):
            if pulp.value(x[i,j]) > 0:
                a += 1
        print(f'user {j} : {a}' )

#テーマごとの人数を確認
    for i in range(theme):
        b = 0
        for j in range(n):
            if pulp.value(x[i,j]) > 0:
                b += 1
        print(f'theme {i} : {b}')



    #一人当たりのテーマ属性ごとの数を確認
    for j in range(n):
        cA = 0
        for i in range(themeA):
            if pulp.value(x[i,j]) > 0:
                cA += 1
                if cA > 2:
                    print(f'user {j} : {cA}' 'over in A!!')

    for j in range(n):
        cB = 0
        for i in range(themeA,themeA + themeB):
            if pulp.value(x[i,j]) > 0:
                cB += 1
                if cB > 2:
                    print(f'user {j} : {cB}' 'over in B!!')

    for j in range(n):
        cC = 0
        for i in range(themeA + themeB,theme):
            if pulp.value(x[i,j]) > 0:
                cC += 1
                if cC > 2:
                    print(f'user {j} : {cC}' 'over in C!!')

    print('finish!')

    print("目的関数値 = {}".format(pulp.value(problem.objective)))
#結果をexcelに書き込み
    output = xlwt.Workbook()
    sheet = output.add_sheet('Sheet2')

    c = np.zeros([theme,n])
    for i in range(theme):
        for j in range(n):
            if pulp.value(x[i,j]) > 0:
                c[i,j] = 1

    for i in range(theme):
        for j in range(n):
            sheet.write(i, j, c[i,j])

    output.save('output.xls')

    ani = animation.ArtistAnimation(fig, ims, interval=100, repeat_delay=100)
    #ani.save('warifuri.gif')
    plt.show()

if __name__ == '__main__':
    main()
