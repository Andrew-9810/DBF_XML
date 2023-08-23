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


ROOT = []
ROOT.append('50106400138')
ROOT.append('00138501064')


visited = set()
dup = {x for x in ROOT if x in visited or (visited.add(x) or False)}
print(dup)
