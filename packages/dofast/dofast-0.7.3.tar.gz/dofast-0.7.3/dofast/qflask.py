import codefast as cf
from dofast._flask.config import AUTH_KEY
from dofast._flask.utils import authenticate_flask
from dofast.security._hmac import certify_token
from dofast.toolkits.telegram import bot_messalert
from flask import Flask, request

from .network import Twitter

app = Flask(__name__)
authenticate_flask(app)

@app.route('/tweet', methods=['GET', 'POST'])
def tweet():
    msg = request.get_json()
    text = cf.utils.decipher(AUTH_KEY, msg.get('text'))
    media = [f'/tmp/{e}' for e in msg.get('media')]
    cf.info(f'Input tweet: {text} / ' + ''.join(media))
    Twitter().post([text] + media)
    return 'SUCCESS'


@app.route('/messalert', methods=['GET', 'POST'])
def msg():
    js = request.get_json()
    bot_messalert(js['text'])
    return 'SUCCESS'


@app.route('/nsq', methods=['GET', 'POST'])
def nsq():
    msg = request.get_json()
    topic = msg.get('topic')
    channel = msg.get('channel')
    data = msg.get('data')
    cf.net.post(f'http://127.0.0.1:4151/pub?topic={topic}&channel={channel}',
                json={'data': data})
    print(topic, channel, data)
    return 'SUCCESS'


@app.route('/hello')
def hello_world():
    return 'SUCCESS!'


def run():
    app.run(host='0.0.0.0', port=6363, debug=True)
    # app.run(host='0.0.0.0', port=6363, ssl_context=('path_to.cer', 'path_to.key'), debug=True)

if __name__ == '__main__':
    run()
