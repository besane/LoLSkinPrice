# -*- codeing = utf-8 -*-
import time

import requests
import json, os
from PIL import Image
from io import BytesIO
import sqlite3


def translate_html_to_dict(url):
    # 获取网站源码
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'

    datas = json.loads(response.text) # 将html的字符串转化为字典
    return datas


def get_hero_info_lists(url):
    """

    Args:
        url: https://101.qq.com/#/hero 这个网页下面找到的hero list js

    Returns:
        List of all hero information directories. The keys in a directory are as follows:
        'heroId': 腾讯内部ID, "910"
        'name': 英雄称号, "异画师"
        'alias': 英文名字, "Hwei"
        'title': 中文名, "彗"
        'roles': 分路, "['mage', 'support']"
        'isWeekFree': 是否周免, "0"
        'attack': 物理指数, 满分十分
        'defense': 坦克指数, 满分十分
        'magic': 法师指数, 满分十分
        'difficulty': 难度指数, 满分十分
        'selectAudio': 选择英雄播报语音url(实测登不上)
        'banAudio': 禁用英雄播报语音url(实测登不上)
        'isARAMweekfree': 是否大乱斗周免(ARAM: All Random All Middle, 即大乱斗)
        'ispermanentweekfree': 是否永久周免
        'changeLabel': "改动英雄" or "无改动"
        'goldPrice': 金币价格
        'couponPrice': 点券价格
        'camp': N/A
        'campId': N/A
        'keywords': 搜索关键词, "异画师,彗,yihuashi,hui"
        'instance_id': 不清楚什么用, "89056f8e-8fe5-4bec-ae9a-c23c6ffd1a07"

    """

    info_lists = translate_html_to_dict(url)
    return info_lists['hero']


def get_skin_info_lists(hero_info_lists):
    """

    Args:
        hero_info_lists: 所有英雄信息，具体类型见get_hero_info_lists的返回

    Returns:
        List of all skin information directories. The keys in a directory are as follows:
        'skinId': 皮肤ID, '950011'
        'heroId': 对应英雄ID, '950'
        'heroName': 对应英雄称号, '百裂冥犬'
        'heroTitle': 对应英雄名字, '纳亚菲利'
        'name': 皮肤名字, '源计划：狂猎 纳亚菲利'
        'chromas': 是否炫彩, '0'
        'chromasBelongId': N/A
        'isBase': 是否原皮, '0'
        'emblemsName': N/A
        'description': 皮肤背景故事, '源计划的实验永远地改变了犬形英雄纳亚菲利，让她能够吸收猎物的意识，与自己的意识化为一体。莫德凯撒发现了这一能力背后的潜力，于是借由病毒感染为她的程序指派了新的任务：清除全人类的自由意志。现在，她将向所有幸存者证明：抵抗不过是白费力气。'
        'mainImg': 皮肤原画, 'https://game.gtimg.cn/images/lol/act/img/skin/big_f49826f7-59ea-4077-8bcd-6f78866dcb8f.jpg'
        'iconImg': 小头像(局内头像), 'https://game.gtimg.cn/images/lol/act/img/skin/small_f49826f7-59ea-4077-8bcd-6f78866dcb8f.jpg'
        'loadingImg': 加载界面图片, 'https://game.gtimg.cn/images/lol/act/img/skinloading/f49826f7-59ea-4077-8bcd-6f78866dcb8f.jpg'
        'videoImg': N/A, 'https://game.gtimg.cn/images/lol/act/img/skinvideo/sp_f49826f7-59ea-4077-8bcd-6f78866dcb8f.jpg'
        'sourceImg': N/A, 'https://game.gtimg.cn/images/lol/act/img/guidetop/guide_f49826f7-59ea-4077-8bcd-6f78866dcb8f.jpg'
        'vedioPath': N/A(这拼写...)
        'suitType': '18', TODO: 确认这个key的意义，目前猜测是系列皮肤ID
        'publishTime': 发布时间, 但get到的为空值
        'chromaImg': N/A
        'centerImg': 图片中心, 'https://game.gtimg.cn/images/lol/act/img/center/f49826f7-59ea-4077-8bcd-6f78866dcb8f.jpg'
        'instanceId': 不清楚什么用, 'f49826f7-59ea-4077-8bcd-6f78866dcb8f'

    """

    skin_info_lists = []
    for hero_info in hero_info_lists:
        hero_js_addr = 'https://game.gtimg.cn/images/lol/act/img/js/hero/' + hero_info['heroId'] + '.js?ts=2889127'  # 具体到某个英雄的js页面
        hero_detail = translate_html_to_dict(hero_js_addr)  # 获取英雄详细信息
        for skin in hero_detail['skins']:
            if skin['chromas'] == '1':
                continue
            skin_info_lists.append(skin)
    return skin_info_lists

def download_skins(skin_info_lists):
    """

    Args:
        skin_info_lists: 所有皮肤信息，具体类型见get_skin_info_lists的返回

    Returns:
        下载失败个数
    """
    download_fail_skins = []
    i = 0
    for skin in skin_info_lists:
        i = i + 1
        print(str(i) + '/' + str(len(skin_info_lists)))

        filename = "D:\\LOL\\" + skin['heroName'] + skin['heroTitle'] + "\\" + skin['name'] + ".jpg"
        filepath = "D:\\LOL\\" + skin['heroName'] + skin['heroTitle'] + "\\"
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        address = skin['mainImg']
        res = requests.get(url=address, params={'param':'1'}, headers={'Connection':'close'})
        if res.status_code != 200: # 网页链接失败
            download_fail_skins.append(skin['name'])
            continue

        # 保存图片
        try:
            image = Image.open(BytesIO(res.content))
            image.save(filename)
            print('成功下载' + skin['name'] + '.jpg')
        except:
            filename = filename.replace('/', '')
            image = Image.open(BytesIO(res.content))
            rgb_image = image.convert('RGB')
            rgb_image.save(filename)
            print('成功下载' + skin['name'] + '.jpg')
        time.sleep(.1)
    print(f'Failed download pictures[{len(download_fail_skins)}]:', download_fail_skins)
    return len(download_fail_skins)


if __name__ == '__main__':
    print('preparing...')
    start_time = time.time()
    hero_lists = get_hero_info_lists('https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts=2889125')
    skin_lists = get_skin_info_lists(hero_lists)
    print(f'get skin information finish in {time.time() - start_time} s \n Start downloading skin picture')
    start_time = time.time()
    download_skins(skin_lists)
    print(f'download skin picture finish in {time.time() - start_time} s')