from flask import Flask, request, abort, render_template
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import(InvalidSignatureError)
from linebot.models import *
from liffpy import (LineFrontendFramework as LIFF, ErrorResponse)
import os

#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

app = Flask(__name__, static_folder='static', template_folder='templates')

# 環境變數取得token和secret
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

# 確保環境變數存在
if CHANNEL_ACCESS_TOKEN is None or CHANNEL_SECRET is None:
    raise ValueError("The CHANNEL_ACCESS_TOKEN and CHANNEL_SECRET need to be set as environment variables.")

liff_api = LIFF(CHANNEL_ACCESS_TOKEN)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/")
def index():
    return render_template("liff.html")

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 頭部資訊
    signature = request.headers['X-Line-Signature']
    # 獲取請求內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 處理webhook主體
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 其他消息處理功能省略...

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
