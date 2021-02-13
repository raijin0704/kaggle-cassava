from .common import process_common


def create_env():
    try:
        from google.colab import auth
    except ModuleNotFoundError:
        from .kaggle_notebook import process_kaggle_notebook
        env_dict = process_kaggle_notebook()
    else:
        from .colab import process_colab
        env_dict = process_colab()
    finally:
        process_common()

    return env_dict
