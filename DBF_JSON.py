import pandas as pd
from dbfread import DBF
from dotenv import load_dotenv

import json
import logging
import os
import datetime
from pathlib import Path

load_dotenv()

INPUT_DATA_PUTH = os.getenv('INPUT_DATA_PUTH')
GUIDE = os.getenv('GUIDE')


# Настройка логирования
logging.basicConfig(
    # format='%(asctime)s - %(levelname)s - %(message)s',
    format='%(message)s',
    level=logging.DEBUG,
    filename='DBF_JSON.log',
    filemode='w'
)


def data_dir_actual(path_dir):
    """Ищет в имени папок дату и отдает последнюю."""
    list_name = os.listdir(path=path_dir)
    # Самая минимальная дата для сравнения.
    data_actual = datetime.date(datetime.MINYEAR, 1, 1)
    for name_dir in list_name:
        try:
            # Получение даты из имени папки.
            list_data = name_dir.split('.')
            yrar = int(list_data[2])
            month = int(list_data[1])
            day = int(list_data[0])
            date_obj = datetime.date(yrar, month, day)

            # Вычисляю свежую дату.
            if data_actual < date_obj:
                data_actual = date_obj
            # Ловлю ошибки на случай присутсвия не даты в имени.
        except ValueError and IndexError:
            continue
    list_data_actual = str(data_actual).split('-')
    return f'{list_data_actual[2]}.{list_data_actual[1]}.{list_data_actual[0]}'

def main():
    """Точка входа в программу."""
    # Получаю список УСЗН для поиска в папках.
    dist_helper = pd.read_excel(f'{GUIDE}')
    list_USZN_name = dist_helper['title'].tolist()
    logging.debug(f'Список УСЗН получен: {list_USZN_name}')

    ROOT_D = {}
    set_OTD_SV = set()
    COUNT = 1
    count = 1

    for name in list_USZN_name:
        # Прохожу по папкам с наименованиями УСЗН текущей датой.
        root = Path(INPUT_DATA_PUTH)
        path_dir = root / 'Входящие файлы' / name

        try:
            Data_dir = data_dir_actual(path_dir)
        except FileNotFoundError:
            continue

        path_dir_iter = path_dir / Data_dir
        logging.debug(f'Путь для поиска: {path_dir_iter}')
        '''
        Изначально прохожу по файлам RAZD чтоб сформировать шаблон с данными, 
        и затем добавлять в этот шаблон данные RAZS
        '''
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

                            # Проверка на существование записи
                            try:
                                tmp_list = ROOT_D[OTD_SV]
                                tmp_list.append(recipient)
                                ROOT_D[OTD_SV] = tmp_list
                            except KeyError:
                                ROOT_D[OTD_SV] = [recipient]
                            # Пишу данныe в список
                            set_OTD_SV.add(OTD_SV)

            list_OTD_SV = list(set_OTD_SV)
            ROOT_D['list_OTD_SV'] = list_OTD_SV

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
                            PR_SUM = db_string['PR_SUM']
                            KAT_EDV1 = db_string['KAT_EDV1']
                            SUM_VIP = db_string['SUM_VIP']

                            payment = {
                                'PR_SUM': PR_SUM,
                                'KAT_EDV1': KAT_EDV1,
                                'SUM_VIP': SUM_VIP
                            }

                            for OTD in list_OTD_SV:
                                len_list = len(ROOT_D[OTD])
                                for iter in range(len_list):
                                    if ROOT_D[OTD][iter]['NOM_VD'] == NOM_VD:
                                        ROOT_D[OTD][iter]['data'].append(
                                            payment)
                                        logging.debug(
                                            f'Отработано: {COUNT}'
                                            f' NOM_VD: {NOM_VD}'
                                        )

                                        COUNT += 1
        except FileNotFoundError:
            continue

    logging.debug(ROOT_D)
    filename = 'RAZ_DS.json'
    myfile = open(filename, mode='w', encoding='utf-8')
    json.dump(ROOT_D, myfile, ensure_ascii=False, indent=4)
    myfile.close()


if __name__ == '__main__':
    main()
