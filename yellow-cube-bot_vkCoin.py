# coding=utf-8
import random
import sqlite3
import vk_api
import vkcoin
from vk_api.longpoll import VkLongPoll
from vkbottle import Bot, Message
from vkcoinapi import *
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
# Login = padenev2005@gmail.com
# Password = Klopik21*
conn = sqlite3.connect(r"all_inf.db")
c = conn.cursor()
sqlite3.connect(":memory:", check_same_thread=False)
conn_timer = sqlite3.connect(r"timer.db")
t = conn_timer.cursor()
sqlite3.connect(":memory:", check_same_thread=False)
#  ab4145d1b0425733b338a2082ae05c1452c98a5d38a14a1100f239b07dc2249b6278d9b1e05d2679a4222


vk_session = vk_api.VkApi(token='ab4145d1b0425733b338a2082ae05c1452c98a5d38a14a1100f239b07dc2249b6278d9b1e05d2679a4222')
bot = Bot("ab4145d1b0425733b338a2082ae05c1452c98a5d38a14a1100f239b07dc2249b6278d9b1e05d2679a4222")
group_id = '-195266217'
coin = VKCoin(key='8jrkRfHFBk76U4e8n7Cl&oJJe!BFkMnfA5&zh4#6dA88tjZQ19', merchantId=192557599)
pay = VKCoin(key='8jrkRfHFBk76U4e8n7Cl&oJJe!BFkMnfA5&zh4#6dA88tjZQ19', merchantId=192557599)
coin_sema = VKCoin(key='8jrkRfHFBk76U4e8n7Cl&oJJe!BFkMnfA5&zh4#6dA88tjZQ19', merchantId=192557599)
merchant = vkcoin.VKCoin(user_id=192557599, key='8jrkRfHFBk76U4e8n7Cl&oJJe!BFkMnfA5&zh4#6dA88tjZQ19')
vk = vk_session.get_api()
longpoll_type = VkLongPoll(vk_session)

time = 3600

while True:
	try:
		print(time - 1)

		@bot.error_handler.captcha_handler
		async def solve_captcha(e: VKError):
		    logger.error("Captcha. Solving...")
		    async with aiohttp.ClientSession() as session:
		        async with session.get(e.raw_error["captcha_img"]) as response_image:
		            image = await response_image.content.read()
		        async with session.post(
		            "https://rucaptcha.com/in.php",
		            data={"key": os.environ["RUCAPTCHA_TOKEN"], "file": image},
		        ) as response_wait:
		            result_id = (await response_wait.text()).split("|")[1]
		        await asyncio.sleep(5)
		        async with session.get(
		            "https://rucaptcha.com/res.php",
		            params={
		                "key": os.environ["RUCAPTCHA_TOKEN"],
		                "id": result_id,
		                "action": "get",
		            },
		        ) as result:
		            key = (await result.text()).split("|")[1]
		    logger.success(f"Captcha was solved. Key: {key}")
		    return key

		@bot.on.message(text='найти беседу', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Найти беседу"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Реферальная система"), color="positive")
			await ans(f'Ссылка на беседу: https://vk.me/join/AJQ1dzCl5xeBFUu30n9DcDHb', keyboard=keyboard.generate())
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()


		@bot.on.message(text='пополнить', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Найти беседу"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Реферальная система"), color="positive")
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()
			await ans('✅Вот ссылка для пополнения:\n',merchant.get_payment_url(amount=1000000, payload=random.randint(12414, 14141941148124), free_amount=True), keyboard=keyboard.generate())


		@bot.on.chat_message(text='пополнить', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Кубик"), color="positive")
			await ans('✅Вот ссылка для пополнения:\n',merchant.get_payment_url(amount=1000000, payload=random.randint(12414, 14141941148124), free_amount=True), keyboard=keyboard.generate())




		@bot.on.chat_message(text='/check')
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			get = merchant.get_balance(493626256, 399467546, 448286665, 197860247)
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Кубик"), color="positive")
			if ans.from_id == 192557599 or ans.from_id == 418294336:
				await bot.api.messages.send(
					message=f"@id493626256 : \n{get['493626256'] / 1000} Vk Coins\n\n@id399467546 : \n{get['399467546'] / 1000} Vk Coins\n\n"
							f"@id448286665 : \n{get['448286665'] / 1000} Vk Coins\n\n@id197860247 :\n {get['197860247'] / 1000} Vk Coins\n\n",
					peer_id=ans.from_id, random_id=random.randint(1, 20139012739812691263961293612936), keyboard=keyboard.generate())




		@bot.on.message(text='get id <user>')
		async def changes(ans: Message, user):
			c.execute("SELECT adm FROM us WHERE id=%d" % ans.from_id)
			adm = int(c.fetchone()[0])
			if adm >= 9:
				c.execute("SELECT id FROM us WHERE name=%s" % user)
				ids = int(c.fetchone()[0])
				await ans(f'{ids}')
			else:
				keyboard = Keyboard(one_time=False)
				keyboard.add_row()
				keyboard.add_button(Text(label="Баланс"), color="primary")
				keyboard.add_button(Text(label="Пополнить"), color="positive")
				keyboard.add_button(Text(label="Вывод"), color="negative")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 10"), color="secondary")
				keyboard.add_button(Text(label="Казино 50"), color="secondary")
				keyboard.add_button(Text(label="Казино 100"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 250"), color="secondary")
				keyboard.add_button(Text(label="Казино 500"), color="secondary")
				keyboard.add_button(Text(label="Казино 1000"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Реферальная система"), color="positive")
				await ans('Ничего не понял, но очень интересно.\n\tТыкай на кнопки)')



		@bot.on.chat_message(text='get bal')
		async def changes(ans: Message):
			c.execute("SELECT adm FROM us WHERE id=%d" % ans.from_id)
			adm = int(c.fetchone()[0])
			if adm >= 9:
				if ans.reply_message.from_id is not None:
					c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.reply_message.from_id))
					bal = c.fetchone()[0]
					await ans(f'Balance: {bal}')
			else:
				keyboard = Keyboard(one_time=False)
				keyboard.add_row()
				keyboard.add_button(Text(label="Баланс"), color="primary")
				keyboard.add_button(Text(label="Пополнить"), color="positive")
				keyboard.add_button(Text(label="Вывод"), color="negative")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 10"), color="secondary")
				keyboard.add_button(Text(label="Казино 50"), color="secondary")
				keyboard.add_button(Text(label="Казино 100"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 250"), color="secondary")
				keyboard.add_button(Text(label="Казино 500"), color="secondary")
				keyboard.add_button(Text(label="Казино 1000"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Реферальная система"), color="positive")
				await ans('Ничего не понял, но очень интересно.\n\tТыкай на кнопки)')

		@bot.on.chat_message(text='get real bal')
		async def changes(ans: Message):
			c.execute("SELECT adm FROM us WHERE id=%d" % ans.from_id)
			adm = int(c.fetchone()[0])
			if adm >= 9:
				if ans.reply_message.from_id is not None:
					bal = ('{:,}'.format(merchant.get_balance(int(ans.reply_message.from_id))[str(ans.reply_message.from_id)]).replace(',', ' '))
					await ans(f'Real balance: {bal}')
			else:
				keyboard = Keyboard(one_time=False)
				keyboard.add_row()
				keyboard.add_button(Text(label="Баланс"), color="primary")
				keyboard.add_button(Text(label="Пополнить"), color="positive")
				keyboard.add_button(Text(label="Вывод"), color="negative")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 10"), color="secondary")
				keyboard.add_button(Text(label="Казино 50"), color="secondary")
				keyboard.add_button(Text(label="Казино 100"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 250"), color="secondary")
				keyboard.add_button(Text(label="Казино 500"), color="secondary")
				keyboard.add_button(Text(label="Казино 1000"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Реферальная система"), color="positive")
				await ans('Ничего не понял, но очень интересно.\n\tТыкай на кнопки)')		

		@bot.on.chat_message(text='get id')
		async def changes(ans: Message):
			c.execute("SELECT adm FROM us WHERE id=%d" % ans.from_id)
			adm = int(c.fetchone()[0])
			if adm >= 9:
				if ans.reply_message.from_id is not None:
					await ans(f'id: {ans.reply_message.from_id}')
			else:
				keyboard = Keyboard(one_time=False)
				keyboard.add_row()
				keyboard.add_button(Text(label="Баланс"), color="primary")
				keyboard.add_button(Text(label="Пополнить"), color="positive")
				keyboard.add_button(Text(label="Вывод"), color="negative")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 10"), color="secondary")
				keyboard.add_button(Text(label="Казино 50"), color="secondary")
				keyboard.add_button(Text(label="Казино 100"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 250"), color="secondary")
				keyboard.add_button(Text(label="Казино 500"), color="secondary")
				keyboard.add_button(Text(label="Казино 1000"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Реферальная система"), color="positive")
				await ans('Ничего не понял, но очень интересно.\n\tТыкай на кнопки)')



	



		@bot.on.message(text='edit balance <user_id> <summ>')
		async def changes(ans: Message, user_id, summ):
			c.execute("SELECT adm FROM us WHERE id=%d" % ans.from_id)
			adm = int(c.fetchone()[0])
			if adm >= 9:
				c.execute("SELECT balance FROM us WHERE id=%d" % int(user_id))
				bal = int(c.fetchone()[0])
				c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + int(summ), int(user_id)))
				conn.commit()
				await ans(f'Успешно!')
				await bot.api.messages.send(user_id=int(user_id), random_id=random.randint(1, 12313131), message=f'Вам добавлено {summ} VkCoins')
			else:
				keyboard = Keyboard(one_time=False)
				keyboard.add_row()
				keyboard.add_button(Text(label="Баланс"), color="primary")
				keyboard.add_button(Text(label="Пополнить"), color="positive")
				keyboard.add_button(Text(label="Вывод"), color="negative")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 10"), color="secondary")
				keyboard.add_button(Text(label="Казино 50"), color="secondary")
				keyboard.add_button(Text(label="Казино 100"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 250"), color="secondary")
				keyboard.add_button(Text(label="Казино 500"), color="secondary")
				keyboard.add_button(Text(label="Казино 1000"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Реферальная система"), color="positive")
				await ans('Ничего не понял, но очень интересно.\n\tТыкай на кнопки)')





		@bot.on.message(text='change <chat_id> <number>')
		async def changes(ans: Message, chat_id, number):
			c.execute("SELECT adm FROM us WHERE id=%d" % ans.from_id)
			adm = int(c.fetchone()[0])
			if adm >= 9:
				t.execute("UPDATE chat_1 SET win=%d WHERE chat_id=%d" % (int(number), int(chat_id)))
				conn_timer.commit()
				await ans(f'Ах ты шуллер, ну окей. Изменено на {number}')
			else:
				keyboard = Keyboard(one_time=False)
				keyboard.add_row()
				keyboard.add_button(Text(label="Баланс"), color="primary")
				keyboard.add_button(Text(label="Пополнить"), color="positive")
				keyboard.add_button(Text(label="Вывод"), color="negative")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 10"), color="secondary")
				keyboard.add_button(Text(label="Казино 50"), color="secondary")
				keyboard.add_button(Text(label="Казино 100"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 250"), color="secondary")
				keyboard.add_button(Text(label="Казино 500"), color="secondary")
				keyboard.add_button(Text(label="Казино 1000"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Реферальная система"), color="positive")
				await ans('Ничего не понял, но очень интересно.\n\tТыкай на кнопки)')



		@bot.on.message(text='/check')
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			get = merchant.get_balance(493626256, 399467546, 448286665, 197860247)
			if ans.from_id == 192557599 or ans.from_id == 418294336:
				keyboard = Keyboard(one_time=False)
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Найти беседу"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Реферальная система"), color="positive")
			await bot.api.messages.send(
				message=f"@id493626256 : \n{get['493626256'] / 1000} Vk Coins\n\n@id399467546 : \n{get['399467546'] / 1000} Vk Coins\n\n"
						f"@id448286665 : \n{get['448286665'] / 1000} Vk Coins\n\n@id197860247 :\n {get['197860247'] / 1000} Vk Coins\n\n",
				peer_id=ans.from_id, random_id=random.randint(1, 20139012739812691263961293612936), keyboard=keyboard.generate())



		@bot.on.message(text='история')
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			if ans.from_id == 192557599:
				transactions = coin.getTransactions()
				keyboard = Keyboard(one_time=False)
				keyboard.add_row()
				keyboard.add_button(Text(label="Баланс"), color="primary")
				keyboard.add_button(Text(label="Пополнить"), color="positive")
				keyboard.add_button(Text(label="Вывод"), color="negative")
				keyboard.add_row()
				keyboard.add_button(Text(label="Найти беседу"), color="positive")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 10"), color="secondary")
				keyboard.add_button(Text(label="Казино 50"), color="secondary")
				keyboard.add_button(Text(label="Казино 100"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 250"), color="secondary")
				keyboard.add_button(Text(label="Казино 500"), color="secondary")
				keyboard.add_button(Text(label="Казино 1000"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Реферальная система"), color="positive")
				await ans(f"{transactions}", keyboard=keyboard.generate())



		@bot.on.chat_message(text='кубик', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			keyboard = Keyboard(inline=True)
			keyboard.add_row()
			keyboard.add_button(Text(label="⚀ (1)"), color="secondary")
			keyboard.add_button(Text(label="⚁ (2)"), color="secondary")
			keyboard.add_button(Text(label="⚂ (3)"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="⚃ (4)"), color="secondary")
			keyboard.add_button(Text(label="⚄ (5)"), color="secondary")
			keyboard.add_button(Text(label="⚅ (6)"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Чётное"), color="positive")
			keyboard.add_button(Text(label="Нечётное"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Банк"), color="primary")
			await ans('Выбери, каким окажется кубик сейчас!', keyboard=keyboard.generate())



		'''
		@bot.on.message(text='кубик', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			keyboard = Keyboard(inline=True)
			keyboard.add_row()
			keyboard.add_button(Text(label="⚀ (1)"), color="secondary")
			keyboard.add_button(Text(label="⚁ (2)"), color="secondary")
			keyboard.add_button(Text(label="⚂ (3)"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="⚃ (4)"), color="secondary")
			keyboard.add_button(Text(label="⚄ (5)"), color="secondary")
			keyboard.add_button(Text(label="⚅ (6)"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Чётное"), color="positive")
			keyboard.add_button(Text(label="Нечётное"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Банк"), color="primary")
			await ans('Выбери, каким окажется кубик сейчас!', keyboard=keyboard.generate())
		'''


		@bot.on.chat_message(text="⚀ (1)", lower=True)
		async def wrapper(ans: Message):
			#  192557599:1:10000;12332131:4:500;
			await ans('Чтобы поставить на ⚀ (1) напиши: \n"ставка <сумма>"')
			c.execute('UPDATE us SET old_stav=? WHERE id=?', (1, ans.from_id))
			conn.commit()


		@bot.on.chat_message(text="⚁ (2)", lower=True)
		async def wrapper(ans: Message):
			#  192557599:1:10000;12332131:4:500;
			await ans('Чтобы поставить на ⚁ (2) напиши: \n"ставка <сумма>"')
			c.execute('UPDATE us SET old_stav=? WHERE id=?', (2, ans.from_id))
			conn.commit()


		@bot.on.chat_message(text="⚂ (3)", lower=True)
		async def wrapper(ans: Message):
			#  192557599:1:10000;12332131:4:500;
			await ans('Чтобы поставить на ⚂ (3) напиши: \n"ставка <сумма>"')
			c.execute('UPDATE us SET old_stav=? WHERE id=?', (3, ans.from_id))
			conn.commit()



		@bot.on.chat_message(text="⚃ (4)", lower=True)
		async def wrapper(ans: Message):
			#  192557599:1:10000;12332131:4:500;
			await ans('Чтобы поставить на ⚃ (4) напиши: \n"ставка <сумма>"')
			c.execute('UPDATE us SET old_stav=? WHERE id=?', (4, ans.from_id))
			conn.commit()


		@bot.on.chat_message(text="⚄ (5)", lower=True)
		async def wrapper(ans: Message):
			#  192557599:1:10000;12332131:4:500;
			await ans('Чтобы поставить на ⚄ (5) напиши: \n"ставка <сумма>"')
			c.execute('UPDATE us SET old_stav=? WHERE id=?', (5, ans.from_id))
			conn.commit()


		@bot.on.chat_message(text="⚅ (6)", lower=True)
		async def wrapper(ans: Message):
			#  192557599:1:10000;12332131:4:500;
			await ans('Чтобы поставить на ⚅ (6) напиши: \n"ставка <сумма>"')
			c.execute('UPDATE us SET old_stav=? WHERE id=?', (6, ans.from_id))
			conn.commit()


		@bot.on.chat_message(text="нечётное", lower=True)
		async def wrapper(ans: Message):
			#  192557599:1:10000;12332131:4:500;
			await ans('Чтобы поставить на нечётное напиши: \n"ставка <сумма>"')
			c.execute('UPDATE us SET old_stav=? WHERE id=?', (8, ans.from_id))
			conn.commit()


		@bot.on.chat_message(text="чётное", lower=True)
		async def wrapper(ans: Message):
			#  192557599:1:10000;12332131:4:500;
			await ans('Чтобы поставить на чётное напиши: \n"ставка <сумма>"')
			c.execute('UPDATE us SET old_stav=? WHERE id=?', (7, ans.from_id))
			conn.commit()



		@bot.on.chat_message(text="ставка <summ>", lower=True)
		async def wrapper(ans: Message, summ):
			if int(summ) < 1:
				await ans('❌Ставка не может быть меньше 1 VkCoins\n Чтобы отменить ставку напишите "отмена"') 
			else:
				c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
				bal = c.fetchone()[0]
				if int(summ) > int(bal):
					await ans(f'❌Недостаточно средств. Ссылка на пополнение:\n {merchant.get_payment_url(1000, random.randint(12312, 19361631236163), True)}')
				else:
					c.execute("SELECT old_stav FROM us WHERE id=%d" % ans.from_id)
					old_stav = c.fetchone()[0]
					old_stav = int(old_stav)
					if old_stav != 0:
						chat_id = ans.chat_id
						if old_stav == 1:
							st = int(summ)
							await ans(f"✅Ставка {summ} VkCoins на ⚀ (1) успешно поставлена!")
							c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
							bal = c.fetchone()[0]
							c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
							conn.commit()
							t.execute("SELECT stavki FROM chat_1 WHERE chat_id=%d" % ans.chat_id)
							res = t.fetchone()[0]
							print(ans.chat_id)
							new_res=f'{res}{ans.from_id}:1:{summ};'
							t.execute('UPDATE chat_1 SET stavki=? WHERE chat_id=?', (new_res, ans.chat_id))
							conn_timer.commit()
							print('СТАВКИ:',res)
							t.execute("SELECT total FROM chat_1 WHERE chat_id=%d" % chat_id)
							res = int(t.fetchone()[0])
							t.execute("UPDATE chat_1 SET total=%d WHERE chat_id=%d" % (int(summ)+res, chat_id))
							conn_timer.commit()
						elif old_stav == 2:
							st = int(summ)
							await ans(f"✅Ставка {summ} VkCoins на ⚁ (2) успешно поставлена!")
							c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
							bal = c.fetchone()[0]
							c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
							conn.commit()
							t.execute("SELECT stavki FROM chat_1 WHERE chat_id=%d" % ans.chat_id)
							res = t.fetchone()[0]
							print(ans.chat_id)
							new_res=f'{res}{ans.from_id}:2:{summ};'
							t.execute('UPDATE chat_1 SET stavki=? WHERE chat_id=?', (new_res, ans.chat_id))
							conn_timer.commit()
							print('СТАВКИ:',res)
							t.execute("SELECT total FROM chat_1 WHERE chat_id=%d" % chat_id)
							res = int(c.fetchone()[0])
							t.execute("UPDATE chat_1 SET total=%d WHERE chat_id=%d" % (int(summ)+res, chat_id))
							conn_timer.commit()
						elif old_stav == 3:
							st = int(summ)
							await ans(f"✅Ставка {summ} VkCoins на ⚂ (3) успешно поставлена!")
							c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
							bal = c.fetchone()[0]
							c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
							conn.commit()
							t.execute("SELECT stavki FROM chat_1 WHERE chat_id=%d" % ans.chat_id)
							res = t.fetchone()[0]
							print(ans.chat_id)
							new_res=f'{res}{ans.from_id}:3:{summ};'
							t.execute('UPDATE chat_1 SET stavki=? WHERE chat_id=?', (new_res, ans.chat_id))
							conn_timer.commit()
							print('СТАВКИ:',res)
							t.execute("SELECT total FROM chat_1 WHERE chat_id=%d" % chat_id)
							res = int(t.fetchone()[0])
							c.execute("UPDATE chat_1 SET total=%d WHERE chat_id=%d" % (int(summ)+res, chat_id))
							conn_timer.commit()
						elif old_stav == 4:
							st = int(summ)
							await ans(f"✅Ставка {summ} VkCoins на ⚃ (4) успешно поставлена!")
							c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
							bal = c.fetchone()[0]
							c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
							conn.commit()
							t.execute("SELECT stavki FROM chat_1 WHERE chat_id=%d" % ans.chat_id)
							res = t.fetchone()[0]
							print(ans.chat_id)
							new_res=f'{res}{ans.from_id}:4:{summ};'
							t.execute('UPDATE chat_1 SET stavki=? WHERE chat_id=?', (new_res, ans.chat_id))
							conn_timer.commit()
							print('СТАВКИ:',res)
							t.execute("SELECT total FROM chat_1 WHERE chat_id=%d" % chat_id)
							res = int(t.fetchone()[0])
							t.execute("UPDATE chat_1 SET total=%d WHERE chat_id=%d" % (int(summ)+res, chat_id))
							conn_timer.commit()
						elif old_stav == 5:
							st = int(summ)
							await ans(f"✅Ставка {summ} VkCoins на ⚄ (5) успешно поставлена!")
							c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
							bal = c.fetchone()[0]
							c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
							conn.commit()
							t.execute("SELECT stavki FROM chat_1 WHERE chat_id=%d" % ans.chat_id)
							res = t.fetchone()[0]
							print(ans.chat_id)
							new_res=f'{res}{ans.from_id}:5:{summ};'
							t.execute('UPDATE chat_1 SET stavki=? WHERE chat_id=?', (new_res, ans.chat_id))
							conn_timer.commit()
							print('СТАВКИ:',res)
							t.execute("SELECT total FROM chat_1 WHERE chat_id=%d" % chat_id)
							res = int(t.fetchone()[0])
							t.execute("UPDATE chat_1 SET total=%d WHERE chat_id=%d" % (int(summ)+res, chat_id))
							conn_timer.commit()
						elif old_stav == 6:
							st = int(summ)
							await ans(f"✅Ставка {summ} VkCoins на ⚅ (6) успешно поставлена!")
							c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
							bal = c.fetchone()[0]
							c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
							conn.commit()
							t.execute("SELECT stavki FROM chat_1 WHERE chat_id=%d" % ans.chat_id)
							res = t.fetchone()[0]
							print(ans.chat_id)
							new_res=f'{res}{ans.from_id}:6:{summ};'
							t.execute('UPDATE chat_1 SET stavki=? WHERE chat_id=?', (new_res, ans.chat_id))
							conn_timer.commit()
							print('СТАВКИ:',res)
							t.execute("SELECT total FROM chat_1 WHERE chat_id=%d" % chat_id)
							res = int(t.fetchone()[0])
							t.execute("UPDATE chat_1 SET total=%d WHERE chat_id=%d" % (int(summ)+res, chat_id))
							conn_timer.commit()
						elif old_stav == 7:
							st = int(summ)
							await ans(f"✅Ставка {summ} VkCoins на чётное успешно поставлена!")
							c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
							bal = c.fetchone()[0]
							c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
							conn.commit()
							t.execute("SELECT stavki FROM chat_1 WHERE chat_id=%d" % ans.chat_id)
							res = t.fetchone()[0]
							print(ans.chat_id)
							new_res=f'{res}{ans.from_id}:7:{summ};'
							t.execute('UPDATE chat_1 SET stavki=? WHERE chat_id=?', (new_res, ans.chat_id))
							conn_timer.commit()
							print('СТАВКИ:',res)
							t.execute("SELECT total FROM chat_1 WHERE chat_id=%d" % chat_id)
							res = int(t.fetchone()[0])
							t.execute("UPDATE chat_1 SET total=%d WHERE chat_id=%d" % (int(summ)+res, chat_id))
							conn_timer.commit()
						elif old_stav == 8:
							st = int(summ)
							await ans(f"✅Ставка {summ} VkCoins на нечётное успешно поставлена!")
							c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
							bal = c.fetchone()[0]
							c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
							conn.commit()
							t.execute("SELECT stavki FROM chat_1 WHERE chat_id=%d" % ans.chat_id)
							res = t.fetchone()[0]
							print(ans.chat_id)
							new_res=f'{res}{ans.from_id}:8:{summ};'
							t.execute('UPDATE chat_1 SET stavki=? WHERE chat_id=?', (new_res, ans.chat_id))
							conn_timer.commit()
							print('СТАВКИ:',res)
							t.execute("SELECT total FROM chat_1 WHERE chat_id=%d" % chat_id)
							res = int(t.fetchone()[0])
							t.execute("UPDATE chat_1 SET total=%d WHERE chat_id=%d" % (int(summ)+res, chat_id))
							conn_timer.commit()
						c.execute("UPDATE us SET old_stav=%d WHERE id=%d" % (0, ans.from_id))
						conn.commit()
					else:
						await ans('❌Сначала нужно выбрать, на что вы хотите поставить!\nДля этого напишите "кубик" и нажмите на кнопки.')



		@bot.on.chat_message(text='банк', lower=True)
		async def Bank(ans: Message):
			chat_id = ans.chat_id
			t.execute('SELECT stavki FROM chat_1 WHERE chat_id=%d' % chat_id)
			res = t.fetchone()[0]
			print(f'\n{res}')
			bank = ''
			result = res.split(';')
			del result[0]
			del result[-1]
			bank = ''
			st_1 = '•Ставки на ⚀ (1):\n'
			st_2 = '•Ставки на ⚁ (2):\n'
			st_3 = '•Ставки на ⚂ (3):\n'
			st_4 = '•Ставки на ⚃ (4):\n'
			st_5 = '•Ставки на ⚄ (5):\n'
			st_6 = '•Ставки на ⚅ (6):\n'
			st_7 = '•Ставки на чётное:\n'
			st_8 = '•Ставки на нечётное:\n'
			st_all = set()
			print(result)
			for ell in result:
				el = ell.split(':')
				c.execute('SELECT name FROM us WHERE id=%d' % int(el[0]))
				name = c.fetchone()[0]
				if int(el[1]) == 1:
					st_1 += f"\t- @id{el[0]}({name}) поставил {el[2]} VkCoins\n"
					st_all.add(1)
				elif int(el[1]) == 2:
					st_2 += f"\t- @id{el[0]}({name}) поставил {el[2]} VkCoins\n"
					st_all.add(2)
				elif int(el[1]) == 3:
					st_3 += f"\t- @id{el[0]}({name}) поставил {el[2]} VkCoins\n"
					st_all.add(3)
				elif int(el[1]) == 4:
					st_4 += f"\t- @id{el[0]}({name}) поставил {el[2]} VkCoins\n"
					st_all.add(4)
				elif int(el[1]) == 5:
					st_5 += f"\t- @id{el[0]}({name}) поставил {el[2]} VkCoins\n"
					st_all.add(5)
				elif int(el[1]) == 6:
					st_6 += f"\t- @id{el[0]}({name}) поставил {el[2]} VkCoins\n"
					st_all.add(6)
				elif int(el[1]) == 7:
					st_7 += f"\t- @id{el[0]}({name}) поставил {el[2]} VkCoins\n"
					st_all.add(7)
				elif int(el[1]) == 8:
					st_8 += f"\t- @id{el[0]}({name}) поставил {el[2]} VkCoins\n"
					st_all.add(8)
			print(st_all)
			if st_all == set():
				bank = '🎲В этом раунде пока никто не поставил!'
			else:
				if 1 in st_all:
					bank += st_1
				if 2 in st_all:
					bank += st_2
				if 3 in st_all:
					bank += st_3
				if 4 in st_all:
					bank += st_4
				if 5 in st_all:
					bank += st_5
				if 6 in st_all:
					bank += st_6
				if 7 in st_all:
					bank += st_7
				if 8 in st_all:
					bank += st_8
			print(bank)
			t.execute("SELECT time FROM chat_1 WHERE chat_id=%d" % ans.chat_id)
			time1 = t.fetchone()[0]
			a = int(time1)
			h = a // 3600
			m = (a // 60) % 60
			s = a % 60
			if m < 10:
				m = str('0' + str(m))
			else:
				m = str(m)
			if s < 10:
				s = str('0' + str(s))
			else:
				s = str(s)
			print(str(m) + ':' + str(s))
			time = str(m) + ':' + str(s)
			t.execute("SELECT hash FROM chat_1 WHERE chat_id=%d" % ans.chat_id)
			hash2 = (t.fetchone()[0])
			print('hash:', hash2)
			hash_object = hashlib.sha384(hash2.encode())
			hash2 = hash_object.hexdigest()
			await ans(f'🎲{bank}\n\n•Хэш: {hash2}\n\n\n\t•Отставшееся время: {time}')





		@bot.on.message(text='магазин <name>')
		async def wrapper(ans: Message, name):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			if ans.from_id == 192557599:
				keyboard = Keyboard(one_time=False)
				keyboard.add_row()
				keyboard.add_button(Text(label="Баланс"), color="primary")
				keyboard.add_button(Text(label="Пополнить"), color="positive")
				keyboard.add_button(Text(label="Вывод"), color="negative")
				keyboard.add_row()
				keyboard.add_button(Text(label="Найти беседу"), color="positive")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 10"), color="secondary")
				keyboard.add_button(Text(label="Казино 50"), color="secondary")
				keyboard.add_button(Text(label="Казино 100"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Казино 250"), color="secondary")
				keyboard.add_button(Text(label="Казино 500"), color="secondary")
				keyboard.add_button(Text(label="Казино 1000"), color="secondary")
				keyboard.add_row()
				keyboard.add_button(Text(label="Реферальная система"), color="positive")
				coin.setShopName(name=f'{name}')
				await ans(f"Имя магазина успешно изменено!", keyboard=keyboard.generate())
				if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
					c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
					ref = int(c.fetchone()[0])
					c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
					ref_done = int(c.fetchone()[0])
					if ref_done == 0 :
						bonus = 1000
						data = await bot.api.users.get(user_ids=int(ans.ref_source))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
						c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
						c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
						conn.commit()
						if ref != 35:
							data = await bot.api.users.get(user_ids=int(ans.from_id))
							first_name = data[0].first_name
							last_name = data[0].last_name
							await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
							c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
							bal = int(c.fetchone()[0])
							c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
							conn.commit()
						else:
							await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
							c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
							bal = int(c.fetchone()[0])
							c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
							conn.commit()



		@bot.on.chat_message(text='баланс', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
			bal = c.fetchone()[0]
			bal = ('{:,}'.format(bal).replace(',', ' '))
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Кубик"), color="positive")
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()
			await ans(f'💳Ваш баланс: \n{bal} VkCoin', keyboard=keyboard.generate())
			c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
			bal = c.fetchone()[0]
			if bal != 0:
				bal = ('{:,}'.format(bal).replace(',', ' '))
				await ans(f'💳Ваш тестовый баланс: \n{bal} VkCoin', keyboard=keyboard.generate())


		@bot.on.message(text='баланс', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
			bal = c.fetchone()[0]
			bal = ('{:,}'.format(bal).replace(',', ' '))
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Найти беседу"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Реферальная система"), color="positive")
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()
			await ans(f'💳Ваш баланс: \n{bal} VkCoin', keyboard=keyboard.generate())
			c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
			bal = c.fetchone()[0]
			if bal != 0:
				bal = ('{:,}'.format(bal).replace(',', ' '))
				await ans(f'💳Ваш тестовый баланс: \n{bal} VkCoin', keyboard=keyboard.generate())


		@bot.on.chat_message(text='вывод', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()[0]
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Кубик"), color="positive")
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()
			if int(res) == 0:
				await ans(f'❌На балансе нет VkCoins', keyboard=keyboard.generate())
			else:
				data = {'merchantId': 192557599, 'key':'8jrkRfHFBk76U4e8n7Cl&oJJe!BFkMnfA5&zh4#6dA88tjZQ19', 'toId': ans.from_id, 'amount': int(res) * 1000}
				data['markAsMerchant'] = True
				data['shopName'] = 'Yellow Cube'
				merchant._send_api_request('send', params=data)
				res = ('{:,}'.format(res).replace(',', ' '))
				await ans(f'✅Вывод средств: \n{res} VkCoins', keyboard=keyboard.generate())
				c.execute("UPDATE us SET balance=%d" % (0))
				conn.commit()



		@bot.on.message(text='вывод', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()[0]
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Найти беседу"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Реферальная система"), color="positive")
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()
			if int(res) == 0:
 				await ans(f'❌На балансе нет VkCoins', keyboard=keyboard.generate())
			else:
				data = {'merchantId': 192557599, 'key': '8jrkRfHFBk76U4e8n7Cl&oJJe!BFkMnfA5&zh4#6dA88tjZQ19',
						'toId': ans.from_id, 'amount': int(res) * 1000}
				data['markAsMerchant'] = True
				data['shopName'] = 'Yellow Cube'
				merchant._send_api_request('send', params=data)
				res = ('{:,}'.format(res).replace(',', ' '))
				await ans(f'✅Вывод средств: \n{res} VkCoins', keyboard=keyboard.generate())
				c.execute("UPDATE us SET balance=%d" % (0))
				conn.commit()

		@bot.on.message(text='казино <summ>', lower=True)
		async def casino(ans: Message, summ):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
			bal = c.fetchone()[0]
			win = random.randint(1, 3)
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Найти беседу"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Реферальная система"), color="positive")
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()
			if int(bal) < int(summ):
				await ans(f'❌Недостаточно средств. Ссылка на пополнение:\n {merchant.get_payment_url(1000, random.randint(12312, 19361631236163), True)}', keyboard=keyboard.generate())
			else:
				if win == 1:
					summ1 = ('{:,}'.format(int(summ)).replace(',', ' '))
					c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) + int(summ), ans.from_id))
					conn.commit()
					c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					bal = '{:0,.0f}'.format(int(bal))
					await ans(f'✅Победа +{summ1} VkCoin\n💳Ваш баланс: \n{bal} VkCoin', keyboard=keyboard.generate())
				else:
					summ1 = ('{:,}'.format(int(summ)).replace(',', ' '))
					c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
					conn.commit()
					c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					bal = ('{:,}'.format(bal).replace(',', ' '))
					await ans(f'❌Поражение -{summ1} VkCoin\n💳Ваш баланс: \n{bal} VkCoin', keyboard=keyboard.generate())



		@bot.on.chat_message(text='казино <summ>', lower=True)
		async def casino(ans: Message, summ):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
			bal = c.fetchone()[0]
			win = random.randint(1, 3)
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Кубик"), color="positive")
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()
			if int(bal) < int(summ):
				await ans(f'❌Недостаточно средств. Ссылка на пополнение:\n {merchant.get_payment_url(1000, random.randint(12312, 19361631236163), True)}',
					keyboard=keyboard.generate())
			else:
				if win == 1:
					summ1 = ('{:,}'.format(int(summ)).replace(',', ' '))
					c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) + int(summ), ans.from_id))
					conn.commit()
					c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					bal = '{:0,.0f}'.format(int(bal))
					await ans(f'✅Победа +{summ1} VkCoin\n💳Ваш баланс: \n{bal} VkCoin', keyboard=keyboard.generate())
				else:
					summ1 = ('{:,}'.format(int(summ)).replace(',', ' '))
					c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
					conn.commit()
					c.execute("SELECT balance FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					bal = ('{:,}'.format(bal).replace(',', ' '))
					await ans(f'❌Поражение -{summ1} VkCoin\n💳Ваш баланс: \n{bal} VkCoin', keyboard=keyboard.generate())


		@bot.on.message(text='/add', lower=True)
		async def test_add_bal(ans: Message):
			c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
			bal = c.fetchone()[0]
			c.execute("UPDATE us SET test_bal=%d WHERE id=%d" % (int(bal) + 50000, ans.from_id))
			conn.commit()
			c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
			bal = c.fetchone()[0]
			bal = ('{:,}'.format(bal).replace(',', ' '))
			await ans(f'💳Ваш тестовый баланс: \n{bal} VkCoin')
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()


		@bot.on.message(text='/казино <summ>', lower=True)
		async def casino(ans: Message, summ):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
			bal = c.fetchone()[0]
			win = random.randint(1, 3)
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Найти беседу"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Реферальная система"), color="positive")
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()
			if int(bal) < int(summ):
				await ans(f'❌Недостаточно средств.\n Пополнение тестового баланса по команде "/add"', keyboard=keyboard.generate())
			else:
				if win == 1:
					summ1 = ('{:,}'.format(int(summ)).replace(',', ' '))
					c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					c.execute("UPDATE us SET test_bal=%d WHERE id=%d" % (int(bal) + int(summ), ans.from_id))
					conn.commit()
					c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					bal = '{:0,.0f}'.format(int(bal))
					await ans(f'✅Победа +{summ1} VkCoin\n💳Ваш тестовый баланс: \n{bal} VkCoin', keyboard=keyboard.generate())
				else:
					summ1 = ('{:,}'.format(int(summ)).replace(',', ' '))
					c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					c.execute("UPDATE us SET test_bal=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
					conn.commit()
					c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					bal = ('{:,}'.format(bal).replace(',', ' '))
					await ans(f'❌Поражение -{summ1} VkCoin\n💳Ваш тестовый баланс: \n{bal} VkCoin', keyboard=keyboard.generate())



		@bot.on.chat_message(text='/казино <summ>', lower=True)
		async def casino(ans: Message, summ):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
			bal = c.fetchone()[0]
			win = random.randint(1, 3)
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Кубик"), color="positive")
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()
			if int(bal) < int(summ):
				await ans(f'❌Недостаточно средств.\n Пополнение тестового баланса по команде "/add"', keyboard=keyboard.generate())
			else:
				if win == 1:
					summ1 = ('{:,}'.format(int(summ)).replace(',', ' '))
					c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					c.execute("UPDATE us SET test_bal=%d WHERE id=%d" % (int(bal) + int(summ), ans.from_id))
					conn.commit()
					c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					bal = '{:0,.0f}'.format(int(bal))
					await ans(f'✅Победа +{summ1} VkCoin\n💳Ваш тестовый баланс: \n{bal} VkCoin', keyboard=keyboard.generate())
				else:
					summ1 = ('{:,}'.format(int(summ)).replace(',', ' '))
					c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					c.execute("UPDATE us SET test_bal=%d WHERE id=%d" % (int(bal) - int(summ), ans.from_id))
					conn.commit()
					c.execute("SELECT test_bal FROM us WHERE id=%d" % ans.from_id)
					bal = c.fetchone()[0]
					bal = ('{:,}'.format(bal).replace(',', ' '))
					await ans(f'❌Поражение -{summ1} VkCoin\n💳Ваш тестовый баланс: \n{bal} VkCoin', keyboard=keyboard.generate())




		@bot.on.chat_message(text='помощь', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Кубик"), color="positive")
			await ans('Мои команды:\n\tПополнить\n\tВывод\n\tКазино {сумма}\n\tБаланс', keyboard=keyboard.generate())
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()



		@bot.on.message(text='помощь', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			keyboard = Keyboard(one_time=False)
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Найти беседу"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Реферальная система"), color="positive")
			await ans('Мои команды:\n\tПополнить\n\tВывод\n\tКазино {сумма}\n\tБаланс', keyboard=keyboard.generate())
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()


		@bot.on.chat_message(text='привет', lower=True)
		async def wrapper(ans: Message):
			c.execute("SELECT * FROM us WHERE id=%d" % ans.from_id)
			res = c.fetchone()
			if res is not None:
				pass

			else:
				info = vk_session.method('users.get', {'user_ids': ans.from_id})
				data = info[0]
				from_id = ans.from_id
				name = data['first_name'] + ' ' + data['last_name']
				c.execute("INSERT INTO us(balance, id, name) VALUES (?, ?, ?)", (0, int(from_id), name))
				conn.commit()
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Кубик"), color="positive")
			await ans('Ну привет!', keyboard=keyboard.generate())
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()



		@bot.on.message(text=['реф', 'реферальная система'], lower=True)
		async def referal(ans: Message):
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Найти беседу"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Реферальная система"), color="positive")
			data =  vk.utils.getShortLink(url=f'vk.me/-195266217?ref=100&ref_source={ans.from_id}')
			link = data['short_url']
			print(link)
			#  link = f'vk.me/-195266217?ref=100&ref_source={ans.from_id}'
			await ans(f'За каждого приглашенного друга вы получаете 1 000 VkCoins\nПригласите 35 друзей и получите бонус в 50 000 VkCoins\nВаша реферальная ссылка: {link}')
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()

		@bot.on.message()
		async def text(ans: Message):
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Найти беседу"), color="positive")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Реферальная система"), color="positive")
			if ans.ref_source is not None and int(ans.from_id) != int(ans.ref_source):
				c.execute("SELECT ref FROM us WHERE id=%d" % int(ans.ref_source))
				ref = int(c.fetchone()[0])
				c.execute("SELECT ref_done FROM us WHERE id=%d" % int(ans.from_id))
				ref_done = int(c.fetchone()[0])
				if ref_done == 0 :
					bonus = 1000
					data = await bot.api.users.get(user_ids=int(ans.ref_source))
					first_name = data[0].first_name
					last_name = data[0].last_name
					await ans(f'Вас пригласил: @id{ans.ref_source}({first_name} {last_name})\n Он получил бонус: {bonus} VKCoins', keyboard=keyboard.generate())
					c.execute("UPDATE us SET ref_done=%d WHERE id=%d" % (1, ans.from_id))
					c.execute("UPDATE us SET ref=%d WHERE id=%d" % (ref + 1, int(ans.ref_source)))
					conn.commit()
					if ref != 35:
						data = await bot.api.users.get(user_ids=int(ans.from_id))
						first_name = data[0].first_name
						last_name = data[0].last_name
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source),message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nВаш бонус: 1 000 VkCoins\nПригласите еще {35 - (ref + 1)} друзей и получите бонус 50 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % (int(ans.ref_source)))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 1000, int(ans.ref_source)))
						conn.commit()
					else:
						await bot.api.messages.send(random_id=random.randint(1, 128321983), user_id=int(ans.ref_source) ,message=f'@id{ans.from_id}({first_name} {last_name}) был приглашен по вашей ссылке. \nУра! Это был 35-ый приглашенный пользователь, ваш бонус: 50 000 VkCoins\nВы можете приглашать еще друзей, но бонус будет 1 000 VkCoins')
						c.execute("SELECT balance FROM us WHERE id=%d" % int(ans.ref_source))
						bal = int(c.fetchone()[0])
						c.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + 50000, int(ans.ref_source)))
						conn.commit()

			data = vk.groups.isMember(group_id=195266217, user_id=int(ans.from_id), extended=True)
			print('IS IN GROUP:', data['member'])
			await ans(f'Ничего не понял, но очень интересно!\n\tТыкай на кнопки)', keyboard=keyboard.generate())

		@bot.on.chat_invite()
		async def wrapper(ans: Message):
			keyboard = Keyboard(one_time=False)
			keyboard.add_row()
			keyboard.add_button(Text(label="Баланс"), color="primary")
			keyboard.add_button(Text(label="Пополнить"), color="positive")
			keyboard.add_button(Text(label="Вывод"), color="negative")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 10"), color="secondary")
			keyboard.add_button(Text(label="Казино 50"), color="secondary")
			keyboard.add_button(Text(label="Казино 100"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Казино 250"), color="secondary")
			keyboard.add_button(Text(label="Казино 500"), color="secondary")
			keyboard.add_button(Text(label="Казино 1000"), color="secondary")
			keyboard.add_row()
			keyboard.add_button(Text(label="Кубик"), color="positive")
			await ans("‍Большое спасибо за приглашение! Выражаем вам огромную благодарность за добавление бота в беседу.\n\n Выдайте боту доступ ко всей переписке или права администратора, в случае если вы не создатель беседы, пользоваться ботом можно через упоминания.", keyboard=keyboard.generate())




		if __name__ == "__main__":
			bot.run_polling()

	except:
		print('ERROR motherFucker')
