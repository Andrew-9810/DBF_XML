# import json
#
# data = {}
#
# data['people'] = []
#
# data['dbf'].append({
#     'OTD_SV': '',
#     'value': '{NOM_VD: '',...}'
#
# })
#
# data['people'].append({
#     'name': 'Larry',
#     'website': 'pythonist.ru',
#     'from': 'Michigan'
# })
# data['people'].append({
#     'name': 'Tim',
#     'website': 'pythonist.ru',
#     'from': 'Alabama'
# })
# with open('RAZ_SD.json', 'w') as outfile:
#     json.dump(data, outfile)


# ROOT = []
# ROOT.append('50106400138')
# ROOT.append('00138501064')
#
#
# visited = set()
# dup = {x for x in ROOT if x in visited or (visited.add(x) or False)}
# print(dup)


# a = {'053', '095', '142', '063', '111', '065', '043', '083', '147', '117', '018', '123', '138', '069', '041', '101', '004', '016'}
# for i in a:
#     print(i)



# from pathlib import Path
#
# if not Path('ГКУ').exists():
#     path = Path('ГКУ')
#     path.mkdir()
#     print('+')
# else:
#     print("-")
#
# if Path(f'ГКУ/dbd.dbf').is_file():
#     print('Существует')
# else:
#     print('НЕсуществует')
#     Path(f'ГКУ/dbd.dbf').touch(mode=0o644)


# def createOrderAjax(request):
#     if request.method == 'POST':
#         goods = json.loads(request.body.decode('utf-8'))
#         kod = goods['massiv']['kod_klienta']
#
#         kontragent = User.objects.get(username=kod)  # Получаем клиента
#         order = Order.objects.create(  # Создаем заказ
#             client=kontragent,
#             payment_date=timezone.now(),
#             comment="Создано электронно",
#         )
#         # Ниже добавляем товары к заказу
#         for row in goods['massiv']['goods']:
#             product = Goods.objects.create(
#                 kod=row['kod'],
#                 name=row['name'],
#                 proizvod=row['proizvod'],
#                 srok=row['srok'],
#                 kol=row['kol'],
#                 flag=row['flag'],
#                 price=row['price'],
#                 rprice=row['rprice'],
#                 nds=row['nds'],
#                 comment=row['comment'],
#                 ean13=row['ean13'],
#                 order=order
#             )
#
#         # Формируем dbf и шлем заявку на сервер заявок
#         table = dbf.Table('or.dbf',
#                           'kod C(30); name C(200); proizvod C(100); srok C(10);  kol N(10, 0); quant N(10, 0); fasovka C(10); flag N(1, 0); price N(10, 2); rprice N(10, 2); nds N(2, 0); comment C(100); ean13 C(13)',
#                           codepage='cp866')
#         table.open()
#         for row in goods['massiv']['goods']:
#             datum = (row['kod'], row['name'], row['proizvod'], row['srok'],
#                      row['kol'], 0, '0', BoolNumeric(row['flag']), row['price'], row['rprice'],
#                      row['nds'], row['comment'], row['ean13'])
#             table.append(datum)
#         table.close()
#
#     return JsonResponse({'msg': order.pk})
#
#
# def BoolNumeric(logic):
#     if logic == 'true':
#         return 1
#     else:
#         return 0
# ===========================================================================
# from dbfpy import dbf
#
# # Определяем набор полей файла. C — строка, N — число, D — дата, L — булево.
# # Для строк нужно указать длину, для чисел — количество разрядов целой и дробной частей.
#
#
# dbf = dbf.Dbf("dbfile.dbf", new=True)
# dbf.addField(
#     ("NAME", "C", 15),
#     ("SURNAME", "C", 25),
#     ("INITIALS", "C", 10),
#     ("BIRTHDATE", "D"),
# )
#
# for (n, s, i, b) in (
#         ("John", "Miller", "YC", (1980, 10, 11)),
#         ("Andy", "Larkin", "", (1980, 4, 11)),
# ):
#     rec = dbf.newRecord()
#     rec["NAME"] = n
#     rec["SURNAME"] = s
#     rec["INITIALS"] = i
#     rec["BIRTHDATE"] = b
#     rec.store()
# dbf.close()

# import dbfpy3
# header = dbfpy3.header()
# header.add_field(("name", "C", 10))



# import datetime
# import dbf
#
# # Создаю таблицу в памяти
# table = dbf.Table(
#         filename='test',
#         field_specs='name C(25); age N(3,0); birth D; qualified L',
#         on_disk=False,
#         )
# #
# table.open(dbf.READ_WRITE)
#
# # добавьте в него несколько записей
# for datum in (
#         ('Spanky', 7, dbf.Date.fromymd('20010315'), False),
#         ('Spunky', 23, dbf.Date(1989, 7, 23), True),
#         ('Sparky', 99, dbf.Date(), dbf.Unknown),
#         ):
#     table.append(datum)
#     print(f'Печатаю: {table}')
#     print('#' * 15)
#
# # выполните итерацию по таблице и распечатайте записи
# for record in table:
#     print(record)
#     print('###--------')
#     print(record[0:3])
#     print([record.name, record.age, record.birth])
#     print('###--------#')
#
#
#
# # сделайте копию тестовой таблицы (структура, а не данные)
# custom = table.new(
#         filename='test_on_disk.dbf',
#         default_data_types=dict(C=dbf.Char, D=dbf.Date, L=dbf.Logical),
#         )
#
# # автоматически открывается и закрывается
# with custom:
#     # копирование записей из тестового в пользовательский
#     for record in table:
#         custom.append(record)
#     print(custom)
#     # измените каждую запись в пользовательском режиме (можно было бы сделать это на предыдущем шаге)
#     for record in custom:
#         dbf.write(record, name=record.name.upper())
#         # и распечатайте измененную запись
#         print(record)
#         print('***--------')
#         print(record[0:3])
#         print([record.name, record.age, record.birth])
#         print('***--------*')
#
# table.close()

#
# import datetime
# import dbf
#
# # Создаю таблицу в памяти
# table = dbf.Table(
#         filename='RAZ_Dtest.dbf',
#         field_specs=('N_UCH C(3); NOM_VD C(8); IST_SR C(2); FAM C(30);'
#                      ' IMJA C(20); OTCH C(30); OTD_SV C(3); GOR C(3); ULICA C(3);'
#                      ' DOM C(6); KORPUS C(2); KVART C(9); DOS_UCH C(2); DAT_VIP C(2);'
#                      ' TIP_D C(2)'),
#         on_disk=True,
#         )
# #
# table.open(dbf.READ_WRITE)
#
# # добавьте в него несколько записей
# for datum in (
#         ('Spanky', 7, dbf.Date.fromymd('20010315'), False),
#         ('Spunky', 23, dbf.Date(1989, 7, 23), True),
#         ('Sparky', 99, dbf.Date(), dbf.Unknown),
#         ):
#     table.append(datum)
#     print(f'Печатаю: {table}')
#     print('#' * 15)


# import xml.etree.ElementTree as ET
# from pathlib import Path
#
# # path = Path('D:\Голованов\DBF_XML_inp\Конвертер2\ГКУ\ГКУ\OUT-700-Y-2023-ORG-052-050-000000-DCK-00000-DPT-00059-DCK-00000-DIS-050-DCK-00003-OUTNMB-0000000015.xml')
# path = Path('D:\Голованов\DBF_XML_inp\Конвертер2\ЕДК\ЕДК\OUT-700-Y-2023-ORG-052-050-000000-DCK-00000-DPT-00059-DCK-00000-DIS-050-DCK-00001-OUTNMB-0000000001.xml')
# root = ET.parse(f'{path}').getroot()
#
# count = 0
# # for tag in root.findall('ПачкаИсходящихДокументов/ЗАПОЛНЕННОЕ_ПОРУЧЕНИЕ_НА_ДОСТАВКУ_ГКУ'):
# for element in root.findall('ПачкаИсходящихДокументов/ЗАПОЛНЕННОЕ_ПОРУЧЕНИЕ_НА_ДОСТАВКУ_ЕДК'):
#     count += 1
#     if element.find('НомерВыплатногоДела').text == '50165422':
#         print(element.find('НомерВыплатногоДела').text, count)

# x = int(input())
# if x in [1, 2, 3, 4, 5, 6, 7]:
#     print("True")
# else:
#     print("False")

# import json
#
# list_OTD_SV = ['004']
#
# with open('RAZ_DS.json', 'r', encoding='utf-8') as path_file:
#     """Пути до файлов RAZD.dbf, RAZS.dbf"""
#     json_data = json.load(path_file)
#     # Для создания DBF в одной из папок ГКУ или ЕДК.
#     for OTD in list_OTD_SV:
#         # Получатели в отделении связи.
#         recipients_OTD = json_data[OTD]
#         len_recipients = len(recipients_OTD)
#         # Прохожусь по списку
#
#         for val in recipients_OTD:
#             print(val)
        # for list_of_OTD_SV in range(len_recipients):
        #     # -->Номер выплатного дела получателя.
        #     print(list_of_OTD_SV)
        #     NOM_VD_recipient = json_data[OTD][list_of_OTD_SV]['NOM_VD']
        #     print(NOM_VD_recipient)
            # list_data = len(json_data[OTD][list_of_OTD_SV]['data'])
            #
            # # -->Получаю значение категории выплаты .
            # for data in range(list_data):
            #     KAT_EDV1 = json_data[OTD][list_of_OTD_SV]['data'][data]['KAT_EDV1']
            #     PR_SUM = json_data[OTD][list_of_OTD_SV]['data'][data]['NOM_SP']
            #     SUM_VIP = json_data[OTD][list_of_OTD_SV]['data'][data]['SUM_VIP']

                #
                # name_file_dbf = f'N{OTD}_02.dbf'



#
# import os
# from dotenv import load_dotenv
# from pathlib import Path
#
#
# load_dotenv()
#
# INPUT_DATA_PUTH = os.getenv('INPUT_DATA_PUTH')
# p = Path(INPUT_DATA_PUTH)
# path_dir = p / 'Входящие файлы'
# print(path_dir)
# list_name = os.listdir(path=path_dir)
# print(list_name)


#
# def data_dir_actual(path_dir):
#     """Ищет в имени папок дату и отдает последнюю."""
#     list_name = os.listdir(path=path_dir)
#     # Самая минимальная дата для сравнения.
#     data_actual = datetime.date(datetime.MINYEAR, 1, 1)
#     for name_dir in list_name:
#         try:
#             # Получение даты из имени папки.
#             list_data = name_dir.split('.')
#             year = int(list_data[2])
#             month = int(list_data[1])
#             day = int(list_data[0])
#             date_obj = datetime.date(year, month, day)
#
#             # Вычисляю свежую дату.
#             if data_actual < date_obj:
#                 data_actual = date_obj
#             # Ловлю ошибки на случай присутсвия не даты в имени.
#         except ValueError and IndexError:
#             continue
#
#     list_data_actual = str(data_actual).split('-')
#     return f'{list_data_actual[2]}.{list_data_actual[1]}.{list_data_actual[0]}'
#
#
#
#
# # Настройка логирования
# logging.basicConfig(
#     # format='%(asctime)s - %(levelname)s - %(message)s',
#     format='%(message)s',
#     level=logging.DEBUG,
#     filename='DBF_JSON.log',
#     filemode='w'
# )
#
# with open('PATH_DB.json', 'r', encoding='utf-8') as path_file:
#     """Пути до файлов RAZD.dbf, RAZS.dbf"""
#     connect_data = json.load(path_file)
#     path_dir_root = connect_data['path']
#     print(path_dir_root)
#
# # Получаю список УСЗН для поиска в папках.
# dist_helper = pd.read_excel(f'{path_dir_root}\\dist_helper.xlsx')
# list_USZN_name = dist_helper['title'].tolist()
#
# ROOT_D = {}
# set_OTD_SV = set()
# COUNT = 1
# count = 1
#
# for name in list_USZN_name:
#     # Прохожу по папкам с наименованиями УСЗН текущей датой.
#     path_dir_iter_test = f'{path_dir_root}\\Входящие файлы\\{name}'
#
#     # Вызов функции поиска свежей даты
#     try:
#         Data_dir = data_dir_actual(path_dir_iter_test)
#     except FileNotFoundError:
#         continue
#
#     print(Data_dir)
#======================================================
# Однопоточчный
# import time
#
# def heavy(n):
#     for x in range(1, n):
#         for y in range(1, n):
#             x**y
#
# def sequential(n):
#     for i in range(n):
#         heavy(500)
#     print(f"{n} циклов вычислений закончены")
#
# if __name__ == "__main__":
#     start = time.time()
#     sequential(80)
#     end = time.time()
#     print("Общее время работы: ", end - start)
#
# # 80 циклов вычислений закончены
# # Общее время работы:  23.573118925094604

# import threading
# import time
#
#
# def heavy(n, i, thead):
#     for x in range(1, n):
#         for y in range(1, n):
#             x ** y
#     print(f"Цикл № {i}. Поток {thead}")
#
#
# def sequential(calc, thead):
#     print(f"Запускаем поток № {thead}")
#     for i in range(calc):
#         heavy(500, i, thead)
#     print(f"{calc} циклов вычислений закончены. Поток № {thead}")
#
#
# def threaded(theads, calc):
#     # theads - количество потоков
#     # calc - количество операций на поток
#
#     threads = []
#
#     # делим вычисления на `theads` потоков
#     for thead in range(theads):
#         t = threading.Thread(target=sequential, args=(calc, thead))
#         threads.append(t)
#         t.start()
#
#     # Подождем, пока все потоки
#     # завершат свою работу.
#     for t in threads:
#         t.join()
#
#
# if __name__ == "__main__":
#     start = time.time()
#     # разделим вычисления на 4 потока
#     # в каждом из которых по 20 циклов
#     threaded(4, 20)
#     end = time.time()
#     print("Общее время работы: ", end - start)
#
# # Показано часть вывода
# # ...
# # ...
# # ...
# # Общее время работы:  43.33752250671387


import multiprocessing
import time


def heavy(n, i, proc):
    for x in range(1, n):
        for y in range(1, n):
            x ** y
    print(f"Цикл № {i} ядро {proc}")


def sequential(calc, proc):
    print(f"Запускаем поток № {proc}")
    for i in range(calc):
        heavy(500, i, proc)
    print(f"{calc} циклов вычислений закончены. Процессор № {proc}")


def processesed(procs, calc):
    # procs - количество ядер
    # calc - количество операций на ядро

    processes = []

    # делим вычисления на количество ядер
    for proc in range(procs):
        p = multiprocessing.Process(target=sequential, args=(calc, proc))
        processes.append(p)
        p.start()

    # Ждем, пока все ядра
    # завершат свою работу.
    for p in processes:
        p.join()


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