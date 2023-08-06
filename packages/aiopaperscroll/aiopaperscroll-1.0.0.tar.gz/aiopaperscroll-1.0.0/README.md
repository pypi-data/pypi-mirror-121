# AioPaperScroll SDK для Python3.8+
**AioPaperScroll SDK для Python3.8+** простая и асинхронная реализация методов API PaperScroll

[Документация PaperScroll API](https://paperscroll.docs.apiary.io)

### Установка

```js
$ pip install https://github.com/old-pinky/AioPaperScroll-SDK/archive/refs/heads/main.zip
```

### Пример использования

```python
from aiopaperscroll import AsyncPaperScroll
import asyncio

paperClient = AsyncPaperScroll(access_token='access_token', merchant_id)
paperApi = paperClient.getApi()

async def main():
    someMerchants = await paperApi.getMerchants()
    print(someMerchants)

asyncio.run(main())
```