from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import requests
from bs4 import BeautifulSoup
import re

API_TOKEN = '5023249269:AAGB1oG1pL6ZHW6Deysp6B4CZIvNa0YJccA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


URL = 'https://cbu.uz/ru/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', 'accept': '*/*'}


products = []
car = []
msg = "UZS → $ выберите /uzs_d\n$ → UZS выберите /d_uzs\n\nUZS → EUR выберите /uzs_e\nEUR → UZS выберите /e_uzs\n\nUZS → RUB выберите /uzs_r\nRUB → UZS выберите /r_uzs"



def get_html(URL):
    r = requests.get(URL, headers=HEADERS)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='exchange__item')
    for item in items:
        products.append({
            'price': item.find('div', class_='exchange__item_value').get_text()
        })

    return products


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        products = []
        html = get_html(URL)
        products.extend(get_content(html.text))
        
    else:
        print('Error')


class Stat(StatesGroup):
    duzs = State()
    uzsd = State()

    euzs = State()
    uzse = State()
    
    ruzs = State()
    uzsr = State()



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name}. Чтобы рассчитать валюту выберите:")
    await message.answer(msg)

    parse()
    for i in products:
        car.append(i.get('price'))



@dp.message_handler(commands=['res'])
async def res(message: types.Message):
    await message.answer(msg)




@dp.message_handler(commands=['d_uzs'])
async def duzs(message: types.Message):
    await message.answer("Введите сумму в USD")
    await Stat.duzs.set()

@dp.message_handler(state=Stat.duzs)
async def duzs1(message: types.Message, state: FSMContext):
    dollar = float(car[0].replace('USD = ', ''),)
    mst = float(re.sub('[^0-9,.]', '', message.text))
    sum = dollar * mst
    sum2 = round(sum, 2)
    mes = f'<strong>Результат: {mst:,} $ = {sum2:,} сум</strong>\n\n<i><b>По курсу 1$ = {dollar:,} сум</b></i>\n<a href="https://cbu.uz/ru/">Подробнее</a>\n\nЧтобы продолжить выберите /res'
    await message.answer(mes, parse_mode='HTML')
    await state.finish()



@dp.message_handler(commands=['uzs_d'])
async def uzsd(message: types.Message):
    await message.answer("Введите сумму в UZS")
    await Stat.uzsd.set()

@dp.message_handler(state=Stat.uzsd)
async def uzsd1(message: types.Message, state: FSMContext):
    dollar = float(car[0].replace('USD = ', ''),)
    mst = float(re.sub('[^0-9,.]', '', message.text))
    sum = mst / dollar
    sum2 = round(sum, 2)
    mes = f'<strong>Результат: {mst:,} сум = {sum2:,} $</strong>\n\n<i><b>По курсу ЦБ 1$ = {dollar:,} сум</b></i>\n<a href="https://cbu.uz/ru/">Подробнее</a>\n\nЧтобы продолжить выберите /res'
    await message.answer(mes, parse_mode='HTML')
    await state.finish()




@dp.message_handler(commands=['e_uzs'])
async def euzs(message: types.Message):
    await message.answer("Введите сумму в EUR")
    await Stat.euzs.set()

@dp.message_handler(state=Stat.euzs)
async def euzs1(message: types.Message, state: FSMContext):
    euro = float(car[1].replace('EUR = ', ''),)
    mst = float(re.sub('[^0-9,.]', '', message.text))
    sum = euro * mst
    sum2 = round(sum, 2)
    mes = f'<strong>Результат: {mst:,} € = {sum2:,} сум</strong>\n\n<i><b>По курсу 1€ = {euro:,} сум</b></i>\n<a href="https://cbu.uz/ru/">Подробнее</a>\n\nЧтобы продолжить выберите /res'
    await message.answer(mes, parse_mode='HTML')
    await state.finish()




@dp.message_handler(commands=['uzs_e'])
async def uzse(message: types.Message):
    await message.answer("Введите сумму в UZS")
    await Stat.uzse.set()

@dp.message_handler(state=Stat.uzse)
async def uzse1(message: types.Message, state: FSMContext):
    euro = float(car[1].replace('EUR = ', ''),)
    mst = float(re.sub('[^0-9,.]', '', message.text))
    sum = mst / euro
    sum2 = round(sum, 2)
    mes = f'<strong>Результат: {mst:,} сум = {sum2:,} €</strong>\n\n<i><b>По курсу 1€ = {euro:,} сум</b></i>\n<a href="https://cbu.uz/ru/">Подробнее</a>\n\nЧтобы продолжить выберите /res'
    await message.answer(mes, parse_mode='HTML')
    await state.finish()




@dp.message_handler(commands=['r_uzs'])
async def ruzs(message: types.Message):
    await message.answer("Введите сумму в RUB")
    await Stat.ruzs.set()

@dp.message_handler(state=Stat.ruzs)
async def ruzs1(message: types.Message, state: FSMContext):
    rub = float(car[2].replace('RUB = ', ''),)
    mst = float(re.sub('[^0-9,.]', '', message.text))
    sum = rub * mst
    sum2 = round(sum, 2)
    mes = f'<strong>Результат: {mst:,} ₽ = {sum2:,} сум</strong>\n\n<i><b>По курсу 1₽ = {rub:,} сум</b></i>\n<a href="https://cbu.uz/ru/">Подробнее</a>\n\nЧтобы продолжить выберите /res'
    await message.answer(mes, parse_mode='HTML')
    await state.finish()



@dp.message_handler(commands=['uzs_r'])
async def uzsr(message: types.Message):
    await message.answer("Введите сумму в UZS")
    await Stat.uzsr.set()

@dp.message_handler(state=Stat.uzsr)
async def uzsr1(message: types.Message, state: FSMContext):
    rub = float(car[2].replace('RUB = ', ''),)
    mst = float(re.sub('[^0-9,.]', '', message.text))
    sum = mst / rub
    sum2 = round(sum, 2)
    mes = f'<strong>Результат: {mst:,} сум = {sum2:,} ₽</strong>\n\n<i><b>По курсу 1₽ = {rub:,} сум</b></i>\n<a href="https://cbu.uz/ru/">Подробнее</a>\n\nЧтобы продолжить выберите /res'
    await message.answer(mes, parse_mode='HTML')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)