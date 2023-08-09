import pathlib
import zipfile

import requests


def download_utbot(project_dir: pathlib.Path):
    zip_file_name = project_dir / 'utbot-cli-python.zip'
    zip_dir = project_dir / 'utbot-cli-python'
    jar_file = project_dir / 'utbot-cli-python.jar'
    if not jar_file.exists():
        print('Downloading utbot...')
        # with open(str(zip_file_name), 'wb') as fout:
        #     utbot_url = 'https://drive.google.com/file/d/1m9LRy9ICfHSFprBM0dIKfcBOONatfTgl/view?usp=sharing'
        #     data = requests.get(utbot_url, stream=True)
        #     for chunk in data.iter_content(chunk_size=4096):
        #         fout.write(chunk)
        # zip_file = zipfile.ZipFile(zip_file_name, 'r')
        # zip_file.extractall(zip_dir)
        utbot_url = 'https://disk.yandex.ru/d/tuX_RKTcf3sXPQ'
        with open(jar_file, 'wb') as f:
            data = requests.get(utbot_url, stream=True)
            for chunk in data.iter_content(chunk_size=4096):
                f.write(chunk)
    # jar_file = list(zip_dir.iterdir())[0]
    return jar_file
