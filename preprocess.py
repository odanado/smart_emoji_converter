import argparse
import os
import hashlib
import json

from PIL import Image
from tqdm import tqdm

from utils import calc_hash


def main(args):
    ret = {'size': int(args.image_size), 'emoji': {}}
    size = [int(args.image_size) for _ in range(2)]

    for filename in tqdm(os.listdir(args.imgs_dir)):
        path = os.path.join(args.imgs_dir, filename)
        k = calc_hash(path, size)
        name, _ = os.path.splitext(filename)
        ret['emoji'][k] = name

    with open(args.save_file, 'w') as f:
        json.dump(ret, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='preprocess for smart emoji converter')
    parser.add_argument('imgs_dir')
    parser.add_argument('save_file')
    parser.add_argument('image_size')

    args = parser.parse_args()
    main(args)
