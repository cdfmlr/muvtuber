(translation in progress)

# muvtuber

[中文文档](README.md)

Makes your AI vtuber.

> Make AI a virtual anchor: understand the barrage, witty words, sorrow and joy, in a simple implementation.

![obs](attachments/obs.png)

- Test live: http://live.bilibili.com/26949229
- QQ exchange group: 569686683
- Introductory article: [Zhihu - Write an AI virtual anchor: understand the barrage, witty words, sorrow and joy, in a simple implementation](https://zhuanlan.zhihu.com/p/609878670)
- We're currently developing this project for the Chinese Bilibili platform. We're still working on integrating it with YouTube, Twitch, and other platforms. Stay tuned for updates, and we welcome your contributions.

[TOC]

## Project composition

![muvtuber-impl](attachments/muvtuber-impl.png)



| Module                                                         | Description                                                         | Based on                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [blivechat](https://github.com/cdfmlr/blivechat/tree/muvtuber) | Get messages in the live room                                       | [xfgryujk/blivechat](https://github.com/xfgryujk/blivechat) |
| [Live2dView](https://github.com/cdfmlr/live2dview)           | Frontend: Displays the [Live2D] (https://www.live2d.com/en/) model       | [guansss/pixi-live2d-display](https://github.com/guansss/pixi-live2d-display) |
| [Live2dDriver](https://github.com/cdfmlr/live2ddriver)       |  Drive front-end Live2D model and action expressions                                        | -                                                            |
| [ChatGPTChatbot](https://github.com/cdfmlr/chatgpt_chatbot)  | A chatbot based on [ChatGPT] (https://chat.openai.com).  | [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT)    |
| [MusharingChatbot](https://github.com/cdfmlr/musharing_chatbot) | A simple chatter based on [ChatterBot] (https://github.com/gunthercox/ChatterBot). | [RaSan147/ChatterBot_update](https://github.com/RaSan147/ChatterBot_update) <br/> [musharing-team/chatbot_api](https://github.com/musharing-team/chatbot_api) |
| [Emotext](https://github.com/murchinroom/emotext)            | Chinese Text sentiment analysis                            | [cdfmlr/murecom-verse-1](https://github.com/cdfmlr/murecom-verse-1) |
| [externalsayer](https://github.com/cdfmlr/externalsayer)     | Call the EXPOSED API (external API) for TTS text-to-speech.       | [Azure: TTS](https://azure.microsoft.com/zh-cn/products/cognitive-services/text-to-speech/) |
| [audioview](https://github.com/cdfmlr/audioview)             | Web-based audio playback. Used to output audio from docker to OBS   | -                                                            |
| [muvtuberdriver](https://github.com/cdfmlr/muvtuberdriver)   | Assemble the modules to drive the entire process                    | -                                                            |

Module not in use：

| Module | Description |
| ---- | ---- |
| [muvtuber-proto](https://github.com/cdfmlr/muvtuber-proto)   | proto definition                             |
| [sayerapigo](https://github.com/murchinroom/sayerapigo) |  Go language's Sayer (TTS) interface server + client framework |
| [chatbotapipy](https://github.com/murchinroom/chatbotapipy) | A server-side framework for the Chatbot API for the Python language    |


## Quick Start

Version v0.3.0 is fully Dockerized, so any common operating system should be supported. Now it only takes a few commands to start the entire project:

0. Install Docker and Docker Compose.

1. Pull the code:

```sh
# Pull code
git clone --recursive https://github.com/cdfmlr/muvtuber.git
cd muvtuber
```

⚠️ Since git submodules are used, be sure to pull recursively. You cannot download zip, or clone without the '--recursive' parameter.

🚧 The default main branch is the latest version in development and is not guaranteed to run. Please use the tag version: [click here] (https://github.com/cdfmlr/muvtuber/tags).

2. Modify the configuration: (see [Configuration Details] (#configurationdetils)) for details)

```sh
vim docker-compose.yml
# Modify the values of HTTP_PROXY and HTTPS_PROXY according to your actual situation
# If you don't need it, just delete it.

vim configs/externalsayer/config.yaml
# Configure TTS text-to-speech: 
# Configure the key, region, and role (SSML template) of the Azure Speech Synthesis Service

vim configs/muvtuberdriver/config.yaml
# Configuration of the main program:
# Your roomID, ChatGPT's apiKey, and initialprompt.
# The addresses of various servers do not need to be changed, and they have been set up with docker-compose.yml.
```

3. Start the service:

```sh
docker compose up -d # automatically download or build and start various services

# docker compose ps # View service status
# docker compose logs -f # View logs (Ctrl+C stop)
```

- You can pull images 🎉 directly from Docker Hub
    - In v0.3.5, CI mechanism added. All Docker images are automatically built by GitHub Actions and pushed to Docker Hub ([murchinroom/xxx](https://hub.docker.com/u/murchinroom)).
    - There are many mirrors, please keep the network open. Testing under poor network conditions (campus network directly connected to Docker Hub) requires about 252.4s to pull all images.
- You can also build various images locally:
    - Make sure your network environment has access to Docker Hub and GitHub.
    - In Chinese mainland or other areas where the network environment is restricted, please use 'Dockerfile'. Other regions recommend 'gh. Dockerfile`。
- Make sure you have at least 1 GB of free hard disk space.
- If you encounter problems, you can take a look at [Troubleshooting] (#Troubleshooting).

4. Configure OBS to start live streaming: (The following three are all new browser sources)
   - Streamer Live2DView:'http://localhost:51070/#/?driver=ws://localhost:51071/live2d'
   - Voice AudioView:'http://127.0.0.1:51082/?controller=ws://127.0.0.1:51081/'
   - Barrage Blivechat: Open the http://localhost:51060 with a browser, configure it as needed, and then copy and paste the link and style.

## Configuration details

### Network environment configuration

If your network environment is not good and it is difficult to connect directly to GitHub and ChatGPT, you need to do some proxy configuration.

> Preconditions: You have a magic item that can make the network better (industry black talk: proxies).

In your proxy settings (which may be hidden deeper, such as in advanced settings), you can find a value like "native http listening port" and fill this port in:

- 'musharing_chatbot/Dockerfile':

```dockerfile
  HTTPS_PROXY=http://host.docker.internal:1000
  ```

Replace '1000'

- 'docker-compose.yml':

```yaml
    chatgpt_chatbot:
      ...
      environment:
        - HTTP_PROXY=http://host.docker.internal:1000
        - HTTPS_PROXY=http://host.docker.internal:1000
  ```

Replace '1000'

(Of course, you can also reverse and change the port of the agent software to 1000 haha, but it is not recommended, I am afraid that there will be conflicts, or cause you other problems)

### externalsayer configuration details

Here> The TTS service that uses free, high-quality Azure is configured here. (This is also currently only supported.) ）
> Introduction of the service: 
> https://azure.microsoft.com/zh-cn/products/cognitive-services/text-to-speech/

The configuration of this block is in 'configs/externalsayer/config.yaml':

```yaml
SrvAddr: "localhost:50010"
EnabledSayer: "azure"
AzureSayer:
  SpeechKey: "your-key"
  SpeechRegion: "eastus"
  FormatMicrosoft: "audio-16khz-32kbitrate-mono-mp3"
  FormatMimeSubtype: "mp3"
  Roles:
    "default": '<speak version="1.0" xml:lang="zh-CN"><voice name="zh-CN-XiaoxiaoNeural">{{.}}</voice> </speak>'
```

You need to change: SpeechKey, SpeechRegion, and Roles.

- SpeechKey, SpeechRegion: The key and region of the TTS service that you apply for on Azure.
   - For the specific application process, please refer to the document: [Quick Start: Convert text to speech] (https://learn.microsoft.com/zh-CN/azure/cognitive-services/speech-service/get-started-text-to-speech)
- Roles: '<voice name='xx-XX-Xxx'>' The name here should be filled with voice, i.e. the name of the "voice person". The specific list can be obtained with the following command:

```sh
curl https://eastus.tts.speech.microsoft.com/cognitiveservices/voices/list --header 'Ocp-Apim-Subscription-Key: xxx'
```

I formatted the result of the request into this file for easy finding: ['externalsayer/azuresayer/voices.']
/voices-list.json`](https://github.com/cdfmlr/externalsayer/blob/23e32a07de224d6ac19cf3aee0575a3e81e9836a/azuresayer/voices/voices-list.json)。

You can audition and select the sound in "[Speech Studio] (https://aka.ms/speechstudio/voicegallery)" on the website. Then find the ''ShortName": "xx-XX-XXXX"" in the file and fill in the '<voice name="xx-XX-XXXX" > `。

🌟 A more recommended way is to write something casually in "[Speech Studio] (https://aka.ms/speechstudio/voicegallery)", select the voice to make it speak, fine-tune the parameters, and when you are satisfied, export the SSML and replace the content with '{{.}} Remove the line breaks (I wrote a script to help do this, [can be found here] (https://github.com/cdfmlr/externalsayer/tree/23e32a07de224d6ac19cf3aee0575a3e81e9836a/azuresayer/voices)) and write it into the configuration.

### OBS configuration in detail

Detailed explanation of OBS configuration for newbies:

- Avatar (Live2DView): Source > '+' > Browser > New > URL: http://localhost:9000/#/
  - Be careful to tick "Control audio via OBS" and turn off the sound, otherwise you may hear the cute pinching ghost animal Japanese.
- blivechat: Source > '+' > browser > New > URL: 
  - Open the http://localhost:12450 with a browser first
  - Home > Room Number: Set your room number > to enter the room
  - Pop-up window -> Copy address
  - Paste the URL into OBS
- Audio view of the host's speech:
  - Source > '+' > browser > New > URL
  - Fill in 'http://127.0.0.1:51082/?controller=ws://127.0.0.1:51081/'
  - It is recommended to check "Control audio via OBS" to adjust the volume as needed.
- Other Audio (BGM): Source > '+' >Audio Input Acquisition > New > Device: BlackHole 2ch
  - To install a virtual sound card first, here is the use of [BlackHole] (https://github.com/ExistentialAudio/BlackHole) for a Mac system.
  - Before starting the live stream, select BlackHole > the AirPlay icon on the right of the sound > > Control Center.
  - Then the sound output by the computer will > BlackHole -> OBS.
- B station push: Preferences> Live > Service: Select 'Bilibili Live ...', fill in the push code with "B site home page > avatar > Recommended service > Live broadcast center > "My Live Room" on the left> Fill in the live broadcast category, room title > Start live streaming, and then the streaming key will be displayed."

## Troubleshooting 

### 💥 docker compose up ProxyError when building musharing_chatbot images

If a ProxyError occurs, or:

- Cannot connect to proxy.
- Name or service not known.

You need to modify the proxy settings in 'musharing_chatbot/Dockerfile'.

```docker
# TODO: modify port 1000 to your own port to your local proxy
RUN	HTTPS_PROXY=http://host.docker.internal:1000 poetry run python -m spacy download en_core_web_sm
```

This thing must access GitHub, and if your network environment does not allow direct access to GitHub, you can use a proxy. If you have direct access to GitHub (you can also count it with side-route), you can remove 'HTTPS_PROXY=http://host.docker.internal:1000'.

### 💥 After booting chatgpt_chatbot keeps experiencing network issues

View the logs and discover:

```
...
muvtuber-chatgpt_chatbot-1    |     raise ProxyError(e, request=request)
muvtuber-chatgpt_chatbot-1    | requests.exceptions.ProxyError: HTTPSConnectionPool(host='openaipublic.blob.core.windows.net', port=443): Max retries exceeded with url: /encodings/cl100k_base.tiktoken ( Caused by ProxyError('Cannot connect to proxy.', NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f968bfdbac0> : Failed to establish a new connection: [Errno -2] Name or service not known')))
```

The proxy configuration needs to be modified in 'docker-compose.yml':

```yaml
  chatgpt_chatbot:
    ...
    environment:
      - HTTP_PROXY=http://host.docker.internal:10809
      - HTTPS_PROXY=http://host.docker.internal:10809
```

If your network environment does not allow direct access to OpenAI's APIs, you can use a proxy. If you can access ChatGPT directly (you can also use side-route), you need to delete the two-line configuration.

If you still have the 'Name or service not known' error after configuration, you can try to write the IP of the host (that is, the local IPv4 address under the host Ethernet) through the 'settings-resources-proxies' of Docker Desktop. (Thanks to [@RAINighty](https://github.com/RAINighty) for the solution, see discussion in https://github.com/cdfmlr/muvtuber/issues/30)

## Configure the development environment

Docker is still not supported as a development environment. You need to develop locally, and then docker builds the deployment.

-1. Local development environment:

```sh
$ uname -mrs
Darwin 22.3.0 arm64
# At present, the TTS module still depends on macOS, other systems may not work.
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

Package management configuration for Node.js and Python:

```sh
# Unified use of PNPM on the front end (cherish hard disks, away from npm)
pnpm config set auto-install-peers true -g
# Python uses pyenv + poetry in unison
poetry config virtualenvs.prefer-active-python true
Poetry config virtualenvs.in-project true # is just a personal conservative preference
```

0. You can now use git submodule to pull the entire project at once, without manually clone modules:

```sh
git clone --recursive https://github.com/cdfmlr/muvtuber.git
```

Next, compile and run each module, you can open 7 terminal pages in advance, and then:

1. [blivechat](https://github.com/cdfmlr/blivechat/tree/muvtuber)

```sh
cd blivechat

# Compile the frontend
cd frontend
pnpm install
pnpm run build
cd ..

# Run the service
pyenv local 3.9.16
poetry install
poetry run python main.py
# The service runs on http://localhost:12450 and automatically opens in the default browser
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
Poetry run python -m spacy download en_core_web_sm # A dependency that cannot be executed, but does not pretend to run.
PYTHONPATH=$PYTHONPATH:. poetry run python musharing_chatbot
# MusharingChatbot gRPC server: localhost:50051
```


5. [Live2dDriver](https://github.com/cdfmlr/live2ddriver)

```sh
#git clone https://github.com/cdfmlr/live2ddriver.git
cd live2ddriver

go run . -shizuku localhost:9004 -verbose
# live2d shizuku driver: localhost:9004
# Websocket Message Forwarder: localhost:9001 # The frontend will connect this

# If you do not develop the module, you can also build it out and run it again
```

6. [Live2dView](https://github.com/cdfmlr/live2dview)

```sh
#git clone https://github.com/cdfmlr/live2dview.git
cd live2dview

pnpm install
pnpm exec quasar dev
# Browser Access: Debug (Play) Page: http://localhost:9000/#/debug
# Production Environment: OBS Add Browser Source: http://localhost:9000/

# If you don't develop this module, you can build & serve:
pnpm exec quasar build
httpstatic -d dist/spa/ -l :9000 # Some of your static web service tools, such as python -m http.server, if the development environment is better to have a relaxed CROS. The https://github.com/cdfmlr/tools/#httpstatic is used here
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

The muvtuberdriver must start correctly after all previous services have started correctly, or it will panic exit.

```sh
#git clone https://github.com/cdfmlr/muvtuberdriver.git
cd muvtuberdriver

go run . -c config.yaml
# chatgpt_access_token: Browser access https://chat.openai.com/api/auth/session get
# roomid Your B station live room ID, https://live.bilibili.com/000000?... 000000 in # If you do not develop the module, you can also build it out and run it again
```

10. OBS

```sh
brew install obs
# or: https://obsproject.com

# Start OBS, set:
# - Blivechat's barrage box: localhost:12450/...
# - Live2DView：localhost:9000
# - Audio (say) output: The audio device you are using
# [Start Live Broadcast]
```

## Deployment

> Deploy using the docker compose method described earlier. Deployment documentation for bulk microservices is no longer available.

## FAQ

**Can I (personal/commercial/and whatever) use this project? **

-OK. Open source under the MIT license without any restrictions.
  - Permissions：✅ Commercial use ✅ Modification ✅ Distribution ✅ Private use
  - Limitations：❌ Liability ❌ Warranty

Does it work on Microsoft Windows? **

-OK. v0.3.0 completes Dockerization, as long as the host can install Docker: all services run in containers, and all clients are browsers (which can embed OBS).

**Is the author looking for cooperation? **

- ✅ You want to write code with me (contribute)
- ✅ You're going to give me money to write what I want to write (donate)
- ❌ You're going to give me money to write what you want (outsourced)
  - I'm sorry, but I have limited time, energy, and ability.


Why is it so complicated?|| What is the significance of this project? **

- Just for fun.

## TODO

- [Issues](https://github.com/cdfmlr/muvtuber/issues)
- [project-muvtuber](https://github.com/users/cdfmlr/projects/3)

## Open source

All affiliated projects are open source under the MIT license unless otherwise stated.

Any issue issues, PR contributions, and discussions are welcome.

