import json
import logging
import os
import pandas as pd


from dbfread import DBF
from dotenv import load_dotenv


load_dotenv()
Data_dir = '21.08.2023'

# Настройка логирования
logging.basicConfig(
    # format='%(asctime)s - %(levelname)s - %(message)s',
    format='%(message)s',
    level=logging.DEBUG,
    filename='valid_name_DBF.log',
    filemode='w'
)

with open('PATH_DB.json', 'r', encoding='utf-8') as path_file:
    """Пути до файлов RAZD.dbf, RAZS.dbf"""
    connect_data = json.load(path_file)
    path_dir = connect_data['path']

# Получаю список УСЗН для поиска в папках.
dist_helper = pd.read_excel(f'{path_dir}\\dist_helper.xlsx')
USZN_name = dist_helper['title'].tolist()

ROOT_D = {}
set_OTD_SV = set()
COUNT = 1
count = 1

for name in USZN_name:
    # Прохожу по папкам с наименованиями УСЗН текущей датой.
    path_dir_iter = f'{path_dir}\\Входящие файлы\\{name}\\{Data_dir}'

    try:
        # Ловлю ошибку если папки с наименованием УСЗН нет.
        for root, dirs, files in os.walk(path_dir_iter):
            logging.debug('#' * 50)


            for file in files:
                # Рекурсивно ищу файлы DBF.
                if file.endswith(('.dbf', '.DBF')) and file[3] == 'D':
                    name_OTD_SV = file[9:12]
                    dbf_file_puth = root + '/' + str(file)

                    # Открываю файл
                    db = DBF(dbf_file_puth, encoding='cp866')
                    for _, db_string in enumerate(db):
                        OTD_SV = db_string['OTD_SV']
                        if name_OTD_SV != OTD_SV:
                            logging.debug(f'Есть невалидные файлы {file}')

                # Рекурсивно ищу файлы DBF.
                if file.endswith(('.dbf', '.DBF')) and file[3] == 'S':
                    name_NOM_SP = file[4:8]

                    dbf_file_puth = root + '/' + str(file)

                    # Открываю файл
                    db = DBF(dbf_file_puth, encoding='cp866')

                    for _, db_string in enumerate(db):
                        NOM_SP = db_string['NOM_SP']
                        if name_NOM_SP != NOM_SP[0:4]:
                            logging.debug(f'Есть невалидные файлы {file}')
    except FileNotFoundError:
        continue
