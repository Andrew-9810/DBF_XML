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

# # Создаю таблицу в памяти
# table = dbf.Table(
#         filename='test.dbf',
#         field_specs='NOM_VD C(8); SUM_VIP N(9,2); PR_SUM C(8); COD_NP C(2); K_SCH C(2); D_SP D',
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


import xml.etree.ElementTree as ET
from pathlib import Path

# path = Path('D:\Голованов\DBF_XML_inp\Конвертер2\ГКУ\ГКУ\OUT-700-Y-2023-ORG-052-050-000000-DCK-00000-DPT-00059-DCK-00000-DIS-050-DCK-00003-OUTNMB-0000000015.xml')
path = Path('D:\Голованов\DBF_XML_inp\Конвертер2\ЕДК\ЕДК\OUT-700-Y-2023-ORG-052-050-000000-DCK-00000-DPT-00059-DCK-00000-DIS-050-DCK-00001-OUTNMB-0000000001.xml')
root = ET.parse(f'{path}').getroot()

count = 0
# for tag in root.findall('ПачкаИсходящихДокументов/ЗАПОЛНЕННОЕ_ПОРУЧЕНИЕ_НА_ДОСТАВКУ_ГКУ'):
for element in root.findall('ПачкаИсходящихДокументов/ЗАПОЛНЕННОЕ_ПОРУЧЕНИЕ_НА_ДОСТАВКУ_ЕДК'):
    count += 1
    if element.find('НомерВыплатногоДела').text == '50165422':
        print(element.find('НомерВыплатногоДела').text, count)





    # value = tag.get('')
    # if value is not None:
    #     print(value)
#
