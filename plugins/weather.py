# -*- coding: utf-8 -*-
__author__ = 'ratijha'
import requests
import time
import re

API_KEY='ab21eaa0df2e41c4292c243f32bbd222'
location_id = 1269750

iconmap = {
    "01": ":sunny:",
    "02": ":partly_sunny:",
    "03": ":partly_sunny:",
    "04": ":cloud:",
    "09": ":droplet:",
    "10": ":droplet:",
    "11": ":zap:",
    "13": ":snowflake:",
    "50": ":umbrella:",    # mist?
}


def weather(command):
    '''
    It will get the weather information for the given location
    :param command:
    :return:
    '''
    # session = requests.session()
    # session.verify(False)
    weather_api_key=API_KEY
    # url = 'http://api.openweathermap.org/data/2.5/forecast?id={0}&APPID={1}'.format(command,weather_api_key)
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={0}&cnt=5&units=metric&APPID={1}'.format(command,weather_api_key)
    dat = requests.get(url).json()
    msg = ["{0}: ".format(dat["city"]["name"])]
    # msg = ["{0}: ".format(dat["name"])]
    for day in dat["list"]:
        name = time.strftime("%a", time.gmtime(day["dt"]))
        high = str(int(round(float(day["main"]["temp_max"]))))
        icon = iconmap.get(day["weather"][0]["icon"][:2], ":question:")
        msg.append(u"{0} {1}° {2}".format(name, high, icon))

    return " ".join(msg)


def on_message(msg):
    # text = msg.get("text", "")
    match = re.findall(r"weather (.*)", msg)
    if not match:
        return

    searchterm = match[0]
    return weather(searchterm.encode("utf8"))
