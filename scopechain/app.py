from flask import Flask, request, render_template
from blockchain import Blockchain
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from argparse import ArgumentParser

app = Flask(__name__)

# How to use another method that involved other file's Class
# @app.route('/test')
# def test():
#     a = Blockchain.test()
#     print(a)
#     return True


@app.route('/')
def index():

    with open('./image.png', 'rb') as img:
        base64_string = base64.b64encode(img.read())

    return render_template('index.html', arg=base64_string, len=len(base64_string))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    with open('./image.png', 'rb') as img:
        base64_string = base64.b64encode(img.read())

    img = Image.open(BytesIO(base64.b64decode(base64_string)))
    plt.imshow(img)
    app.run(host='0.0.0.0', port=port, debug=True,
            use_reloader=False, threaded=True)
