import matplotlib.pyplot as plt

# data
arr = [
    [52, 32, 8, 3, 2, 2, 0, 1],
    [55, 25, 12, 3, 5, 0, 0, 0],
    [54, 27, 10, 3, 3, 2, 1, 0],
    [52, 25, 13, 5, 4, 1, 0, 0],
    [50, 24, 13, 7, 5, 1, 0, 0],
    [56, 21, 14, 5, 2, 2, 0, 0],
    [56, 21, 17, 2, 3, 1, 0, 0],
    [49, 30, 12, 4, 3, 1, 1, 0],
    [49, 26, 13, 7, 3, 1, 0, 1],
    [57, 20, 11, 3, 4, 2, 2, 1],
    [50, 24, 15, 5, 5, 0, 0, 1],
    [51, 29, 9, 7, 1, 2, 1, 0],
    [47, 36, 7, 6, 2, 2, 0, 0],
    [46, 33, 12, 6, 0, 1, 1, 1],
    [58, 19, 12, 5, 4, 1, 1, 0],
    [56, 22, 12, 7, 1, 1, 0, 1],
    [58, 22, 7, 7, 4, 1, 1, 0],
    [49, 30, 14, 4, 2, 1, 0, 0],
    [61, 13, 14, 8, 3, 1, 0, 0],
    [48, 37, 4, 6, 3, 2, 0, 0]
]

xData = ['0-50,000', '50,001-100,000', '100,001-150,000',
         '150,001-200,000', '200,001-250,000', '250,001-300,000', '300,001 - 350,000', '350,001 - ']

result_arr = []

for i in range(8):
    result_sum = 0
    for j in range(20):
        result_sum += arr[j][i]
    result_arr.append(result_sum)


fig = plt.figure()


ax1 = fig.add_subplot(111)

ax1.bar(xData, result_arr)


for i, v in enumerate(xData):
    plt.text(v, result_arr[i], result_arr[i],                 # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
             fontsize=9,
             color='blue',
             # horizontalalignment (left, center, right)
             horizontalalignment='center',
             verticalalignment='bottom')

plt.show()
