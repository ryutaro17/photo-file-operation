import os
import datetime
import shutil

# データを写真の日付(更新時間：mtime)で仕分けするためのプログラム

input_path = 'your input directory'
output_path = 'your output directry'

files = os.listdir(input_path)

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

    # YYYY-MM-DDの文字列作成
    yyyymmdd = mtime_datetime.strftime('%Y-%m-%d')

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




