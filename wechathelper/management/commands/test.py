
import io
from PIL import Image
from wxpy import *
import time

qr_code_path = '/Users/chenjunqian/Downloads/MyGithub/wechathelper/wechathelper/management/commands/'

def qr_callback(uuid, status, qrcode):
    print(
        'uuid : '+str(uuid)+'\n'
        +'status : '+str(status)+'\n'
        +'qrcode : '+str(type(qrcode))+'\n'
    )
    # image = Image.open(io.BytesIO(qrcode))
    # image.save(qr_code_path)


# bot = Bot(
#     cache_path=True,
#     qr_path=qr_code_path,
#     qr_callback=qr_callback,
#     console_qr=-2
#     )
bot = Bot()
print(bot.user_details(bot.friends()))



# for friend in bot.friends():
#     print(bot.usr)

while True:
    time.sleep(5)