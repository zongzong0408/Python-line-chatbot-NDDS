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

import os
import random
import json

"""
    機器人初始化
"""
with open("data.json", "r", encoding = "utf-8") as file:
    Data = json.load(file)

Api = Data["Bot Token"]
Secret = Data["Channel Secret"]
Id = Data["User ID"]

app = Flask(__name__)

line_bot_api = LineBotApi(Api)
handler = WebhookHandler(Secret)
line_bot_api.push_message(Id, TextSendMessage(text = "Line Bot 'NDDS' is starting."))

@app.route("/callback", methods=["POST"])
def callback():

    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text = True)
    app.logger.info("Request body : " + body)

    try:

        handler.handle(body, signature)

    except InvalidSignatureError:

        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return "OK"


"""
    訊息傳遞區塊(命令)
"""
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):

#     if event.source.user_id != Id:

#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text = event.message.text)
#         )


"""
    機器人開始
"""
if __name__ == "__main__":
    # port = int(os.environ.get('POST', 5000))
    # app.run(host = '0.0.0.0', port = port)
    app.run()