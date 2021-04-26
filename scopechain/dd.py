def solution(citations):
    answer = 0
    cnt = 0
    temp = 0
    for i in range(len(citations)+1):
        cnt = 0
        # print('i : {0}'.format(i))
        if i == 0:
            continue
        else:
            for j in citations:
                # print('j : {0}'.format(j))
                if j >= i:
                    # print('j >= i ? {0}'.format(j >= i))
                    cnt = cnt + 1
                    # print('cnt : {0}'.format(cnt))
            if cnt >= i:
                temp = i
                if answer < temp:
                    answer = i
    return answer


a = solution([3, 0, 6, 1, 5])
