import matplotlib.pyplot as plt


# xlabel
cycle = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# use 1 thread
simul1 = [0.40, 0.51, 0.56, 0.50, 0.48, 0.50, 0.42, 0.53, 0.58,
          0.61, 0.57, 0.66, 0.53, 0.50, 0.50, 0.55, 0.56, 0.63, 0.63, 0.60]

# use 2 threads
simul2 = [0.47, 0.36, 0.38, 0.40, 0.41, 0.47, 0.46, 0.44, 0.47,
          0.38, 0.44, 0.46, 0.45, 0.38, 0.38, 0.49, 0.41, 0.39, 0.42, 0.50]

# use 5 threads
simul3 = [0.33, 0.33, 0.33, 0.29, 0.31, 0.33, 0.30, 0.32, 0.30,
          0.28, 0.34, 0.35, 0.35, 0.26, 0.33, 0.26, 0.34, 0.29, 0.27, 0.34]

# use 7 threads
simul4 = [0.33, 0.33, 0.34, 0.29, 0.31, 0.33, 0.30, 0.32, 0.34,
          0.34, 0.34, 0.31, 0.28, 0.31, 0.35, 0.35, 0.32, 0.30, 0.31, 0.33]

# use 11 threads
simul5 = [0.38, 0.33, 0.34, 0.34, 0.35, 0.37, 0.33, 0.32, 0.33,
          0.31, 0.34, 0.39, 0.38, 0.37, 0.34, 0.34, 0.37, 0.33, 0.41, 0.32]


fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.plot(cycle, simul1, label='1 thread')
ax1.plot(cycle, simul2, label='2 thread')
ax1.plot(cycle, simul3, label='5 thread')
ax1.plot(cycle, simul4, label='7 thread')
ax1.plot(cycle, simul5, label='11 thread')

values = range(len(cycle))

plt.xticks(values, cycle)

ax1.legend()

plt.show()
