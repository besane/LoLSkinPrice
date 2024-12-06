# -*- codeing = utf-8 -*-
import requests
import json, os
from PIL import Image
from io import BytesIO


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
    download_fail_skins = []
    heroes = datas['hero'] # dict_keys(['hero', 'version', 'fileName', 'fileTime'])
    with open('skin_infos.txt', 'w+', encoding='utf-8') as file:
        i = 0
        for hero in heroes: # dict_keys(['heroId', 'name', 'alias', 'title', 'roles', 'isWeekFree', 'attack', 'defense', 'magic', 'difficulty', 'selectAudio', 'banAudio', 'isARAMweekfree', 'ispermanentweekfree', 'changeLabel', 'goldPrice', 'couponPrice', 'camp', 'campId', 'keywords', 'instance_id'])
            i = i + 1
            print(str(i) + '/' + str(len(heroes)))

            # file.write(hero['name'] + ' ' + hero['title'] + '\n')
            hero_js_addr = 'https://game.gtimg.cn/images/lol/act/img/js/hero/' + hero['heroId'] + '.js?ts=2889127' # 具体到某个英雄的js页面
            hero_detail = translate_html_to_dict(hero_js_addr) # 获取英雄详细信息

            for skin in hero_detail['skins']:
                if skin['chromas'] == '1': #炫彩
                    continue

                # file.write(skin['name'] + ' ' + skin['mainImg'] + '\n')
                filename = "D:\\LOL\\" + hero['name'] + hero['title'] + "\\" + skin['name'] + ".jpg"
                filepath = "D:\\LOL\\" + hero['name'] + hero['title'] + "\\"
                if not os.path.exists(filepath):
                    os.makedirs(filepath)

                address = skin['mainImg']
                res = requests.get(address)
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
    print(f'Failed download pictures[{len(download_fail_skins)}]:', download_fail_skins)


if __name__ == '__main__':
    datas = translate_html_to_dict('https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts=2889125')
    get_skin_addresses(datas)
    # print(data)