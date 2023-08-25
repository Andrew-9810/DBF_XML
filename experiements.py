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

import dbfpy3
header = dbfpy3.header()
header.add_field(("name", "C", 10))

