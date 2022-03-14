import argparse as ap
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance


def args_init():
    path = 'res.png'
    parser = ap.ArgumentParser(description='adds glitch effects to the picture')
    parser.add_argument('input')
    parser.add_argument('filter', nargs='?', choices=['lines', 'glitch', 'glow', 'default'], default='default')
    parser.add_argument('-a', type=int, nargs='?', default=4)
    parser.add_argument('-o', '--out', nargs='?', default=path)
    args = parser.parse_args()
    return args


def make_image(filename, filter_, opt, *args, **kw):
    try:
        with Image.open(filename) as im:
            im.convert('RGB')
            return filter_(im, opt, *args, **kw)
    except FileNotFoundError:
        print(f'file: {filename} not found')


def lines(im, wd):
    black = (0, 0, 0)
    w, h = im.size
    draw = ImageDraw.Draw(im)
    for i in range(0, h, wd * 2):
        draw.line(((0, i), (w, i)), fill=black, width=wd)
    return im


def glitch(im, delta):
    r = Image.new('L', im.size)
    r1, g, b = im.split()
    r.paste(r1, (delta, 0))
    res = Image.merge('RGB', (r, g, b))
    return res


def glow(im, radius):
    gl = ImageEnhance.Color(im).enhance(1.2)
    gl = ImageEnhance.Contrast(gl).enhance(1.5)
    gl = ImageEnhance.Sharpness(gl).enhance(1.2)
    gl = gl.filter(ImageFilter.GaussianBlur(radius))
    res = Image.blend(im, gl, 0.6)
    return res



def main():
    filters = {'lines': lines, 'glitch': glitch, 'glow': glow}
    args = args_init()
    filter_ = args.filter
    source, out, opt = args.input, args.out, args.a
    if filter_ == 'default':
        im = make_image(source, glow, 40)
        im = glitch(im, 6)
        im = lines(im, 2)
        im.save(out, 'PNG')
        return
    im = make_image(source, filters[filter_], opt)
    im.save(out, 'PNG')

if __name__ == '__main__':
    main()

