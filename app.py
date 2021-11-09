# web app
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('ILwxcGYJhnPBWqlcRjYm8C3YYvcvcL0R1dgThhW2Vmj5zp0fB2TggcYrbVqKtsw9cjYuN2G+QfMo84udNL08SvycHqm3qqGuiIQNoxZwWVyjE51a8sVeELo5dmKBWxG4gR50BbyHnC5F4httFDaKVwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9532738f595361fee12a7d4b16733653')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉,你說什麼?'
    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了沒':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '你想訂位嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))
            

if __name__ == "__main__":
    app.run()