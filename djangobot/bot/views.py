from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

from django.http import HttpResponseServerError

from .models import LineUser

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FollowEvent,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackTemplateAction,
    PostbackEvent
)

import os
import json

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

    """ラインの友達追加時・メッセージ受信時に呼ばれる"""
    if request.method == 'POST':
        request_json = json.loads(request.body.decode('utf-8'))
        events = request_json['events']
        line_user_id = events[0]['source']['userId']

        # 友達追加時
        if events[0]['type'] == 'follow':
            LineUser.objects.create(user_id=line_user_id)

        # アカウントがブロックされたとき
        elif events[0]['type'] == 'unfollow':
            LineUser.objects.filter(user_id=line_user_id).delete()
        
        # postbackの処理
        elif events[0]['type'] == 'postback':
            # ポストバックの内容を取得
            w_action = events[0]["postback"]["data"].split("&")[0].replace("action=", "")
            w_step = events[0]["postback"]["data"].split("&")[1].replace("step=", "")
            
            # 登録時の処理
            if w_action == "register":
                if w_step == 'open':
                    # 鍵が開いている状態の加速度情報をDBに登録

                    # 加速度情報を取得する処理（とりあえず仮の値を使う）

                    x = 1
                    y = 1
                    z = 1

                    # 加速度情報の登録
                    registering_user = LineUser.objects.get(user_id = line_user_id)
                    # 加速度情報を更新
                    registering_user.x_open = x
                    registering_user.y_open = y
                    registering_user.z_open = z
                    # 保存
                    registering_user.save()
                elif w_step == 'close':
                    # 鍵が閉まっている状態の加速度情報をDBに登録

                    # 加速度情報を取得する処理（とりあえず仮の値を使う）

                    x = 2
                    y = 2
                    z = 2

                    # 加速度情報の登録
                    # ユーザーのデータのオブジェクトを取得
                    registering_user = LineUser.objects.get(user_id = line_user_id)
                    # 加速度情報を更新
                    registering_user.x_close = x
                    registering_user.y_close = y
                    registering_user.z_close = z
                    # 保存
                    registering_user.save()

    # tryがうまく行けば200を返す
    return HttpResponse('OK', status=200)


# 加速度情報の登録を促すためのメッセージ（登録してすぐ送信）
initialize_button_message = TemplateSendMessage(
    alt_text='initialize button',
    template=ButtonsTemplate(
        title='鍵の情報を登録',
        text='鍵の状態を計算するための情報を登録します',
        actions=[
            PostbackTemplateAction(
                label='OK',
                display_text='鍵の状態を登録',
                data='action=register&step=start'
            )

        ]
    )
)

# 鍵が開いている状態を登録するためのメッセージ
register_open_button_message = TemplateSendMessage(
    alt_text='register open button',
    template=ButtonsTemplate(
        title='鍵が開いているときの状態を登録',
        text='鍵が開いている時の状態を登録します。鍵が開いており、本製品が正しく取り付けられていることを確認して、OKを押して下さい',
        actions=[
            PostbackTemplateAction(
                label='OK',
                display_text='開いている状態を登録',
                data='action=register&step=open'
            )

        ]
    )
)

# 鍵が閉まっている状態を登録するためのメッセージ
register_close_button_message = TemplateSendMessage(
    alt_text='register close button',
    template=ButtonsTemplate(
        title='鍵が閉まっているときの状態を登録',
        text='鍵が閉まっている時の状態を登録します。鍵が閉まっており、本製品が正しく取り付けられていることを確認して、OKを押して下さい',
        actions=[
            PostbackTemplateAction(
                label='OK',
                display_text='閉まっている状態を登録',
                data='action=register&step=close'
            )

        ]
    )
)

# 登録が正常に行われなかったときに再登録するためのメッセージ
reregister_button_message = TemplateSendMessage(
    alt_text='initialize button',
    template=ButtonsTemplate(
        title='登録に失敗しました',
        text='再度登録をやり直す場合はOKを押して下さい',
        actions=[
            PostbackTemplateAction(
                label='OK',
                display_text='鍵の状態を登録',
                data='action=register&step=1'
            )
        ]
    )
)

# addメソッドの引数にイベントのモデルを入れる
# 関数名は自由
@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text='初めまして'),
         TextSendMessage(text='登録ありがとうございます'),
         initialize_button_message,]
    )

@handler.add(PostbackEvent)
def handle_postback_event(event):
# ポストバックの内容を取得
    w_action = event.postback.data.split("&")[0].replace("action=", "")
    w_step = event.postback.data.split("&")[1].replace("step=", "")
    
    # 登録時の処理
    if w_action == "register":
        # ステップごとに処理を記述
        # ステップ１
        if w_step == 'start':
            # 鍵が開いている状態を登録するためのメッセージを送信
            line_bot_api.reply_message(
                event.reply_token,
                register_open_button_message
            )
        # ステップ２
        elif w_step == 'open':
            try:
                # 正常に登録できたら、閉まっている状態の登録に進む
                line_bot_api.reply_message(
                    event.reply_token,
                    register_close_button_message
                )
            except:
                # 失敗したらもう一度登録し直す
                line_bot_api.reply_message(
                    event.reply_token,
                    reregister_button_message
                )
        # ステップ３
        elif w_step == 'close':
            try:
                # 正常に登録できたら、完了メッセージを送信
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='正常に登録が完了しました')
                )
            except:
                # 失敗したらもう一度登録し直す
                line_bot_api.reply_message(
                    event.reply_token,
                    reregister_button_message
                )





# オウム返し
@handler.add(MessageEvent, message=TextMessage) 
# Messageが送られてきた時の処理のため、
# MessageEventを第一引数に、第二引数でmessageにmessage内容を代入
def handle_text_message(event):
    line_bot_api.reply_message(event.reply_token,
                            initialize_button_message,)
        




@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)

