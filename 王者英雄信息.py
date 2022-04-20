import json
import requests


url = 'https://pvp.qq.com/web201605/js/herolist.json'
herolist = requests.get(url)  # 获取英雄列表json文件
herolist_json = herolist.json()  # 转化为json格式
print(herolist_json)