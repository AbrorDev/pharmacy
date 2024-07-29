import requests
import json

BASE_URL = 'http://127.0.0.1:8000/drugs'

def get_data(part_url, params=None, part=None, duplicate=True):
    url = f'{BASE_URL}/{part_url}/'
    response = requests.get(url=url, params=params).text
    data = json.loads(response)

    if part:
        new_data = []
        for i in data:
            if duplicate == False and i[part] not in new_data:
                new_data.append(i[part])
            elif duplicate:
                new_data.append(i[part])
        return new_data
    return data

def post_user(tg_id, is_admin=False, is_owner=False):
    url = f'{BASE_URL}/Telegran%20Users/'
    user = get_data(part_url='Telegran%20Users')
    user_exist = False
    for i in user:
        user_exist = user_exist or i['tg_id'] == tg_id
    if user_exist == False:
        data = {
            'tg_id': tg_id,
            'is_admin':is_admin,
            'is_owner':is_owner
        }
        post = requests.post(url=url, data=data)
    return

def update_user(tg_id, is_admin, is_owner):
    data = get_data(part_url='Telegran%20Users')
    user_id = 0
    for i in data:
        if i['tg_id'] == tg_id:
            user_id = i['id']
    updated_data = {
        'is_admin':is_admin,
        'is_owner':is_owner
    }
    url = f'{BASE_URL}/Telegran%20Users/{user_id}/'
    response = requests.patch(url=url, json=updated_data)
    return

def post_pharmacy(name, owner, phone, location_latitute, location_longitude):
    url = f'{BASE_URL}/Pharmacy/'
    pharmacy = get_data(part_url='Pharmacy')
    user = get_data(part_url='Telegran%20Users')
    user_id = 0
    is_admin = False
    for i in user:
        if i['tg_id'] == owner:
            user_id = i['id']
            is_admin = i['is_admin']

    exist_pharmacy = False
    for i in pharmacy:
        exist_pharmacy = exist_pharmacy or i['owner'] == owner
    if exist_pharmacy == False:
        data = {
            'name':name,
            'owner':user_id,
            'contact':phone,
            'location_latitute':location_latitute,
            'location_longitude':location_longitude
        }
        post = requests.post(url=url, data=data)
        update_user(owner, is_admin=is_admin, is_owner=True)
        return 'Dorixona muvafaqqiyatli yaratilindi. Sizga bir necha kunda aloqaga chiqamiz...'
    return 'Siz yana dorixona yarata olmaysiz...'

def update_pharmacy(owner, which_part, value):
    name = ''
    phone = ''
    location_latitute = ''
    location_longitude = ''
    pharmacy = get_data(part_url='Pharmacy/filter', params={'owner':owner})[0]
    pharmacy_id = 0
    pharmacy_id = pharmacy['id']
    name = pharmacy['name']
    phone = pharmacy['contact']
    location_latitute = pharmacy['location_latitute']
    location_longitude = pharmacy['location_longitude']
    if which_part == 'name':
        name = value
    elif which_part == 'phone':
        phone = value
    elif which_part == 'location':
        location_latitute = value[0]
        location_longitude = value[1]
    data = {
        'name':name,
        'contact':phone,
        'location_latitute':location_latitute,
        'location_longitude':location_longitude
    }
    url = f'{BASE_URL}/Pharmacy/{pharmacy_id}/'
    post = requests.patch(url=url, json=data)
    return "O'zgarishlar muvafaqqiyatli amalga oshirilindi..."


# dori qo'shilishi
def add_to_store(pharmacy_id, product_id, special_code, price):
    url = f'{BASE_URL}/Store/'
    product_store = get_data(part_url='Store')
    product_exist = False
    for i in product_store:
        if i['pharmacy']==pharmacy_id and i['product'] == product_id:
            product_exist = True

    if product_exist == False:
        data = {
            'pharmacy':pharmacy_id,
            'product':product_id,
            'special_code':special_code,
            'price':price
        }
        post = requests.post(url=url, data=data)
        return 'Mahsulot muvafaqqiyatli qo\'shildi...'
    return 'Mahsulot allaqachon omborda mavjud...'

def update_store_product(pharmacy, drug, which_part, value):
    special_code = ''
    price = ''
    pharmacy = get_data(part_url='Store/filter', params={'pharmacy':pharmacy, 'product_id':drug})[0]
    product_id = pharmacy['id']
    special_code = pharmacy['special_code']
    price = pharmacy['price']
    if which_part == 'specail_code':
        special_code = value
    elif which_part == 'price':
        price = value
    data = {
        'special_code':special_code,
        'price':price,
    }
    url = f'{BASE_URL}/Store/{product_id}/'
    update = requests.patch(url=url, json=data)
    return "O'zgarishlar muvafaqqiyatli amalga oshirilindi..."

def delete_store_product(pharmacy, drug):
    pharmacy = get_data(part_url='Store/filter', params={'pharmacy':pharmacy, 'product_id':drug}, part='id')[0]

    url = f'{BASE_URL}/Store/{pharmacy}/'
    delete = requests.delete(url=url)

    return 'Muvafaqqiyatli o\'chirilindi...'