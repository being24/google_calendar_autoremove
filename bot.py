#!/usr/bin/env python3
# coding: utf-8

import argparse
import configparser
import errno
import json
import os
import pprint
import time
import typing
from datetime import datetime, timedelta, timezone

import requests


def get_conversations_history(
        token: str,
        channel: str,
        latest: float = 0,
        limit: int = 100):

    Conversations_History_API_URL = "https://slack.com/api/conversations.history"

    params = {
        'token': token,
        'channel': channel,
        "limit": limit,
        "latest": latest}
    r = requests.get(Conversations_History_API_URL, params=params)
    json_data = r.json()
    if json_data.get('ok', False) is False:
        print(json_data)
        raise Exception('FAILED TO GET CONVERSATIONS HISTORY!')
    else:
        return json_data


def return_timestamp_movedbyday(diff: int = -1):
    JST = timezone(timedelta(hours=+9), 'JST')
    td_two_days_before = timedelta(days=diff)
    today_at_midnight = datetime.now(JST).replace(
        hour=0, minute=0, second=0, microsecond=0)
    two_days_before = today_at_midnight + td_two_days_before
    return two_days_before.timestamp()


def delete_message(token: str, channel: str, ts: float):
    Chat_Delete_API_URL = "https://slack.com/api/chat.delete"

    params = {'token': token, 'channel': channel, "ts": ts}
    r = requests.get(Chat_Delete_API_URL, params=params)
    json_data = r.json()

    if json_data.get('ok', False) is False:
        print('message の削除に失敗')
        print(json_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='slackの邪魔なbotの書き込みを削除するスクリプト')

    parser.add_argument('-d', '--day', help='指定された日数より前のbotの書き込みを削除する')
    args = parser.parse_args()
    day = args.day

    if day is not None:
        day = int(day) * -1
    else:
        day = -1

    currentpath = os.path.dirname(os.path.abspath(__file__))
    config_ini = configparser.ConfigParser()
    config_ini_path = currentpath + '/config.ini'

    if not os.path.exists(config_ini_path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(
                errno.ENOENT), config_ini_path)

    config_ini.read(config_ini_path, encoding='utf-8')

    read_default = config_ini['DEFAULT']
    Token = read_default.get('OAuth_Token')
    CHANNEL_ID = read_default.get('CHANNEL_ID')
    GOOGLE_CALENDER_ID = read_default.get('GOOGLE_CALENDER_ID')

    json_data = get_conversations_history(Token, CHANNEL_ID)

    cnt = 0

    for i in json_data["messages"]:
        if 'bot_id' in i:
            if i["bot_id"] == GOOGLE_CALENDER_ID:
                two_day = return_timestamp_movedbyday(2)
                eight_day = return_timestamp_movedbyday(8)

                if "this week" in i["text"]:
                    if float(i["ts"]) > eight_day:
                        delete_message(Token, CHANNEL_ID, i["ts"])
                        cnt += 1
                else:
                    if float(i["ts"]) > two_day:
                        delete_message(Token, CHANNEL_ID, i["ts"])
                        cnt += 1

    print(f"{cnt} msg del done")
