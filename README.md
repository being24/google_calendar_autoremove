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
# config.iniの記述について
```py
[DEFAULT]
OAuth_Token = token #ここにslackAPIのトークン
CHANNEL_ID = id #ここにチャンネルID
GOOGLE_CALENDER_ID = id #ここにbotのID
```
チャンネルIDとbotのIDは書き込みのリンクを取得すると得られます。  
APIの権限取得が少々面倒ですが、権限不足の場合はAPIの戻り値にその旨と必要な権限が出るのでAPIのテストページで地道にやってくといいです。また、APIを取った人が出来ない事はbotにもできないので、削除等を伴うbotのAPItokenを取得する人はそのワークスペースのadmin以上になる必要があります。（この辺はdiscordの方が柔軟なので見習ってほしい…）
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