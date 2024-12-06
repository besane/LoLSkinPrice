# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import requests
from main import askURL
import json


def translate_html_to_dict(url):
    # 获取网站源码
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'

    datas = json.loads(response.text) # 将html的字符串转化为字典
    return datas


def get_skin_addresses(datas):
    addresses = []
    heroes = datas['hero'] # dict_keys(['hero', 'version', 'fileName', 'fileTime'])
    with open('skin_infos.txt', 'w+', encoding='utf-8') as file:
        i = 0
        for hero in heroes:
            i = i + 1
            print(str(i) + '/' + str(len(heroes)))
            # dict_keys(['heroId', 'name', 'alias', 'title', 'roles', 'isWeekFree', 'attack', 'defense', 'magic', 'difficulty', 'selectAudio', 'banAudio', 'isARAMweekfree', 'ispermanentweekfree', 'changeLabel', 'goldPrice', 'couponPrice', 'camp', 'campId', 'keywords', 'instance_id'])
            file.write(hero['name'] + ' ' + hero['title'] + '\n')
            hero_js_addr = 'https://game.gtimg.cn/images/lol/act/img/js/hero/' + hero['heroId'] + '.js?ts=2889127'
            hero_detail = translate_html_to_dict(hero_js_addr)
            for skin in hero_detail['skins']:
                if skin['chromas'] == '1':
                    continue
                print(skin['name'] + ' ' + skin['mainImg'] + '\n')
                file.write(skin['name'] + ' ' + skin['mainImg'] + '\n')


if __name__ == '__main__':
    datas = translate_html_to_dict('https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts=2889125')
    get_skin_addresses(datas)
    # print(data)