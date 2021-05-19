import logging
import os

import pandas as pd
from navec import Navec
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

# import from other modules
from functions import get_groups, sort_list, check_value
from DB import read_list, insert_into_list, drop, delete_from_list
from config import token, ids


logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)

navec = Navec.load('navec_hudlit_v1_12B_500K_300d_100q.tar')

def auth(func): # authentication wrapper
	async def wrapper(message):
		if not (message['from']['id'] in ids) :
			return await message.reply("Доступ закрыт", reply = False)
		return await func(message)
	return wrapper

@dp.message_handler(commands=['start']) # Diplays the message with the user id.
async def welcome(message: types.Message):
	await message.answer('Ваш id '+str(message['from']['id'])+'\n'+'. Дождитесь разрешения администратора')

@dp.message_handler(commands=['create']) # Creates sample list
@auth
async def create_list(message: types.Message):
	shopping_list = ['Творог','Тушенка','Бананы','Фундук','Фарш','Хлеб','Яйца','Пиво','Хлопья','Яблоки','Перец','Кетчуп','Котлеты','Лимонад', 'Мороженное']
	for i in shopping_list:
		insert_into_list(str(message['from']['id']), i)
	await message.answer('Таблица user'+str(message['from']['id'])+' создана')


@dp.message_handler(commands=['sort']) # Shows sorted list
@auth
async def show_sorted_list(message: types.Message):
	shop = pd.read_excel('Data.xlsx', engine = 'openpyxl')
	global shopping_list
	shopping_list = read_list(str(message['from']['id']))
	shop, groups = get_groups(shopping_list = shopping_list, shop = shop, navec = navec)
	
	if len(shopping_list) > 0:
		shopping_list = sort_list(shop, groups)
		text = ''
		ind = 0
		for i in shopping_list:
			text += i+"    /del{} \n".format(ind)
			ind += 1
	else:
		text = 'Список пуст'
	await message.answer(text, parse_mode = 'HTML')

@dp.message_handler(commands=['clear']) # Deletes all items from the list
@auth
async def clean_list(message: types.Message):
	drop(message['from']['id'])
	await message.answer('Список пуст')

@dp.message_handler(lambda message: message.text.startswith('/del')) # Deletes given item from the list
@auth
async def clean_list(message: types.Message):
	ind = int(message.text[4::])
	try:
		global shopping_list
		item = shopping_list[ind]
		delete_from_list(str(message['from']['id']), item)
		reply = 'Удалено'
	except:
		reply = 'Позиция не найдена'
	await message.answer(reply)

@dp.message_handler() # Adds item to the list
@auth
async def echo(message: types.Message):
	if check_value(message.text, navec):
		insert_into_list(str(message['from']['id']), message.text)
		reply = 'Добавил'
	else:
		reply = 'Не знаю такого слова'
	await message.answer(reply)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)