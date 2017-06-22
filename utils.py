import hashlib

from PIL import Image


def calc_hash(image_path, size):
    img = Image.open(image_path, 'r')
    img = img.resize(size)
    ret = hashlib.md5(img.tobytes()).hexdigest()
    return ret
