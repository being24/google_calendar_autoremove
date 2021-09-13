#!/usr/bin/env python3
# coding: utf-8

import argparse
import json
import os
from datetime import datetime, timedelta, timezone

import requests


def get_conversations_history(
        token: str,
        channel: str,
        latest: int = 0,
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

    with open(f'{currentpath}/config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    def load_conversations_and_del_msg(Token, CHANNEL_ID, BOT_ID, KEY) -> None:
        json_data = get_conversations_history(Token, CHANNEL_ID)

        cnt = 0

        for i in json_data["messages"]:
            if 'bot_id' in i:
                if i["bot_id"] == BOT_ID:
                    two_day = return_timestamp_movedbyday(-1)
                    seven_day = return_timestamp_movedbyday(-6)

                    if "this week" in i["text"]:
                        if float(i["ts"]) < seven_day:
                            delete_message(Token, CHANNEL_ID, i["ts"])
                            cnt += 1
                    else:
                        if float(i["ts"]) < two_day:
                            delete_message(Token, CHANNEL_ID, i["ts"])
                            cnt += 1

        print(f"{KEY} : {cnt} msg del done") # hoge

    for i in data.keys():
        temp_dict = data[i]
        load_conversations_and_del_msg(
            temp_dict["OAuth_Token"],
            temp_dict["CHANNEL_ID"],
            temp_dict["BOT_ID"],
            i)
