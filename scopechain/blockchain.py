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
from multiprocessing import Process, Value
from ctypes import c_bool, c_int
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

    def find_proof(self, flags, idx, last_proof, proof, last_hash, proof_result, start, end):

        for i in range(start, end):
            # print('NOW PROOF : ', proof)
            if flags.value is True:
                print('[fun{0}] flags.value is True'.format(idx))
                break
            if self.valid_proof(last_proof, proof, last_hash) is True:
                flags.value = True
                proof_result.value = proof
                print('[fun{0} is finished] proof : {1}'.format(
                    idx, proof_result.value))
                print('NOW FLAGS : ', flags.value)
                break
            proof += 1

    def proof_of_work(self, last_block):
        """
            Simple Proof of Work Algorithm:
            - Find a number p' such that hash(pp') contains leading 4 zeroes
            - Where p is the previous proof, and p' is the new proof

            :param last_block: <dict> last Block
            :return: <int>
            """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        # Flags
        flags = Value(c_bool, False)
        proof_result = Value(c_int, 0)

        # Proof
        proof1 = 0
        proof2 = 150001

        start_time = time.time()
        p1 = Process(target=self.find_proof, args=(flags, 0,
                                                   last_proof, proof1, last_hash, proof_result, 0, 150001))
        p2 = Process(target=self.find_proof, args=(flags, 1,
                                                   last_proof, proof2, last_hash, proof_result, 150001, sys.maxsize))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

        end_time = time.time()
        print('TIMETIMETIMETIME : ', end_time-start_time)

        print('proof_result : ', proof_result.value)

        return proof_result.value

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
