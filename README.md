# muvtuber

Makes your AI vtuber.

> 让 AI 成为虚拟主播：看懂弹幕，妙语连珠，悲欢形于色，以一种简单的实现

![obs](attachments/obs.png)

## 项目构成

![muvtuber-impl](attachments/muvtuber-impl.png)



| 服务                                                         | 说明                                                         | 基于                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [xfgryujk/blivechat](https://github.com/xfgryujk/blivechat)  | 获取直播间弹幕消息。                                         | [xfgryujk/blivechat](https://github.com/xfgryujk/blivechat) 做的非常好，直接用了，没有额外封装。 |
| [Live2dView](https://github.com/cdfmlr/live2dview)           | 前端：显示 [Live2D](https://www.live2d.com/en/) 模型         | [guansss/pixi-live2d-display](https://github.com/guansss/pixi-live2d-display) |
| [Live2dDriver](https://github.com/cdfmlr/live2ddriver)       | 驱动前端 Live2D 模型动作表情                                 | -                                                            |
| [ChatGPTChatbot](https://github.com/cdfmlr/chatgpt_chatbot)  | 基于 [ChatGPT](https://chat.openai.com) 的优质聊天机器人     | [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT)    |
| [MusharingChatbot](https://github.com/cdfmlr/musharing_chatbot) | 基于 [ChatterBot](https://github.com/gunthercox/ChatterBot) 的简单聊天机 | [RaSan147/ChatterBot_update](https://github.com/RaSan147/ChatterBot_update) <br/> [musharing-team/chatbot_api](https://github.com/musharing-team/chatbot_api) |
| [Emotext](https://github.com/cdfmlr/emotext)                 | 中文文本情感分析                                             | [cdfmlr/murecom-verse-1](https://github.com/cdfmlr/murecom-verse-1) |
| [muvtuberdriver](https://github.com/cdfmlr/muvtuberdriver)   | 组装各模块，驱动整个流程                                     | -                                                            |
| [muvtuber-proto](https://github.com/cdfmlr/muvtuber-proto)   | proto 定义                                                   |                                                              |

## 起步

0. 开发环境：

```sh
$ uname -mrs
Darwin 22.3.0 x86_64
# 目前 TTS 模块还依赖于 macOS，其他系统可能不行。
$ go version  
go version go1.19.6 darwin/amd64
$ python3 --version
Python 3.10.9
$ poetry --version
Poetry (version 1.3.2)
$ node --version
v19.4.0
$ pnpm --version
7.26.0
```

1. [xfgryujk/blivechat](https://github.com/xfgryujk/blivechat)

```sh
# clone repo
git clone --recursive https://github.com/xfgryujk/blivechat.git
cd blivechat

# 编译前端
cd frontend
npm install
npm run build
cd ..

# 运行服务
pip3 install -r requirements.txt
python3 main.py
```

2. [Emotext](https://github.com/cdfmlr/emotext)

```sh
git clone https://github.com/cdfmlr/emotext.git
cd emotext

poetry install
poetry run python emotext/httpapi.py --port 9003
# emotext server: http://localhost:9003
```

3. [ChatGPTChatbot](https://github.com/cdfmlr/chatgpt_chatbot)

```sh
git clone https://github.com/cdfmlr/chatgpt_chatbot.git
cd chatgpt_chatbot

poetry install
poetry run python chatgpt
# ChatGPTChatbot gRPC server: localhost:50052
```

4. [MusharingChatbot](https://github.com/cdfmlr/musharing_chatbot)

```sh
git clone https://github.com/cdfmlr/musharing_chatbot.git
cd musharing_chatbot

poetry install
poetry run python -m spacy download en_core_web_sm  # 一个执行不到的依赖，但是不装跑不起来。
PYTHONPATH=$PYTHONPATH:. poetry run python musharing_chatbot
# MusharingChatbot gRPC server: localhost:50051
```


5. [Live2dDriver](https://github.com/cdfmlr/live2ddriver)

```sh
git clone https://github.com/cdfmlr/live2ddriver.git
cd live2ddriver

go run . -shizuku localhost:9004 -verbose
# live2d shizuku driver: localhost:9004
# websocket message forwarder: localhost:9001 # 前端会连这个
```

6. [Live2dView](https://github.com/cdfmlr/live2dview)

```sh
git clone https://github.com/cdfmlr/live2dview.git
cd live2dview

pnpm install
pnpm exec quasar dev
# 浏览器访问: 调试(戏)页: http://localhost:9000/#/debug
# 生产环境: OBS 添加浏览器源: http://localhost:9000/
```

7. [muvtuberdriver](https://github.com/cdfmlr/muvtuberdriver)

```sh
git https://github.com/cdfmlr/muvtuberdriver.git
cd muvtuberdriver

go run . -chatgpt_access_token='eyJ***99A' -chatgpt_prompt="请扮演一个正在直播的 vtuber，之后我的输入均为用户评论，用简短的一句话回答它们" -roomid 000000 -reduce_duration=2s
# chatgpt_access_token: 浏览器访问https://chat.openai.com/api/auth/session获取
# roomid 你的 b 站直播间 id，https://live.bilibili.com/000000?... 中的000000
```

8. OBS

```sh
brew install obs
# 或：https://obsproject.com

# 启动 OBS，设置：
# - blivechat 的弹幕框：localhost:12450/...
# - Live2DView：localhost:9000
# - 音频（say）的输出：你使用的音频设备
# 【开始直播】
```

## TODO

- [ ] 文档：各项目的 README、文档
- [ ] Topic：直播话题：一起看，打游戏，互动游戏，……
- [ ] murecom for muvtuber：基于心情的 BGM
- [ ] Live2D View & Driver：焦点控制、像官方的 Viewer 那样丰富的任意动作、表情控制（离散 -> 连续）
- [ ] Chatbot：
  - [ ] ChatGPT 平替
  - [x] ChatGPT 多用户轮流访问：提高可用性
  - [ ] MusharingChatbot（ChatterBot）重新训练
- [ ] Sayer（TTS）：不依赖于 macOS 的平替
- [ ] 工程化：
  - [ ] 全部内部接口 => gRPC
  - [ ] 散装微服务 => 容器编排
- [ ] 一个 muvtuber 出道介绍视频：匿名 m
- [ ] Filter：优先 + 排队，不要直接扔，存着，词穷的时候别冷场
- [ ] ……

## 开放源代码

所有下属项目除非特别说明，一律在 MIT 协议下开放源代码。

欢迎任何有关 Issue 问题、PR 贡献以及讨论。

（以上说明仅限于本人维护的项目，如 [muvtuberdriver](https://github.com/cdfmlr/muvtuberdriver)；不包括[xfgryujk/blivechat](https://github.com/xfgryujk/blivechat)、[OBS](https://obsproject.com) 等。）









