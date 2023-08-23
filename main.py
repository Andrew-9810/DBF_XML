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
    filename='main.log',
    filemode='w'
)

with open('PATH_DB.json', 'r', encoding='utf-8') as path_file:
    """Пути до файлов RAZD.dbf, RAZS.dbf"""
    connect_data = json.load(path_file)
    path_dir = connect_data['path']

# Получаю список УСЗН для поиска в папках.
dist_helper = pd.read_excel(f'{path_dir}\\dist_helper.xlsx')
USZN_name = dist_helper['title'].tolist()


ROOT = []
for name in USZN_name:
    # Прохожу по папкам с наименованиями УСЗН текущей датой.
    path_dir_iter = f'{path_dir}\\Входящие файлы\\{name}\\{Data_dir}'
    try:
        # Ловлю ошибку если папки с наименованием УСЗН нет.
        for root, dirs, files in os.walk(path_dir_iter):
            for file in files:
                # Рекурсивно ищу файлы DBF.
                if file.endswith(('.dbf', '.DBF')) and file[3] == 'D':

                    dbf_file_puth = root + '/' + str(file)

                    # Открываю файл
                    db = DBF(dbf_file_puth, encoding='cp866')

                    for count, db_string in enumerate(db):

                        NOM_VD = db_string['NOM_VD']
                        OTD_SV = db_string['OTD_SV']
                        # FAM = db_string['FAM']
                        # IMJA = db_string['IMJA']
                        # OTCH = db_string['OTCH']
                        # FIO = f'{FAM} {IMJA} {OTCH}'
                        text = {OTD_SV:
                                    {'NOM_VD': NOM_VD,
                                     'data': []
                                     }
                                }
                        # Добавляем шаблоны в JSON.
                        filename = 'RAZ_DS.json'
                        myfile = open(filename, mode='a+', encoding='utf-8')

                        json.dump(text, myfile, ensure_ascii=False)
                        myfile.close()

            for file in files:
                # Рекурсивно ищу файлы DBF.
                if file.endswith(('.dbf', '.DBF')) and file[3] == 'S':

                    dbf_file_puth = root + '/' + str(file)

                    # Открываю файл
                    db = DBF(dbf_file_puth, encoding='cp866')

                    for count, db_string in enumerate(db):

                        NOM_VD = db_string['NOM_VD']
                        NOM_SP = db_string['NOM_SP']
                        KAT_EDV1 = db_string['KAT_EDV1']
                        # Нужно читать из JSON

                        text = {OTD_SV:
                                    {'NOM_VD': NOM_VD,
                                     'data': []
                                     }
                                }
                        logging.debug(text)

    except FileNotFoundError:
        continue


