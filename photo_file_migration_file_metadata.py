import os
import shutil
import datetime

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import dateutil.parser
import ffmpeg

# データを写真の日付(更新時間：exif.)で仕分けするためのプログラム

# 静止画(jpeg)
def get_jpeg_DateTimeDigitized(file_path):
    try:
        with Image.open(file_path) as f:
            exif = f._getexif()

        for id, value in exif.items():
            tag_ = TAGS.get(id, id)
            if tag_ == 'DateTimeDigitized':
                return datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        return None
    except Exception as other:
        print(other)
        print(file_path)
        return None

# 静止画(tiff)
def get_tiff_DateTimeOriginal(file_path):
    try:
        with Image.open(file_path) as f:
            for key in f.tag.keys():
                # DatTimeOriginal
                if key == 36867:
                    return datetime.datetime.strptime(f.tag[key][0], '%Y:%m:%d %H:%M:%S')
        return None
    except Exception as other:
        print(other)
        print(file_path)
        return None

# 動画
def get_JST_creation_time(file_path):
    try:
        video_info = ffmpeg.probe(file_path)
        # UTC
        creation_time = video_info['format']['tags']['creation_time']
        # JST
        JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        jst_timestamp = dateutil.parser.parse(creation_time).astimezone(JST)
        return jst_timestamp
    except Exception as other:
        print(other)
        print(file_path)
        return None

input_path = 'your input dir'
output_path = 'your output dir'

files = os.listdir(input_path)

for file in files:
    path = os.path.join(input_path, file)
    if os.path.isdir(path):
        # ディレクトリの場合はcontinue
        continue

    #拡張子
    root, ext = os.path.splitext(file)
    ext = ext.lower()

    # 撮影日
    create_time = None

    if ext == '.jpg' or ext == '.jpeg':
        # exif DateTimeDigitizedの取り出し
        create_time = get_jpeg_DateTimeDigitized(path)
    elif ext == '.nef':
        # exif DateTimeDigitizedの取り出し
        create_time = get_tiff_DateTimeOriginal(path)
    elif ext == '.mp4':
        create_time = get_JST_creation_time(path)

    if create_time == None:
        continue

    # YYYY-MM-DDの文字列作成
    yyyymmdd = create_time.strftime('%Y-%m-%d')

    # outputディレクトリの作成
    output_dir = os.path.join(output_path, yyyymmdd)

    # ディレクトリがなければ作成する
    if os.path.exists(output_dir) == False:
        os.mkdir(output_dir)
        print(output_dir)

    # コピーのファイルパス
    output_file = os.path.join(output_dir, file)

    print(output_file)

    # ファイルをコピーする
    if os.path.exists(output_file) == False:
        shutil.copy2(path, output_file)

print('finish')




