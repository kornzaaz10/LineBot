from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import oil_price

app = Flask(__name__)

line_bot_api = LineBotApi('OLOz4VzGV5UWnisCWZ7XIG2hjWMXgiWovJlzsNYDjYPS9H3QnBfcviaDiRscYOM7duwxsOLEMDPVTRWMICu19XBWJXDhNK4BzmTSU2S0n7WBf/+cTq68LFRd7Lp3Y/IV+YJilL9GrFJymp+T8jY4jAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3406e2ef6f2fc4aba0a065df4a6ddcb7')

@app.route("/",methods=['GET'])
def default_action():
    return 'Hello'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'ราคาน้ำมัน':
        l = oil_price.get_prices()
        s = ""
        for p in l :
            s += "%s %.2f บาท\n"%(p[0],p[1])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=s))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text+'เจ้าคะ'))


if __name__ == "__main__":
    app.run()