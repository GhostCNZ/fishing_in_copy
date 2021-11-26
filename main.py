import datetime
import requests
from loguru import logger

# 节日锚点
holiday_list = [
    # {"张颖生日": "2021-11-26"},
    {"平安夜": "2021-12-24"},
    {"圣诞节": "2021-12-25"},
    {"元旦假期": "2022-01-01"},
    {"春节假期": "2022-01-31"},
]


def get_holiday():
    global holiday_list
    """
    获取配置中的节日设置
    :return: list——>[{'节日名':'节日日期'}]
    """
    holiday_content = ''
    # 今天日期
    now_str = datetime.datetime.now().strftime('%Y-%m-%d')
    now = datetime.datetime.strptime(now_str, "%Y-%m-%d")
    for holiday_info in holiday_list:
        holiday_name = list(holiday_info.keys())[0]
        holiday_date = holiday_info[holiday_name]
        future = datetime.datetime.strptime(holiday_date, "%Y-%m-%d")
        days = (future - now).days
        holiday_content = holiday_content + '距离' + holiday_name + '还有' + str(days) + '天' + '\n'
    return holiday_content


def get_tg():
    """
    获取日记
    :return: bool or str
    """
    url = f"https://fabiaoqing.com/jichou/randomrj.html"
    try:
        res = requests.post(url=url).json()
        return res['tgrj'] + '\n'
    except:
        return False


def get_weather():
    """
    获取天气预报
    :return: str or false
    """
    url = f"http://apis.juhe.cn/simpleWeather/query"
    params = {
        'city': '太原',
        'key': '7612ddda2313a41481327cbef5261b46',
    }
    try:
        res = requests.get(url=url, params=params).json()
        now_str = datetime.datetime.now().strftime('%Y-%m-%d')
        weather_content = f"""【摸鱼办公室】\n今天是 {now_str} 星期 {datetime.datetime.now().weekday() + 1}\n{res['result']['city']} 当前天气 {res['result']['realtime']['info']} {res['result']['realtime']['temperature']}摄氏度\n早上好，摸鱼人！上班点快到了，收拾收拾，该吃饭吃饭，该溜达溜达，该上厕所上厕所。别闲着\n"""
        return weather_content
    except:
        return False


if __name__ == '__main__':
    holiday_content = get_holiday()
    if not holiday_content:
        logger.error(f"节日为空。")
        holiday_content = ''
    else:
        logger.info(f"获取到节日：\n{holiday_content}")
    tg_content = get_tg()
    if not tg_content:
        logger.error(f"日记为空。")
        tg_content = ''
    else:
        logger.info(f"获取到日记：\n{tg_content}")
    weather_content = get_weather()
    if not weather_content:
        logger.error(f"天气为空。")
        weather_content = ''
    else:
        logger.info(f"获取到天气：\n{weather_content}")
    complete_content = weather_content + '\n' + holiday_content + '\n' + tg_content + '\n' + '工作再累 一定不要忘记摸鱼哦！有事没事起身去茶水间去厕所去廊道走走，别老在工位上坐着钱是老板的，但命是自己的'
    logger.info(f"整合内容开始推送：\n{complete_content}")
