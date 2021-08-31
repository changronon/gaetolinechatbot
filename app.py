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

line_bot_api = LineBotApi('FV4H4oYbJuoRJlmkITERsAbtli3pfwsZFNvcZA3S8lI5Cm/BO5AyJrU7j8Gxm/iV0VZUnoQtQP027TPN/7Rl2Fbe7zRlAZojwAnPQNx3EMKw99L0Zr1G11xxpBYlLKx6vHCFJA2P3GAXfig/tjNEqwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6f023657c5566249390ba0a6be3038ac')


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
    print("event.reply_token:", event.reply_token)
    print("event.source.user_id:", event.source.user_id)
    print("event.message.text:", event.message.text)
    
    # 加了這行
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()