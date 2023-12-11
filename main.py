from aiogram import Dispatcher, Bot, executor, types
from config import TOKEN_API

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboard import kb_lang, kb_main_en, kb_main_ua, kb_rates_ua, kb_rates_en, kb_choosing, kb_choosing_2
from parser import parse_currencies, parse_cash_market

storage = MemoryStorage()
bot = Bot(token=TOKEN_API, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
currencies_bank = parse_currencies()
currencies_cash = parse_cash_market()
currentLanguage = ''


I18N_DOMAIN = "exchange_bot"
LOCALES_DIR = "locales"
DEFAULT_LANGUAGE = "en"

#инициализация и подключение мидлвари
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR, DEFAULT_LANGUAGE)
dp.middleware.setup(i18n)


class ProfileStatesGroup(StatesGroup):

    currency1 = State()
    amount = State()
    currency2 = State()


@dp.message_handler(Text(equals=["Back ⛔️"]), state='*')
async def cmd_back(message: types.Message, state: FSMContext):
    if currentLanguage == 'en':
        await state.finish()
        await message.answer(text='You are in the main menu',
                             reply_markup=kb_main_en)
    elif currentLanguage == 'ua':
        await state.finish()
        await message.answer(text='Ви в головному меню',
                             reply_markup=kb_main_ua)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, selective=True, one_time_keyboard=True
    )
    keyboard.add(
        KeyboardButton(text="Українська 🇺🇦"),
        KeyboardButton(text="English 🇬🇧")
    )
    await message.answer(text="Welcome to Exchange Bot!\nChoose the language below/Виберіть мову нижче",
                         reply_markup=kb_lang)


@dp.message_handler(Text(equals=['English 🇬🇧', 'Українська 🇺🇦']))
async def flag_en(message: types.Message):
    global currentLanguage
    if message.text == 'Українська 🇺🇦':
        currentLanguage = 'ua'
        await message.answer(text="Українська вибрана")
        await message.answer(text="Виберіть опцію нижче",
                             reply_markup=kb_main_ua)
    elif message.text == 'English 🇬🇧':
        currentLanguage = 'en'
        await message.answer(text="English has been chosen")
        await message.answer(text="Choose the option below",
                             reply_markup=kb_main_en)


@dp.message_handler(Text(equals=['Змінити мову 🇬🇧/🇺🇦', "Change language 🇺🇦/🇬🇧"]))
async def change_language_button(message: types.Message):
    await message.answer(text="Choose the language below/Виберіть мову нижче",
                         reply_markup=kb_lang)


@dp.message_handler(Text(equals=['Show rates 📊', 'Показати курси 📊']))
async def showing_rates(message: types.Message):
    if currentLanguage == 'en':
        await message.answer(text="Choose the option below",
                             reply_markup=kb_rates_en)

    elif currentLanguage == 'ua':
        await message.answer(text="Оберіть опцію нижче",
                             reply_markup=kb_rates_ua)


@dp.message_handler(Text(equals=['Avarage exchange rate in banks', 'Середній курс валют у банках']))
async def showing_rates_bank(message: types.Message, answer=''):
    if currentLanguage == 'en':
        for currencies, value in currencies_bank.items():
            answer += f'Currency: {currencies}\nBuy: {value["buy"][:7]}\nSale: {value["sale"][:7]}\n\n'

        await message.answer("🏦 Avarage rates in the banks 🏦\n\n" + answer)
    elif currentLanguage == 'ua':
        for currencies, value in currencies_bank.items():
            answer += f'Валюта: {currencies}\nКупівля: {value["buy"][:7]}\nПродаж: {value["sale"][:7]}\n\n'

        await message.answer("🏦 Середній курс валют у банках 🏦\n\n" + answer)


@dp.message_handler(Text(equals=['Cash market', 'Готівковий ринок']))
async def showing_rates_cash(message: types.Message, answer=''):
    if currentLanguage == 'en':
        for currencies, value in currencies_cash.items():
            answer += f'Currency: {currencies}\nBuy: {value["buy"][:7]}\nSale: {value["sale"][:7]}\n\n'

        await message.answer("💸 Avarage rates on cash market 💸\n\n" + answer)
    elif currentLanguage == 'ua':
        for currencies, value in currencies_cash.items():
            answer += f'Валюта: {currencies}\nКупівля: {value["buy"][:7]}\nПродаж: {value["sale"][:7]}\n\n'

        await message.answer("💸 Середній курс на готівковому ринку 💸\n\n" + answer)


@dp.message_handler(Text(equals=["Back", "Назад"]))
async def cmd_back(message: types.Message):
    if currentLanguage == 'en':
        await message.answer(text='You are in the main menu',
                             reply_markup=kb_main_en)
    elif currentLanguage == 'ua':
        await message.answer(text='Ви в головному меню',
                             reply_markup=kb_main_ua)


@dp.message_handler(Text(equals=["Порахувати гроші 💰", "Count money 💰"]))
async def cmd_count_money(message: types.Message):
    if currentLanguage == 'en':
        await message.answer(text='Choose the currency which ypu want to trade',
                             reply_markup=kb_choosing)
    elif currentLanguage == 'ua':
        await message.answer(text='Виберіть валюту яку хочете перевести',
                             reply_markup=kb_choosing)
    await ProfileStatesGroup.currency1.set()


@dp.message_handler(lambda message: message.text not in ["UAH", "USD", "EUR", "PLN"],state=ProfileStatesGroup.currency1)
async def process_currency_invalid(message: types.Message):
    if currentLanguage == 'en':
        await message.answer(text='Choose the currency which ypu want to trade')
    elif currentLanguage == 'ua':
        await message.answer(text='Виберіть валюту яку хочете перевести')


@dp.message_handler(state=ProfileStatesGroup.currency1)
async def cmd_choose_currencie_bank(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['currency1'] = message.text
    markup = types.ReplyKeyboardRemove()
    if currentLanguage == 'en':
        await message.answer(text=f'Write the amount of {data["currency1"]}',
                             reply_markup=markup)
    elif currentLanguage == 'ua':
        await message.answer(text=f'Напишіть сумму {data["currency1"]}',
                             reply_markup=markup)

    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit(), state=ProfileStatesGroup.amount)
async def process_currency_invalid(message: types.Message):
    if currentLanguage == 'en':
        await message.answer(text='Write only digits')
    elif currentLanguage == 'ua':
        await message.answer(text='Пишіть тільки цифрами')


@dp.message_handler(state=ProfileStatesGroup.amount)
async def cmd_choose_currency_bank(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text

    if currentLanguage == 'en':
        await message.answer(text='Choose the currency in which you want to convert',
                             reply_markup=kb_choosing)
    elif currentLanguage == 'ua':
        await message.answer(text='Виберіть валюту в яку ви хочете перевести',
                             reply_markup=kb_choosing)

    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: message.text not in ["UAH", "USD", "EUR", "PLN"],state=ProfileStatesGroup.currency2)
async def process_currency_invalid(message: types.Message):
    if currentLanguage == 'en':
        await message.answer(text='Please, hoose the option below')
    elif currentLanguage == 'ua':
        await message.answer(text='Будь-ласка, оберіть опцію нижче')


@dp.message_handler(state=ProfileStatesGroup.currency2)
async def cmd_choose_currency_bank(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['currency2'] = message.text

        currency2 = data['currency2']
        currency1 = data['currency1']
    if currency1 == currency2:
        if currentLanguage == 'en':
            await message.answer("We can't count the same currency",
                                 reply_markup=kb_main_en)
        elif currentLanguage == 'ua':
            await message.answer("Ми не можемо порахувати однакову валюту",
                                 reply_markup=kb_main_ua)
    elif currency1 == "UAH" and currency2 in currencies_bank.keys():
        value_buy = int(data["amount"]) / float(currencies_bank[currency2]["buy"][:7])
    elif currency1 in currencies_bank.keys() and currency2 == "UAH":
        value_buy = int(data["amount"]) * float(currencies_bank[currency1]["buy"][:7])
    elif currency1 in currencies_bank.keys() and currency2 in currencies_bank.keys():
        value_buy = (int(data["amount"]) * float(currencies_bank[currency1]["buy"][:7])) / \
                    float(currencies_bank[currency2]["sale"][:7])

    if currentLanguage == "ua":
        await message.answer(
            text=f"За {data['amount']} {data['currency1']} ви можете придбати {round(value_buy, 2)} {data['currency2']}"
                 f"\n\nРозрахунок за середнім курсом банків *",
            reply_markup=kb_main_ua)

    elif currentLanguage == "en":
        await message.answer(
            text=f"For {data['amount']} {data['currency1']} you can buy {round(value_buy, 2)} {data['currency2']}"
                 f"\n\nCounted by the avarage rates in the banks *",
            reply_markup=kb_main_ua)

    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
