import requests
from lxml import etree
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json

url = 'https://pvp.qq.com/web201605/js/herolist.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}
driver = webdriver.Chrome(ChromeDriverManager().install())
herolist = requests.get(url)  # 获取英雄列表json文件
fp = open('wzry.txt', 'w')
herolist_json = herolist.json()  # 转化为json格式
hero_name = list(map(lambda x: x['cname'], herolist.json()))  # 提取英雄的名字
hero_number = list(map(lambda x: x['ename'], herolist.json()))  # 提取英雄的编号
number = len(hero_name)
herourl = 'https://pvp.qq.com/web201605/herodetail/%d.shtml'
data_dict = {
    '姓名': [],
    '生存能力': [],
    '攻击伤害': [],
    '技能效果': [],
    '上手难度': [],
    '英雄定位': []
}
pos_list = ['','战士','法师','坦克','刺客','射手','辅助']
for i in range(number):
    index = hero_number[i]
    name = hero_name[i]
    hero_url = format(herourl % index)
    driver.get(hero_url)
    sleep(2)
    page_text = driver.page_source
    tree = etree.HTML(page_text)
    li_list = tree.xpath('/html/body/div[3]/div[1]/div/div/div[1]/ul/li')
    fp.write(name + ':' + '\n')
    data_dict['姓名'].append(name)
    pos = tree.xpath('/html/body/div[3]/div[1]/div/div/div[1]/span/i/@class')[0].split('-')[-1]
    pos = eval(pos)
    data_dict['英雄定位'].append(pos_list[pos])
    for li in li_list:
        shuxing = li.xpath('./em/text()')[0]
        shuzi = li.xpath('./span/i/@style')[0].split(':')[-1]
        str_str = shuxing + '------' + shuzi
        fp.write('     ' + str_str + '\n')
        shuzhi = eval(shuzi.split('%')[0])
        if shuzhi>=70:
            value='高'
        elif shuzhi>=40:
            value='中'
        else:
            value='低'

        data_dict[shuxing].append(value)
    print(str(i + 1) + '.' + name + '--------录入完成')
out = pd.DataFrame(data_dict)
out.to_csv('王者荣耀_离散值.csv', index=False)
