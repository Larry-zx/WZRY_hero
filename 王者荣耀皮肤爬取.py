import requests
import os

url = 'https://pvp.qq.com/web201605/js/herolist.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}
herolist = requests.get(url)  # 获取英雄列表json文件

herolist_json = herolist.json()  # 转化为json格式
hero_name = list(map(lambda x: x['cname'], herolist.json()))  # 提取英雄的名字
hero_number = list(map(lambda x: x['ename'], herolist.json()))  # 提取英雄的编号
number = len(hero_name)

print('一共有' + str(number) + '个英雄')
if not os.path.exists('./wzry_pifu'):
    os.mkdir('./wzry_pifu')
count = 0
h_count = 0
for i in range(number):  # 英雄遍历
    if not os.path.exists('./wzry_pifu' + hero_name[i]):
        os.mkdir('./wzry_pifu' + hero_name[i])
    if (hero_number[i] != 518):
        cloth_list_str = herolist.json()[i]['skin_name']  # 将皮肤放入列表中
        cloth_list = cloth_list_str.split('|')
    else:
        cloth_list = ['冷晖之枪', '幸存者', '神威']
    pifu_number = len(cloth_list)
    h_count += 1
    for j in range(pifu_number):  # 皮肤遍历
        count += 1
        pic_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/' + str(hero_number[i]) + '/' + str(
            hero_number[i]) + '-bigskin-' + str(j + 1) + '.jpg'
        print(pic_url)
        response = requests.get(url=pic_url, headers=headers)
        pic_data = response.content
        hero_cloth_name = cloth_list[j]
        pic_name = './wzry_pifu/' + hero_name[i] + '/' + hero_cloth_name + '.jpg'
        with open(pic_name, 'wb') as fp:
            fp.write(pic_data)
        print(str(count) + '----' + str(h_count) + hero_name[i] + '的' + hero_cloth_name + '皮肤' + '-------' + '下载成功！')
