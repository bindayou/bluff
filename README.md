# bluff

Based on the latest python3.6, the smallest and flexible Python asynchronous crawler library.

![bluff_process](https://github.com/BlingBlingdevelopers/bluff/blob/master/static/bluff_process.png)

- [DevelopmentPlan](#DevelopmentPlan)
    - [v0.1](#v0.1edition)
      - [new_characteristic](#v0.new_characteristic)
      - [new_module](#v0.1new_module)
      - [change_module](#v0.1change_module)
      - [todo](#v0.1todo)
- [Example](#Example)
- [Contribution](#Contribution)

# DevelopmentPlan

## v0.1edition

### v0.1new_characteristic

### v0.1new_module

| module  | explain |
| --- | ---- |
| item |  definition of reptilian results | 
| log  |  log record module |
| parser |  scheduling based on analytical results |
| request |  initiate a request  |
| selector | different analytical methods   |
| spider |  The main class that provides inheritance  |
    
### v0.1change_module

Not available

### v0.1todo
-  Code structure (is finshed!!)
    -  Introduction of ABC classes and external exposure interface restrictions 
-  Execution speed (is begining!!!)
    -  Quoting profile, optimizing speed 
    -  Optimal scheduling 
-   Added function 
    -  Splash rendering
# Example

The examples are in the /example/ directory, Including common tests and pytest tests 

`cd bluff/example | pipenv run python test_spider.py` 

then, you can catch the log on /bluff/log

`cat bluff.log`

it`s looking beautiful!!!

or you can write a python script like this

```angular2html
import sys
sys.path.append("/home/linhanqiu/Proj/bluff/")
from bluff import Css, Item, Parser, Spider


class Post(Item):
    title = Css('.ph')

    async def save(self):
        print(self.title)


class MySpider(Spider):
    start_url = 'http://blog.sciencenet.cn/home.php?mod=space&uid=40109&do=blog&view=me&from=space'
    parsers = [
        Parser('http://blog.sciencenet.cn/home.php\?mod=space&uid=\d+&do=blog&view=me&from=space&amp;page=\d+'),
        Parser(
            'blog\-\d+\-\d+\.html',
            Post)]


MySpider.run()
```

# Contribution
- Pull request.
- Open issue.

### Welcome to rebuild this immaturity！！！！！
