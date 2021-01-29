import os
import sys

from kaggle_secrets import UserSecretsClient


def _kaggle_gcp_authority():
    user_secrets = UserSecretsClient()
    user_credential = user_secrets.get_gcloud_credential()
    user_secrets.set_tensorflow_credential(user_credential)


def process_kaggle_notebook():
    # GCP設定
    _kaggle_gcp_authority()

    # 各種pathの設定
    # DATA_PATH = '../input/cassava-leaf-disease-classification/'
    # OUTPUT_DIR = './output/'
    # NOTEBOOK_PATH = './__notebook__.ipynb'
    env_dict = {
        'env': 'kaggle',
        'data_path': '../input/cassava-leaf-disease-classification/',
        'output_dir': './output/',
        'notebook_dir': './__notebook__.ipynb'
    }

    os.makedirs(env_dict['output_dir'], exist_ok=True)
    # system path
    sys.path.append('../input/pytorch-image-models/pytorch-image-models-master')

    return env_dict