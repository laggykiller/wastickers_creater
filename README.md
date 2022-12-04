# wasticker_creater
Create .wasticker file on computer for importing into WhatsApp

# Downloading
Precompiled version is available for Windows. Simply download it, unzip and run `wastickers-create.exe`.

For other OS, or if you do not trust the precompiled version, please download this repository and run the script directly, which you will need `python3` and other dependencies
- If you are using Windows, you will also need `ffmpeg`, `imagemagick` and `zip`. These can be easily installed using chocolately
- If you are using MacOS, you will also need `ffmpeg` and `imagemagick`. These can be easily installed using homebrew
- If you are using Linux, you will also need `ffmpeg` and `imagemagick`. These can be easily installed using package manager of your distro

# How to use?
1. Copy videos/images into `input` folder
    - Note that the maximum amount of sticker per pack is 30
    - By default, the script will modify files for complying to WhatsApp limitations:
        - The video/image in 512x512 pixels
        - For static sticker, the size should be <100KB and in PNG format
        - For dynamic sticker, the size should be <500KB and in WEBP format
    - You may run `wastickers-create.py direct` if you want to pack files into .wasticker file directly
    - Note that ffmpeg does not support decoding WEBP format video, so if you put webp file into input folder, they will be converted to static stickers (Unless you run with `wastickers-create.py direct`)
    - A good use of this repo is for converting stickers from Signal / Telegram to WhatsApp. You may take a look at these repo for downloading stickers from Signal / Telegram:
        - https://github.com/teynav/signalApngSticker (My fork: https://github.com/laggykiller/wasticker_creater)
        - https://github.com/signalstickers/Adhesive
        - https://github.com/signalstickers/signalstickers-client
    - Learn more about WhatsApp sticker limitations from https://github.com/WhatsApp/stickers/blob/main/Android/README.md
2. (Optional) Change content of `author.txt` to your name, and change content of `title.txt` to title of the sticker pack (If you delete author.txt and/or title.txt, the script will ask you to input author and title name each time it runs)
3. (Optional) Add `cover.png` (It should be 96x96 and <50KB). If not added, the script will generate one from the first sticker
4. Running
    - `wastickers-create.py` (Will modify files to comply with WhatsApp's limitations)
    - `wastickers-create.py direct` (Pack into .wasticker file directly)
    - If you are using precompiled version on windows, use `wastickers-create.exe`

# How to compile?
Just run `compile-windows.py` and get it from `dist`

Note that the compile script will download `ffmpeg`, `imagemagick`, `bzip2` and `zip` binaries automatically, as well as pip installing `requests`, `pyunpack`, `patool` and `pyinstaller` if not found

# How to import .wasticker file into WhatsApp
1. Download Sticker maker on your phone [iOS version](https://apps.apple.com/us/app/sticker-maker-studio/id1443326857) [Android version](https://play.google.com/store/apps/details?id=com.marsvard.stickermakerforwhatsapp)
2. Transfer the .wasticker file into your phone
3. Share the file to Sticker Maker app
4. Inside Sticker Maker app, you can then import the stickers into WhatsApp

# How does this work?
`.wasticker` files are actually zip files. They contain `author.txt` (Author of sticker pack), `title.txt` (Title of sticker pack), stickers file in png/webp format and cover photo in png.

Note that the zip file was created with 'junk-paths' (`zip -j`)

The stickers and cover photo file names are unix timestamp.

# DISCLAIMER
The author of this repo is NOT affiliated with WhatsApp or Sticker Maker