## 企业微信发送消息
![](https://img.shields.io/badge/python-3.6-green)
### 功能
支持两种消息方式送至企业微信方式：
> #### 发送消息至群组机器人
    
### 使用方法
#### 安装依赖

    python3 -m pip install -r requirement.txt    

#### 发送消息至群组机器人
    webhook地址直接填key之后的内容

    python3 sendMessage.py --action="sendBot" --webhookKey="企业微信机器人webhook地址" --content="发送内容"

### 添加到zabbix
#### 上传脚本至服务器
上传位置根据zabbix_server.conf中的AlertScriptsPath值决定 ,修改get_zabbix_img.py中zabbix相关配置
#### 添加报警媒介
管理->报警媒介类型->创建媒体类型

其中脚本参数如图**不要加引号**
![](https://github.com/s-h/workweixin/blob/master/img/1.png)
脚本名称为上传至AlertScriptsPath目录的脚本名称
#### 用户资料
点击zabbix页面右上角![](https://github.com/s-h/workweixin/blob/master/img/5.png)图标->报警媒介->添加
![](https://github.com/s-h/workweixin/blob/master/img/2.png)
可选择报警级别
#### 配置动作
配置->动作->创建动作->操作(报警内容设置)->恢复操作(恢复报警设置)
![](https://github.com/s-h/workweixin/blob/master/img/3.png)
![](https://github.com/s-h/workweixin/blob/master/img/4.png)