from PIL import Image
import sys, os


def main():
    lists = sys.argv[1:]
    for i in lists:
        f, e = os.path.splitext(i)
        outfile = f + '.png'
        if e == '.webp':
            with Image.open(i) as im:
                im = im.convert("RGB")
                im.save(outfile, "PNG")


if __name__ == '__main__':
    main()
