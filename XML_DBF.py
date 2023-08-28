import json
import logging
from pathlib import Path
import dbf
import xml.etree.ElementTree as ET


DEBUG = True

# Настройка логирования
logging.basicConfig(
    # format='%(asctime)s - %(levelname)s - %(message)s',
    format='%(message)s',
    level=logging.DEBUG,
    filename='main.log',
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


if DEBUG:
    list_OTD_SV = ['004']
else:
    list_OTD_SV = ['053', '016', '069', '065', '111', '147', '018', '142', '117', '138', '041', '063', '095', '083', '004', '123', '101', '043']


with open('RAZ_DS.json', 'r', encoding='utf-8') as path_file:
    """Пути до файлов RAZD.dbf, RAZS.dbf"""
    json_data = json.load(path_file)
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
                PR_SUM = json_data[OTD][list_of_OTD_SV]['data'][data]['NOM_SP']
                SUM_VIP = json_data[OTD][list_of_OTD_SV]['data'][data]['SUM_VIP']

                logging.debug(f'category: {KAT_EDV1}, SUMM: {SUM_VIP}')
                name_file_dbf = f'N{OTD}_02.dbf'
                # SUB в ГКУ, остальное в ЕДК
                if KAT_EDV1 == 'SUB':
                    # Проверяю существует ли папка
                    if not Path('ГКУ').exists():
                        """Создаю папку"""
                        path = Path('ГКУ')
                        path.mkdir()
                    # Проверяю существует ли файл
                    if not Path(f'ГКУ/{name_file_dbf}').is_file():
                        create_DBF(f'ГКУ/{name_file_dbf}')

                    path = Path(
                        'D:\Голованов\DBF_XML_inp\Конвертер2\ГКУ\ГКУ\OUT-700-Y-2023-ORG-052-050-000000-DCK-00000-DPT-00059-DCK-00000-DIS-050-DCK-00003-OUTNMB-0000000015.xml'
                    )
                    root = ET.parse(f'{path}').getroot()

                    for element in root.findall('ПачкаИсходящихДокументов/ЗАПОЛНЕННОЕ_ПОРУЧЕНИЕ_НА_ДОСТАВКУ_ГКУ'):

                        if element.find('НомерВыплатногоДела').text == NOM_VD_recipient and float(element.find('СуммаКдоставке').text) == SUM_VIP:
                            logging.debug(f"НАШЕЛСЯ! {element.find('НомерВыплатногоДела').text}")

                    # Пишу в файл
                    table = dbf.Table(filename=f'ГКУ/{name_file_dbf}')
                    table.open(dbf.READ_WRITE)

                    # Забираю из XML
                    COD_NP = '0'
                    K_SCH = '01'

                    for datum in (
                            # XML
                            (f'{NOM_VD_recipient}',
                             # XML
                             f'{SUM_VIP}',
                             f'{PR_SUM}',
                             f'{COD_NP}',
                             f'{K_SCH}',
                            # XML
                             dbf.Date.fromymd('20010315')),
                    ):
                        table.append(datum)

                else:
                    # Проверяю существует ли папка
                    if not Path('ЕДК').exists():
                        """Создаю папку"""
                        path = Path('ЕДК')
                        path.mkdir()
                    # Проверяю существует ли файл
                    if not Path(f'ЕДК/{name_file_dbf}').is_file():
                        create_DBF(f'ЕДК/{name_file_dbf}')

                    # path = Path('D:\Голованов\DBF_XML_inp\Конвертер2\ЕДК\ЕДК\OUT-700-Y-2023-ORG-052-050-000000-DCK-00000-DPT-00059-DCK-00000-DIS-050-DCK-00001-OUTNMB-0000000001.xml')
                    # root = ET.parse(f'{path}').getroot()
                    # Пишу в файл
                    table = dbf.Table(filename=f'ЕДК/{name_file_dbf}')
                    table.open(dbf.READ_WRITE)
                    # Забираю из XML
                    COD_NP = '0'
                    K_SCH = '01'

                    for datum in (
                            (f'{NOM_VD_recipient}',
                             f'{SUM_VIP}',
                             f'{PR_SUM}',
                             f'{COD_NP}',
                             f'{K_SCH}',
                             dbf.Date.fromymd('20010315')),
                    ):
                        table.append(datum)
