from telegram.ext import Updater
from telegram.ext import CommandHandler
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
from tele import chat_id, bot, token
import uuid
from io import BytesIO
from PIL import Image
import numpy as np
import pickle

app = Flask(__name__)

# updater
# updater = Updater(token=token, use_context=True)

# dispatcher = updater.dispatcher


# start_handler = CommandHandler('start', runbot)
# dispatcher.add_handler(start_handler)
# updater.start_polling()


# Module :: Snapshot cam display
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

    # ################## backup #################
    # encode image
    # base64_string = base64.b64encode(test)
    # imgdata = base64_string.decode('utf-8')
    ##############################################
    # jsonObj = json.dumps({'location': loc, 'name': name,
    #                       'phone': phone}, ensure_ascii=False)
    ####################################

    # b64로 인코드 후 utf-8로 디코딩함
    b64 = base64.b64encode(pickle.dumps(test))
    b64 = b64.decode('utf-8')
    # print(b64)
    # print(pickle.loads(base64.b64decode(b64)))
    # 블록에 저장되어 있는 바이트 문자를 다시 numpy array로 가져올 때 아래와 같이 하면 된다.
    # print(np.array_equal(pickle.loads(base64.b64decode(b64)), test))
    ####################################
    jsonObj = json.dumps(
        {'snapshot': b64}, ensure_ascii=False)
    jsonObj = json.loads(jsonObj)
    filename = 'test{0}.jpg'.format(cnt)
    with open(filename, 'wb') as f:
        cv2.imwrite(filename, np.array(test.tolist()))

    # Save image file module
    # filename = 'test{0}.jpg'.format(cnt)
    # with open(filename, 'wb') as f:
    #     cv2.imwrite(filename, test)
    # cnt = cnt + 1

    # Bot part
    # Convert numpy array to Image using PIL
    converted_img = Image.fromarray(test, 'RGB')

    # 나중에 def로 분리할지 생각 해보기
    bio = BytesIO()
    bio.name = str(uuid.uuid4())
    converted_img.save(bio, 'JPEG')
    bio.seek(0)
    # Send Photo 잠시 막아둠
    # bot.sendPhoto(
    #     chat_id=chat_id, photo=bio)

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

    # updater
    # updater = Updater(token=token, use_context=True)

    # dispatcher = updater.dispatcher

    # # Command handler

    # def runbot(update, context):
    #     context.bot.send_message(
    #         chat_id=update.effective_chat.id, text=blockchain.chain)

    # start_handler = CommandHandler('start', runbot)
    # dispatcher.add_handler(start_handler)
    # updater.start_polling()


def runbot(update, context):
    convImg = blockchain.chain[-1]['transactions'][0]['img'].encode('utf-8')
    convtImg = pickle.loads(base64.b64decode(
        convImg))
    converted_img = Image.fromarray(convtImg, 'RGB')

    bio = BytesIO()
    bio.name = str(uuid.uuid4())
    converted_img.save(bio, 'JPEG')
    bio.seek(0)

    bot.sendPhoto(
        chat_id=chat_id, photo=bio)

    # context.bot.send_message(
    #     chat_id=update.effective_chat.id, text=blockchain.chain[-1]['transactions'])


@ app.route('/')
def index():

    return render_template('index.html')


if __name__ == '__main__':
    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', runbot)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    p1 = Process(target=new_mine)
    p2 = Process(target=catchCam)

    new_mine()
    p2.start()
    app.run(host='0.0.0.0', port=port, debug=True,
            use_reloader=False, threaded=True)
