import copy
import time

from get_all_skin_picture import translate_html_to_dict
import re
import requests
import json
import sqlite3

hero_list = {
    '辛吉德': ['炼金男爵', '哨兵'],
    '烈娜塔': ['炼金男爵', '先知'],
    '希尔科': ['炼金男爵', '统领'],
    '卡蜜尔': ['执法官', '伏击专家'],
    '布里茨': ['海克斯机械', '统领'],
    '蔚': ['执法官', '搏击手'],
    '凯特琳': ['执法官', '狙神'],
    '艾克': ['野火帮', '极客', '伏击专家'],
    '阿木木': ['海克斯机械', '监察'],
    '玛尔扎哈': ['海克斯机械', '先知'],
    '蒙多医生': ['试验品', '统领'],
    '图奇': ['试验品', '狙神'],
    '阿卡丽': ['蓝发小队', '迅击战士'],
    '瑟提': ['蓝发小队', '格斗家'],
    '伊泽瑞尔': ['皮城学院', '蓝发小队', '炮手'],
    '俄洛伊': ['蓝发小队', '哨兵'],
    '德莱文': ['铁血征服者', '搏击手'],
    '芮尔': ['铁血征服者', '哨兵', '先知'],
    '卡西奥佩娅': ['黑色玫瑰', '统领'],
    '弗拉基米尔': ['黑色玫瑰', '监察', '法师'],
    '伊莉丝': ['黑色玫瑰', '双形战士', '格斗家'],
    '乐芙兰': ['黑色玫瑰', '法师'],
    '黑默丁格': ['皮城学院', '先知'],
    '杰斯': ['皮城学院', '双形战士'],
    '特朗德尔': ['极客', '格斗家'],
    '吉格斯': ['极客', '统领'],
    '兰博': ['机械公敌', '极客', '哨兵'],
    '史密奇': ['炼金男爵', '伏击专家'],
    '塞薇卡': ['百变铁手', '炼金男爵', '搏击手'],
    '荏妮': ['炼金男爵', '格斗家'],
    '洛里斯': ['执法官', '哨兵'],
    '斯特卜': ['执法官', '格斗家'],
    '麦迪': ['执法官', '狙神'],
    '爆爆': ['家人', '极客', '伏击专家'],
    '范德尔': ['家人', '监察'],
    '刀疤': ['野火帮', '监察'],
    '努努和威朗普': ['试验品', '格斗家', '先知'],
    '金克丝': ['蓝发小队', '伏击专家'],
    '泽丽': ['野火帮', '狙神'],
    '蔚奥莱': ['家人', '搏击手'],
    '娜美': ['外交官', '法师'],
    '库奇': ['极客', '炮手'],
    '盖伦': ['外交官', '监察'],
    '薇古丝': ['蓝发小队', '先知'],
    '魔腾': ['海克斯机械', '迅击战士'],
    '德莱厄斯': ['铁血征服者', '监察'],
    '艾瑞莉娅': ['蓝发小队', '哨兵'],
    '安蓓萨': ['外交官', '铁血征服者', '迅击战士'],
    '婕拉': ['试验品', '法师'],
    '普朗克': ['极客', '双形战士', '搏击手'],
    '蕾欧娜': ['皮城学院', '哨兵'],
    '克格莫': ['海克斯机械', '狙神'],
    '崔斯特': ['执法官', '迅击战士'],
    '拉克丝': ['皮城学院', '法师'],
    '莫德凯撒': ['铁血征服者', '统领'],
    '莫甘娜': ['黑色玫瑰', '先知'],
    '崔丝塔娜': ['外交官', '炮手'],
    '斯维因': ['铁血征服者', '双形战士', '法师'],
    '厄加特': ['试验品', '搏击手', '炮手'],
    '佐伊': ['蓝发小队', '法师'],
}

def get_all_champion_info(url):
    """
    Get All Champion Information

    Retrieves and returns champion information from a specified URL. The function
    uses an external helper function `translate_html_to_dict` to parse the HTML content
    from the given URL into a dictionary structure. It then extracts the 'data' portion
    of this dictionary, which is assumed to contain the relevant champion information.

    Returns:
        dict: A dictionary containing champion data parsed from the provided URL.
        chessId: 棋子ID,
        title: 英雄称号,
        name: 原画,
        displayName: 英雄名字,
        raceIds: 种族ID,
        jobIds: 职业ID,
        price: 价格,
        skillName: 技能名,
        skillType: '主动' or '被动',
        skillImage: 技能图片,
        skillIntroduce: 技能介绍,
        skillDetail: 技能细节,
        life: 生命值,
        magic: 法力值,
        startMagic: 初始法力值,
        armor: 护甲,
        spellBlock: 魔抗,
        attackMag: 平A回复法力值?,
        attack: 攻击力,
        attackSpeed: 攻速,
        attackRange: 攻击距离,
        crit: 暴击率,
        originalImage: 技能图标,
        lifeMag: 不清楚,
        TFTID: 云顶之弈ID,
        synergies: N/A,
        illustrate: N/A,
        recEquip: N/A,
        proStatus: N/A,
        hero_EN_name: 英文名,
        races: 种族,
        jobs: 职业,
        attackData: 攻击力数据,
        lifeData 生命值数据:

    Note:
        The `translate_html_to_dict` function is not defined within this snippet and must be
        implemented elsewhere in the codebase for this function to work correctly.

    Example Usage:
        # Assuming `translate_html_to_dict` is properly defined and imported
        url = "https://example.com/champion-stats"
        champion_data = get_all_champion_info(url)
        print(champion_data)

    Requirements:
        - The `translate_html_to_dict` function must accept a string (URL) as an argument
          and return a dictionary where the 'data' key holds the desired champion information.

    Raises:
        Any exceptions raised by `translate_html_to_dict` will propagate to the caller.

    """
    champion_info = translate_html_to_dict(url)
    return champion_info['data']


def get_race_and_job_levels():
    data = {}
    race_info = translate_html_to_dict('https://game.gtimg.cn/images/lol/act/img/tft/js/race.js')['data']
    job_info = translate_html_to_dict('https://game.gtimg.cn/images/lol/act/img/tft/js/job.js')['data']

    for info in race_info:
        data[info['name']] = [int(key) for key in info['level'].keys()]
    for info in job_info:
        data[info['name']] = [int(key) for key in info['level'].keys()]
    return data


def get_fetters_score_with_db(champions, fetter_levels):
    conn = sqlite3.connect('tft_champions.db')
    cursor = conn.cursor()

    fetters = {} # 所有羁绊
    activated_fetters = {} # 已激活的羁绊

    # 计算羁绊数量
    for champion in champions:
        cursor.execute(f'SELECT races, jobs FROM Champions WHERE displayName="{champion}"')
        race_and_job = cursor.fetchall()
        if not race_and_job:
            print(f'WARNING: There is no such data[{champion}]')
            continue
        for fetter in race_and_job[0]:
            fetter = fetter.split(',')
            for fet in fetter:
                fetters[fet] = fetters.get(fet, 0) + 1

    # 计算已激活的羁绊总数以及统计哪些羁绊已激活
    for fetter in fetters.keys():
        for level in fetter_levels[fetter]:
            if fetters[fetter] >= level:
                activated_fetters[fetter] = level
    score = sum(activated_fetters.values())

    cursor.close()
    conn.close()

    return score, activated_fetters


def get_fetters_score_locally(champions, fetter_levels):
    fetters = {}  # 所有羁绊
    activated_fetters = {}  # 已激活的羁绊

    # 计算羁绊数量
    for champion in champions:
        for fetter in hero_list[champion]:
            fetters[fetter] = fetters.get(fetter, 0) + 1

    # 计算已激活的羁绊总数以及统计哪些羁绊已激活
    for fetter in fetters.keys():
        for level in fetter_levels[fetter]:
            if fetters[fetter] >= level:
                activated_fetters[fetter] = level
    score = sum(activated_fetters.values())

    return score, activated_fetters

max_score = 0
champions_list = []
final_fetters = {}
fetter_levels = get_race_and_job_levels()

def get_max_fetter(level, heroes, **visited):
    # TODO: 剪枝、增加级别控制、增加外交官处理
    global max_score
    global champions_list
    global fetter_levels
    global final_fetters

    if len(heroes) == level:
        # print(heroes)
        score, _ = get_fetters_score_locally(heroes, fetter_levels)
        # print(heroes, _, score)
        if score > max_score:
            max_score = score
            champions_list = heroes
            final_fetters = _
        return

    # 计算当前羁绊
    fetters = set()
    for hero in heroes:
        for fetter in hero_list[hero]:
            fetters.add(fetter)

    # 获取可以和当前英雄凑羁绊的英雄
    new_heroes = set()
    for fetter in fetters:
        for hero in hero_list:
            if (fetter in hero_list[hero]) and (hero not in heroes) and not visited[hero]:
                new_heroes.add(hero)

    for new_hero in new_heroes:
        visited[new_hero] = True
        hero_tmp = copy.deepcopy(heroes)
        hero_tmp.append(new_hero)
        get_max_fetter(level, hero_tmp, **visited)

    return


def init_tft_db():

    # 连接到SQLite数据库
    conn = sqlite3.connect('tft_champions.db')
    cursor = conn.cursor()

    # 定义创建表的SQL语句
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Champions (
        chessId INTEGER PRIMARY KEY,
        title TEXT,
        name TEXT,
        displayName TEXT,
        raceIds TEXT,
        jobIds TEXT,
        price REAL,
        skillName TEXT,
        skillType TEXT,
        skillImage TEXT,
        skillIntroduce TEXT,
        skillDetail TEXT,
        life INTEGER,
        magic INTEGER,
        startMagic INTEGER,
        armor INTEGER,
        spellBlock INTEGER,
        attackMag REAL,
        attack REAL,
        attackSpeed REAL,
        attackRange REAL,
        crit REAL,
        originalImage TEXT,
        lifeMag REAL,
        TFTID TEXT,
        synergies TEXT,
        illustrate TEXT,
        recEquip TEXT,
        proStatus TEXT,
        hero_EN_name TEXT,
        id INTEGER,
        races TEXT,
        jobs TEXT,
        attackData TEXT,
        lifeData TEXT
    );
    """

    # 执行创建表的SQL语句
    cursor.execute(create_table_query)
    conn.commit()

    # 关闭连接
    cursor.close()
    conn.close()


def write_champion_info_into_db(champion_info):
    conn = sqlite3.connect('tft_champions.db')
    cur = conn.cursor()

    for champion in champion_info:
        cur.execute(f"""INSERT INTO Champions VALUES(
                    "{int(champion['chessId'])}",
                    "{champion['title']}",
                    "{champion['name']}",
                    "{champion['displayName']}",
                    "{champion['raceIds']}",
                    "{champion['jobIds']}",
                    "{float(champion['price'])}",
                    "{champion['skillName']}",
                    "{champion['skillType']}",
                    "{champion['skillImage']}",
                    "{champion['skillIntroduce']}",
                    "{champion['skillDetail']}",
                    "{0 if champion['life'] == "" else int(champion['life'])}",
                    "{0 if champion['magic'] == "" else int(champion['magic'])}",
                    "{0 if champion['startMagic'] == "" else int(champion['startMagic'])}",
                    "{0 if champion['armor'] == "" else int(champion['armor'])}",
                    "{0 if champion['spellBlock'] == "" else int(champion['spellBlock'])}",
                    "{float(champion['attackMag'])}",
                    "{float(champion['attack'])}",
                    "{float(champion['attackSpeed'])}",
                    "{float(champion['attackRange'])}",
                    "{float(champion['crit'])}",
                    "{champion['originalImage']}",
                    "{float(champion['lifeMag'])}",
                    "{champion['TFTID']}",
                    "{champion['synergies']}",
                    "{champion['illustrate']}",
                    "{champion['recEquip']}",
                    "{champion['proStatus']}",
                    "{champion['hero_EN_name']}",
                    "{int(champion['id'])}",
                    "{champion['races']}",
                    "{champion['jobs']}",
                    "{champion['attackData']}",
                    "{champion['lifeData']}");""")
    conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    # levels = get_race_and_job_levels()
    # print(levels)
    visited_flag = {}
    for all_hero in hero_list:
        visited_flag[all_hero] = False
    start_time = time.time()
    for all_hero in hero_list:
        visited_flag[all_hero] = True
        # print(visited_flag)
        get_max_fetter(6, [all_hero], **visited_flag)
    print(time.time() - start_time)
    print(max_score, champions_list, final_fetters)
    # # score, activated_fetters = get_fetters_score(['克格莫', '刀疤', '泽丽', '盖伦', '德莱厄斯', '阿木木', '范德尔', '弗拉基米尔'], levels)
    # score, activated_fetters = get_fetters_score(['黑默丁格', '盖伦', '伊莉丝', '玛尔扎哈', '杰斯', '乐芙兰', '弗拉基米尔', '努努和威朗普', '莫甘娜'], levels)
    # print(score, activated_fetters)

    # get_max_fetter(3)

    # init_tft_db()
    # all_champion_info = get_all_champion_info('https://game.gtimg.cn/images/lol/act/img/tft/js/chess.js')
    # # write_champion_info_into_db(all_champion_info)
    # for champion in all_champion_info:
    #     if champion['races'] == "":
    #         continue
    #     print("'" + champion['displayName'] + "': ['" + champion['races'] + "','" + champion['jobs'] + "'],")

    # get_max_fetter(3, [], [], [])