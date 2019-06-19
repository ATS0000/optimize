import xlrd
import matplotlib.pyplot as plt

book = xlrd.open_workbook('NN-2opt_and_rand-2opt_data.xlsx')
sheet = book.sheet_by_name('Sheet1')

def get_list(sheet):
    return [sheet.row_values(row) for row in range(sheet.nrows)]
w = get_list(sheet)


fig = plt.figure(figsize=(6, 6))

ax = fig.add_subplot(1,1,1)

N = 3
t = 0

x = [0]*11
y = [0]*11
e = [0]*11


for i in range(11):
    x[i] = N
    y[i] = w[212][2+t] - w[103][2+t]
    e[i] = w[216][2+t]

    t += 2
    N += 9

'''
for i in range(11):

    #print(x,y)
    #plt.scatter(N, w[212][1+t], c='red')
    #plt.scatter(N, w[212][2+t], c='blue')
    #plt.scatter(N, w[103][1+t], c='black')
    #plt.scatter(N, w[103][2+t], c='green')
    #plt.scatter(N, w[212][2+t] - w[103][2+t] , c='red')
    plt.scatter(x, y, c='red')

'''
for x, y, e in zip(x, y, e):
    ax.errorbar(x, y, e, fmt='ro', capsize=5, ecolor='black')



#plt.scatter(0,0,c='red', label = "rand")
#plt.scatter(0,0,c='blue', label = "rand + 2-opt")
#plt.scatter(0,0,c='black', label = "NN")
#plt.scatter(0,0,c='green', label = "NN + 2-opt")
plt.scatter(0,0,c='red', label = "(rand + 2-opt) - (NN + 2-opt)")
plt.xlabel("N (number of city)")
plt.ylabel("distance_total_difference [a.u.]")
plt.legend() # 凡例を表示
plt.show()
