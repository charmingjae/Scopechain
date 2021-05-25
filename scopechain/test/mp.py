from multiprocessing import Process, Value
from ctypes import c_bool
import multiprocessing
import time


flags = Value(c_bool, False)
print(flags)

if flags.value is True:
    print('True!!!!')
else:
    print('False!!!')

# def fun1(flags):
#     for i in range(1, 11):
#         if flags.value is True:
#             break
#         print('fun1 : ', i)
#         print('fun1 now flags is : ', flags)
#         if i == 5:
#             flags = True
#             print('fun1 now flags is : ', flags)
#             break
#         time.sleep(1)


# def fun2(flags):
#     for i in range(100, 201):
#         if flags is True:
#             break
#         print('fun2 : ', i)
#         print('fun2 now flags is : ', flags)
#         time.sleep(1)


# if __name__ == '__main__':
#     procs = []
#     proc1 = Process(target=fun1, args=(flags,))
#     proc2 = Process(target=fun2, args=(flags,))

#     procs.append(proc1)
#     proc1.start()
#     procs.append(proc2)
#     proc2.start()

#     for i in procs:
#         i.join()
