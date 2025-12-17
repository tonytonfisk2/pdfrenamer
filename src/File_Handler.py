import os
import glob

def extract_files(dir_path):
    processed_dir = os.path.join(dir_path, 'processed')
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    files = glob.glob(os.path.join(dir_path, '*.pdf'))

    return files, processed_dir

def rename_files(dir_path):
    return None