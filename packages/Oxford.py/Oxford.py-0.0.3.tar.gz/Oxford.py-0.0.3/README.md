### Oxford.py

What is this package for?

This package wrappers Oxford api. Why? The oxford api returns large amount of `dict` which hard to read so we decided to simplify it for the oxforfd api users. This package is open source [CONTRIBUTE HERE](https://github.com/ProjectsWithPython/Oxford.py)


Get your API key and App ID from https://developer.oxforddictionaries.com/

**Uses:**

*This package works asynchronous.*

`Oxford.api_request`

This returns that whole massive dict so if you want to work with this you can.


```py
import asyncio
from oxford import Oxford
x = Oxford(your_app_id, your_app_key, language ='en-gb')
async def main():
    data = await x.api_request('People')
    return data

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

`Oxford.get_word_defination()`
```py
import asyncio
from oxford import Oxford
x = Oxford(your_app_id, your_app_key, language ='en-gb')
async def main():
    data = await x.get_word_defination('People')
    return data

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

And much more, I'll leave them to you to explore :)