# Preprocess each PDF.

import re
#remove noise
def preprocess(lines):
    p_lines = []
    noise_keywords = [
        'sida', 'page', 'besöksadress', 'hemsida',
        'telefon', 'bic', 'bankgiro', 'adress', 'innehar',
        'från förfallodagen', 'ange detta', 'payment to',
        'bet.villkor', 'lev.villkor', 'leveranssätt','artikelnr', 'benämning', 'lev.antal', 'à-pris', 'belopp',
        'enhet', 'kundnr', 'vårt ordernr', 'ert bestnr', 'er ref',
        'vår referens', 'säljare', 'rma nr', ',', '#'
    ]
    for text in lines:

        text = text.lower()
        if not text:
            continue 
        if any(noise in text for noise in noise_keywords):
            continue
        if len(text) > 50:
            continue
        if len(text) <= 1:
            continue
        
        text = re.sub(r"[ \t]+", " ", text) 
        p_lines.append(text)
 
    return p_lines