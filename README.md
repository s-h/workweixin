## 企业微信发送消息
### 功能
支持两种消息方式送至企业微信方式：
> #### 发送消息至企业应用
> #### 发送消息至群组机器人
    
### 使用方法
#### 安装依赖

    python3 -m pip install -r requirement.txt    

#### 发送消息至企业应用

    python3 sendMessage.py --action="sendApp" --corpid="企业id" --corpsecret="应用凭证秘钥" --agentid="应用id" --conten="发送内容"

#### 发送消息至群组机器人

    python3 sendMessage.py --action="sendBot" --webhookKey="企业微信机器人webhook地址" --content="发送内容"
