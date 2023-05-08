import requests
from flask import Blueprint, request, session, jsonify
from data_sheet import User
from tool import check_Indonesia

app=Blueprint("user/register",__name__)
ALGORITHM='HS256'
SECRET_KEY='culchyufrtedt'

@app.route("",methods=['POST'])
def register():
    try:
        phone=request.json.get("phone")
        password=request.json.get("password")
        checkpassword=request.json.get("checkpassword")
        indonesia = requests.get("Indonesia")
        ischeak = check_Indonesia(indonesia)
        if password==checkpassword and ischeak == True:
            result=session.query(User).filter(User.phonenum==phone).first()
            if result is None:
                newuser=User(mailnum=phone,password=password)
                session.add(newuser)  # 添加记录
                session.flush()
                session.commit()
                return jsonify(code=200,message='success')
            return jsonify(code=403,message="该用户已存在")
        return jsonify(code=403,message="两次输入的密码不一致")
    except Exception as e:
        return jsonify(code=404,message=f'{e}')
