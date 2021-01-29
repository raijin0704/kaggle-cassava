import json
import subprocess



def process_common():
    # ライブラリ関係
    subprocess.run('pip install mlflow'.split(' '))