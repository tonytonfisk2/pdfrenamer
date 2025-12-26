from datetime import datetime

def write_log(message):
    with open('../logs/logs.txt', 'a', encoding='UTF-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} - {message} \n')

def clear_log():
    with open('../logs/logs.txt', 'w') as f:
        f.write('')
    