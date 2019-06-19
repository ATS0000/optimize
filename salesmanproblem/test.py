import numpy as np

x = int(input('数を入力してください'))
print(x)

n = 1
xx = 0

while n<10 :
    x = int(input('数を入力してください'))
    if x%2 == 0:
        x = 0
    if x > xx:
        xx = x

    n = n+1

if xx % 2 ==0:
    print('ダメ')
else:
    print(xx)
