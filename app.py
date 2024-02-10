from dotenv import load_dotenv
import os
from command_actions import CommandActions
from flask import Flask, abort, request
from linebot.v3.webhook import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

load_dotenv()
CHANNEL_SECRET = os.environ['LINE_SECRET']
ACCESS_TOKEN = os.environ['LINE_ACCESS_TOKEN']

handler = WebhookHandler(CHANNEL_SECRET)
configuration = Configuration(access_token=ACCESS_TOKEN)

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    select_commands = CommandActions()
    with ApiClient(configuration) as api_client:
        commands = message_split(event.message.text)
        # 入力したコマンドを判別、アクションを行う。
        msg = select_commands.witch_select_command(commands)
        line_bot_api = MessagingApi(api_client)
        
        line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=msg)]
                )
            )
        
        # if "@清算マン" in event.message.text:
        #     commands = message_split(event.message.text)
        #     print(commands[0])
        #     if commands[0] == '金払え':
        #         msg = f'{commands[1]}に{commands[2]}円払ってください'
        #     elif commands[0] == '金払った':
        #         msg = f'{commands[1]}に{commands[2]}円支払いました。'
        #     else:
        #         msg = 'ごめんね。\nまだ他のメッセージには対応してないよ'
        #     line_bot_api = MessagingApi(api_client)
        
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[TextMessage(text=msg)]
        #         )
        #     )
        # else:
        #     print("何もしない")

def message_split(message):
    split_message = message.split()
    return split_message


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
