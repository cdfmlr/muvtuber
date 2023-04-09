# muvtuber

Makes your AI vtuber.

> 让 AI 成为虚拟主播：看懂弹幕，妙语连珠，悲欢形于色，以一种简单的实现

![obs](attachments/obs.png)

- 不定期的测试直播：http://live.bilibili.com/26949229
- QQ 交流群：569686683
- 介绍文章：[知乎 - 写个AI虚拟主播：看懂弹幕，妙语连珠，悲欢形于色，以一种简单的实现](https://zhuanlan.zhihu.com/p/609878670)

## 项目构成

![muvtuber-impl](attachments/muvtuber-impl.png)



| 服务                                                         | 说明                                                         | 基于                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [blivechat](https://github.com/cdfmlr/blivechat/tree/muvtuber) | 获取直播间弹幕消息。                                         | [xfgryujk/blivechat](https://github.com/xfgryujk/blivechat) 做的非常好，直接用了，没有额外封装。 |
| [Live2dView](https://github.com/cdfmlr/live2dview)           | 前端：显示 [Live2D](https://www.live2d.com/en/) 模型         | [guansss/pixi-live2d-display](https://github.com/guansss/pixi-live2d-display) |
| [Live2dDriver](https://github.com/cdfmlr/live2ddriver)       | 驱动前端 Live2D 模型动作表情                                 | -                                                            |
| [ChatGPTChatbot](https://github.com/cdfmlr/chatgpt_chatbot)  | 基于 [ChatGPT](https://chat.openai.com) 的优质聊天机器人     | [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT)    |
| [MusharingChatbot](https://github.com/cdfmlr/musharing_chatbot) | 基于 [ChatterBot](https://github.com/gunthercox/ChatterBot) 的简单聊天机 | [RaSan147/ChatterBot_update](https://github.com/RaSan147/ChatterBot_update) <br/> [musharing-team/chatbot_api](https://github.com/musharing-team/chatbot_api) |
| [Emotext](https://github.com/cdfmlr/emotext)                 | 中文文本情感分析                                             | [cdfmlr/murecom-verse-1](https://github.com/cdfmlr/murecom-verse-1) |
| [externalsayer](https://github.com/cdfmlr/externalsayer)     | 调用公开的 API （external API）进行 TTS 文本语音合成。       | [Azure: TTS](https://azure.microsoft.com/zh-cn/products/cognitive-services/text-to-speech/) |
| [audioview](https://github.com/cdfmlr/audioview)             | 基于 Web 的音频播放。用于从 docker 中输出音频到 OBS          | -                                                            |
| [muvtuberdriver](https://github.com/cdfmlr/muvtuberdriver)   | 组装各模块，驱动整个流程                                     | -                                                            |
| [muvtuber-proto](https://github.com/cdfmlr/muvtuber-proto)   | proto 定义                                                   |                                                              |

## 快速开始

v0.3.0 版本已实现了完全 Docker 化，所以应该支持任意常用操作系统了。现在只需要几个命令即可启动整个项目：

0. 安装 Docker 以及 Docker Compose。

1. 拉取代码：

```sh
# 拉取代码
git clone --recursive https://github.com/cdfmlr/muvtuber.git
cd muvtuber
```

2. 修改配置：

```sh
vim docker-compose.yml
# 按照你的实际情况修改 HTTP_PROXY、HTTPS_PROXY 的值
# 如果不需要，直接删掉就行。

vim configs/externalsayer/config.yaml
# 配置 TTS 文本语音合成: 
# 配置 azure 语音合成服务的 key、region 和 role (SSML 模板)

vim configs/muvtuberdriver/config.yaml
# 主程序的配置:
# 你的房间号（roomid）、ChatGPT 的 apiKey 以及 initialprompt.
# 各种 server 的地址都不用改，已经配合 docker-compose.yml 设好了.
```

3. 启动服务：

```sh
# 启动各种服务
# 首次运行需要 build 各种镜像，耗时较长，并且请确保网络能够访问 Docker Hub、GitHub （我已尽量写了使用国内源，但不保没有遗漏）
# 之后我可能会把打包好的镜像上传，到时候直接 pull 就行了。
docker compose up -d
# docker compose ps       # 查看服务状态
# docker compose logs -f  # 查看日志（Ctrl+C 停止）
```

**已知问题**：运行完 `docker compose up -d` 然后 `docker compose ps -a` 或者看日志*可能*发现，muvtuberdriver 错误退出了。这是个 bug，详见 [#27](https://github.com/cdfmlr/muvtuber/issues/27)。要根治这个问题需要完成一个历史遗留的重构。但因为现在进入 v0.3.1 的 freeze 了，所以留在 v0.3.2 解决这个问题。。总之现在手动重启一下这个服务即可：

```sh
docker compose restart muvtuberdriver
```

4. 配置 OBS，开始直播：（下面三个都是新建浏览器源）
   - 主播 Live2DView：`http://localhost:51070/#/?driver=ws://localhost:51071/live2d`
   - 语音 AudioView：`http://127.0.0.1:51082/?controller=ws://127.0.0.1:51081/`
   - 弹幕 Blivechat：先用浏览器打开 http://localhost:12450，按需配置，然后复制粘贴链接和样式。

## OBS 配置详解

给新手的 OBS 配置详解：

- 虚拟形象（Live2DView）：来源 > `+` > 浏览器 > 新建 > URL: http://localhost:9000/#/
  - 注意把「通过 OBS 控制音频」勾上哦，然后把那条声音关掉，不然有机会听到可爱捏鬼畜日语。
- 弹幕框（blivechat）：来源 > `+` > 浏览器 > 新建 > URL: 
  - 先用浏览器打开 http://localhost:12450
  - 首页 > 房间号：设置为你的房间号 > 进入房间
  - 弹出的窗口 -> 拷贝地址
  - 粘贴到 OBS 的 URL
- 主播说话的音频（audioview）：
  - 来源 > `+` > 浏览器 > 新建 > URL
  - 填入 `http://127.0.0.1:51082/?controller=ws://127.0.0.1:51081/`
  - 建议把「通过 OBS 控制音频」勾上，方便按需调节音量。
- 其他音频（BGM）：来源 > `+` >音频输入采集 > 新建 > 设备：BlackHole 2ch
  - 要先安装一个虚拟声卡，这里以 mac 系统使用 [BlackHole](https://github.com/ExistentialAudio/BlackHole) 为例。
  - 在开始直播前，控制中心 > 声音> 右边 AirPlay 图标 > 选 BlackHole。
  - 然后电脑输出的声音就会 -> BlackHole -> OBS。
- B 站推流：设置（Preferences）> 直播 > 服务：选 `Bilibili Live ...`，推流码填「B 站首页 > 头像 > 推荐服务 > 直播中心 > 左侧“我的直播间”> 填好直播分类、房间标题 > 开始直播，然后会显示的串流密钥」

## 配置开发环境

目前仍不支持用 docker 作为开发环境。需要在本地开发，然后 docker 构建部署。

 -1. 本地开发环境：

```sh
$ uname -mrs
Darwin 22.3.0 arm64
# 目前 TTS 模块还依赖于 macOS，其他系统可能不行。
$ go version  
go version go1.20.1 darwin/arm64
$ python3 --version
Python 3.9.16  # blivechat
Python 3.10.10 # others
$ poetry --version
Poetry (version 1.4.0)
$ node --version
v18.14.2
$ pyenv --version
pyenv 2.3.14
$ pnpm --version
7.29.0
```

Node.js 和 Python 的包管理配置：

```sh
# 前端统一使用 pnpm (珍爱硬盘，远离 npm)
pnpm config set auto-install-peers true -g
# python统一使用 pyenv + poetry
poetry config virtualenvs.prefer-active-python true
poetry config virtualenvs.in-project true  # 只是个人的保守偏好
```

0. 现在可用 git submodule 一次性拉取整个项目，无需手动 clone 各个模块了:

```sh
git clone --recursive https://github.com/cdfmlr/muvtuber.git
```

接下来编译运行各个模块，可以预先开 7 个终端页，然后：

1. [blivechat](https://github.com/cdfmlr/blivechat/tree/muvtuber)

```sh
cd blivechat

# 编译前端
cd frontend
pnpm install
pnpm run build
cd ..

# 运行服务
pyenv local 3.9.16
poetry install
poetry run python main.py
# 服务运行在 http://localhost:12450，会自动在默认浏览器打开
```

2. [Emotext](https://github.com/cdfmlr/emotext)

```sh
cd emotext

pyenv local 3.10.10
poetry install
poetry run python emotext/httpapi.py --port 9003
# emotext server: http://localhost:9003
```

3. [ChatGPTChatbot](https://github.com/cdfmlr/chatgpt_chatbot)

```sh
cd chatgpt_chatbot

pyenv local 3.10.10
poetry install
poetry run python chatgpt
# ChatGPTChatbot gRPC server: localhost:50052
```

4. [MusharingChatbot](https://github.com/cdfmlr/musharing_chatbot)

```sh
cd musharing_chatbot

pyenv local 3.10.10
poetry install
poetry run python -m spacy download en_core_web_sm  # 一个执行不到的依赖，但是不装跑不起来。
PYTHONPATH=$PYTHONPATH:. poetry run python musharing_chatbot
# MusharingChatbot gRPC server: localhost:50051
```


5. [Live2dDriver](https://github.com/cdfmlr/live2ddriver)

```sh
#git clone https://github.com/cdfmlr/live2ddriver.git
cd live2ddriver

go run . -shizuku localhost:9004 -verbose
# live2d shizuku driver: localhost:9004
# websocket message forwarder: localhost:9001 # 前端会连这个

# 不开发该模块也可以 build 出来再运行
```

6. [Live2dView](https://github.com/cdfmlr/live2dview)

```sh
#git clone https://github.com/cdfmlr/live2dview.git
cd live2dview

pnpm install
pnpm exec quasar dev
# 浏览器访问: 调试(戏)页: http://localhost:9000/#/debug
# 生产环境: OBS 添加浏览器源: http://localhost:9000/

# 如果不开发这个模块可以 build & serve:
pnpm exec quasar build
httpstatic -d dist/spa/ -l :9000  # 你的某种静态网页服务工具，如 python -m http.server，如果开发环境最好有宽松的 CROS。这里用的是 https://github.com/cdfmlr/tools/#httpstatic
```

7. [audioview]()

```sh
cd audioview

pnpm install
pnpm run dev
# pnpm run build
```

8. [externalsayer](https://github.com/cdfmlr/externalsayer)

```sh
cd externalsayer

go run . -h
```

9. [muvtuberdriver](https://github.com/cdfmlr/muvtuberdriver)

muvtuberdriver 必须在前面所有服务正确启动后才能启动，否则会 panic 退出。

```sh
#git clone https://github.com/cdfmlr/muvtuberdriver.git
cd muvtuberdriver

go run . -c config.yaml
# chatgpt_access_token: 浏览器访问https://chat.openai.com/api/auth/session获取
# roomid 你的 b 站直播间 id，https://live.bilibili.com/000000?... 中的000000

# 不开发该模块也可以 build 出来再运行
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

## 部署

> 使用前文的 docker compose 方式部署。不再提供散装微服务的部署文档了。

## FAQ

我（个人/商业/以及任意情况）可以使用这个项目嘛？

- 可以。在 MIT 协议下开放源代码，没有任何限制。
  - Permissions：✅ Commercial use ✅ Modification ✅ Distribution ✅ Private use
  - Limitations：❌ Liability ❌ Warranty

在 Microsoft Windows 系统中可以运行嘛？

- 可以。v0.3.0 完成了完全 Docker 化，只要宿主机能装 docker 就行：所有服务都跑在容器中，所有客户端都是浏览器（可以嵌入 OBS）。

作者寻求合作嘛？

- TL;DR：可白嫖，不合作（你给我钱，我给你代码），欢迎贡献（你无条件给我/这个项目钱/代码）
- 你想用我的实现：请直接使用，直接白嫖，不用找我谈钱，我不需要。这是个在 MIT 协议下的开源项目。你可以自由、免费使用我已有的实现，以及未来的任何更新。
- 你想要我实现某种功能：请于 issue 里提出，大家一起讨论、实现。时间精力有限，我不保证能实现，如果你有能力实现，欢迎贡献代码。
- 你给我钱做某种商用产品（包括但不限于去某平台直播、做广告or带货数字人）：请参考上面两种情况。我不缺钱，我只缺时间。
- 你要无条件给我钱：如果你想赞助，我非常欢迎。
- 你要一起写代码：非常欢迎，请于 issue 里自行承包 TODO 或者提出想法。请务必不要被项目复杂度吓到，单独每个模块不难的，我也会尽力帮助你的。

为何如此复杂？|| 这个项目的意义是什么？

- 我自己都觉得复杂。但这是刻意为之的，用来自己的走出舒适区。这是个学习项目，为磨练技术而生。她充满了探索，而没有明确的目标。它不是用来赚钱的工具，亦不是用来娱乐的玩具。
- 在**机器学习**方面：用来学习包括但不限于 AIGC 等技术（实用技术，从模型到服务的，真正有用的，不是只能躺在 Jupiter Notebook 里的 demo）虽然现在都是调 API，但我也有在研究自己做模型......
- 在**云计算**方面：用来学习散装微服务 -> Docker -> Docker Compose -> Kubernetes 的云化流程，以及探索 Serverless、FaaS 等技术......
- 在软件工程（**开发**）方面：用来学习这种一大堆乱七八遭的东西如何组合、重构，使之更协调、更优雅地工作。而且这个甚至不是个正常的 web 项目，我对这种工程如何实现一无所知......
- 在软件工程（**管理**）方面：这一大堆东西在高层次如何协调、推进：哪怕只有一个人开发，现在它的复杂度也已经到了需要去管理了。父、子模块、容器以及依赖的版本规划；想法 -> TODO -> 实现 的规划......
- 以及我一个人如何在有限的时间内兼顾学习（📖）、工作（💰）、爱好（💻）、生活（🎮🎸📷🎬🎧...）以及多个（复杂）项目：时间、精力、知识如何管理？我需要更加**高效**。我已被逼上 GTD，Zettelkasten 也已经写入了 inbox。 
- 为达成这些目标，需要相当长的时间来推进这个项目。

## TODO

- [ ] 文档：各项目的 README、文档
- [ ] Topic：直播话题：一起看，打游戏，互动游戏，……
- [ ] murecom for muvtuber：基于心情的 BGM
- [ ] Live2D View & Driver：焦点控制、像官方的 Viewer 那样丰富的任意动作、表情控制（离散 -> 连续）
- [ ] Chatbot：
  - [ ] ChatGPT 平替
  - [x] ~~ChatGPT 多用户轮流访问：提高可用性~~ 换成 API 了。
  - [x] ~~MusharingChatbot（ChatterBot）重新训练~~ 计划用 T5 替换基础模型。
- [x] Sayer（TTS）：不依赖于 macOS 的平替
- [ ] 工程化：
  - [ ] 全部内部接口 => gRPC （已部分实现）
  - [ ] 散装微服务 => 容器编排 （已部分实现）
- [ ] 一个 muvtuber 出道介绍视频：匿名 m
- [ ] Filter：优先 + 排队，不要直接扔，存着，词穷的时候别冷场
- [ ] ……

## 开放源代码

所有下属项目除非特别说明，一律在 MIT 协议下开放源代码。

欢迎任何有关 Issue 问题、PR 贡献以及讨论。









