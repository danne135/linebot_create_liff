from flask import Flask, request, abort, render_template
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from liffpy import (
    LineFrontendFramework as LIFF,
    ErrorResponse
)
import os

app = Flask(__name__, template_folder='templates')
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

channel_access_token = os.getenv('co8ujSpXAemy3BjpjuSmOkEhUDnwnDmzCwsCtN/5httvZW+17I3ty4PN1LxwzN4Zku0ni0kQ+XK3VwKqkwGnAjwFRPY/ujvnzoOfnFU1dmFxLWdjmriP2+SmQ1I+O9jURfasevDW78dWfOIYBLZZ2QdB04t89/1O/w1cDnyilFU=')
if channel_access_token is None:
    raise ValueError("CHANNEL_ACCESS_TOKEN environment variable is not set or has no value.")
line_bot_api = LineBotApi(channel_access_token)

handler_secret = os.getenv('HANDLER_SECRET')
if handler_secret is None:
    raise ValueError("HANDLER_SECRET environment variable is not set or has no value.")
handler = WebhookHandler(handler_secret)

liff_api_token = os.getenv('Ue3f6985f37141fff5f5f466ca20df3c7')
if liff_api_token is None:
    raise ValueError("LIFF_API_TOKEN environment variable is not set or has no value.")
liff_api = LIFF(liff_api_token)

try:
    now_LIFF_APP_number = len(liff_api.get())
except:
    now_LIFF_APP_number = 0

target_LIFF_APP_number = 10
print(target_LIFF_APP_number, now_LIFF_APP_number)
if now_LIFF_APP_number < target_LIFF_APP_number:
    for i in range(target_LIFF_APP_number - now_LIFF_APP_number):
        liff_api.add(view_type="full", view_url="https://www.google.com")


@app.route("/")
def index():
    return render_template("./liff.html")


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '最新合作廠商' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'Maso的鑄鐵坊':
        message = TextSendMessage(text="Maso的鑄鐵坊，目前施工中...")
        line_bot_api.reply_message(event.reply_token, message)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
