import matplotlib.pyplot as plt


# xlabel
cycle = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


# use 5 threads
simul1 = [0.33, 0.33, 0.33, 0.29, 0.31, 0.33, 0.30, 0.32, 0.30,
          0.28, 0.34, 0.35, 0.35, 0.26, 0.33, 0.26, 0.34, 0.29, 0.27, 0.34]

# use 9 threads
simul2 = [0.37, 0.37, 0.43, 0.35, 0.35, 0.41,
          0.38, 0.35, 0.35, 0.37, 0.40, 0.33, 0.42, 0.35, 0.37, 0.35, 0.41, 0.41, 0.39, 0.36]


# use 11 threads
simul3 = [0.41, 0.38, 0.37, 0.48, 0.40, 0.38,
          0.40, 0.38, 0.44, 0.45, 0.37, 0.49, 0.37, 0.42, 0.41, 0.43, 0.40, 0.42, 0.38, 0.41]


# use 13 threads
simul4 = [0.42, 0.41, 0.38, 0.40, 0.36, 0.38,
          0.49, 0.47, 0.40, 0.39, 0.40, 0.38, 0.43, 0.38, 0.42, 0.38, 0.40, 0.40, 0.40, 0.38]


fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.plot(cycle, simul1, label='5 thread',
         linewidth=2.2, marker='o', markersize=4)
ax1.plot(cycle, simul2, label='9 thread',
         linestyle='--', marker='o', markersize=4)
ax1.plot(cycle, simul3, label='11 thread',
         linestyle='--', marker='o', markersize=4)
ax1.plot(cycle, simul4, label='13 thread',
         linestyle='--', marker='o', markersize=4)

values = range(len(cycle))

plt.xticks(values, cycle)

ax1.legend()

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

plt.ylabel('Average block generation time', fontsize=10, color='blue')  # y축 라벨
plt.xlabel('Cycle', fontsize=10, color='blue')  # x축 라벨
# plt.title('Sales for 10 days', fontsize=20, color='blue')  # 타이틀 설정
yticks = list(ax1.get_yticks())  # y축 눈금을 가져온다.

for y in yticks:
    ax1.axhline(y, linestyle=(0, (2, 3)), color='grey', alpha=0.2)  # 눈금선 생성


plt.show()
