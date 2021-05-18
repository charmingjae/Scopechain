import multiprocessing
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
import datetime
import time

app = Flask(__name__)


# Module :: Snapshot cam display
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def catchCam():
    global capture

    while cv2.waitKey(33) < 0:
        ret, frame = capture.read()
        cv2.imwrite('./img/a.jpg', frame)

        shutil.copyfile(os.path.join('./img', 'a.jpg'),
                        os.path.join('./img', 'a_tmp.jpg'))

        cv2.imwrite('./img/a.jpg', frame)

        return frame

    capture.release()
    cv2.destroyAllWindows()


# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


@ app.route('/chain', methods=['GET'])
def full_chain():
    chains = blockchain.chain
    response = {
        'chain': chains,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


mine_cnt = 1


def new_mine():
    global mine_cnt
    if mine_cnt > 100:
        return
    start_time = time.time()
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

    response = '''\n[ NOTICE ] %s번째 블록이 생성되었습니다. | proof=%s | transaction Length=%s |''' % (
        block['index'], block['proof'], len(block['transactions']))

    print(response)
    end_time = time.time()
    print("걸린 시간 : {} sec".format(end_time-start_time))
    mine_cnt += 1
    # threading.Timer(5, new_mine).start()
    threading.Timer(0, new_mine).start()


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


img_tmp = 'a'
cnt = 1


def new_tran():
    # declare global variable
    global img_tmp
    global cnt

    test = catchCam()

    # b64로 인코드 후 utf-8로 디코딩함
    b64 = base64.b64encode(pickle.dumps(test))
    b64 = b64.decode('utf-8')

    # jsonObj = json.dumps(
    #     {'snapshot': b64, 'timestamp': str(datetime.datetime.now())}, ensure_ascii=False)
    jsonObj = json.dumps(
        {'snapshot': b64, 'timestamp': str(datetime.datetime.now())}, ensure_ascii=False)
    jsonObj = json.loads(jsonObj)
    filename = 'test{0}.jpg'.format(cnt)
    with open(filename, 'wb') as f:
        cv2.imwrite(filename, np.array(test.tolist()))

    # Bot part
    # Convert numpy array to Image using PIL
    converted_img = Image.fromarray(test, 'RGB')

    # 나중에 def로 분리할지 생각 해보기
    bio = BytesIO()
    bio.name = str(uuid.uuid4())
    converted_img.save(bio, 'JPEG')
    bio.seek(0)

    required = ['snapshot', 'timestamp']
    if not all(k in jsonObj for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    # index = blockchain.new_transaction(
    #     jsonObj['location'], jsonObj['name'], jsonObj['phone'])
    index = blockchain.new_transaction(
        jsonObj['snapshot'], jsonObj['timestamp'])
    # print('트랜잭션 생성 완료')
    # print(blockchain.current_transactions)
    threading.Timer(0, new_tran).start()


imgCnt = 0


def runbot(cnt):
    global imgCnt
    # 1. blockchain.chain[cnt]의 길이를 가져온다
    # 2. 가져온 길이만큼 돌면서 이미지를 전송한다
    # 3. imgCnt ++
    # 4. 만약 imgCnt가 10을 넘어가면 브레이크
    chainLength = len(blockchain.chain[cnt]['transactions'])
    for i in range(chainLength-1):
        print(i)
        if imgCnt > 9:
            break
        else:
            convImg = blockchain.chain[cnt]['transactions'][i]['img'].encode(
                'utf-8')
            convtImg = pickle.loads(base64.b64decode(
                convImg))
            converted_img = Image.fromarray(convtImg, 'RGB')

            bio = BytesIO()
            bio.name = str(uuid.uuid4())
            converted_img.save(bio, 'JPEG')
            bio.seek(0)

            bot.sendPhoto(
                chat_id=chat_id, photo=bio)
            imgCnt = imgCnt + 1


# 개수 받아서 그만큼 보내기

def step1(update, context):
    msg = "입력한 개수 : " + context.args[0]
    bot.sendMessage(chat_id=chat_id, text=msg)
    # -1부터 거꾸로 가기
    for i in range(-1, (-1*cnt)-1, -1):
        runbot(i)

    # 입력한 개수 만큼 보내기
    # 현재 체인 길이와 입력 개수 비교해서 체인의 길이가 더 길면 그만큼 보내고.. 아니면 체인의 길이만큼 보내기


def getcnt(update, context):
    global imgCnt
    imgCnt = 0
    # parse time from args
    time1 = context.args[0] + ' ' + context.args[1]
    time2 = context.args[3] + ' ' + context.args[4]

    # print blockchain length
    arr = list(filter(lambda x: x['timestamp'] >
                      time1 and x['timestamp'] < time2, blockchain.chain))

    arrIndex = []
    # print('arr length : ', len(arr))
    for i in arr:
        if len(arrIndex) >= 10:
            break
        arrIndex.append(i['index'])
    print(arrIndex)
    for j in arrIndex:
        runbot(j)


@ app.route('/')
def index():

    return render_template('index.html')


if __name__ == '__main__':

    # # Instantiate the blockchain
    blockchain = Blockchain()

    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', runbot)
    step1_handler = CommandHandler('step1', step1, pass_args=True)
    getCnt_handler = CommandHandler('getCnt', getcnt)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(step1_handler)
    dispatcher.add_handler(getCnt_handler)
    updater.start_polling()

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    # p1 = Process(target=new_mine, args=(blockchain,))
    # p2 = Process(target=catchCam)
    # p3 = Process(target=new_tran, args=(blockchain,))

    # new_mine()
    # p1.start()
    # p2.start()
    # p3.start()

    new_mine()
    new_tran()
    # p1.join()
    # p3.join()

    app.run(host='0.0.0.0', port=port, debug=True,
            use_reloader=False, threaded=True)
