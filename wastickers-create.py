import os
import shutil
import time
import mimetypes
import sys
from wand.image import Image
import tempfile
import ffmpeg
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.environ['MAGICK_HOME'] = './'

mimetypes.init()

vid_img_ext = []
for ext in mimetypes.types_map:
    if mimetypes.types_map[ext].split('/')[0] == 'image' or mimetypes.types_map[ext].split('/')[0] == 'video':
        vid_img_ext.append(ext)
vid_img_ext.append('.webp')
vid_img_ext.append('.webm')

vid_img_ext = tuple(vid_img_ext)

os.makedirs('input', exist_ok=True)

if os.listdir('input') == []:
    print('Place stickers into input folder')
    input('Press Enter to close...')
    exit()

if len(os.listdir('input')) > 30:
    print('Too many files. Maximum number is 30 files excluding cover')
    input('Press Enter to close...')
    exit()

shutil.rmtree('temp', ignore_errors=True)
os.mkdir('temp')

if os.path.isfile('author.txt'):
    shutil.copy('author.txt', './temp/author.txt')
else:
    author = input('Enter author name: ')
    with open('./temp/author.txt', 'w+') as f:
        f.write(author)

if os.path.isfile('title.txt'):
    shutil.copy('title.txt', './temp/title.txt')
    with open('title.txt') as f:
        title = f.read().replace('\n', '')
else:
    title = input('Enter title name: ')
    with open('./temp/title.txt', 'w+') as f:
        f.write(title)

fname = int(time.time())

if 'cover.png' in os.listdir():
    shutil.copy('cover.png', './temp/cover.png')
else:
    orig = os.path.join('input', os.listdir('input')[0])
    new = os.path.join('temp', str(fname) + '.png')
    size_limit = 50000
    res = 96
    quality = 100
    for quality in range(100, 0, -10):
        with Image(filename=orig + '[0]') as img:
            img.resize(width=res, height=res)
            img.background_color = 'none'
            img.gravity = 'center'
            img.extent(width=res, height=res)
            img.compression_quality = quality
            img.save(filename=new)

        size = os.path.getsize(new)
        if size >= size_limit:
            print(f'File {new}: Size too large ({size}), redoing with {quality=}')
        else:
            break

fname = int(time.time())
for i in os.listdir('input'):
    fname += 1

    if os.path.splitext(i)[-1].lower() in vid_img_ext:
        with Image(filename=orig) as img:
            frames = img.iterator_length()
        
        orig = os.path.join('input', i)
        if frames == 1:
            new = os.path.join('temp', str(fname) + '.png')
        else:
            new = os.path.join('temp', str(fname) + '.webp')

        print(f'Processing {orig}')

        if len(sys.argv) >= 2 and sys.argv[1] == 'direct':
            shutil.copy(orig, new)
            continue

        res = 512
        quality = 100
        for quality in range(90, 0, -10):
            if frames > 1 and os.path.splitext(i)[-1].lower() == '.webp':
                # ffmpeg do not support webp decoding (yet)
                # Converting animated .webp to images or .webp directly can result in broken frames
                # Converting to .mp4 first is safe way of handling .webp
                
                with tempfile.TemporaryDirectory() as tempdir:
                    tmp_f = os.path.join(tempdir, 'temp.mp4')

                    with Image(filename=orig) as img:
                        img.save(filename=tmp_f)
                    
                    (
                        ffmpeg
                        .input(tmp_f)
                        .filter('scale', res, -1, flags='neighbor', sws_dither='none')
                        .filter('scale', res, res, force_original_aspect_ratio='decrease')
                        .filter('pad', res, res, '(ow-iw)/2', '(ow-ih)/2', color='black@0')
                        .filter('setsar', 1)
                        .output(new, vcodec='webp', pix_fmt='yuva420p', quality=quality, lossless=0, loop=0)
                        .run(overwrite_output=True)
                    )
            else:
                with Image(filename=orig) as img:
                    img.resize(width=res, height=res)
                    img.background_color = 'none'
                    img.gravity = 'center'
                    img.extent(width=res, height=res)
                    img.compression_quality = quality
                    img.save(filename=new)

            size = os.path.getsize(new)
            if (frames == 1 and size >= 100000) or (frames > 1 and size >= 500000):
                print(f'File {new}: Size too large ({size}), redoing with {quality=}')
            else:
                break

print('Zipping...')
os.system(f'zip -jr {title}.wastickers ./temp')

shutil.rmtree('./temp')

print()
print('Done')
input('Press Enter to close...')