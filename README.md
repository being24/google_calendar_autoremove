# google_calendar_autoremove
研究室用に作成したgoogleカレンダーの通知を削除するスクリプト。  
アイコンは趣味です。

# how to use
python3でbot.pyを実行すると指定されたチャンネルの指定された送信者の書き込みを削除します。

```sh
python3 bot.py
```
でデフォルト（２日前）以前の書き込みを削除し、
```sh
python3 bot.py -d (day:int)
```
でday日前からの書き込みを削除します。引数に0以下を入れるとすべて消えます。
# licence of Icon
## Шигастон_Республикасы.png

```
ソース: http://scp-jp.wikidot.com/scp-1558-jp  
URL: http://scp-jp.wikidot.com/local--files/scp-1558-jp/%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89.png  
ライセンス: CC BY-SA 3.0　

タイトル: シガスタンの国璽  
著作権者:  くなぬい@トンムイヤー、kossy  
公開年: 2019
```