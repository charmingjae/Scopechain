from ctypes import c_bool
import multiprocessing
from multiprocessing.sharedctypes import Value
import time

start_time = time.time()


def count(name):
    for i in range(1, 50001):
        print(name, " : ", i)


num_list = ['p1', 'p2', 'p3', 'p4']


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=2)
    pool.map(count, num_list)
    pool.close()


def fun1(flags, idx, start, end):
    for i in range(start, end):
        if flags.value is True:
            print('[fun{0}] breaks'.format(idx))
            break
        print(i)
        if i == 5:
            flags.value = True
            break
        time.sleep(1)


def test():
    flags = Value(c_bool, False)

    pool = multiprocessing.Pool(processes=2)
    pool.map(fun1, flags)
