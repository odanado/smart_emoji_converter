import os
import hashlib

import numpy as np
from scipy import ndimage
from PIL import Image


def load_image(path):
    img = Image.open(path).convert('LA')
    return np.asarray(img.resize((128, 128)))


def load_images(images_path):
    ret = {}
    for filename in os.listdir(images_path):
        emoji_name, _ = os.path.splitext(filename)
        filename = os.path.join(images_path, filename)

        ret[emoji_name] = load_image(filename)

    return ret


def compare_image(img1, img2):
    def f(img):
        return np.asarray(img) // 16 * 16

    diff = np.sum(f(img1) - f(img2) != 0)
    return diff


def calc_feature(path):
    ret = 0
    img = Image.open(path).convert('LA')
    img = np.array(img)

    feature = ndimage.gaussian_filter(img, 3)
    return hashlib.md5(feature.tobytes()).hexdigest()


def calc_hash(image_path, size):
    img = Image.open(image_path, 'r')
    img = img.resize(size)
    ret = hashlib.md5(img.tobytes()).hexdigest()
    return ret
