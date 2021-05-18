import time
import concurrent.futures


def fun1():
    for i in range(1, 10):
        print('[func1] : ', i)
        time.sleep(1)


def fun2():
    for i in range(11, 20):
        print('[fun2] : ', i)
        if i == 15:
            break
        time.sleep(1)


with concurrent.futures.ThreadPoolExecutor() as executor:
    future1 = executor.submit(fun1)
    future2 = executor.submit(fun2)

    flag = 0
    # while (not(future1.done()) and not(future2.done())):
    while True:
        if future1.done():
            print('future1 done')
            flag = 1
            break

        if future2.done():
            print('future2 done')
            flag = 2
            break

    print('NOW FLAG : ', flag)
    if flag == 1:
        future2.cancel()

    elif flag == 2:
        # ??
        result = future1
        print('cancel result : ', result)
