from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
import os

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"] # YOUR_CHANNEL_ACCESS_TOKENは環境変数であり、後に設定する
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]# YOUR_CHANNEL_SECRETも環境変数であり、後に設定する

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@csrf_exempt #csrf攻撃対策
def callback(request):
    # リクエストヘッダーから署名検証用の値を取得する
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    #リクエストの内容を取得
    body = request.body.decode('utf-8')
    try:
        # 署名を検証して問題がなければ下に定義されたhandleを実行する
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 検証でエラーがあればエラー文を出す
        HttpResponseForbidden()
    # tryがうまく行けば200を返す
    return HttpResponse('OK', status=200)


# オウム返し
@handler.add(MessageEvent, message=TextMessage) 
# Messageが送られてきた時の処理のため、
# MessageEventを第一引数に、第二引数でmessageにmessage内容を代入
def handle_text_message(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=event.message.text))