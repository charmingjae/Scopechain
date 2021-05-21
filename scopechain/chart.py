import matplotlib.pyplot as plt


# xlabel
cycle = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# use 1 thread
simul1 = [0.58, 0.54, 0.69, 0.58, 0.56, 0.51, 0.71, 0.69, 0.75, 0.50]

# use 2 threads
simul2 = [0.49, 0.40, 0.40, 0.44, 0.37, 0.48, 0.50, 0.51, 0.45, 0.41]

# use 5 threads
simul3 = [0.34, 0.39, 0.32, 0.33, 0.39, 0.33, 0.35, 0.36, 0.37, 0.37]

# use 7 threads
simul4 = [0.34, 0.31, 0.30, 0.34, 0.34, 0.34, 0.30, 0.34, 0.34, 0.34]


fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.plot(cycle, simul1, label='1 thread')
ax1.plot(cycle, simul2, label='2 thread')
ax1.plot(cycle, simul3, label='5 thread')
ax1.plot(cycle, simul4, label='7 thread')

ax1.legend()

plt.show()
