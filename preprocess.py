import argparse
import os
import hashlib
import json

from PIL import Image
from tqdm import tqdm

from utils import calc_feature


def main(args):
    ret = {}

    for filename in tqdm(os.listdir(args.imgs_dir)):
        path = os.path.join(args.imgs_dir, filename)
        k = calc_feature(path)
        name, _ = os.path.splitext(filename)
        ret[k] = name

    with open(args.save_file, 'w') as f:
        json.dump(ret, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='preprocess for smart emoji converter')
    parser.add_argument('imgs_dir')
    parser.add_argument('save_file')

    args = parser.parse_args()
    main(args)
