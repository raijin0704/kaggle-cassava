from .colab import process_colab
from .kaggle_notebook import process_kaggle_notebook
from .common import process_common


def create_env():
    try:
        from google.colab import auth
    except ImportError:
        env_dict = process_kaggle()
    else:
        env_dict = process_colab()
    finally:
        process_common()

    return env_dict