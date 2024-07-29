import math

from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_location import SendLocation

import appbot.keyboards as kb
from appbot.states import SearchState, PharmacyState
from appbot.config import ADMINS, OWNERS
from appbot import api

router = Router()

@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(text=f'{message.photo[-1].file_id}')

@router.message(CommandStart())
async def start(message: Message):
    api.post_user(message.from_user.id)
    await message.answer('Assalomu aleykum. "Dori izlash" botimizga xush kelibsiz', reply_markup=kb.main)

@router.message(Command('help'))
async def help(message: Message):
    text = 'Sizga qanday yordam kerak?'
    if message.from_user.id in OWNERS:
        text += f"""\n\n/settings - sozlamalar
/pharmacy - dorixonadagi dorilar ma'lumotlari"""
    elif message.from_user.id in ADMINS:
        text += f'\n\n/admin - admin paneli'
    text += '\n\nOperatorlarimiz bilan bog\'lanish uchun: +998900200174'
    await message.answer(text=text)

# dorini izlash
@router.message(F.text=='🔍Dori izlash')
async def search_drug(message: Message, state: FSMContext):
    await state.set_state(SearchState.drug)
    await message.answer("Dorini nomini kiriting:")

@router.message(SearchState.drug)
async def drug_state(message: Message, state: FSMContext):
    await state.update_data(drug=message.text)
    drug = api.get_data(part_url='Store/filter', params={'product':message.text})
    if drug:
        await state.set_state(SearchState.condition)
        await message.answer("Dorini qaysi tartibda chiqaray?",reply_markup=kb.condition)
    else:
        await message.answer("Siz izlagan dori dorixonalarda mavjud emas...")
        await state.clear()

# Narxi bo'yicha
@router.callback_query(SearchState.condition)
async def drug_condition(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'price':
        await state.update_data(condition=callback.data)
        data = await state.get_data()
        
        pharmacies = api.get_data(part_url='Store/filter', params={'product':data['drug']})

        drug = api.get_data(part_url='Product/filter', params={'name':data['drug']})[0]
        info = f'''Nomi: {drug['name']}
Ishlab chiqaruvchi: {drug['company'][0]}, {drug['company'][1]}
Dori shakli: {drug['type_name']}
Farmakoterapevtik guruhi: {drug['pharma_group']}
Yaroqlilik muddati: {drug['validity_date']}
Dori haqida:
{drug['description']}'''
        await callback.message.answer_photo(drug['image'])
        await callback.message.answer(text=info)
        
        data = []
        for i in pharmacies:
            pharmacy = api.get_data(part_url='Pharmacy/filter', params={'name':i['pharmacy']})[0]
            
            pharmacy_info = f'''Dorixona: {pharmacy['name']}
Kontakt: {pharmacy['contact']}
Dorining narxi: {i['price']}
            '''
            await callback.message.answer_location(pharmacy['location_latitute'], pharmacy['location_longitude'])
            await callback.message.answer(text=pharmacy_info)
        await state.clear()
    else:
        await state.set_state(SearchState.distance)
        await callback.message.answer('Lokatsiyangizni yuboring:', reply_markup=kb.distance)

# lokatsiya
@router.message(SearchState.distance)
async def drug_location(message: Message, state: FSMContext):
    await state.update_data(distance=[message.location.latitude, message.location.longitude])
    data = await state.get_data()
    latitude = data['distance'][0]
    longitude = data['distance'][1]
    
    stores = api.get_data(part_url='Store/filter', params={'product': data['drug']})
    # print(stores)
    
    pharmacy_distance = []
    for i in stores:
        pharmacy = api.get_data(part_url='Pharmacy/filter', params={'name':i['pharmacy']})[0]
        distance = math.sqrt((float(latitude)-float(pharmacy['location_latitute']))**2+(float(longitude)-float(pharmacy['location_longitude']))**2)
        pharmacy_distance.append([pharmacy['id'], distance])

    sorted_combined = sorted(pharmacy_distance, key=lambda x: x[1])

    # Unzip the sorted combined list back into two arrays
    sorted_id, sorted_distance = zip(*sorted_combined)

    # Convert the tuples back into lists (optional)
    sorted_id = list(sorted_id)
    sorted_distance = list(sorted_distance)

    drug = api.get_data(part_url='Product/filter', params={'name':data['drug']})[0]
    info = f'''Nomi: {drug['name']}
Ishlab chiqaruvchi: {drug['company'][0]}, {drug['company'][1]}
Dori shakli: {drug['type_name']}
Farmakoterapevtik guruhi: {drug['pharma_group']}
Yaroqlilik muddati: {drug['validity_date']}
Dori haqida:
{drug['description']}'''
    await message.answer_photo(drug['image'])
    await message.answer(text=info)

    for i in range(len(sorted_id)):
        pharmacy = api.get_data(part_url=f'Pharmacy/{sorted_id[i]}')
        pharmacy_drug = api.get_data(part_url='Store/filter', params={'product': data['drug'], 'pharmacy':sorted_id[i]})[0]
        pharmacy_info = f'''Dorixona: {pharmacy['name']}
Kontakt: {pharmacy['contact']}
Dorining narxi: {pharmacy_drug['price']}
            '''
        await message.answer_location(pharmacy['location_latitute'], pharmacy['location_longitude'])
        await message.answer(text=pharmacy_info)

    await state.clear()


@router.message(F.text=='✉️Biz bilan aloqa')
async def user_complaint(message: Message):
    await message.answer('Bizning kompaniya sizga dorilarni osonlik bilan topa olishingizga yordam beradi.\n\nAgar savollaringiz bo\'lsa adminstratorlarimiz bilan bog\'lanishingiz mumkin:\n\n+99890-020-01-74 ga murojaat qiling')

@router.message(F.text=='🏥Dorixona ochish')
async def open_pharmacy(message: Message, state: FSMContext):
    await state.set_state(PharmacyState.name)
    await state.update_data(owner=message.from_user.id)
    await message.answer(text='Dorixona nomini kiriting:')

@router.message(PharmacyState.name)
async def pharmacy_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(PharmacyState.phone)
    await message.answer('Dorixonaning telefon raqamini kiriting:', reply_markup=kb.phone)

@router.message(PharmacyState.phone)
async def pharmacy_phone(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
    else:
        await state.update_data(phone=message.text)
    await state.set_state(PharmacyState.location)
    await message.answer('Dorixonaning lokatsiyasini yuboring:', reply_markup=kb.distance)

@router.message(PharmacyState.location)
async def pharmacy_location(message: Message, state: FSMContext):
    await state.update_data(location=[message.location.latitude, message.location.longitude])
    
    data = await state.get_data()

    post = api.post_pharmacy(name=data['name'], owner=data['owner'], phone=data['phone'], location_latitute=data['location'][0], location_longitude=data['location'][1])

    await message.answer(text=post, reply_markup=kb.main)
    await state.clear()

@router.message()
async def echo(message: Message):
    await message.answer('Sizga qanaqadir dori kerakmi?', reply_markup=kb.main)