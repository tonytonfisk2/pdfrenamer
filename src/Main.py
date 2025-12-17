import os
import shutil
import yaml

from Extract import extract
from Preprocess import preprocess
from Search import search
from File_Handler import extract_files


def main():

    DIR_PATH = '../data'
    PDF_TYPE = 'invoice'

    with open('../config/keywords.yaml', 'r', encoding='UTF-8') as file:
        keywords = yaml.safe_load(file)

    invoice_field = keywords[PDF_TYPE]

    vat_mapping = keywords.get('vat_mapping', {})

    files, pf = extract_files(DIR_PATH)

    for file_path in files:
        try:
            result = {}

            text = extract(file_path)
            text = preprocess(text)
            for k, k_list in invoice_field.items():
                s = search(text, k_list, k, vat_mapping)
                result.update(s)

            required_fields = ['Datum', 'Företagnamn', 'Fakturanummer']
            missing_fields = [field for field in required_fields if field not in result or not result[field]]

            if missing_fields:
                print(f"   WARNING: Missing fields {missing_fields} for {os.path.basename(file_path)}")
                print(f"   Skipping file rename.\n")
                continue
           
            new_filename = f"{result['Datum']} {result['Företagnamn'].title()} {result['Fakturanummer'].title()}.pdf"
            new_filepath = os.path.join(pf, new_filename)

            shutil.copy2(file_path, new_filepath)

            print(result)
        except Exception as e:
            print(str(e))

        

if __name__ == "__main__":
    main()