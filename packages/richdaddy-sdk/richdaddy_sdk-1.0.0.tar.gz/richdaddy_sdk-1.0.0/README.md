# RichDaddy_SDK для Python 3.7+
**RichDaddy_SDK для Python3.7 +** простая реализация методов API RichDaddy

[Документация RichDaddy API](https://vk.com/@richda-bogatyi-papa-api)

### Установка

```js
$ pip install richdaddy_sdk
```
или 
```js
$ pip install https://github.com/old-pinky/RichDaddy_SDK/archive/refs/heads/main.zip
```


### Пример использования (Асинхронная версия)

```python
from richdaddy_sdk.aiorichdaddy import AsyncRichDaddy
import asyncio

ard = AsyncRichDaddy(access_token='access_token')
ardApi = ard.getApi()


async def main():
    usersget = await ardApi.usersGet(userIds=['6105969c6f40ac82f08ef4a1'], userVkIds=[446645455]) #Необязательно указывать сразу 2 метода userIds и userVkIds
    print(usersget)

    pay = await ardApi.transfersCreate(id='6105969c6f40ac82f08ef4a1', dialog=True, title='Hello!', label='My name is Vladimir Putin', amount=1000)
    print(pay)
    
    trans_get = await ardApi.transfersGet()
    print(trans_get)

asyncio.run(main())
```

### Пример использования (Синхронная версия)

```python
from richdaddy_sdk.syncrichdaddy import RichDaddy

rd = RichDaddy(access_token='access_token')
rdApi = rd.getApi()

usersget = rdApi.usersGet(userIds=['6105969c6f40ac82f08ef4a1'], userVkIds=[446645455]) #Необязательно указывать сразу 2 метода userIds и userVkIds
print(usersget)

pay = rdApi.transfersCreate(id='6105969c6f40ac82f08ef4a1', dialog=True, title='Hello!', label='My name is Vladimir Putin', amount=1000)
print(pay)

trans_get = rdApi.transfersGet()
print(trans_get)
```