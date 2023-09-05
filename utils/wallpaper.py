import os
import ctypes
from PIL import Image
from env import ROOT_PATH, getKey, setKey
import time

WALLPAPER_PATH = os.path.join(ROOT_PATH, 'storage', 'wallpapers')
ASSET_PATH = os.path.join(ROOT_PATH,  'storage', 'assets')


def create_black_background(size):
    background = Image.new('RGBA', size, (0, 0, 0, 255))
    return background


def set_wallpaper(image):
    TEMP_PATH = os.path.join(ROOT_PATH, 'storage', 'temp.png')
    image.save(TEMP_PATH, format='png')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, TEMP_PATH, 0)


def reduce_image_opacity(image_path, opacity=0.5):
    image = Image.open(image_path)
    image = image.convert('RGBA')
    image_data = image.getdata()

    # iterate through every pixel and reduce the opacity
    new_image_data = []
    for pixel in image_data:
        new_image_data.append((
            int(pixel[0] * opacity),
            int(pixel[1] * opacity),
            int(pixel[2] * opacity),
            int(pixel[3] * opacity),
        ))
    image.putdata(new_image_data)
    return image


def generate_wallpaper():
    previous_wallpaper_time = getKey('previous_wallpaper_time')
    previous_wallpaper_opacity = getKey('previous_wallpaper_opacity')

    if previous_wallpaper_time is None:
        setKey('previous_wallpaper_time', time.time())

    if previous_wallpaper_opacity is None:
        setKey('previous_wallpaper_opacity', 0.01)

    # check how many days have passed since the last wallpaper change
    days_passed = (time.time() - float(previous_wallpaper_time)
                   ) // (24 * 60 * 60)

    increment_factor = 0.01

    # increase opacity by 0.1 for every day passed on the previous wallpaper opacity
    opacity = min(1, float(previous_wallpaper_opacity) +
                  (days_passed * 0.01) + increment_factor)

    # set precision to 2 decimal places
    opacity = round(opacity, 2)

    wallpaper_size = (1920, 1080)
    background = create_black_background(wallpaper_size)

    # get the sticker image
    sticker_path = os.path.join(ASSET_PATH, 'faang.png')

    sticker = Image.open(sticker_path)

    # reduce the opacity of the sticker image
    sticker = reduce_image_opacity(sticker_path, opacity)

    # get the sticker size
    sticker_size = sticker.size

    # paste sticker on top of background
    background.paste(sticker, (
        (wallpaper_size[0] - sticker_size[0]) // 2,
        (wallpaper_size[1] - sticker_size[1]) // 2
    ), sticker)

    set_wallpaper(background)

    # update the previous wallpaper time and opacity
    setKey('previous_wallpaper_time', time.time())
    setKey('previous_wallpaper_opacity', opacity)


if __name__ == '__main__':
    setKey('previous_wallpaper_time', time.time())
    setKey('previous_wallpaper_opacity', 0.01)
    for x in range(100):
        generate_wallpaper()
        time.sleep(1)
