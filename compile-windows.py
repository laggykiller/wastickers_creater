import os
import shutil
try:
    import requests
except ModuleNotFoundError:
    os.system('pip install requests')
    import requests

try:
    from pyunpack import Archive
except ModuleNotFoundError:
    os.system('pip install pyunpack patool')
    from pyunpack import Archive

magick_path = shutil.which('magick')
if magick_path == None:
    print('Please download and install imagemagick')
    print('Choose those end with -dll and does not have "static" suffix')
    print('Reference: https://stackoverflow.com/a/44639935')
    print('Example: https://imagemagick.org/archive/binaries/ImageMagick-7.1.0-53-Q16-HDRI-x64-dll.exe')
    input('Press Enter to exit...')
else:
    magick_dir = os.path.split(magick_path)[0]

if os.path.isdir('bin/ffmpeg') == False:
    print('Downloading ffmpeg')
    with open('bin/ffmpeg.7z', 'wb+') as f:
        f.write(requests.get('https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z').content)

    print('Extracting ffmpeg')
    os.makedirs('bin/ffmpeg', exist_ok=True)
    Archive('bin/ffmpeg.7z').extractall("bin/ffmpeg")
    for i in os.listdir('bin/ffmpeg'):
        i_path = os.path.join('bin/ffmpeg', i)
        for j in os.listdir(i_path):
            j_path = os.path.join(i_path, j)
            os.rename(j_path, os.path.join('bin/ffmpeg', j))

    print('Extracting ImageMagick')
    os.makedirs('bin/ImageMagick', exist_ok=True)
    Archive('bin/ImageMagick.zip').extractall("bin/ImageMagick")

if os.path.isdir('bin/zip') == False:
    print('Downloading zip')
    with open('bin/zip.zip', 'wb+') as f:
        f.write(requests.get('https://sourceforge.net/projects/gnuwin32/files/zip/3.0/zip-3.0-bin.zip').content)

    print('Extracting zip')
    os.makedirs('bin/zip', exist_ok=True)
    Archive('bin/zip.zip').extractall("bin/zip")

if os.path.isdir('bin/bzip2') == False:
    print('Downloading bzip2')
    with open('bin/bzip2.zip', 'wb+') as f:
        f.write(requests.get('https://sourceforge.net/projects/gnuwin32/files/bzip2/1.0.5/bzip2-1.0.5-bin.zip').content)

    print('Extracting bzip2')
    os.makedirs('bin/bzip2', exist_ok=True)
    Archive('bin/bzip2.zip').extractall("bin/bzip2")

print('Creating exe')
os.system('pip install pyinstaller')
os.system(f'pyinstaller --add-data "./bin/ffmpeg/bin/*;./" --add-data "./bin/zip/bin/*;./" --add-data "./bin/bzip2/bin/*;./" --add-data "{magick_dir}/*;./magick" .\wastickers-create.py')