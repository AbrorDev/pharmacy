from aiogram.fsm.state import StatesGroup, State

# dorini izlash uchun
class SearchState(StatesGroup):
    drug = State()
    condition = State()
    distance = State()

# reklama berish uchun
class AdvertState(StatesGroup):
    message = State()
    is_sent = State()

# dorixona ochish uchun
class PharmacyState(StatesGroup):
    name = State()
    owner = State()
    phone = State()
    location = State()

# dorixonani ma'lumotlarini o'zgartirish
class PharmacyChange(StatesGroup):
    owner = State()
    which_part = State()
    name = State()

# yangi dori qo'shish
class AddDrugState(StatesGroup):
    pharmacy = State()
    drug = State()
    code = State()
    price = State()

# dori ma'lumotlarini yangilash
class UpdateDrugState(StatesGroup):
    pharmacy = State()
    drug = State()
    part = State()
    value = State()

# dorini o'chirish
class DeleteDrugeState(SearchState):
    pharmacy = State()
    drug = State()

# admin tomonidan