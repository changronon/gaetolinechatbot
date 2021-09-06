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

app = Flask(__name__)

line_bot_api = LineBotApi('g/nQVJOVCYLs/qqQsXuzn3NNgnCAT32o+xoEcOFBhjK+NUEAtqujMPAo+bpTj9xlJ4kny8z750qqUkEld3Q3S+kSurmLTkCV5Ti0vNb4ln6Z8ABnuRva4LA32pj53WVPf88gHzNwSpiiuZeiufEBSAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1ab2a06316420a3b5ff91b0510618a60')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()