from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router, flags
from aiogram.fsm.context import FSMContext
import asyncio

from appbot.config import ADMINS
from appbot.states import AdvertState
import appbot.keyboards as kb
from appbot import api

router_admin = Router()

@router_admin.message(Command('admin'))
@flags.authorization(is_authorized=True)
async def advert_message(message: Message, state: FSMContext):
    await message.answer(text='Nima qilmoqchisiz?', reply_markup=kb.admin)

@router_admin.callback_query(F.data == 'advertisment')
@flags.authorization(is_authorized=True)
async def advert_to_all(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdvertState.message)
    await callback.message.answer(text='Reklamani yuboring:')

@router_admin.message(AdvertState.message)
@flags.authorization(is_authorized=True)
async def advert_message(message: Message, state: FSMContext):
    await state.update_data(message=message)
    await state.set_state(AdvertState.is_sent)
    await message.answer(text='Reklamani yuboraveraymi?', reply_markup=kb.yes_no)

@router_admin.callback_query(AdvertState.is_sent)
@flags.authorization(is_authorized=True)
async def is_send(callback: CallbackQuery, state: FSMContext):
    await state.update_data(is_send=callback.data)
    data = await state.get_data()
    if data['is_send'] == 'yes':
        for i in ADMINS:
            await data['message'].copy_to(chat_id=i)
            await asyncio.sleep(0.05)
        
        await callback.message.answer(text='Reklama hammaga yuborildi...')
    else:
        await callback.message.answer(text='Yuborilish bekor qilindi...')
     
    await state.clear()

@router_admin.callback_query(F.data == 'user_count')
@flags.authorization(is_authorized=True)
async def user_count(callback: CallbackQuery, state: FSMContext):
    count = len(api.get_data(part_url='Telegran%20Users'))
    await callback.message.answer(text=f'{count} ta odam botdan foydalanmoqda...')


@router_admin.callback_query(F.data == 'cancel_admin')
@flags.authorization(is_authorized=True)
async def user_count(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=f'Bekor qilindi...')

# @router_admin.callback_query(F.data.split('_')[0] == 'company')
# @flags.authorization(is_authorized=True)
# async def advert_to_all(callback: CallbackQuery, state: FSMContext):
#     companies = ['shayana farm', 'oson apteka']
#     page = 1
#     await callback.message.answer('Kompaniyani tanlang:', reply_markup=await kb.generate_keyboard())