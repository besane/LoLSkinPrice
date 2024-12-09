from get_all_skin_picture import translate_html_to_dict
import re
import requests
import json
import sqlite3

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
    all_champion_info = get_all_champion_info('https://game.gtimg.cn/images/lol/act/img/tft/js/chess.js')
    print(len(all_champion_info))
    init_tft_db()
    write_champion_info_into_db(all_champion_info)
    # for champion in champion_info['data']:
    #     print(champion)
        # print(str(champion['chessId']) + ' ' + champion['title'] + ' ' + champion['displayName'] + ' ' + str(champion['price']) + ' ' + champion['races'] + ' ' + champion['jobs'])