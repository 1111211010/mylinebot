from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage

from datetime import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def index(request):
    return HttpResponse("Hello World")

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:

           # 若有訊息事件
            if isinstance(event, MessageEvent):

                txtmsg = event.message.text

                if txtmsg in ["你好", "Hello", "早安", "Hi"]:
                    
                    stkpkg, stkid = 1070, 17840
                    replymsg = "你好, 請問需要為你做什麼?"

                    line_bot_api.reply_message(
                    event.reply_token,
                    [StickerSendMessage(package_id = stkpkg, sticker_id=stkid),
                     TextSendMessage( text = replymsg )])

                elif txtmsg in ["龍山寺求籤","求籤","龍山寺拜拜"]:

                    num = random.choice(range(1,101))
                    imgurl = f"https://www.lungshan.org.tw/fortune_sticks/images/{num:0>3d}.jpg"

                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(original_content_url=imgurl,
                        preview_image_url=imgurl))

                elif txtmsg == "淺草寺求籤":
                    num = random.choice(range(1,101))
                    imgurl1 = f"https://qiangua.temple01.com/images/qianshi/fs_akt100/{num}.jpg"
                    imgurl2 = f"https://qiangua.temple01.com/images/qianshi/fs_akt100/back/{num}.jpg" 

                    line_bot_api.reply_message(
                        event.reply_token,
                        [ImageSendMessage(original_content_url=imgurl1,
                        preview_image_url=imgurl1),
                        ImageSendMessage(original_content_url=imgurl2,
                        preview_image_url=imgurl2)])

                 else:

                replymsg = "你所傳的訊息是:\n" + txtmsg
                
                # 回傳收到的文字訊息
                line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage( text = txtmsg ),
                     
                     StickerSendMessage(package_id=1070, sticker_id=17840),
                     
                     ImageSendMessage(original_content_url='https://ws.taipei-101.com.tw/upload/firework/20220105/ada6f07c3d244c4f80e0f231be729313/ada6f07c3d244c4f80e0f231be729313.jpg', preview_image_url='https://ws.taipei-101.com.tw/upload/firework/20220105/ada6f07c3d244c4f80e0f231be729313/ada6f07c3d244c4f80e0f231be729313.jpg'),

                    LocationSendMessage(title='台北101', address='Taipei', latitude=25.033976,longitude=121.564539)
                    ])



        return HttpResponse()
    else:
        return HttpResponseBadRequest()
