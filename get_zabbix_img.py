#!/usr/bin/env python3
#coding: utf-8
#获取zabbix图片
#参考https://blog.csdn.net/zyh960/article/details/118762911
import requests
import base64
from io import BytesIO
import hashlib

zabbix_server = 'http://x.x.x.x/zabbix/' #zabbix的IP地址
zabbix_user= 'zabbix_user'
zabbix_password = 'zabbix_password'

headers = {
    "zabbix_server": zabbix_server,
    "Origin": zabbix_server,
    "Referer": "{zabbix_server}index.php".format(zabbix_server=zabbix_server),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
}
session = requests.session()
session.headers = headers


def get_zabbix_img(id):
    url = '{zabbix_server}index.php'.format(zabbix_server=zabbix_server)
    data = {
        "name": zabbix_user,
        "password": zabbix_password,
        "autologin": "1",
        "enter": "登录",
    }
    html = session.post(url=url,headers=headers,data=data,verify=False)
    if html.status_code == 200:
        graph_params = {
            "from":"now-1h",
            "to":"now",
            "itemids[0]": id,
            "type": "0",
            "profileIdx": "web.item.graph.filter",
            "profileIdx2": id,
            "width": "1820",
            "height":"600",
        }
        graph_url = '{zabbix_server}chart.php?'.format(zabbix_server=zabbix_server)
        #模拟登陆，发送get请求获取图片数据
        graph_req = session.get(url=graph_url, params=graph_params,verify=False)
        
        img_base64 = base64.b64encode(BytesIO(graph_req.content).read())

        # 测试生成图片
        #with open("test.png", 'wb') as f:
            #f.write(base64.b64decode(img_base64))
            #f.close()

        img_md5 = hashlib.md5(BytesIO(graph_req.content).read()).hexdigest().upper()
        return (img_base64, img_md5)
    else:
        print(html.status_code)

if __name__ == '__main__':
   img_base64 = get_zabbix_img(41444)
   print(img_base64)
