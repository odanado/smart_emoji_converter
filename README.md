# smart_emoji_converter
Bot宛に送られた文章を絵文字化するBotです

# Requirement
- Docker

# Installation

1. Build
```
$ docker build -t smart-emoji-converter .
```

2. Preprocess

token は https://api.slack.com/methods/emoji.list/test を参照してください
```
$ docker run --rm -v $PWD:/src smart-emoji-converter python download.py ${domain} ${token} imgs
$ docker run --rm -v $PWD:/src smart-emoji-converter python preprocess.py imgs emoji.json
```
3. Create config

`rtmbot.conf` を作成してください  
tokenは https://api.slack.com/slack-apps からSlack Botを作成し取得してください
```
DEBUG: True
SLACK_TOKEN: "xoxb-11111111111-222222222222222"
ACTIVE_PLUGINS:
  - plugins.smart_converter.SmartConverter
```

# Usage
```
$ docker run --rm -v $PWD:/src smart-emoji-converter rtmbot
```
