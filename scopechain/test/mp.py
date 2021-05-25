from multiprocessing import Process, Value
from ctypes import c_bool
import multiprocessing
import time


# if flags.value is True:
#     print('True!!!!')
# else:
#     print('False!!!')


# def fun1(flags):
#     for i in range(1, 11):
#         print(i)
#         if i == 5:
#             flags.value = True
#             print('NOW FLAG : ', flags.value)
#             break
#         print('NOW FLAG : ', flags.value)
#         time.sleep(1)


# def fun2(flags):
#     for i in range(100, 111):
#         if flags.value is True:
#             break
#         print(i)
#         print('NOW FLAG : ', flags.value)
#         time.sleep(1)

def fun1(flags):
    for i in range(1, 11):
        print(i)
        if i == 5:
            flags.value = True
            print('NOW FLAG : ', flags.value)
            break
        print('NOW FLAG : ', flags.value)
        time.sleep(1)


def fun2(flags):
    for i in range(100, 111):
        if flags.value is True:
            break
        print(i)
        print('NOW FLAG : ', flags.value)
        time.sleep(1)


def test():
    flags = Value(c_bool, False)

    p1 = Process(target=fun1, args=(flags,))
    p2 = Process(target=fun2, args=(flags,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print('flags : ', flags.value)


if __name__ == '__main__':
    test()

    # flags = Value(c_bool, False)
    # print(flags.value)
    # p1 = Process(target=fun1, args=(flags,))
    # p2 = Process(target=fun2, args=(flags,))

    # p1.start()
    # p2.start()

    # p1.join()
    # p2.join()
