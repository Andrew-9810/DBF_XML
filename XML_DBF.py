import dbf
from dotenv import load_dotenv

import json
import logging
import os
from pathlib import Path
import xml.etree.ElementTree as ET
import time
import multiprocessing


DEBUG = True

load_dotenv()

PATH_XML_GKU = os.getenv('PATH_XML_GKU')
PATH_XML_EDK = os.getenv('PATH_XML_EDK')


# Настройка логирования
logging.basicConfig(
    # format='%(asctime)s - %(levelname)s - %(message)s',
    format='%(message)s',
    level=logging.DEBUG,
    filename='XML_DBF.log',
    filemode='w'
)


def create_DBF(filename):
    """Создает DBF файл."""
    table = dbf.Table(
        filename=filename,
        field_specs='NOM_VD C(8); SUM_VIP N(9,2); PR_SUM C(8); COD_NP C(2); K_SCH C(2); D_SP D',
        on_disk=True,
    )
    return table


def path_KAT_EDV_1(dir_name, name_file_dbf,
        path_XML, NOM_VD_recipient, SUM_VIP, PR_SUM):
    """Создает необходимые папки, пишет в файл DBF"""
    if not Path(dir_name).exists():
        """Создаю папку"""
        path = Path(dir_name)
        path.mkdir()
        # Проверяю существует ли файл
    path_result_DBF = f'{dir_name}/{name_file_dbf}'
    if not Path(f'{dir_name}/{name_file_dbf}').is_file():
        create_DBF(path_result_DBF)

    path_XML = Path(path_XML)
    root = ET.parse(f'{path_XML}').getroot()

    for element in root.findall(
            f'ПачкаИсходящихДокументов/ЗАПОЛНЕННОЕ_ПОРУЧЕНИЕ_НА_ДОСТАВКУ_{dir_name}'):

        if element.find('НомерВыплатногоДела').text == NOM_VD_recipient and \
                float(element.find('СуммаКдоставке').text) == SUM_VIP:
            logging.debug(f'NOM_VD: {NOM_VD_recipient}, SUM_VIP: {SUM_VIP}')
            # Пишу в файл
            table = dbf.Table(filename=path_result_DBF)
            table.open(dbf.READ_WRITE)

            if element.find('КодДоставки').text in ['1', '2', '3', '4', '5', '6', '7']:
                COD_NP = element.find('КодДоставки').text
            else:
                COD_NP = '8'

            Date = element.find('ДатаВыдачиДокумента').text
            year = Date[6:]
            month = Date[3:5]
            day = Date[0:2]
            D_SP = f'{year}{month}{day}'
            K_SCH = '01'

            for datum in (
                    (f'{NOM_VD_recipient}',
                     f'{SUM_VIP}',
                     f'{PR_SUM}',
                     f'{COD_NP}',
                     f'{K_SCH}',
                     dbf.Date.fromymd(f'{D_SP}')),
            ):
                table.append(datum)


with open('RAZ_DS.json', 'r', encoding='utf-8') as path_file:
    json_data = json.load(path_file)
    if DEBUG:
        # list_OTD = json_data['list_OTD_SV']
        # list_OTD_SV = []
        # list_OTD_SV.append(list_OTD[0])
        list_OTD_SV = ['004']
    else:
        list_OTD_SV = json_data['list_OTD_SV']

    func()
    # Для создания DBF в одной из папок ГКУ или ЕДК.
    for OTD in list_OTD_SV:
        # Получатели в отделении связи.
        recipients_OTD = json_data[OTD]
        len_recipients = len(recipients_OTD)
        for list_of_OTD_SV in range(len_recipients):
            # -->Номер выплатного дела получателя.
            NOM_VD_recipient = json_data[OTD][list_of_OTD_SV]['NOM_VD']
            list_data = len(json_data[OTD][list_of_OTD_SV]['data'])
            logging.debug('-' * 30)
            logging.debug(NOM_VD_recipient)
            logging.debug(list_data)
            # -->Получаю значение категории выплаты .
            for data in range(list_data):
                KAT_EDV1 = json_data[OTD][list_of_OTD_SV]['data'][data]['KAT_EDV1']
                PR_SUM = json_data[OTD][list_of_OTD_SV]['data'][data]['PR_SUM']
                SUM_VIP = json_data[OTD][list_of_OTD_SV]['data'][data]['SUM_VIP']

                logging.debug(f'OTD_SV: {OTD}, category: {KAT_EDV1}, SUMM: {SUM_VIP}')
                name_file_dbf = f'N{OTD}_02.dbf'
                # SUB в ГКУ, остальное в ЕДК
                if KAT_EDV1 == 'SUB':
                    dir_name = 'ГКУ'
                    path_KAT_EDV_1(dir_name, name_file_dbf,
                                   PATH_XML_GKU, NOM_VD_recipient, SUM_VIP, PR_SUM)

                else:

                    dir_name = 'ЕДК'
                    path_KAT_EDV_1(dir_name, name_file_dbf,
                                   PATH_XML_EDK, NOM_VD_recipient, SUM_VIP, PR_SUM)

if __name__ == "__main__":
    start = time.time()
    # узнаем количество ядер у процессора
    n_proc = multiprocessing.cpu_count()
    # вычисляем сколько циклов вычислений будет приходится
    # на 1 ядро, что бы в сумме получилось 80 или чуть больше
    calc = 80 // n_proc + 1
    processesed(n_proc, calc)
    end = time.time()
    print(f"Всего {n_proc} ядер в процессоре")
    print(f"На каждом ядре произведено {calc} циклов вычислений")
    print(f"Итого {n_proc * calc} циклов за: ", end - start)