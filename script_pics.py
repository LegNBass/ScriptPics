#!/usr/local/bin/python3
import sys

from functools import reduce
from PIL import Image, ImageFont, ImageDraw


def script_generator(script):
    index = 0
    while True:
        if index < len(script) - 1:
            yield script[index]
            index += 1
        else:
            yield script[index]
            index = 0


def main(image_path, script_file, font_file, inverted=False):

    image = Image.open(image_path)
    image = image.convert('1')
    # pdb.set_trace()

    size = (360, 203)

    script = script_file.read().replace('\n', '')
    image.thumbnail(size, Image.ANTIALIAS)
    # image.save('foo.bmp')

    size = image.size

    gen = script_generator(script)
    out_list = []
    for rownum in range(size[1]):
        line = []
        for colnum in range(size[0]):
            if not inverted:
                line.append(
                    '  ' if not image.getpixel((colnum, rownum)) else "{}{}".format(gen.__next__(), gen.__next__())
                )
            else:
                line.append(
                    '  ' if image.getpixel((colnum, rownum)) else "{}{}".format(gen.__next__(), gen.__next__())
                )
        out_list.append(''.join(line))
    # out_string = '\n'.join(out_list)

    font = ImageFont.truetype(font_file, 16)

    full_size = reduce(lambda x, y: (max(x[0],  y[0]), x[1] + y[1]), (font.getsize(line) for line in out_list), (0, 0))

    out_img = Image.new('1', full_size, 1)
    draw = ImageDraw.Draw(out_img)

    y_text = 0
    for line in out_list:
        width, height = font.getsize(line)
        draw.text((0, y_text), line, font=font)
        y_text += height

    out_img.save('img.png')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', type=str)
    parser.add_argument('script_file', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('font_file', type=str)
    parser.add_argument('-i', '--inverted', type=bool, nargs='?', default=False)
    args = parser.parse_known_args()[0]

    main(args.image_file, args.script_file, args.font_file, args.inverted)
