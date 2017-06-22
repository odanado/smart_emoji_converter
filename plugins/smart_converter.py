import os
import json
import random

from rtmbot.core import Plugin

from utils import calc_hash

CONVERT_COMMAND = ('convert -pointsize 140 -font /usr/share/fonts/truetype/mplus/mplus-1p-black.ttf '
                   '-annotate 0 {str} -gravity center -fill black -size 128x128 xc:none {file}')


def convert(c, size):
    filename = '/tmp/{:032x}.png'.format(random.getrandbits(128))
    cmd = CONVERT_COMMAND.format(str=c, file=filename)
    os.system(cmd)
    return calc_hash(filename, size)


class SmartConverter(Plugin):
    def __init__(self, *args, **kwargs):
        with open('./emoji.jon') as f:
            data = json.load(f)
            self.emoji = data['emoji']
            self.emoji_size = (data['size'], data['size'])

        super(SmartConverter, self).__init__(*args, **kwargs)

    def process_message(self, data):
        bot_id = self.slack_client.api_call('auth.test')['user_id']
        if 'text' not in data:
            return

        text = data['text']
        channel = data['channel']
        if not text.startswith('<@{}>'.format(bot_id)):
        # if not data['channel'].startswith("D"):
            return

        text = ' '.join(text.split(' ')[1:])
        output_text = ''
        for c in text:
            h = convert(c, self.emoji_size)
            if h in self.emoji:
                output_text += ':{}:'.format(self.emoji[h])
            else:
                output_text += c

        print(output_text)
        self.outputs.append((channel, output_text))
