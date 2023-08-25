import json
import logging
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    # format='%(asctime)s - %(levelname)s - %(message)s',
    format='%(message)s',
    level=logging.DEBUG,
    filename='main.log',
    filemode='w'
)



# list_OTD_SV = ['053', '016', '069', '065', '111', '147', '018', '142', '117', '138', '041', '063', '095', '083', '004', '123', '101', '043']
list_OTD_SV = ['004']
with open('RAZ_DS.json', 'r', encoding='utf-8') as path_file:
    """Пути до файлов RAZD.dbf, RAZS.dbf"""
    json_data = json.load(path_file)
    # Для создания DBF в одной из папок ГКУ или ЕДК
    for OTD in list_OTD_SV:

        recipients_OTD = json_data[OTD]
        len_recipients = len(recipients_OTD)
        for list_of_OTD_SV in range(len_recipients):
            NOM_VD_recipient = json_data[OTD][list_of_OTD_SV]['NOM_VD']
            list_data = len(json_data[OTD][list_of_OTD_SV]['data'])
            logging.debug('-' * 30)
            logging.debug(NOM_VD_recipient)
            logging.debug(list_data)
            for data in range(list_data):
                KAT_EDV1 = json_data[OTD][list_of_OTD_SV]['data'][data]['KAT_EDV1']
                logging.debug(KAT_EDV1)
                name_file_dbf = f'N{OTD}_02.dbf'
                # Проверить наличие дир далее создать
                if KAT_EDV1 == 'SUB':
                    if not Path('ГКУ').exists():
                        path = Path('ГКУ')
                        path.mkdir()
                    if not Path(f'ГКУ/{name_file_dbf}').is_file():
                        Path(f'ГКУ/{name_file_dbf}').touch(mode=0o644)
                else:
                    if not Path('ЕДК').exists():
                        path = Path('ЕДК')
                        path.mkdir()
                    if not Path(f'ЕДК/{name_file_dbf}').is_file():
                        Path(f'ЕДК/{name_file_dbf}').touch(mode=0o644)
