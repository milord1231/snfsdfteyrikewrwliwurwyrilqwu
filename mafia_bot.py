# -*- coding: utf8 -*-
import random
import sqlite3
import vk_api
from vk_api.longpoll import VkLongPoll
from vkbottle import Bot, Message
from vkbottle.keyboard import Keyboard, Text
from vkbottle import Bot, Message, keyboard_gen
from vkbottle.branch import Branch, ExitBranch 
import hashlib 
from vkbottle.user import User, Message
from vkbottle import VKError
from vkbottle.utils import logger
import aiohttp
import asyncio
import random
import os
from SimpleQIWI import *
import requests
import json
from datetime import datetime

QIWI_TOKEN = QIWI_TOKEN
QIWI_ACCOUNT = NUMBER

bot = Bot(A_TOKEN)
conn = sqlite3.connect(r"inf_users.db")
c = conn.cursor()
sqlite3.connect(":memory:", check_same_thread=False)
group_id = '-195266218'
vk_session = vk_api.VkApi(token=A_TOKEN)
token = A_TOKEN
from vk_api.longpoll import VkLongPoll, VkEventType
longpoll_type = VkLongPoll(vk_session)
print('\n\n\n|---------------|\n'
	'|--BOT RUNNING--|\n'
	'|---------------|\n')
api = QApi(token=QIWI_TOKEN, phone=QIWI_ACCOUNT)
#  🌕


def currency_k(n):
	if 'k' in n or 'к' in n:
		n = str(n)
		numb = list(n)
		j = 1
		if "к" in numb or "k" in numb:
			count = 0
			if "к" in numb:
				count = numb.count("к")
			elif 'k' in numb:
				count = numb.count("k")
			for i in range(count):
				numb.pop()
			if "к" in numb or "k" in numb or len(numb) > count:
				err = True
				value = 0
				return True, value
			else:
				value = ""
				for i in range(len(numb)):
					value += str(numb[i])
				value = int(value) * 1000 ** count
				err = False
				return False, value
	else:
		return False, int(n)


def get_user_balance(user_id):
	c.execute("SELECT balance FROM users_info WHERE id=%d" % user_id)
	balance = c.fetchone()[0]
	norm_bal = balance
	balance = ('{:,} $'.format(balance).replace(',', ' '))
	c.execute("SELECT card_balance FROM users_info WHERE id=%d" % user_id)
	card_balance = c.fetchone()[0]
	norm_card_bal = card_balance
	card_balance = ('{:,} $'.format(card_balance).replace(',', ' '))
	data = balance, card_balance, norm_bal, norm_card_bal
	return data
    

def edit_user_balance(user_id, summ, reverse=False):
	bal, card_balance, norm_bal, norm_card_bal = get_user_balance(user_id)
	if reverse:
		c.execute("UPDATE users_info SET balance=%d WHERE id=%d" % (int(norm_bal) - int(summ), user_id))
		conn.commit()
	else:
		c.execute("UPDATE users_info SET balance=%d WHERE id=%d" % (int(norm_bal) + int(summ), user_id))
		conn.commit()

def edit_user_card_balance(user_id, summ, reverse=False):
	bal, card_balance, norm_bal, norm_card_bal = get_user_balance(user_id)
	if reverse:
		c.execute("UPDATE users_info SET card_balance=%d WHERE id=%d" % (int(norm_card_bal) - int(summ), user_id))
		conn.commit()
	else:
		c.execute("UPDATE users_info SET card_balance=%d WHERE id=%d" % (int(norm_card_bal) + int(summ), user_id))
		conn.commit()


def is_digit1(string):
	string = str(string)
	if string.isdigit():
		return True
	else:
		try:
			float(string)
			return True
		except ValueError:
			return False

def currency(number):
	data = ('{:,}'.format(number).replace(',', ' '))
	return data


def join_mafia(user_id, mafia_id):
	user_id, mafia_id = int(user_id), int(mafia_id)
	mafia_name = c.execute(f'SELECT name FROM mafias WHERE id={mafia_id}').fetchone()
	c.execute('UPDATE users_info SET mafia_id=%d WHERE id=%d' % (mafia_id, user_id))
	conn.commit()
	c.execute('UPDATE users_info SET mafia_name=? WHERE id=?', (mafia_name[0], user_id))
	conn.commit()


@bot.on.chat_message(text='донат отмена', lower=True)
async def cancle_donate(ans: Message):
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if res is not None:
		pass
	else:
		c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
		conn.commit()
	result = c.execute(f"SELECT * FROM payment_query WHERE user_id = {ans.from_id}").fetchone()
	if result is None:
		await ans('🚫Нет платежей, ожидающих подтверждение.')
	else:
		await ans(f'✅Донат от {result[3]} на {result[1]} р. отменен!')
		c.execute(f"DELETE FROM payment_query WHERE user_id = {ans.from_id}") 
		conn.commit()


@bot.on.message(text='донат', lower=True)
async def err(ans: Message):
	await ans("🚫Использование: 'Донат <сумма>'")


@bot.on.chat_message(text='донат', lower=True)
async def err(ans: Message):
	await ans("🚫Использование: 'Донат <сумма>'")


@bot.on.chat_message(text='донат <summ>', lower=True)
async def donate(ans: Message, summ):
	err = False
	if "k" in str(summ).lower() or "к" in str(summ).lower():
		err, summ = currency_k(str(summ))
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if not is_digit1(summ) or err:
		await ans("🚫Использование: 'Донат <сумма>'") 
	elif int(summ) < 0 or '+' in str(summ):
		await ans("🚫Использование: 'Донат <сумма>'")
	else:
		if res is not None:
			pass
		else:
			c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
			conn.commit()
		result = c.execute(f"SELECT * FROM payment_query WHERE user_id = {ans.from_id}").fetchone()
		if result is None:
			random_code = str(random.randint(100000, 999999))
			date = datetime.fromtimestamp(int(time.time()))
			print(f"\n\n\t\t\t{date}")
			comment = str(ans.from_id) + '|donate'
			c.execute("INSERT INTO payment_query VALUES(?, ?, ?, ?)",  (ans.from_id, int(summ), comment, date))
			conn.commit()
			await ans(f'✅Счет на {summ}р. выставлен. Ожидание оплаты!\n\n\tДля оплаты переведите {summ}p. на номер +79877353524 С ОБЯЗАТЕЛЬНЫМ комментарием: "{comment}" (без ковычек), иначе донат не пройдет.\n\n⚠Для проверки оплаты напишите: "Обновить статус"⚠')
		else:
			await ans(f'🚫У вас есть непогашенный счет. \nЗавершите оплату или отмените её, командой "донат отмена". Если вы уже оплатили счёт, то проверте статус платежа командой "обновить статус".')



@bot.on.chat_message(text='обновить статус', lower=True)
async def update(ans: Message):
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if res is not None:
		pass
	else:
		c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
		conn.commit()
	s = requests.Session()
	s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN  
	parameters = {'rows': '50'}
	h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+ QIWI_ACCOUNT +'/payments', params = parameters)
	req = json.loads(h.text)
	print(req['data'][0]['comment'])
	result = c.execute(f"SELECT * FROM payment_query WHERE user_id = {ans.from_id}").fetchone()
	print(result)
	state = 0
	if result is not None:
		random_code = result[2]
		sum = result[1]
		for i in range(len(req['data'])):
			if req['data'][i]['comment'] == random_code:
				state = 1
				if req['data'][i]['sum']['amount'] == sum:
					c.execute(f"DELETE FROM payment_query WHERE user_id = {ans.from_id}") 
					state = 2
		if state == 2:
			await ans(f'📖Статус платежа:\n\t📝Платеж от {result[3]}\n\t💳Сумма {result[1]} руб.\n⚙Статус: \n  ✅Оплачено')
			prize = int(sum) * 1150
			await ans(f'✅На баланс начислено {currency(prize)}🌕 золотых')
			edit_user_balance(ans.from_id, prize)
		elif state == 1:
			await ans(f'📖Статус платежа:\n\t📝Платеж от {result[3]}\n\t💳Сумма {result[1]} руб.\n⚙Статус: \n  🚫Сумма не соответсвует требованной.')
		else:
			await ans(f'📖Статус платежа:\n\t📝Платеж от {result[3]}\n\t💳Сумма {result[1]} руб.\n⚙Статус: \n  🚫Не оплачено')
	else:
		await ans('🚫Нет платежей, ожидающих подтверждение.')





@bot.on.message(text='донат отмена', lower=True)
async def cancle_donate(ans: Message):
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if res is not None:
		pass
	else:
		c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
		conn.commit()
	result = c.execute(f"SELECT * FROM payment_query WHERE user_id = {ans.from_id}").fetchone()
	if result is None:
		await ans('🚫Нет платежей, ожидающих подтверждение.')
	else:
		await ans(f'✅Донат от {result[3]} на {result[1]} р. отменен!')
		c.execute(f"DELETE FROM payment_query WHERE user_id = {ans.from_id}") 
		conn.commit()



@bot.on.message(text='донат <summ>', lower=True)
async def donate(ans: Message, summ):
	err  = False
	if "k" in str(summ).lower() or "к" in str(summ).lower():
		err, summ = currency_k(str(summ))
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if not is_digit1(summ) or err:
		await ans("🚫Использование: 'Донат <сумма>'") 
	elif int(summ) < 0 or '+' in str(summ):
		await ans("🚫Использование: 'Донат <сумма>'")
	else:
		if res is not None:
			pass
		else:
			c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
			conn.commit()
		result = c.execute(f"SELECT * FROM payment_query WHERE user_id = {ans.from_id}").fetchone()
		if result is None:
			random_code = str(random.randint(100000, 999999))
			date = datetime.fromtimestamp(int(time.time()))
			print(f"\n\n\t\t\t{date}")
			comment = str(ans.from_id) + '|donate'
			c.execute("INSERT INTO payment_query VALUES(?, ?, ?, ?)",  (ans.from_id, int(summ), comment, date))
			conn.commit()
			await ans(f'✅Счет на {summ}р. выставлен. Ожидание оплаты!\n\n\tДля оплаты переведите {summ}p. на номер +79877353524 С ОБЯЗАТЕЛЬНЫМ комментарием: "{comment}" (без ковычек), иначе донат не пройдет.\n\n⚠Для проверки оплаты напишите: "Обновить статус"⚠')
		else:
			await ans(f'🚫У вас есть непогашенный счет. \nЗавершите оплату или отмените её, командой "донат отмена". Если вы уже оплатили счёт, то проверте статус платежа командой "обновить статус".')



@bot.on.message(text='обновить статус', lower=True)
async def update(ans: Message):
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if res is not None:
		pass
	else:
		c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
		conn.commit()
	s = requests.Session()
	s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN  
	parameters = {'rows': '50'}
	h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+ QIWI_ACCOUNT +'/payments', params = parameters)
	req = json.loads(h.text)
	print(req['data'][0]['comment'])
	result = c.execute(f"SELECT * FROM payment_query WHERE user_id = {ans.from_id}").fetchone()
	print(result)
	state = 0
	if result is not None:
		random_code = result[2]
		sum = result[1]
		for i in range(len(req['data'])):
			if req['data'][i]['comment'] == random_code:
				state = 1
				if req['data'][i]['sum']['amount'] == sum:
					c.execute(f"DELETE FROM payment_query WHERE user_id = {ans.from_id}") 
					state = 2
		if state == 2:
			await ans(f'📖Статус платежа:\n\t📝Платеж от {result[3]}\n\t💳Сумма {result[1]} руб.\n⚙Статус: \n  ✅Оплачено')
			prize = int(sum) * 1150
			await ans(f'✅На баланс начислено {currency(prize)}🌕 золотых')
			edit_user_balance(ans.from_id, prize)
		elif state == 1:
			await ans(f'📖Статус платежа:\n\t📝Платеж от {result[3]}\n\t💳Сумма {result[1]} руб.\n⚙Статус: \n  🚫Сумма не соответсвует требованной.')
		else:
			await ans(f'📖Статус платежа:\n\t📝Платеж от {result[3]}\n\t💳Сумма {result[1]} руб.\n⚙Статус: \n  🚫Не оплачено')
	else:
		await ans('🚫Нет платежей, ожидающих подтверждение.')

@bot.on.message(text='баланс', lower=True)
async def balance(ans: Message):
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if res is not None:
		pass
	else:
		c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
		conn.commit()
	bal, card_balance, norm_bal, norm_card_bal = get_user_balance(ans.from_id)
	await ans(f'💰@id{ans.from_id}({first_name}), ваш баланс:\n{bal}\n\n💳Баланс на карте: \n{card_balance}')

@bot.on.chat_message(text='баланс', lower=True)
async def balance(ans: Message):
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if res is not None:
		pass
	else:
		c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
		conn.commit()
	bal, card_balance, norm_bal, norm_card_bal = get_user_balance(ans.from_id)
	await ans(f'💰@id{ans.from_id}({first_name}), ваш баланс:\n{bal}\n\n💳Баланс на карте: \n{card_balance}')


@bot.on.message(text='карта снять', lower=True)
async def err(ans: Message):
	await ans('❌Использование: карта снять <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!')

@bot.on.chat_message(text='карта снять', lower=True)
async def err(ans: Message):
	await ans('❌Использование: карта снять <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!')


@bot.on.message(text='карта положить', lower=True)
async def err(ans: Message):
	await ans('❌Использование: карта положить <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!')


@bot.on.chat_message(text='карта положить', lower=True)
async def err(ans: Message):
	await ans('❌Использование: карта положить <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!')





@bot.on.chat_message(text='карта снять <summ>', lower=True)
async def add_card_balance(ans: Message, summ):
	err = False
	if "k" in str(summ).lower() or "к" in str(summ).lower():
		err, summ = currency_k(str(summ))
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if res is not None:
		pass
	else:
		c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
		conn.commit()
	bal, card_bal, norm_bal, norm_card_bal = get_user_balance(ans.from_id)
	if not is_digit1(summ) or err:
		await ans('❌Использование: карта снять <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!') 
	elif int(summ) < 0 or '+' in str(summ):
		await ans('❌Использование: карта снять <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!') 
	elif int(summ) > int(norm_card_bal):
		await ans('❌На карте нет столько денег')
	else:
		edit_user_card_balance(ans.from_id, int(summ), True)
		edit_user_balance(ans.from_id, int(summ))
		await ans(f'✅Вы сняли с карты {currency(int(summ))}$')



@bot.on.chat_message(text='карта положить <summ>', lower=True)
async def add_card_balance(ans: Message, summ):
	err = False
	if "k" in str(summ).lower() or "к" in str(summ).lower():
		err, summ = currency_k(str(summ))
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if res is not None:
		pass
	else:
		c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
		conn.commit()
	bal, card_bal, norm_bal, norm_card_bal = get_user_balance(ans.from_id)
	if not is_digit1(summ) or err:
		await ans('❌Использование: карта положить <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!.') 
	elif int(summ) < 0:
		await ans('❌Использование: карта положить <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!') 
	elif int(summ) > int(norm_bal):
		await ans('❌На балансе нет столько денег, сколько ты хочешь перевести на карту')
	else:
		edit_user_card_balance(ans.from_id, int(summ))
		edit_user_balance(ans.from_id, int(summ), True)
		await ans(f'✅Баланс карты пополнен на {currency(int(summ))}$')



@bot.on.message(text='карта снять <summ>', lower=True)
async def add_card_balance(ans: Message, summ):
	err = False
	if "k" in str(summ).lower() or "к" in str(summ).lower():
		err, summ = currency_k(str(summ))
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if res is not None:
		pass
	else:
		c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
		conn.commit()
	bal, card_bal, norm_bal, norm_card_bal = get_user_balance(ans.from_id)
	if not is_digit1(summ) or  err:
		await ans('❌Использование: карта снять <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!') 
	elif int(summ) < 0:
		await ans('❌Использование: карта снять <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!') 
	elif int(summ) > int(norm_card_bal):
		await ans('❌На карте нет столько денег')
	else:
		edit_user_card_balance(ans.from_id, int(summ), True)
		edit_user_balance(ans.from_id, int(summ))
		await ans(f'✅Вы сняли с карты {currency(int(summ))}$')



@bot.on.message(text='карта положить <summ>', lower=True)
async def add_card_balance(ans: Message, summ):
	err = False
	if "k" in str(summ).lower() or "к" in str(summ).lower():
		err, summ = currency_k(str(summ))
		await ans(f'{err} {summ}')
	data = await bot.api.users.get(user_ids=ans.from_id)
	first_name = data[0].first_name
	last_name = data[0].last_name
	name = first_name + ' ' + last_name
	c.execute("SELECT * FROM users_info WHERE id=%d" % ans.from_id)
	res = c.fetchone()
	if res is not None:
		pass
	else:
		c.execute("INSERT INTO users_info(balance, id, name) VALUES (?, ?, ?)", (2000, int(ans.from_id), name))
		conn.commit()
	bal, card_bal, norm_bal, norm_card_bal = get_user_balance(ans.from_id)
	summ = int(summ)
	if not is_digit1(summ) or err:
		await ans('❌Использование: карта положить <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!.') 
	elif int(summ) < 0:
		await ans('❌Использование: карта положить <сумма>\n⚠Параметр <сумма> должен быть целым, положительным числом!') 
	elif int(summ) > int(norm_bal):
		await ans('❌На балансе нет столько денег, сколько ты хочешь перевести на карту')
	else:
		edit_user_card_balance(ans.from_id, int(summ))
		edit_user_balance(ans.from_id, int(summ), True)
		await ans(f'✅Баланс карты пополнен на {currency(int(summ))}$')

@bot.on.message(text='мафия помощь', lower=True)
async def help_mafia(ans: Message):
	await ans(f'📖Помощь по мафиям: \n1️⃣ Мафия вступить <id мафии> - подать заявку на вступление\n2️⃣ Мафия создать <название> - создать собстенную "семью" (Стоимость: 2 500 000 $)\n3️⃣ Мафия пригласить <id пользователя> - пригласить пользователя в свою "семью" (Пользователь должен разрешить сообщения боту)\n4️⃣ Мафия список - получить список участиков вашей "семьи"\n5️⃣ Мафия топ - получить список мафий-лидеров\n6️⃣ Мафия распустить - удалить вашу мафию\n7️⃣ Мафия имя <новое имя> - изменить название мафии (Стоимость: 120 000 $)\n8️⃣ Мафия исключить <id участника> - исключить члена мафии\n9️⃣ Мафия профиль - просмотр профиля мафии')


@bot.on.chat_message(text='мафия помощь', lower=True)
async def help_mafia(ans: Message):
	await ans(f'📖Помощь по мафиям: \n1️⃣ Мафия вступить <id мафии> - подать заявку на вступление\n2️⃣ Мафия создать <название> - создать собстенную "семью" (Стоимость: 2 500 000 $)\n3️⃣ Мафия пригласить <id пользователя> - пригласить пользователя в свою "семью" (Пользователь должен разрешить сообщения боту)\n4️⃣ Мафия список - получить список участиков вашей "семьи"\n5️⃣ Мафия топ - получить список мафий-лидеров\n6️⃣ Мафия распустить - удалить вашу мафию\n7️⃣ Мафия имя <новое имя> - изменить название мафии (Стоимость: 120 000 $)\n8️⃣ Мафия исключить <id участника> - исключить члена мафии\n9️⃣ Мафия профиль - просмотр профиля мафии')


@bot.on.message(text='мафия создать <name>', lower=True)
async def help_mafia(ans: Message, name):
	mafia_create_free = c.execute('SELECT mafia_name FROM users_info WHERE id=%d' %  ans.from_id).fetchone()[0]
	if mafia_create_free is None or mafia_create_free == 'none':
		name_true = False
		bal, card_bal, norm_bal, norm_card_bal = get_user_balance(ans.from_id)
		name_tru = c.execute('SELECT name FROM mafias').fetchall()
		for i in range(len(name_tru)):
			if name not in name_tru[i][0]:
				name_true = False
			else:
				name_true = True
				break
		if norm_bal < 2500000 and norm_bal + norm_card_bal < 2500000:
			await ans(f'❌Недостаточно средств на балансе.\n Необходимо 2 500 000 $, у вас: {currency(norm_bal + norm_card_bal)} $ (баланс + баланс на карте)')
		elif name_true:
			await ans(f'❌Данное название уже занято.')
		elif norm_card_bal + norm_bal >= 2500000 and norm_bal < 2500000:
			await ans(f'✅Вы успешно создали мафию, её название:  "{name}". \n⚠Транзакция: \n\t списание с баланса ~ {currency(norm_bal)} $\n\t списание с карты ~ {currency(2500000 - norm_bal)} $')
			ids = c.execute("SELECT id from mafias").fetchall()
			if ids is not None:
				last_id = len(ids)
				c.execute('INSERT INTO mafias(id, name, users, admins) VALUES(?, ?, ?, ?)', (int(last_id) + 1, name, str(ans.from_id) + ';', str(ans.from_id) + '-dev;'))
				conn.commit()
			else:
				last_id = 0
				c.execute('INSERT INTO mafias(id, name, users, admins) VALUES(?, ?, ?, ?)', (int(last_id) + 1, name, str(ans.from_id) + ';', str(ans.from_id) + '-dev;'))
				conn.commit()
			edit_user_balance(ans.from_id, norm_bal, True)
			edit_user_card_balance(ans.from_id, 2500000 - norm_bal, True)
			join_mafia(ans.from_id, last_id + 1)
		else:
			await ans(f'✅Вы успешно создали мафию, её название:  "{name}". \n⚠Транзакция: \n\t списание с баланса ~ 2 500 000 $')
			ids = c.execute("SELECT id from mafias").fetchone()
			if ids is not None:
				last_id = len(ids)
				c.execute('INSERT INTO mafias(id, name, users, admins) VALUES(?, ?, ?, ?)', (int(last_id) + 1, name, str(ans.from_id) + ';', str(ans.from_id) + '-dev;'))
				conn.commit()
			else:
				last_id = 0
				c.execute('INSERT INTO mafias(id, name, users, admins) VALUES(?, ?, ?, ?)', (int(last_id) + 1, name, str(ans.from_id) + ';', str(ans.from_id) + '-dev;'))
				conn.commit()
			edit_user_balance(ans.from_id, 2500000, True)
			join_mafia(ans.from_id, last_id + 1)
	else:
		await ans('❌Вы уже состоите в мафии.\nПокинте её командой "мафия выход" или распустите, если вы создатель мафии командой "мафия распустить".')

@bot.on.chat_message(text='мафия создать <name>', lower=True)
async def help_mafia(ans: Message, name):
	mafia_create_free = c.execute('SELECT mafia_name FROM users_info WHERE id=%d' %  ans.from_id).fetchone()[0]
	if mafia_create_free is None or mafia_create_free == 'none':
		name_true = False
		bal, card_bal, norm_bal, norm_card_bal = get_user_balance(ans.from_id)
		name_tru = c.execute('SELECT name FROM mafias').fetchall()
		for i in range(len(name_tru)):
			if name not in name_tru[i][0]:
				name_true = False
			else:
				name_true = True
				break
		if norm_bal < 2500000 and norm_bal + norm_card_bal < 2500000:
			await ans(f'❌Недостаточно средств на балансе.\n Необходимо 2 500 000 $, у вас: {currency(norm_bal + norm_card_bal)} $ (баланс + баланс на карте)')
		elif name_true:
			await ans(f'❌Данное название уже занято.')
		elif norm_card_bal + norm_bal >= 2500000 and norm_bal < 2500000:
			await ans(f'✅Вы успешно создали мафию, её название:  "{name}". \n⚠Транзакция: \n\t списание с баланса ~ {currency(norm_bal)} $\n\t списание с карты ~ {currency(2500000 - norm_bal)} $')
			ids = c.execute("SELECT id from mafias").fetchall()
			if ids is not None:
				last_id = len(ids)
				c.execute('INSERT INTO mafias(id, name, users, admins) VALUES(?, ?, ?, ?)', (int(last_id) + 1, name, str(ans.from_id) + ';', str(ans.from_id) + '-dev;'))
				conn.commit()
			else:
				last_id = 0
				c.execute('INSERT INTO mafias(id, name, users, admins) VALUES(?, ?, ?, ?)', (int(last_id) + 1, name, str(ans.from_id) + ';', str(ans.from_id) + '-dev;'))
				conn.commit()
			edit_user_balance(ans.from_id, norm_bal, True)
			edit_user_card_balance(ans.from_id, 2500000 - norm_bal, True)
			join_mafia(ans.from_id, last_id + 1)
		else:
			await ans(f'✅Вы успешно создали мафию, её название:  "{name}". \n⚠Транзакция: \n\t списание с баланса ~ 2 500 000 $')
			ids = c.execute("SELECT id from mafias").fetchone()
			if ids is not None:
				last_id = len(ids)
				c.execute('INSERT INTO mafias(id, name, users, admins) VALUES(?, ?, ?, ?)', (int(last_id) + 1, name, str(ans.from_id) + ';', str(ans.from_id) + '-dev;'))
				conn.commit()
			else:
				last_id = 0
				c.execute('INSERT INTO mafias(id, name, users, admins) VALUES(?, ?, ?, ?)', (int(last_id) + 1, name, str(ans.from_id) + ';', str(ans.from_id) + '-dev;'))
				conn.commit()
			edit_user_balance(ans.from_id, 2500000, True)
			join_mafia(ans.from_id, last_id + 1)
	else:
		await ans('❌Вы уже состоите в мафии.\nПокинте её командой "мафия выход" или распустите, если вы создатель мафии командой "мафия распустить".')


def get_user_mafia(user_id):
	result = c.execute('SELECT * FROM users_info WHERE id=%d' % user_id).fetchall()
	mafia_name = result[0][4]
	mafia_id = result[0][5]
	admins_list = ''
	admins = c.execute('SELECT admins FROM mafias WHERE id=%d' % int(mafia_id)).fetchone()[0]
	admins = admins.split(';')
	del admins[-1]
	print(admins)
	for adm in admins:
		adm = adm.split('-')
		info = vk_session.method('users.get', {'user_ids': adm[0]})
		print(info[0])
		data = info[0]
		name = data['first_name'] + ' ' + data['last_name']
		if adm[1] == 'dev':
			admins_list += f"\n@id{adm[0]}({name}) - Босс мафии👑"
		elif adm[1] == 'adm':
			admins_list += f"\n@id{adm[0]}({name}) - Правая рука🎩"
		elif adm[1] == 'help':
			admins_list += f"\n@id{adm[0]}({name}) - Надежный друг🎓"
	users = c.execute('SELECT users FROM mafias WHERE id=%d' % int(mafia_id)).fetchone()[0]
	users = users.split(';')
	del users[-1]
	count = len(users)
	users_list = ''
	for usr in users:
		info = vk_session.method('users.get', {'user_ids': adm[0]})
		data = info[0]
		name = data['first_name'] + ' ' + data['last_name']
		users_list += f"\n@id{adm[0]}({name})"
	return mafia_name, mafia_id, admins_list, users_list, count


def get_mafia_info(mafia_id):
	result = c.execute('SELECT * FROM mafias WHERE id=%d' % mafia_id).fetchall()
	balance = result[0][2]
	rate = result[0][3]
	proporty = result[0][6]
	if proporty is None:
		proporty = 'Нет'
	else:
		proporty = result[0][6]
	return balance, rate, proporty


@bot.on.message(text='мафия профиль', lower=True)
async def profile_mafia(ans: Message):
	in_mafia = c.execute("SELECT mafia_id FROM users_info WHERE id=%d" % ans.from_id).fetchone()
	if in_mafia is not None:
		mafia_name, mafia_id, admins_list, users_list, count = get_user_mafia(ans.from_id)
		balance, rate, proporty = get_mafia_info(mafia_id)
		await ans(f'📖Название мафии: {mafia_name}\n🆔:{mafia_id}\n📊Число участников: {count}/10\n📃Участники: {users_list}\n👔Администрация: {admins_list}\n\n➖➖➖➖➖➖➖\n💰Казна: {currency(balance)} $\n🏆Рейтинг: {currency(rate)}\n🎫Имущество: {proporty}')
	else:
		await ans('❌Вы не состоите в мафии')



@bot.on.chat_message(text='мафия профиль', lower=True)
async def profile_mafia(ans: Message):
	in_mafia = c.execute("SELECT mafia_id FROM users_info WHERE id=%d" % ans.from_id).fetchone()
	if in_mafia is not None:
		mafia_name, mafia_id, admins_list, users_list, count = get_user_mafia(ans.from_id)
		balance, rate, proporty = get_mafia_info(mafia_id)
		await ans(f'📖Название мафии: {mafia_name}\n🆔:{mafia_id}\n📊Число участников: {count}/10\n📃Участники: {users_list}\n👔Администрация: {admins_list}\n\n➖➖➖➖➖➖➖\n💰Казна: {currency(balance)} $\n🏆Рейтинг: {currency(rate)}\n🎫Имущество: {proporty}')
	else:
		await ans('❌Вы не состоите в мафии')



if '__main__' == __name__:
	bot.run_polling()


#  1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟 
