import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

API = '7722768622:AAEHxwhyUKA7nOxeAGpPHT0tBFgMbBhvUO0'
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())
initiate_db()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = KeyboardButton('Рассчитать')
button_info = KeyboardButton('Информация')
button_buy = KeyboardButton('Купить')
kb.row(button_calculate, button_buy)
kb.row(button_info)

inl_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
    [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
])


# buy_inl_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
#     [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
#     [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
#     [InlineKeyboardButton(text='Product4', callback_data='product_buying')]
# ])

async def make_keyboard_for_products(products_list):
    buy_inl_kb = InlineKeyboardMarkup(inline_keyboard=[])
    for product in products_list:
        buy_inl_kb.add(InlineKeyboardButton(text=product, callback_data='product_buying'))
    return buy_inl_kb


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    titles = []
    for product in await get_all_products():
        with open(f'.\\photos\\{product[0]}.jpg', 'rb') as img:
            await message.answer_photo(img, f'Название: {product[1]}\nОписание: {product[2]}\nЦена: {product[3]}')
        titles.append(product[1])
    await message.answer('Выберите продукт для покупки: ', reply_markup=await make_keyboard_for_products(titles))


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(callback):
    await callback.message.answer('Вы успешно приобрели продукт')
    await callback.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=inl_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(callback):
    await callback.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await callback.answer()


@dp.callback_query_handler(text='calories')
async def set_age(callback):
    await callback.message.answer('Введите свой возраст:')
    await callback.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        int(message.text)
    except:
        await message.answer('Значение должно быть числом!')
        await UserState.age.set()
        return
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        int(message.text)
    except:
        await message.answer('Значение должно быть числом!')
        await UserState.growth.set()
        return
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    try:
        int(message.text)
    except:
        await message.answer('Значение должно быть числом!')
        await UserState.weight.set()
        return
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Для оптимального похудения Вам необходимо не больше {result} каллорий в день!')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def start(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)