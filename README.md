# CCTV scope
> 2021 - 1νκΈ°  

<br/>

## π¨π»βπ» Overview  
μ€μν λ λ°μ΄ν°λ² μ΄μ€λ μλ²μ CCTV μμμ μ μ₯νλ©΄ μ μ€λ  κ°λ₯μ±μ΄ ν¬λ€.  
λ°λΌμ λΆμ°μ μ₯ λ°©λ²μ μ±ννλ λΈλ‘μ²΄μΈμ μΌμ ν μ£ΌκΈ°λ³λ‘ CCTVμ μ€λμ·μ μ μ₯ν΄  
νλΆλͺ¨λ κ΄λ¦¬μλ‘ νμ¬κΈ μν  λ μ΄ μ€λμ·μ λ°μλ³Ό μ μκ²λ νκΈ° μν΄μ λ³Έ νλ‘μ νΈλ₯Ό μ§ννμλ€.  

<br/>

## π§ Tech

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


## πββοΈ Getting Started

~~~bash

python3 app.py

~~~  

<br/> 


## π Comment  

> Need 'Telegram bot' Access Token and link point  

λ³Έ νλ‘μ νΈμμλ Python3λ‘ μμ± λ λΈλ‘μ²΄μΈμ μ μ₯ λμ΄ μλ μ΄λ―Έμ§ κ°μ²΄λ₯Ό νλ κ·Έλ¨μΌλ‘ μ μ‘ν©λλ€.  
μ μ‘ λ°©λ²μ Telegramμμ μ κ³΅νλ [Bot API](https://core.telegram.org/bots)λ₯Ό μ¬μ©ν΄μ μ μ‘νκΈ° λλ¬Έμ, κ°λ³μ μΈ [Access Token](https://gabrielkim.tistory.com/entry/Telegram-Bot-Token-%EB%B0%8F-Chat-Id-%EC%96%BB%EA%B8%B0)κ³Ό λ°±μ€λμ Telegramμ μ°κ²°νλ νμΌ(Link point)κ° νμν©λλ€.  

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

<br />  

> Methodology

1. Get block filtered by timestamp

~~~python

list(filter(lambda x: x['timestamp'] > time1 and x['timestamp'] < time2, blockchain.chain))

~~~