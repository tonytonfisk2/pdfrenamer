import os
import glob
import shutil
import yaml
from rename_logic.Extract import extract
from rename_logic.Preprocess import preprocess
from rename_logic.Search import search
from utils import write_log


def extract_files(dir_path):
    files = glob.glob(os.path.join(dir_path, '*.pdf'))

    return files

def rename_files(dir_path, pdf_type):

    with open('../configs/keywords.yaml', 'r', encoding='UTF-8') as file:
        keywords = yaml.safe_load(file)

    invoice_field = keywords[pdf_type]

    v_map = keywords.get('vat_mapping', {})

    processed_dir = os.path.join(dir_path, 'processed')
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    try:
        files = extract_files(dir_path)
        for file_path in files:
            result = {}

            text = extract(file_path)
            text = preprocess(text)
            
            for k, k_list in invoice_field.items():
                s = search(text, k_list, k, v_map)
                result.update(s)
            
            required_fields = [key for key, _ in invoice_field.items()]
            missing_fields = [field for field in required_fields if field not in result or not result[field]]
            
            if missing_fields:
                print(f'Missing fields {missing_fields} for {os.path.basename(file_path)}')
                write_log(f'Missing fields {missing_fields} for {os.path.basename(file_path)}')
                continue
            
            new_filename = ''
            for keyword, _ in invoice_field.items():
                if(str(result[keyword]).isdigit()):
                    new_filename += f'{result[keyword]} '
                else:
                    new_filename += f'{result[keyword].title()} '
            else:
                new_filename += '.pdf'

            new_filepath = os.path.join(processed_dir, new_filename)

            shutil.copy2(file_path, new_filepath)

            print(result)
            write_log(f'Succesfully renamed - {result}')
    except Exception as e:
        print(str(e))
