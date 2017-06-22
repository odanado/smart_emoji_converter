import argparse
import os
import hashlib

import requests
from tqdm import tqdm


SLACK_URL = 'https://{domain}.slack.com/api/emoji.list?token={token}'


def download(save_dir, emoji_name, url):
    res = requests.get(url, stream=True)
    filename = '{}.png'.format(emoji_name)

    filename = os.path.join(save_dir, filename)
    with open(filename, 'wb') as f:
        f.write(res.content)


def main(args):
    if not os.path.exists(args.save_dir):
        os.mkdir(args.save_dir)
    res = requests.get(SLACK_URL.format(domain=args.domain, token=args.token))
    if res.status_code == 200:
        emoji = res.json()['emoji']
        for name, url in tqdm(emoji.items()):
            if url.startswith('alias:'):
                url = emoji.get(url[6:], None)
            if url:
                download(args.save_dir, name, url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='download for smart emoji converter')
    parser.add_argument('domain')
    parser.add_argument('token')
    parser.add_argument('save_dir')

    args = parser.parse_args()
    main(args)
