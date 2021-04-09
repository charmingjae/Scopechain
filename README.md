# CCTV scope
> 2021 - 1학기  

<br/>

## 👨🏻‍💻 Overview  
중앙화 된 데이터베이스나 서버에 CCTV 영상을 저장하면 유실될 가능성이 크다.  
따라서 분산저장 방법을 채택하는 블록체인에 일정한 주기별로 CCTV의 스냅샷을 저장해  
학부모나 관리자로 하여금 원할 때 이 스냅샷을 받아볼 수 있게끔 하기 위해서 본 프로젝트를 진행하였다.  

<br/>

## 🔧 Tech

BE :
```

Python3 ( Python 3.8.3 )

```

Server : 
```

Flask 1.1.2

```

Message :
```

Telegram

```

<br/>


## 🏃‍♂️ Getting Started

~~~bash

python3 app.py

~~~  

<br/> 


## 📖 Comment  

> Need 'Telegram bot' Access Token and link point  

본 프로젝트에서는 Python3로 작성 된 블록체인에 저장 되어 있는 이미지 객체를 텔레그램으로 전송합니다.  
전송 방법은 Telegram에서 제공하는 [Bot API](https://core.telegram.org/bots)를 사용해서 전송하기 때문에, 개별적인 [Access Token](https://gabrielkim.tistory.com/entry/Telegram-Bot-Token-%EB%B0%8F-Chat-Id-%EC%96%BB%EA%B8%B0)과 백앤드와 Telegram을 연결하는 파일(Link point)가 필요합니다.  

<br/>

> Syntax


1. import telegram and set Bot auth
~~~python

import telegram
bot = telegram.Bot(token='your token')
token = 'your token'
chat_id = your chat_id

~~~


2. How to send img

~~~python

from io import BytesIO
from PIL import Image

# Load encoded file using pickle module
convtImg = pickle.loads(base64.b64decode(convImg))
converted_img = Image.fromarray(convtImg, 'RGB')

# Save img object into created BytesIO container
bio = BytesIO()
bio.name = str(uuid.uuid4())
converted_img.save(bio, 'JPEG')
bio.seek(0)

# Send Bytes object to telegram
bot.sendPhoto(chat_id=chat_id, photo=bio)

~~~