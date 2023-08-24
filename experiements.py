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


a = {'053', '095', '142', '063', '111', '065', '043', '083', '147', '117', '018', '123', '138', '069', '041', '101', '004', '016'}
for i in a:
    print(i)