#!/usr/bin/env python
# coding: utf-8

import configparser
import errno
import json
import os
import pprint
import time
import typing
from datetime import datetime, timedelta, timezone

import requests

# Token & Channel ID
CHANNEL_ID = "C011Q2P3DHB"
GOOGLE_CALENDER_ID = "B011NTXG1M0"


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
        raise Exception('FAILD TO GET CONVERSATIONS HISTORY!')
    else:
        return json_data


def retuen_timestanp_movedbyday(diff: int = -2):
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

    config_ini = configparser.ConfigParser()
    config_ini_path = 'config.ini'

    if not os.path.exists(config_ini_path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(
                errno.ENOENT), config_ini_path)

    config_ini.read(config_ini_path, encoding='utf-8')

    read_default = config_ini['DEFAULT']
    Token = read_default.get('OAuth_Token')

    json_data = get_conversations_history(
        Token, CHANNEL_ID, retuen_timestanp_movedbyday())

    cnt = 0

    for i in json_data["messages"]:
        if 'bot_id' in i:
            if i["bot_id"] == GOOGLE_CALENDER_ID:
                delete_message(Token, CHANNEL_ID, i["ts"])
                cnt += 1

    print(f"{cnt} msg del done")
