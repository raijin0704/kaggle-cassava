import io
import os
from requests import get
import subprocess
import sys

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload



def install_apex():
    subprocess.run('git clone https://github.com/NVIDIA/apex'.split(' '))
    # time.sleep(10)
    os.chdir('apex')
    subprocess.run('pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" .'.split(' '))
    os.chdir('..')


def _colab_kaggle_authority():
    drive_service = build('drive', 'v3')
    results = drive_service.files().list(
            q="name = 'kaggle.json'", fields="files(id)").execute()
    kaggle_api_key = results.get('files', [])

    filename = "/root/.kaggle/kaggle.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    request = drive_service.files().get_media(fileId=kaggle_api_key[0]['id'])
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    os.chmod(filename, 600)


def process_colab():

    # kaggle設定
    # _colab_kaggle_authority()
    # subprocess.run('pip install --upgrade --force-reinstall --no-deps kaggle'.split(' '))

    # ファイルタイトル取得
    filename = get('http://172.28.0.2:9000/api/sessions').json()[0]['name']
    title = filename.split('.')[0]

    # ライブラリ関係
    subprocess.run('pip install --upgrade opencv-python'.split(' '))
    subprocess.run('pip install --upgrade albumentations'.split(' '))
    subprocess.run('pip install timm'.split(' '))
    # if CFG['apex']:
    #     print('installing apex')
    #     install_apex()
    #     print('done')

    # 各種pathの設定
    # DATA_PATH = '/content/drive/Shareddrives/便利用/kaggle/cassava/input/'
    # DATA_PATH = '/content/input'
    # OUTPUT_DIR = './output/'
    # NOTEBOOK_PATH = f'/content/drive/Shareddrives/便利用/kaggle/cassava/notebook/{title}.ipynb'
    env_dict = {
        'env': 'colab',
        'title': title,
        'data_path': '/content/input/',
        'output_dir': './output/',
        'notebook_dir': f'/content/drive/Shareddrives/便利用/kaggle/cassava/notebook/{title}.ipynb'
    }

    return env_dict