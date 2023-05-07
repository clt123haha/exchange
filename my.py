import base64
import random
import time
import urllib.parse
import urllib.request
from io import BytesIO
from flask import send_from_directory, make_response
from flask import Flask, request, jsonify,Blueprint,send_file
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import Flask
from random import randint
import os
from data_sheet import get_sheet,session,User,ShortMessage


app = Flask(__name__)

#图形验证码的字符
def image_str():
  random_str =''
  base_str ='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  for i in range(4):
    random_str +=base_str[random.randint(0, len(base_str)-1)]
  return random_str

#制作验证码图片
def creat_image():
    CAPTCHA_text = image_str()
    image = Image.new("RGB", (100, 50), (124, 231, 122))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', size=30)
    x = 15
    for i in CAPTCHA_text:  # 随机验证码
        # 为每个验证码字符设置不同的RGB颜色
        R = str(randint(0, 255))
        G = str(randint(0, 255))
        B = str(randint(0, 255))
        draw.text((x, 10),
                  text=i,
                  font=font,
                  fill="rgb(" + R + "," + G + "," + B + ")",
                  direction=None)
        x += 20
    for i in range(1, randint(7, 15)):
        x, y = randint(0, 100), randint(0, 50)
        x2, y2 = randint(0, 100), randint(0, 50)
        R = str(randint(0, 255))
        G = str(randint(0, 255))
        B = str(randint(0, 255))
        draw.line((x, y, x2, y2), fill="rgb(" + R + "," + G + "," + B + ")", width=2)
    return image,CAPTCHA_text


#存储图片
def generate_captcha_image(save_path=r'E:\Temp\image'):
    image,img_str = creat_image()
    if not os.path.exists(save_path):   # 检测目录是否存在，不在则创建
        os.makedirs(save_path)
    t = time.time()
    image.save('%s/%s.png'%(save_path, str(t)+img_str))
    return '%s/%s.png'%(save_path, str(t)+img_str)


#判断验证码是否正确以及删除过期验证码
def check_Indonesia(indonesia,path=r'E:\Temp\image'):   # 退出程序的时候一定要记得删除验证码，否则内存占用会越来越大
    files=os.listdir(path) # 获取目录下的文件
    os.chdir(path)  # 进入目录
    t = time.time()
    for file in files:
        s = file.title()
        time_f = s[0:len(s)-8]
        indonesia_t = s[len(s)-8:len(s)-4]
        time_f = float(time_f)
        second = t - time_f
        m, s = divmod(second, 60)
        if m >= 10:
            os.remove(file)
        if indonesia_t==indonesia:
            return True
    return False

def check_message(phone,indonesia):   # 退出程序的时候一定要记得删除验证码，否则内存占用会越来越大
    result = session.query(ShortMessage).filter(ShortMessage.phonenumber==phone).first()
    t = time.time()
    second = time.time() - float(result.time)
    m, s = divmod(second, 60)

    if m >= 10:
        return False
    if indonesia == result.meaasge:
        return  True
    return False



#用于获取验证码的接口
@app.route('/get_Indonesia')
def get_Indonesia():
    file_name = generate_captcha_image()
    with open(file_name, 'rb') as f:
        res = base64.b64encode(f.read())
        return res

#手机验证码的字符串
def generate_random_str():
  random_str =''
  base_str ='0123456789'
  for i in range(6):
    random_str +=base_str[random.randint(0, len(base_str)-1)]
  return random_str


# 发送短信验证码
def short_message(mobile):
    url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'
    str = generate_random_str()
    # 定义请求的数据
    values = {
        'account': 'C99499604',  # 用户名
        'password': 'f8306695d35f13813318e04e6a2c4349',
        'mobile': mobile,  # 要发送的号码
        'content': '您的验证码是：{}。请不要把验证码泄露给其他人。'.format(str),  # 发送的
        'format': 'json',  # 格式类型
    }

    # 将数据进行编码
    data = urllib.parse.urlencode(values).encode(encoding='UTF8')

    # 发起请求
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    return str

#发送手机验证码的接口
@app.route('/user/login/mobile_text')
def test():
    phone = request.json.get("phone")
    if phone is None:
        return {'code':201,'message':'请输入手机号码'}
    try:
         indonesia = short_message(phone)
         print(type(indonesia))
    except Exception as e:
        print(e)
        return {'code':202,'meaasge':'发送失败，请稍后再试'}
    try:
        result = session.query(ShortMessage).filter(ShortMessage.phonenumber == phone).first()
        if result is None:
            newMessage = ShortMessage(phonenumber=phone,meaasge="000000",time=str(time.time()))
            session.add(newMessage)
            session.commit()
        else:
            result.meaasge = indonesia
            session.add(result)
            session.commit()
    except Exception as e:
        return {'code':203,'message':'验证码无效'}
    return  {'code':200,'message':'发送成功，短信验证码有效期为十分钟'}

#验证手机验证码的登录接口
@app.route('/user/login/moblie')
def moblie_login():
    indonesia = requests.get("Indonesia")
    message = request.json.get("message")
    phone = request.json.get("phone")
    ischeak = check_Indonesia(indonesia)
    ischeak2 = check_message(phone,message)
    if ischeak == True and idcheak2 == True:
        return {'code':200,'message':'欢迎回来'}
    if ischeak == False:
        return {'code': 304, 'message': '验证码错误'}
    if ischeak2 == False:
        return {'code': 305, 'message': '手机验证码错误'}



#密码登录的接口
@app.route('/user/login/password')
def check_password():
    username = request.json.get("username")
    password = request.json.get("password")
    cheakpassword = request.json.get("cheakpassword")
    indonesia = request.json.get("Indonesia")
    ischeak = check_Indonesia(indonesia)
    result = session.query(User).filter(User.username == username).first()
    if ischeak == False:
        return {'code': 304, 'message': '验证码错误'}
    if cheakpassword != password:
        return {'code': 301, 'message': '请两次输入相同密码'}
    if result == None:
        return {'code': 302, 'message': '账号不存在'}
    if result.password != password:
        return {'code': 303, 'message': '密码错误'}
    return {'code':200,'message':'欢迎回来'}

if __name__ == '__main__':
    get_sheet()
    app.run(host='0.0.0.0', debug=True)