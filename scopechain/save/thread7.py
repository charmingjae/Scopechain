import hashlib
import json
from multiprocessing.context import Process
import threading
import time
from urllib.parse import urlparse
import requests
import datetime
import concurrent.futures
import sys

flags = False
proof_Result = None
time_cnt = 0
arr = [0, 0, 0, 0, 0, 0, 0]
# Block chain


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def test():
        return 'a'

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # print("\n=======================\n")
            # print(f'{last_block}')
            # print(f'{block}')
            # print("\n=======================\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:

                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            # 'timestamp': time(),
            'timestamp': str(datetime.datetime.now()),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, imgFile, timestamp):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'img': imgFile,
            'timestamp': timestamp
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(
            block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

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
        # print("????????? ?????? ?????? : {} sec".format(end_time-start_time))
        # time_cnt += end_time-start_time
        # print('???????????? ?????? ?????? : ', time_cnt)
        # print('???????????? : ', time_cnt/100)
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

        th6.join()

        if flags is True:
            pass
        else:
            th7.start()
            th7.join()

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
        # print("????????? ?????? ?????? : {} sec".format(end_time-start_time))
        time_cnt += end_time-start_time
        print('???????????? ?????? ?????? : ', time_cnt)
        print('???????????? : ', time_cnt/100)
        print('?????? ??? ?????? : ', arr)
        print('cannot found : ', 100 - sum(arr))

        return proof_Result

    @ staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
            Validates the Proof
            :param last_proof: <int> Previous Proof
            :param proof: <int> Current Proof
            :param last_hash: <str> The hash of the Previous Block
            :return: <bool> True if correct, False if not.
            """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[: 4] == "0000"
