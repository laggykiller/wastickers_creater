import os
import subprocess
import shutil
import time
import mimetypes
import sys

mimetypes.init()

vid_img_ext = []
for ext in mimetypes.types_map:
    if mimetypes.types_map[ext].split('/')[0] == 'video' or mimetypes.types_map[ext].split('/')[0] == 'video':
        vid_img_ext.append(ext)

vid_img_ext = tuple(vid_img_ext)

print('HINT: Make sure you have installed ffmpeg, magick and zip')
print('If you are using Windows to run this, these can be easily installed by chocolately')
print()

os.makedirs('input', exist_ok=True)

if os.listdir('input') == []:
    print('Place stickers into input folder')
    exit()

if len(os.listdir('input')) > 30:
    print('Too many files. Maximum number is 30 files excluding cover')

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
        with open(os.devnull, 'wb') as devnull:
            # subprocess.check_call(['magick', f'{orig}[0]', '-resize', f'{res}x{res}', '-background', 'none', '-gravity', 'center', '-extent', f'{res}x{res}', new], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call(['magick', f'{orig}[0]', '-resize', f'{res}x{res}', '-background', 'none', '-gravity', 'center', '-extent', f'{res}x{res}', new], stdout=devnull, stderr=subprocess.STDOUT)
        size = os.path.getsize(new)
        if size >= size_limit:
            print(f'File {new}: Size too large ({size}), redoing with {quality=}')
        else:
            break

fname = int(time.time())
for i in os.listdir('input'):
    fname += 1
    orig = os.path.join('input', i)
    new = os.path.join('temp', str(fname) + '.webp')

    if os.path.splitext(i)[-1] in vid_img_ext:
        cmd_out = subprocess.Popen(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries', 'stream=nb_read_frames', '-print_format', 'default=nokey=1:noprint_wrappers=1', orig], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = cmd_out.communicate()
        stdout_str = stdout.decode(encoding='utf-8').replace('\n', '')
        if stdout_str.isnumeric() == False:
            frames = 1
        else:
            frames = int(stdout_str)

        if len(sys.argv) >= 2 and sys.argv[1] == 'direct':
            shutil.copy(orig, new)
            continue
    
        res = 512
        quality = 100
        for quality in range(100, 0, -10):
            if frames == 1:
                with open(os.devnull, 'wb') as devnull:
                    # subprocess.check_call(['magick', f'{orig}[0]', '-resize', f'{res}x{res}', '-background', 'none', '-gravity', 'center', '-extent', f'{res}x{res}', new], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    subprocess.check_call(['magick', f'{orig}[0]', '-resize', f'{res}x{res}', '-background', 'none', '-gravity', 'center', '-extent', f'{res}x{res}', new], stdout=devnull, stderr=subprocess.STDOUT)
            else:
                with open(os.devnull, 'wb') as devnull:
                    # subprocess.check_call(['ffmpeg', '-y', '-i', orig, '-vcodec', 'webp', '-pix_fmt', 'yuva420p', '-quality', quality, '-lossless', '0', '-vf', '"' + f'scale={res}:-1:flags=neighbor:sws_dither=none,scale={res}:{res}:force_original_aspect_ratio=decrease,pad={res}:{res}:(ow-iw)/2:(oh-ih)/2:color=black@0,setsar=1' + '"', '-loop', '0', new], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    subprocess.check_call(['ffmpeg', '-y', '-i', orig, '-vcodec', 'webp', '-pix_fmt', 'yuva420p', '-quality', quality, '-lossless', '0', '-vf', '"' + f'scale={res}:-1:flags=neighbor:sws_dither=none,scale={res}:{res}:force_original_aspect_ratio=decrease,pad={res}:{res}:(ow-iw)/2:(oh-ih)/2:color=black@0,setsar=1' + '"', '-loop', '0', new], stdout=devnull, stderr=subprocess.STDOUT)
            
            size = os.path.getsize(new)
            if (frames == 1 and size >= 100000) or (frames > 1 and size >= 500000):
                print(f'File {new}: Size too large ({size}), redoing with {quality=}')
            else:
                break

os.system(f'zip -jr {title}.wastickers ./temp')

shutil.rmtree('./temp')