from flask import Flask, request, render_template, jsonify
from telegram import message
from blockchain import Blockchain
import base64
from argparse import ArgumentParser
from uuid import uuid4
import json
import threading
import cv2
import shutil
import os
from multiprocessing import Process
from tele import chat_id, bot
import numpy as np
import uuid

from io import BytesIO

from PIL import Image

app = Flask(__name__)

# Module :: Snopsnot cam display


capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def catchCam():
    global capture
    # capture = cv2.VideoCapture(0)
    # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while cv2.waitKey(33) < 0:
        ret, frame = capture.read()

        #############
        cv2.imwrite('./img/a.jpg', frame)

        shutil.copyfile(os.path.join('./img', 'a.jpg'),
                        os.path.join('./img', 'a_tmp.jpg'))

        #############
        cv2.imwrite('./img/a.jpg', frame)

        return frame

    capture.release()
    cv2.destroyAllWindows()


# How to use another method that involved other file's Class
# @app.route('/test')
# def test():
#     a = Blockchain.test()
#     print(a)
#     return True
###################################################################################
###################################################################################
###################################################################################
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# Instantiate the Blockchain
blockchain = Blockchain()


@ app.route('/chain', methods=['GET'])
def full_chain():
    chains = blockchain.chain
    response = {
        # 'chain': blockchain.chain,
        'chain': chains,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


def new_mine():
    new_tran()
    replaced = blockchain.resolve_conflicts()

    if replaced:
        print(':: Our chain was replaced ::')
    else:
        print(':: Our chain is representative ::')

    # 노드 검증
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = '''[ NOTICE ] %s번째 블록이 생성되었습니다. | proof=%s | transaction Length=%s |''' % (
        block['index'], block['proof'], len(block['transactions']))

    print(response)
    threading.Timer(5, new_mine).start()


@ app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


# @ app.route('/tran/new', methods=['POST'])
img_tmp = 'a'
cnt = 1


def new_tran():
    # declare global variable
    global img_tmp
    global cnt

    test = catchCam()
    print(type(test))
    # snapshot part
    # with open('./img/a_tmp.jpg', 'rb') as img:
    #     base64_string = base64.b64encode(img.read())

    # encode image
    base64_string = base64.b64encode(test)
    print(type(base64_string))

    # imgdata = base64.b64decode(base64_string)
    imgdata = base64_string.decode('utf-8')
    # print(imgdata)
    # jsonObj = json.dumps({'location': loc, 'name': name,
    #                       'phone': phone}, ensure_ascii=False)
    jsonObj = json.dumps({'snapshot': imgdata}, ensure_ascii=False)
    jsonObj = json.loads(jsonObj)

    # Save image file module
    filename = 'test{0}.jpg'.format(cnt)
    with open(filename, 'wb') as f:
        cv2.imwrite(filename, test)
    cnt = cnt + 1

    # Bot part
    # Convert numpy array to Image using PIL

    converted_img = Image.fromarray(test, 'RGB')

    ################################### temp############################
    bio = BytesIO()
    bio.name = str(uuid.uuid4())
    converted_img.save(bio, 'JPEG')
    bio.seek(0)
    bot.sendPhoto(
        chat_id=chat_id, photo=bio)
    ####################################################################

    ######################
    # ENCODING PART
    ######################
    # imgdata = base64.b64decode(base64_string)
    # filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    # with open(filename, 'wb') as f:
    #     f.write(imgdata)
    ######################
    # required = ['location', 'name', 'phone']
    required = ['snapshot']
    if not all(k in jsonObj for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    # index = blockchain.new_transaction(
    #     jsonObj['location'], jsonObj['name'], jsonObj['phone'])
    index = blockchain.new_transaction(
        jsonObj['snapshot'])
###################################################################################
###################################################################################
###################################################################################


@ app.route('/')
def index():

    return render_template('index.html')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    p1 = Process(target=new_mine)
    p2 = Process(target=catchCam)

    new_mine()
    p2.start()
    # new_mine()
    app.run(host='0.0.0.0', port=port, debug=True,
            use_reloader=False, threaded=True)
