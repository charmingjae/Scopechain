def proof_of_work(self, last_block):
    start_time = time.time()
    global flags
    global proof_Result
    global time_cnt
    flags = False
    proof_Result = None
    """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

    last_proof = last_block['proof']
    last_hash = self.hash(last_block)

    # proof = 0
    # while self.valid_proof(last_proof, proof, last_hash) is False:
    #     proof += 1

    # end_time = time.time()
    # print("프루프 걸린 시간 : {} sec".format(end_time-start_time))
    # time_cnt += end_time-start_time
    # print('현재까지 걸린 시간 : ', time_cnt)
    # print('평균시간 : ', time_cnt/100)
    # return proof

    proof1 = 0
    proof2 = 50001
    proof3 = 100001
    proof4 = 150001
    proof5 = 200001
    proof6 = 250001
    proof7 = 300001

    def fun1(last_proof, proof, last_hash, start, finish, idx):
        global proof_Result
        global flags
        global arr
        # print('fun{0} now flags : {1}'.format(idx, flags))
        for i in range(start, finish):
            if flags:
                break
            if self.valid_proof(last_proof, proof, last_hash) is True:
                flags = True
                proof_Result = proof
                arr[idx-1] += 1
                # print('[fun{0} is finished] proof : {1}'.format(
                #     idx, proof_Result))
                break
            proof += 1

    th1 = threading.Thread(target=fun1, args=(
        last_proof, proof1, last_hash, 0, 50001, 1))
    th2 = threading.Thread(target=fun1, args=(
        last_proof, proof2, last_hash, 50001, 100001, 2))
    th3 = threading.Thread(target=fun1, args=(
        last_proof, proof3, last_hash, 100001, 150001, 3))
    th4 = threading.Thread(target=fun1, args=(
        last_proof, proof4, last_hash, 150001, 200001, 4))
    th5 = threading.Thread(target=fun1, args=(
        last_proof, proof5, last_hash, 200001, 250001, 5))
    th6 = threading.Thread(target=fun1, args=(
        last_proof, proof6, last_hash, 250001, 300001, 6))
    th7 = threading.Thread(target=fun1, args=(
        last_proof, proof7, last_hash, 300001, 350001, 7))

    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th5.start()
    th6.start()

    # th6.join()

    th7.start()

    # th7.join()

    # if not th2.is_alive():
    #     print('th2 is not alive')
    #     print('flag : ', flags)
    #     print('proof : ', proof_Result)

    # if not th1.is_alive():
    #     print('th1 is not alive')
    #     print('flag : ', flags)
    #     print('proof : ', proof_Result)

    end_time = time.time()
    print('proof result : {}'.format(proof_Result))
    # print("프루프 걸린 시간 : {} sec".format(end_time-start_time))
    time_cnt += end_time-start_time
    print('현재까지 걸린 시간 : ', time_cnt)
    print('평균시간 : ', time_cnt/100)
    print('범위 별 정보 : ', arr)
    print('None : ', 100 - sum(arr))

    return proof_Result
