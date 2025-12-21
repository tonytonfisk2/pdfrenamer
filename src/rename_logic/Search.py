import re
from datetime import datetime
from collections import defaultdict

def search(text, keywords, category, vmap):
    result = {}
    lines_to_check = 15
    company_count = defaultdict(int)

    for idx, line in enumerate(text):
        for keyword in keywords:
            candidates = []
            if keyword not in line:
                continue

            for j in range(1, lines_to_check + 1):
                if idx + j >= len(text):
                    break
                candidates.append(text[idx + j].replace(' ', ''))

            for j in range(1, lines_to_check + 1):
                if idx - j < 0:
                    break
                candidates.append(text[idx - j].replace(' ', ''))

            if category == 'Fakturadatum' or category == 'Fakturanummer':
                if line.startswith(keyword):
                    value = line[len(keyword):].strip()
                    if value: 
                        validated = validate([value], category)
                        if validated:
                            result[category] = validated
                            return result
                        
            #print(candidates, category)

            if category == 'Företagnamn':
                company_count[keyword] += 1 

            
            validated_value = validate(candidates, category)

            if validated_value:
                result[category] = validated_value
                return result
    
    best_company = ''
    max_count = 0

    if category == 'Företagnamn' and company_count:
        for key, val in company_count.items():
            if val > max_count:
                max_count = val
                best_company = key
        result[category] = best_company

        

    if category == 'Företagnamn' and not result:
        for line in text:
            for vat in vmap.keys():
                if line.upper() == vat:
                    result[category] = vmap[vat]

    return result


def validate(candidates, category):

    DATE_PATTERN = r'''
    \b(
        (?:19\d{2}|20\d{2})[-/.](?:0?[1-9]|1[0-2])[-/.](?:0?[1-9]|[12]\d|3[01]) |
        (?:0?[1-9]|[12]\d|3[01])[-/.](?:0?[1-9]|1[0-2])[-/.](?:19\d{2}|20\d{2}) |
        (?:\d{2})[-/.](?:0?[1-9]|1[0-2])[-/.](?:0?[1-9]|[12]\d|3[01]) |
        (?:0?[1-9]|[12]\d|3[01])[-/.](?:0?[1-9]|1[0-2])[-/.](?:\d{2}) |
        (?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01]) |  # YYYYMMDD
        \d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])              # YYMMDD
    )\b
    '''

    INVOICE_PATTERN = r'(?:^|\s)([F]{0,5}\d{3,})(?:\s|$)'

    if category == 'Datum':
        dates = []
        for val in candidates:
            if re.search(DATE_PATTERN, val, re.IGNORECASE | re.VERBOSE):
                parsed_date = parse_date(val)
                dates.append(parsed_date)
        if(dates):
            return min(dates)

    if category == 'Fakturanummer':
        for val in candidates:
                if len(val) == 10 and (val[:2] in ['55', '56', '16', '21']):
                    continue
                if re.fullmatch(r'se\d{12}', val):
                    continue
                if re.search(INVOICE_PATTERN, val, re.IGNORECASE | re.VERBOSE):
                    return val
    return None

def parse_date(date):
    if len(date) == 6:
        return date
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%y-%m-%d", "%d-%m-%y"):
        try:
            return int(datetime.strptime(date, fmt).strftime("%y%m%d"))
        except ValueError:
            pass
    raise ValueError(f"Unsupported date format: {date}")


