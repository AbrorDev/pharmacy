from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router, flags
from aiogram.fsm.context import FSMContext
import asyncio

from appbot.states import PharmacyChange, AddDrugState, UpdateDrugState, DeleteDrugeState
import appbot.keyboards as kb
from appbot import api

router_owner = Router()

@router_owner.message(Command('settings'))
@flags.owner_authorization(is_owner_authorized=True)
async def settings(message: Message, state: FSMContext):
    await state.set_state(PharmacyChange.which_part)
    await message.answer(text="Dorixonani qaysi ma'lumotini o'zgartirmoqchisiz?", reply_markup=kb.pharmacy_change)

@router_owner.callback_query(PharmacyChange.which_part)
@flags.owner_authorization(is_owner_authorized=True)
async def part(callback: CallbackQuery, state: FSMContext):
    if callback.data == "cancel":
        await callback.message.edit_text(text='Bekor qilindi...')
        await state.clear()
    else:
        await state.update_data(which_part=callback.data)
        await state.set_state(PharmacyChange.name)
        if callback.data=='location':
            await callback.message.answer(text="Lokatsiyani yuboring:", reply_markup=kb.distance)
        elif callback.data=='phone':
            await callback.message.answer(text="Telefon raqamingizni yuboring:", reply_markup=kb.phone)
        else:
            await callback.message.answer(text='Nomini kiriting:')

@router_owner.message(PharmacyChange.name)
@flags.owner_authorization(is_owner_authorized=True)
async def name_part(message: Message, state: FSMContext):
    await state.update_data(owner=message.from_user.id)
    data = await state.get_data()
    if data['which_part']=='location':
        await state.update_data(name=[message.location.latitude, message.longitude])
    else:
        await state.update_data(name=message.text)
    await message.answer(text="Ma'lumotni o'zgartirmoqchimisiz?", reply_markup=kb.yes_no)

@router_owner.callback_query(PharmacyChange.name)
@flags.owner_authorization(is_owner_authorized=True)
async def changed_part(callback: CallbackQuery, state: FSMContext):
    if callback.data=='yes':
        data = await state.get_data()
        update = api.update_pharmacy(owner=data['owner'], which_part=data['which_part'], value=data['name'])
        await callback.message.answer(text=update)
    else:
        await callback.message.answer(text="Ma'lumot o'zgartirilishi bekor qilindi...")
    await state.clear()

@router_owner.message(Command('pharmacy'))
@flags.owner_authorization(is_owner_authorized=True)
async def pharmacy(message: Message):
    await message.answer(text='Dorilar ustida nima qilmoqchisiz?', reply_markup=kb.pharmacy_drug_change)

@router_owner.callback_query(F.data.split('_')[0]=='read')
@flags.owner_authorization(is_owner_authorized=True)
async def read_drug(callback: CallbackQuery):
    pharmacy = api.get_data(part_url='Pharmacy/filter', params={"owner":callback.message.chat.id}, part='id')
    store_types = api.get_data(part_url='Store/filter', params={"pharmacy":pharmacy}, part='type_name', duplicate=False)
    
    data = []
    for i in store_types:
        data.append([i[0], i[1]])
    page = int(callback.data.split('_')[-1])
    
    await callback.message.edit_text('Dori turini tanlang:', reply_markup=kb.generate_keyboard(page, data, 'catalog', 'read'))

@router_owner.callback_query(F.data.split('_')[0]=='catalog')
@flags.owner_authorization(is_owner_authorized=True)
async def get_items(callback: CallbackQuery):
    catalog_id = int(callback.data.split('_')[1])
    pharmacy = api.get_data(part_url='Pharmacy/filter', params={"owner":callback.message.chat.id}, part='id')
    data = api.get_data(part_url='Store/filter', params={"pharmacy":pharmacy, 'type_n':catalog_id}, part='product', duplicate=False)
    
    page = int(callback.data.split('_')[-1])
    await callback.message.edit_text('Dorini tanlang:', reply_markup=kb.generate_keyboard(page, data, 'drug', 'catalog'))

@router_owner.callback_query(F.data.split('_')[0]=='drug')
@flags.owner_authorization(is_owner_authorized=True)
async def get_item(callback: CallbackQuery):
    drug_id = callback.data.split('_')[1]
    pharmacy = api.get_data(part_url='Pharmacy/filter', params={"owner":callback.message.chat.id}, part='id')
    
    data = api.get_data(part_url='Store/filter',params={ 'pharmacy':pharmacy[0], 'product_id':drug_id })[0]

    info = f'''Nomi: {data['product'][0]}
Dori shakli: {data['type_name'][0]}
Maxsus kodi: {data['special_code']}
Narxi: {data['price']}
    '''
    await callback.message.answer_photo(data['product'][2], info)
    await callback.message.delete()

# Yangi dorini qo'shish
@router_owner.callback_query(F.data.split('_')[0]=='create')
@flags.owner_authorization(is_owner_authorized=True)
async def add_bar_code_pharmacy(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddDrugState.drug)
    await callback.message.edit_text(text="Dorining shtrix kodini kiriting:")

@router_owner.message(AddDrugState.drug)
@flags.owner_authorization(is_owner_authorized=True)
async def add_code_pharmacy(message: Message, state: FSMContext):
    await state.update_data(drug=message.text)
    data = await state.get_data()
    drug = api.get_data(part_url='Product/filter', params={'barcode':data['drug']})
    if drug:
        pharmacy = api.get_data(part_url='Pharmacy/filter', params={'owner':message.from_user.id}, part='id')[0]
        
        await state.update_data(drug=message.text, pharmacy=pharmacy)
        await state.set_state(AddDrugState.code)
        await message.answer(text="Maxsus kodini kiriting:")
    else:
        await message.answer('Dorining shtrix kodi xato yoki bunda dorining ma\'lumotlari bizning bazamizda mavjud emas.\n\nBiz bilan bog\'lanish: +99890-020-01-74')
        await state.clear()

@router_owner.message(AddDrugState.code)
@flags.owner_authorization(is_owner_authorized=True)
async def add_price_pharmacy(message: Message, state: FSMContext):
    await state.update_data(code=message.text)
    await state.set_state(AddDrugState.price)
    await message.answer(text="Narxini kiriting:")

@router_owner.message(AddDrugState.price)
@flags.owner_authorization(is_owner_authorized=True)
async def add_successfully_pharmacy(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    drug = api.get_data(part_url='Product/filter', params={'barcode':data['drug']},part='id')[0]
    post = api.add_to_store(data['pharmacy'], drug, data['code'], data['price'])
    await message.answer(text=post)
    await state.clear()

# Dorini ma'lumotlarini o'zgartirish
@router_owner.callback_query(F.data.split('_')[0]=='update')
@flags.owner_authorization(is_owner_authorized=True)
async def update_drug_pharmacy(callback: CallbackQuery, state: FSMContext):
    pharmacy = api.get_data(part_url='Pharmacy/filter', params={'owner':callback.message.chat.id}, part='id')[0]
    await state.update_data(pharmacy = pharmacy)
    await state.set_state(UpdateDrugState.drug)
    await callback.message.edit_text(text="Dorining shtrix kodini kiriting:")

@router_owner.message(UpdateDrugState.drug)
@flags.owner_authorization(is_owner_authorized=True)
async def update_drug_bar_code_pharmacy(message: Message, state: FSMContext):
    await state.update_data(drug=message.text)
    await state.set_state(UpdateDrugState.part)
    await message.answer(text="Qaysi qismi o'zgartirmoqchisiz?", reply_markup=kb.drug_part)

@router_owner.callback_query(UpdateDrugState.part)
@flags.owner_authorization(is_owner_authorized=True)
async def update_drug_part_pharmacy(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'cancel':
        await state.clear()
        await callback.message.answer(text="Bekor qilindi...")
    else:
        await state.update_data(part=callback.data)
        await state.set_state(UpdateDrugState.value)
        await callback.message.edit_text(text="Qiymatini kiriting:")

@router_owner.message(UpdateDrugState.value)
@flags.owner_authorization(is_owner_authorized=True)
async def update_value_pharmacy(message: Message, state: FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    product = api.get_data(part_url='Product/filter', params={'barcode':data['drug']}, part='id')[0]
    pharmacy = api.get_data(part_url='Pharmacy/filter', params={'owner':message.from_user.id}, part='id')[0]
    
    update = api.update_store_product(pharmacy=pharmacy, drug=product, which_part=data['part'], value=data['value'])
    await message.answer(text=update)
    await state.clear()

# Dorini o'chirish
@router_owner.callback_query(F.data.split('_')[0]=='delete')
@flags.owner_authorization(is_owner_authorized=True)
async def delete_drug_pharmacy(callback: CallbackQuery, state: FSMContext):
    pharmacy = api.get_data(part_url='Pharmacy/filter', params={'owner':callback.message.chat.id}, part='id')[0]
    await state.update_data(pharmacy = pharmacy)
    await state.set_state(DeleteDrugeState.drug)
    await callback.message.edit_text(text="Dorining shtrix kodini kiriting:")

@router_owner.message(DeleteDrugeState.drug)
@flags.owner_authorization(is_owner_authorized=True)
async def delete_drug_bar_code_pharmacy(message: Message, state: FSMContext):
    await state.update_data(drug=message.text)
    data = await state.get_data()
    drug = api.get_data(part_url='Product/filter', params={'barcode':data['drug']})
    if drug:
        await message.answer(text=f"Rostdan ham {data['drug']} ni o'chiraveraymi?", reply_markup=kb.yes_no)
    else:
        await message.answer(text="Bunday dori sizning dorixonangizda mavjud emas...")
        await state.clear()

@router_owner.callback_query(DeleteDrugeState.drug)
@flags.owner_authorization(is_owner_authorized=True)
async def delete_drug_pharmacy(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        data = await state.get_data()
        pharmacy = api.get_data(part_url='Pharmacy/filter', params={'owner':callback.message.chat.id}, part='id')[0]
        drug = api.get_data(part_url='Product/filter', params={'barcode':data['drug']}, part='id')
        delete = api.delete_store_product(pharmacy, drug)
        await callback.message.answer(text=delete, reply_markup=kb.main)
    else:
        await callback.message.answer(text="O'chirilish bekor qilindi...")
    await state.clear()

# o'chirish
@router_owner.callback_query(F.data == 'cancel')
@flags.owner_authorization(is_owner_authorized=True)
async def delete_drug_pharmacy(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()