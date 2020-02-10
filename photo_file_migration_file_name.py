import os
import datetime
import shutil
import re

# 写真の日付(ファイルの名前から取り出す)で仕分けするためのプログラム

input_path = 'your input directory'
output_path = 'your output directry'

files = os.listdir(input_path)

pattern = '.+_(.{8})_.+'

for file in files:
    path = os.path.join(input_path, file)
    if os.path.isdir(path):
        # ディレクトリの場合はcontinue
        continue

    # 作成時間(Unixタイム)の取り出し
    mtime = os.path.getmtime(path)

    # datetimeに置き換え
    mtime_datetime = datetime.datetime.fromtimestamp(mtime)

    # あり得ない時間はcontinue
    # 閾値
    min_datetime = datetime.datetime(2015, 1, 1, 0, 0, 0, 0)
    if mtime_datetime < min_datetime:
        continue

    # ファイル名からYYYYMMDDを取り出す
    res_yyyymmdd = re.match(pattern, file).group(1)
    yyyymmdd = res_yyyymmdd[0:4] + '-' + res_yyyymmdd[4:6] + '-' + res_yyyymmdd[6:8]

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
        print(output_file)

print('finish')




