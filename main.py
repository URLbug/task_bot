from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import json
import io

from context import Orders
from database import User, Order, session


config = json.load(open('config.json','rb'))
text = json.load(io.open('text.json','rb'))

bot = Bot(config['TOKEN'])
dp = Dispatcher(bot,storage=MemoryStorage())

ORDERS = {'sum': 1, 'sum_baskets': 1, 'contacts': None, 'GPS': None}
DATA = {'sum_baskets': 0}

# Start command
@dp.message_handler(commands=['start'])
async def start(m: types.Message):

    markup = InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Главное меню', callback_data='menu'))

    await m.reply('Start', reply_markup=markup)

# Menu
@dp.callback_query_handler(text='menu')
async def menu(call: types.CallbackQuery):

    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.InlineKeyboardButton('Корзина', callback_data=f'baskets:{DATA["sum_baskets"]}'),
        types.InlineKeyboardButton('Ассортимент', callback_data='assorts'),
        types.InlineKeyboardButton('Тех. поддержка', callback_data='supports'),
        types.InlineKeyboardButton('О нас', callback_data='about_our')
    )


    await call.message.reply('Menu', reply_markup=markup)

# Assorts groups
@dp.callback_query_handler(text_startswith='minus')
async def minus(call: types.CallbackQuery):
    
    calls = call.data.split(':')
    data = int(calls[1])-1

    if data > 0:
        markup = InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("-", callback_data=f"minus:{data}"),
            types.InlineKeyboardButton(str(data), callback_data="null"),
            types.InlineKeyboardButton("+", callback_data=f"pluse:{data}"),
            types.InlineKeyboardButton("Заказать", callback_data=f"order:{data}"),
            types.InlineKeyboardButton("Добавить в корзину",callback_data=f"add_to_baskets:{data}")
            )
        markup.add(types.InlineKeyboardButton('Главное меню',callback_data='menu'))

        await call.message.edit_reply_markup(markup)

@dp.callback_query_handler(text_startswith='pluse')
async def pluse(call: types.CallbackQuery):
    
    calls = call.data.split(':')
    data = int(calls[1])+1


    markup = InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("-", callback_data=f"minus:{data}"),
        types.InlineKeyboardButton(str(data), callback_data="null"),
        types.InlineKeyboardButton("+", callback_data=f"pluse:{data}"),
        types.InlineKeyboardButton("Заказать", callback_data=f"order:{data}"),
        types.InlineKeyboardButton("Добавить в корзину",callback_data=f"add_to_baskets:{data}")
        )
    markup.add(types.InlineKeyboardButton('Главное меню',callback_data='menu'))

    await call.message.edit_reply_markup(markup)

@dp.callback_query_handler(text='assorts')
async def assorts(call: types.CallbackQuery):

    markup = InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("-", callback_data=f"minus:1"),
            types.InlineKeyboardButton("1", callback_data="null"),
            types.InlineKeyboardButton("+", callback_data=f"pluse:1"),
            types.InlineKeyboardButton("Заказать", callback_data=f"order:1"),
            types.InlineKeyboardButton("Добавить в корзину",callback_data=f"add_to_baskets:1")
            )
    markup.add(types.InlineKeyboardButton('Главное меню',callback_data='menu'))


    await call.message.answer_photo(text['cocos']['url_photo'],caption=f'{text["cocos"]["text"]}\n{text["cocos"]["price"]}', reply_markup=markup)

@dp.callback_query_handler(text_startswith='add_to_baskets')
async def add_to_baskets(call: types.CallbackQuery):

    data = int(call.data.split(':')[1])

    markup = InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("-", callback_data=f"minus:{data}"),
            types.InlineKeyboardButton(str(data), callback_data="null"),
            types.InlineKeyboardButton("+", callback_data=f"pluse:{data}"),
            types.InlineKeyboardButton("Заказать", callback_data=f"order:{data}"),
            types.InlineKeyboardButton("Перейти в корзину",callback_data=f"baskets:{data}")
            )
    markup.add(types.InlineKeyboardButton('Главное меню',callback_data='menu'))

    DATA['sum_baskets'] += data  

    await call.message.edit_reply_markup(markup)
    await call.answer('Ваш товар был успешно добавлен в корзину!')


# Baskets groups
@dp.callback_query_handler(text_startswith='baskets_plus')
async def baskets_plus(call: types.CallbackQuery):

    data = int(call.data.split(':')[1]) + 1

    markup = InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("-", callback_data=f"baskets_minus:{data}"),
            types.InlineKeyboardButton(str(data), callback_data="null"),
            types.InlineKeyboardButton("+", callback_data=f"baskets_plus:{data}"),
            types.InlineKeyboardButton("Заказать", callback_data=f"order:{data}")
            )
    markup.add(types.InlineKeyboardButton('Главное меню',callback_data='menu'))

    DATA['sum_baskets'] += 1  

    await call.message.edit_reply_markup(markup)

@dp.callback_query_handler(text_startswith='baskets_minus')
async def baskets_plus(call: types.CallbackQuery):

    data = int(call.data.split(':')[1]) - 1

    if data > 0:

        markup = InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("-", callback_data=f"baskets_minus:{data}"),
                types.InlineKeyboardButton(str(data), callback_data="null"),
                types.InlineKeyboardButton("+", callback_data=f"baskets_plus:{data}"),
                types.InlineKeyboardButton("Заказать", callback_data=f"order:{data}")
                )
        markup.add(types.InlineKeyboardButton('Главное меню',callback_data='menu'))

        DATA['sum_baskets'] -= 1  

        await call.message.edit_reply_markup(markup)

@dp.callback_query_handler(text_startswith='baskets')
async def baskets(call: types.CallbackQuery):

    data = DATA["sum_baskets"]

    markup = InlineKeyboardMarkup()

    if int(data) > 0:

        markup.add(
            types.InlineKeyboardButton("-", callback_data=f"baskets_minus:{data}"),
            types.InlineKeyboardButton(str(data), callback_data="null"),
            types.InlineKeyboardButton("+", callback_data=f"baskets_plus:{data}"),
            types.InlineKeyboardButton("Заказать", callback_data=f"order:{data}")
            )
        markup.add(types.InlineKeyboardButton('Главное меню',callback_data='menu'))

        
        await call.message.reply_photo(text['cocos']['url_photo'],caption=f'{text["cocos"]["text"]}\n{text["cocos"]["price"]}', reply_markup=markup)
    else: 
        
        markup.add(types.InlineKeyboardButton('Главное меню',callback_data='menu'))

        await call.message.reply('baskets', reply_markup=markup)

# Order groups
@dp.callback_query_handler(text_startswith='order', state=None)
async def order(call: types.CallbackQuery):

    data = int(call.data.split(':')[1])

    ORDERS["sum_baskets"] = str(data*100)
    ORDERS["sum"] = data

    await call.message.reply('GPS')

    await Orders.GPS.set()

@dp.message_handler(state=Orders.GPS)
async def order_gps(m: types.Message):

    if m.text:
        ORDERS["GPS"] = m.text

        await m.reply('contacts')

        await Orders.next()
    
    else:
        await m.reply('try again')

@dp.message_handler(state=Orders.contacts)
async def order_contacts(m: types.Message, state: FSMContext):

    if m.text:
        ORDERS["contacts"] = m.text

        markup = InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Главное меню',callback_data='menu'))

        users = User(sums=ORDERS["sum"], contacts=ORDERS["contacts"], gps=ORDERS["GPS"])
        session.add(users)
        session.commit()
        session.close()

        users = Order(sums=ORDERS["sum"], contacts=ORDERS["contacts"], gps=ORDERS["GPS"], sum_basket=ORDERS["sum_baskets"])
        session.add(users)
        session.commit()
        session.close()

        await m.reply('Goal', reply_markup=markup)

        await state.finish()
    
    else:
        await m.reply('try again')
   

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)