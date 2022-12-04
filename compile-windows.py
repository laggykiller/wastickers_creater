import os
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

print('Downloading ffmpeg')
with open('ffmpeg.7z', 'wb+') as f:
    f.write(requests.get('https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z').content)

print('Downloading ImageMagick')
with open('ImageMagick.zip', 'wb+') as f:
    f.write(requests.get('https://imagemagick.org/archive/binaries/ImageMagick-7.1.0-portable-Q16-x64.zip').content)

print('Downloading zip')
with open('zip.zip', 'wb+') as f:
    f.write(requests.get('https://sourceforge.net/projects/gnuwin32/files/zip/3.0/zip-3.0-bin.zip').content)

print('Downloading bzip2')
with open('bzip2.zip', 'wb+') as f:
    f.write(requests.get('https://sourceforge.net/projects/gnuwin32/files/bzip2/1.0.5/bzip2-1.0.5-bin.zip').content)

print('Extracting ffmpeg')
os.makedirs('ffmpeg', exist_ok=True)
Archive('ffmpeg.7z').extractall("ffmpeg")
for i in os.listdir('ffmpeg'):
    i_path = os.path.join('ffmpeg', i)
    for j in os.listdir(i_path):
        j_path = os.path.join(i_path, j)
        os.rename(j_path, os.path.join('ffmpeg', j))

print('Extracting ImageMagick')
os.makedirs('ImageMagick', exist_ok=True)
Archive('ImageMagick.zip').extractall("ImageMagick")

print('Extracting zip')
os.makedirs('zip', exist_ok=True)
Archive('zip.zip').extractall("zip")

print('Extracting bzip2')
os.makedirs('bzip2', exist_ok=True)
Archive('bzip2.zip').extractall("bzip2")

print('Creating exe')
os.system('pip install pyinstaller')
os.system('pyinstaller --add-data "./ImageMagick/*;./" --add-data "./ffmpeg/bin/*;./" --add-data "./zip/bin/*;./" --add-data "./bzip2/bin/*;./" .\wastickers-create.py')