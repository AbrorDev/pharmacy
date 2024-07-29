from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🔍Dori izlash')], 
    [KeyboardButton(text='✉️Biz bilan aloqa'), KeyboardButton(text='🏥Dorixona ochish')]
], resize_keyboard=True)

condition = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💸Narxi bo'yicha", callback_data='price')],
    [InlineKeyboardButton(text="📍Masofa bo'yicha", callback_data='distance')]
])

distance = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📍Lokatsiyani yuborish', request_location=True)]
], resize_keyboard=True)

yes_no = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ha', callback_data='yes'),
    InlineKeyboardButton(text="Yo'q", callback_data='no')]
])

phone = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📞Telefon raqamini yuborish', request_contact=True)]
], resize_keyboard=True)

pharmacy_change = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Dorixona nomini', callback_data='name')],
    [InlineKeyboardButton(text='Dorixona telefon raqamini', callback_data='phone')],
    [InlineKeyboardButton(text='Dorixona lokatsiyasini', callback_data='location')],
    [InlineKeyboardButton(text='Bekor qilish', callback_data='cancel')],
])

pharmacy_drug_change = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Dorilar ro\'yxati', callback_data='read_catalog_1')],
    [InlineKeyboardButton(text='Yangi dori qo\'shish', callback_data='create')],
    [InlineKeyboardButton(text='Dorining ma\'lumotini o\'zgartirish', callback_data='update')],
    [InlineKeyboardButton(text='Qolmagan dorini belgilash', callback_data='delete')],
    [InlineKeyboardButton(text='Bekor qilish', callback_data='cancel')],
])

def generate_keyboard(page, items, part, crud,qiymat='qw'):
    # Calculate start and end indexes based on page number
    start_index = (page - 1) * 10
    end_index = page * 10

    keyboard = InlineKeyboardBuilder()
    for item in items[start_index:end_index]:
        button = InlineKeyboardButton(text=str(item[0]), callback_data=f"{part}_{item[1]}_1")
        keyboard.add(button)

    # Add navigation buttons
    if page > 1:
        keyboard.add(InlineKeyboardButton(text="Previous", callback_data=f"{crud}_{qiymat}_{page - 1}"))
    if end_index < len(items):
        keyboard.add(InlineKeyboardButton(text="Next", callback_data=f"{crud}_{qiymat}_{page + 1}"))

    return keyboard.adjust(1).as_markup()

drug_part = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Maxsus kodini', callback_data='special_code')],
    [InlineKeyboardButton(text='Narxini', callback_data='price')],
    [InlineKeyboardButton(text='Bekor qilish', callback_data='cancel')],
])

admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Reklama berish', callback_data='advertisment')],
    [InlineKeyboardButton(text='Foydalanuvchilar soni', callback_data='user_count')],
    # [InlineKeyboardButton(text='Kompaniyalar', callback_data='company_1')],
    # [InlineKeyboardButton(text='Dori turlari', callback_data='type')],
    # [InlineKeyboardButton(text='Dorilar', callback_data='drug')],
    # [InlineKeyboardButton(text='Dorixonalar', callback_data='pharmacy')],
    [InlineKeyboardButton(text='Bekor qilish', callback_data='cancel_admin')],
])

# company=InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='')]
# ])