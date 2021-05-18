import time
import multiprocessing
# from threading import Thread
import threading


# start_time = time.time()
# flag = False

# arr = []


# def fun1():
#     global flag
#     for i in range(10):
#         if flag:
#             break
#         print('[fun1] : ', i)
#         arr.append(i)
#         print('[fun1 now arr] : ', arr)
#         time.sleep(1)
#     print('[fun1 process is finished]')


# def fun2():
#     for i in range(4):
#         print('[fun2] : ', i)
#         arr.append(i)
#         print('[fun2 now arr] : ', arr)
#         time.sleep(1)
#     print('[fun2 process is finished]')


# th1 = threading.Thread(target=fun1)
# th2 = threading.Thread(target=fun2)

# th1.start()
# th2.start()

# # th1.join()
# th2.join()

# if not th2.is_alive():
#     print('th2 is not alive')
#     flag = True

import time
import math
import sys


def fun1():
    print('[fun1]')
    print('[fun1]')
    print('[fun1]')
    print('[fun1]')
    print('[fun1]')
    print('[fun1]')
    time.sleep(5)


def fun2():
    for i in range(1, 10):
        print('[fun2]')
        time.sleep(1)


def fun3():
    for i in range(1, 10):
        print('[fun3]')
        time.sleep(1)


th1 = threading.Thread(target=fun1)
th2 = threading.Thread(target=fun2)
th3 = threading.Thread(target=fun3)

th1.start()

th1.join()
th2.start()
th3.start()
