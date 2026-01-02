from datetime import datetime
import os
import shutil

def write_log(message):
    with open('../logs/logs.txt', 'a', encoding='UTF-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} - {message} \n')

def clear_log():
    with open('../logs/logs.txt', 'w') as f:
        f.write('')

def clear_folders(dir_path):
    processed_dir = os.path.join(dir_path, 'processed')
    if os.path.exists(processed_dir):
        for filename in os.listdir(processed_dir):
            file_path = os.path.join(processed_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')


def init():

    DIR_PATH = '../data'
    CONFIG_PATH = '../configs'
    LOG_PATH = '../logs'

    if not os.path.exists(DIR_PATH):
        os.makedirs(DIR_PATH)

    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)

    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

    clear_log()

