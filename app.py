from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
import logging
import sys

app = Flask(__name__)

# 日志配置
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()

# 替换成您的Token、EncodingAESKey和AppID
WECHAT_TOKEN = 'oscar'
WECHAT_AESKEY = 'aALEFhhfFZz7g26WhrsU2HjQWjQkiQgtNqi5NAzWtj8'
WECHAT_APPID = 'wx913eb91e3e41654e'

@app.route('/status')
def status():
    return "Service is running!"

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 记录GET请求的参数
        logger.info("Received GET request with params: %s", request.args)

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
        
        # 记录认证结果
        if hashcode == signature:
            logger.info("Verified GET request successfully.")
            return make_response(echostr)
        else:
            logger.warning("Failed to verify GET request.")
            return make_response("Verification failed", 403)

    else:
        # 记录POST请求的数据
        logger.info("Received POST request with data: %s", request.data)

        # 处理微信发来的消息
        xml_recv = ET.fromstring(request.data)
        msg_type = xml_recv.find("MsgType").text
        from_user = xml_recv.find("FromUserName").text
        to_user = xml_recv.find("ToUserName").text

        if msg_type == "text":
            reply_text = "您发送了文本消息"
            reply_xml = f"""
            <xml>
            <ToUserName><![CDATA[{from_user}]]></ToUserName>
            <FromUserName><![CDATA[{to_user}]]></FromUserName>
            <CreateTime>{int(time.time())}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{reply_text}]]></Content>
            </xml>
            """
            return reply_xml
        else:
            return "success"

if __name__ == '__main__':
    app.run(debug=True)
