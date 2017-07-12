import os
import json
import random
from functools import lru_cache

from rtmbot.core import Plugin

import utils
from utils import calc_feature, compare_image, load_images

CONVERT_COMMAND = ('convert -pointsize 140 -font /usr/share/fonts/truetype/mplus/mplus-1p-black.ttf '
                   '-annotate 0 "{str}" -gravity center -fill black -size 128x128 xc:none {file}')


def create_image(c):
    filename = '/tmp/{:032x}.png'.format(random.getrandbits(128))
    cmd = CONVERT_COMMAND.format(str=c, file=filename)
    os.system(cmd)
    return utils.load_image(filename)


class SmartConverter(Plugin):
    def __init__(self, *args, **kwargs):
        with open('./emoji.json') as f:
            data = json.load(f)
            self.emoji = data

        self.emoji_images = load_images('./imgs')

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
        # print(text)
        for c in text:
            output_text += self.convert(c)

        print(output_text)
        self.outputs.append((channel, output_text))

    @lru_cache(maxsize=1024)
    def convert(self, c):
        img1 = create_image(c)
        ret = [(compare_image(img1, img2), emoji)
               for emoji, img2 in self.emoji_images.items()]
        ret = min(ret)
        if ret[0] < 1000:
            return ':{}:'.format(ret[1])
        else:
            return c
