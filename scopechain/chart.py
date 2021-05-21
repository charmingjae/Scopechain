from matplotlib import pyplot as plt

cycle = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# use 1 thread
simul1 = [0.58, 0.54, 0.69, 0.58, 0.56, 0.51, 0.71, 0.69, 0.75, 0.50]

# use 2 threads
simul2 = [0.47, 0.51, 0.64, 0.56, 0.41, 0.48, 0.45, 0.53, 0.56, 0.58]

# use 4 threads
simul3 = [0.39, 0.41, 0.39, 0.45, 0.38, 0.38, 0.37, 0.46, 0.45, 0.34]

# use 7 threads with no join
simul4 = [0.29, 0.33, 0.31, 0.31, 0.31, 0.32, 0.29, 0.31, 0.34, 0.25]

plt.plot(cycle, simul1)
plt.plot(cycle, simul2)
plt.plot(cycle, simul3)
plt.plot(cycle, simul4)

plt.show()
