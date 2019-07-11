# encoding: utf-8
#import jieba
import sys
import random
sys.path.append("./assest")
from linebot.models import *
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

line_bot_api = LineBotApi('7Gx3IFDSWv/ZOXvjoirXVKaOANy6z9QcCUy5esNsdVTICYK9xWzkFuuFM518hoBj20EPWeqCBBsuqJC8XF+QZiozNKE5aC6owkri3krMYOhJfkgloYeUSmuc9RrXhTFAHmbVmjP8/1eKAJE+0FoATgdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('72307a91890d15c058d402e946bbb2f1') #Your Channel Secret

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
def handle_text_message(event):
    text = event.message.text #message from user
   # line_bot_api.reply_message(
    #    event.reply_token,
     #   TextSendMessage(text="hi"))  # reply the same message from user
    if text == "今日匯率":
        text = "data"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))
        return 0

    buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title='請選擇以下服務',
            text='點選顯示介紹',
            thumbnail_image_url='https://storage.cloud.google.com/ex_rate/tenor.gif',
            actions=[
                MessageTemplateAction(
                    label='今日匯率',
                    text='今日匯率'
                ),
                MessageTemplateAction(
                    label='關於我們',
                    text='關於我們'
                ),
                MessageTemplateAction(
                    label=mood,
                    text=mood
                )
            ]
        )
    )

    line_bot_api.reply_message(event.reply_token, buttons_template)

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
