from pymongo import MongoClient
from django.conf import settings

def get_db_handle(db_name, host, port=None, username=None, password=None):
    client = MongoClient(host=host)
    db_handle = client[db_name]
    return db_handle, client


def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]

def special_characters(s):
    specialRe = ['.', '+', '*', '?', '^', '$', '(', ')', '[', ']', '{', '}', '|', "\\"]
    qs = str()
    for element in range(0, len(s)):
        if s[element] in specialRe :
            qs += f"\{s[element]}"
        else:
            qs += s[element]
    return qs

def count_categories(collection):
    categories = {
        'ข้าวเปลือก':'Paddy rice',
        'ข้าวกล้อง':'Unmilled rice',
        'ข้าวสาร':'Milled rice',
        'ข้าวนึ่ง':'Parboiled rice',
        'ข้าวกล้องงอก':'Germinated rice',
        'ข้าวเม่า':'Milk-stage rice',
        'ข้าวขาวสุก':'Cooked white rice'
    }
    rice_categories_count = {
            'Paddy rice':0,
            'Unmilled rice':0,
            'Milled rice':0,
            'Parboiled rice':0,
            'Germinated rice':0,
            'Milk-stage rice':0,
            'Cooked white rice':0
        }
    all_data = collection

    for item in all_data:
        for phy in item['Physical']:
            rice_cat = phy['riceCategories']
            if rice_cat:
                rice_categories_count[categories[rice_cat]] += 1

    return rice_categories_count

def get_data_from_mongo(pk, fieldGroup):
    fileldCase = {'Sampleinfo': 'Sample info','Physical': 'Physical properties', 'Chemical': 'Chemical properties', 'Nutrition': 'Nutrition', 'Bioactive': 'Bioactive compounds'}
    db, _ = get_db_handle(settings.DB_NAME, settings.HOST_MONGODB )
    collection = get_collection_handle(db, settings.COLLECTION_NAME)
    cursor = collection.find({"cropSampleID":pk})
    collection_meta = get_collection_handle(db, settings.COLLECTION_NAME_META)
    meta_data = collection_meta.find().sort("fieldID", 1)
    meta_s = list()
    for item in meta_data:
        if item['fieldGroup'] == fileldCase[fieldGroup]:
            meta_s.append(item)

    meta_s.sort(key=lambda x: x['fieldID'])
    meta = []
    units = []
    for item in meta_s:
        meta.append(item['fieldNameUIEN'])
        units.append(item['units'])
    list_cur = list(cursor)

    for item in list_cur:
            coll = item[fieldGroup]
            physical = item['Physical']

    list_item = list()

    for item, itemPh in zip(coll, physical):
        item.pop('nutritionDBID')
        item.pop('cropSampleID')
        categories = dict()
        if itemPh['riceCategories']:
            categories['Rice categories'] = {'value':itemPh['riceCategories'],'unit':None}
        for key, value, unit in zip(meta, item.values(),units):
            if value:
                categories[key] = {'value':value,'unit':unit}
        if len(categories) > 1:
            list_item.append(categories)

    return list_item

def get_sample_data(pk):
    db, _ = get_db_handle(settings.DB_NAME, settings.HOST_MONGODB )
    collection = get_collection_handle(db, settings.COLLECTION_NAME)
    cursor = collection.find({"cropSampleID":pk})
    collection_meta = get_collection_handle(db, settings.COLLECTION_NAME_META)
    meta_data = collection_meta.find().sort("fieldID", 1)
    meta_s = list()
    for item in meta_data:
        if item['fieldGroup'] == 'Sample info':
            meta_s.append(item)
    meta_s.sort(key=lambda x: x['fieldID'])
    meta = []
    list_cur = list(cursor)
    for item in list_cur:
        coll = item["Sampleinfo"]

    for item in meta_s:
        meta.append(item['fieldNameUIEN'])
    list_item = list()
    categories = dict()
    meta.pop(0)
    for name, key, value in zip(meta, coll.keys(), coll.values()):
        if value:
            categories[name] = value
    if categories:
        list_item.append(categories)
    return list_item

def adcanced_search_form():
    pass
