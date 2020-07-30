#!/usr/bin/env python3
#coding:utf-8
'''
# =============================================================================
#      FileName: sendMessage.py
#          Desc: 
#        Author: jianghao
#         Email: mail@jianghao.tech
#      HomePage: http://www.github.com/s-h
#       Version: 0.0.1
#    LastChange: 2020-07-29
#       History:
# =============================================================================
'''
# 支持发送消息至企业微信应用
# 支持发送消息至企业微信群组bot
import json
import requests
import time
from optparse import OptionParser

parser = OptionParser()
#执行动作
parser.add_option("--action", type="string", dest="action", help=" \
    应用发送消息(sendApp)、bot发送消息(sendBot)")
#企业id
parser.add_option("--corpid", type="string", dest="corpid")
#应用凭证秘钥
parser.add_option("--corpsecret", type="string", dest="corpsecret")
#消息内容
parser.add_option("--content", type="string", dest="content")
#应用id
parser.add_option("--agentid", type="string", dest="agentid")
#企业微信机器人webhook地址
parser.add_option("--webhookKey", type="string", dest="webhookKey")
(options,args) = parser.parse_args()

def requestURL(url, body=None, n=3):
    # 尝试n回访问url
    if n <= 1:
        print("访问'%s'失败" % url)
        raise ConnectionError
    try:
        rs = requests.post(url, body).json()
    except Exception as e:
        print("连接重试")
        n -= 1
        time.sleep(1)
        requestURL(url, body, n)
    # 
    if rs["errcode"] != 0:
        print(rs["errmsg"])
        raise ConnectionError
    return rs

# 获取企业微信token
def get_token(corpid, corpsecret):
    url = 'https://qyapi.weixin.qq.com'
    token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url, corpid, corpsecret)
    try:
        rs = requestURL(token_url)
    except ConnectionError:
        print("获取token失败")
        exit()
    return rs["access_token"]

# 发送告警信息
def send_message(token, content, agentid):
    url = 'https://qyapi.weixin.qq.com'
    values = {
        "touser": '@all',
        "msgtype": 'text',
        "agentid": agentid, 
        "text": {'content': content},
        "safe": 0
        }
    body=bytes(json.dumps(values, ensure_ascii=False), encoding='utf-8')
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + token
    try:
        rs = requestURL(send_url, body)
    except ConnectionError:
        print("发送消息失败")

def send_boot_message(webhookKey, content):
    url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + webhookKey
    values = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    body=bytes(json.dumps(values, ensure_ascii=False), encoding='utf-8')
    try:
        requestURL(url, body)
    except ConnectionError:
        print("botMessage发送失败")

corpid = options.corpid
corpsecret = options.corpsecret
content = options.content
action = options.action
if action == "sendApp":
    token_rs=get_token(corpid, corpsecret)
    agentid = options.agentid
    token = token_rs
    #发送消息到应用
    send_message(token=token, content=content, agentid=agentid)
elif action == "sendBot":
    #发送消息到群组机器人
    webhookKey = options.webhookKey
    send_boot_message(webhookKey, content)
