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
            logging.debug(f'root: {root} dirs: {dirs} files: {files}')

            for file in files:
                # Рекурсивно ищу файлы DBF.
                if file.endswith(('.dbf', '.DBF')) and file[3] == 'D':
                    dbf_file_puth = root + '/' + str(file)
                    logging.debug(dbf_file_puth)
                    # Открываю файл
                    db = DBF(dbf_file_puth, encoding='cp866')
                    for _, db_string in enumerate(db):
                        NOM_VD = db_string['NOM_VD']
                        OTD_SV = db_string['OTD_SV']
                        recipient = {'NOM_VD': NOM_VD, 'data': []}
                        logging.debug(f'создано: {count}')
                        count += 1

                        try:
                            tmp_list = ROOT_D[OTD_SV]
                            tmp_list.append(recipient)
                            ROOT_D[OTD_SV] = tmp_list
                        except KeyError:
                            ROOT_D[OTD_SV] = [recipient]
                        # Пишу данныe в список
                        set_OTD_SV.add(OTD_SV)


        list_OTD_SV = list(set_OTD_SV)
        for root, dirs, files in os.walk(path_dir_iter):
            logging.debug('*' * 50)
            logging.debug(f'root: {root} dirs: {dirs} files: {files}')
            for file in files:

                # Рекурсивно ищу файлы DBF.
                if file.endswith(('.dbf', '.DBF')) and file[3] == 'S':

                    dbf_file_puth = root + '/' + str(file)
                    logging.debug(dbf_file_puth)
                    # Открываю файл
                    db = DBF(dbf_file_puth, encoding='cp866')

                    for _, db_string in enumerate(db):

                        NOM_VD = db_string['NOM_VD']
                        NOM_SP = db_string['NOM_SP']
                        KAT_EDV1 = db_string['KAT_EDV1']
                        SUM_VIP = db_string['SUM_VIP']

                        payment = {
                            'NOM_SP': NOM_SP,
                            'KAT_EDV1': KAT_EDV1,
                            'SUM_VIP': SUM_VIP
                        }

                        for OTD in list_OTD_SV:
                            len_list = len(ROOT_D[OTD])
                            for iter in range(len_list):
                                if ROOT_D[OTD][iter]['NOM_VD'] == NOM_VD:
                                    ROOT_D[OTD][iter]['data'].append(payment)
                                    logging.debug(f'Отработано: {COUNT} NOM_VD: {NOM_VD}')

                                    COUNT += 1
    except FileNotFoundError:
        continue


logging.debug(ROOT_D)

# После отработки программы мы записываем в путь отработанный архив.
filename = 'RAZ_DS.json'
myfile = open(filename, mode='w', encoding='utf-8')
json.dump(ROOT_D, myfile, ensure_ascii=False)
myfile.close()