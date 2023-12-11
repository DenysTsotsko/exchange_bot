from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_lang = ReplyKeyboardMarkup(resize_keyboard=True)
kb_lang.add(KeyboardButton(text='English 🇬🇧'), KeyboardButton('Українська 🇺🇦'))

kb_main_en = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main_en.add(KeyboardButton('Show rates 📊'), KeyboardButton('Count money 💰')).row(KeyboardButton("Change language 🇺🇦"
                                                                                                   "/🇬🇧"))

kb_main_ua = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main_ua.add(KeyboardButton('Показати курси 📊'), KeyboardButton('Порахувати гроші 💰')).row("Змінити мову 🇬🇧/🇺🇦")


kb_rates_ua = ReplyKeyboardMarkup(resize_keyboard=True)
kb_rates_ua.add(KeyboardButton('Середній курс валют у банках'), KeyboardButton('Готівковий ринок')).row("Назад")

kb_rates_en = ReplyKeyboardMarkup(resize_keyboard=True)
kb_rates_en.add(KeyboardButton('Avarage exchange rate in banks'), KeyboardButton('Cash market')).row("Back")


kb_choosing = ReplyKeyboardMarkup(resize_keyboard=True)
kb_choosing.add(KeyboardButton('UAH'), KeyboardButton('USD')).add(KeyboardButton("EUR"), KeyboardButton("PLN")).\
    add(KeyboardButton("Back ⛔️"))


kb_choosing_2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_choosing_2.add(KeyboardButton('UAH'), KeyboardButton('USD')).add(KeyboardButton("EUR"), KeyboardButton("PLN")).\
    row("Back ⛔️")

