
from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET

app = Flask(__name__)

# 这里替换成您自己的Token
WECHAT_TOKEN = 'your_wechat_token'

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 微信认证
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

        token = WECHAT_TOKEN
        data = [token, timestamp, nonce]
        data.sort()
        temp = ''.join(data)
        hashcode = hashlib.sha1(temp.encode('utf-8')).hexdigest()
        if hashcode == signature:
            return make_response(echostr)
        else:
            return ""
    else:
        # 处理微信发来的消息
        xml_recv = ET.fromstring(request.data)
        msg_type = xml_recv.find("MsgType").text
        from_user = xml_recv.find("FromUserName").text
        to_user = xml_recv.find("ToUserName").text

        if msg_type == "text":
            reply_text = "您发送了文本消息"
            reply_xml = f'''
            <xml>
            <ToUserName><![CDATA[{from_user}]]></ToUserName>
            <FromUserName><![CDATA[{to_user}]]></FromUserName>
            <CreateTime>{int(time.time())}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{reply_text}]]></Content>
            </xml>
            '''
            return reply_xml
        else:
            return "success"

if __name__ == '__main__':
    app.run(debug=True)
