import random
import sqlite3

import vk_api
import vkcoin
from vk_api.longpoll import VkLongPoll
from vkbottle import Bot
from vkcoinapi import *

vk_session = vk_api.VkApi(token='ab4145d1b0425733b338a2082ae05c1452c98a5d38a14a1100f239b07dc2249b6278d9b1e05d2679a4222')
bot = Bot("ab4145d1b0425733b338a2082ae05c1452c98a5d38a14a1100f239b07dc2249b6278d9b1e05d2679a4222")
group_id = '-195266217'
coin = VKCoin(key='8jrkRfHFBk76U4e8n7Cl&oJJe!BFkMnfA5&zh4#6dA88tjZQ19', merchantId=192557599)
pay = VKCoin(key='8jrkRfHFBk76U4e8n7Cl&oJJe!BFkMnfA5&zh4#6dA88tjZQ19', merchantId=192557599)
coin_sema = VKCoin(key='8jrkRfHFBk76U4e8n7Cl&oJJe!BFkMnfA5&zh4#6dA88tjZQ19', merchantId=192557599)
merchant = vkcoin.VKCoin(user_id=192557599, key='8jrkRfHFBk76U4e8n7Cl&oJJe!BFkMnfA5&zh4#6dA88tjZQ19')
vk = vk_session.get_api()
longpoll_type = VkLongPoll(vk_session)
conn = sqlite3.connect(r"all_inf.db")
c = conn.cursor()
sqlite3.connect(":memory:", check_same_thread=False)

while True:
	try:
		@merchant.payment_handler(handler_type='longpoll')
		def payment_received(data):
			user_id = data['from_id']
			amount = data['amount']
			amount = int(amount) / 1000
			print(f'\n Получен платёж на сумму {amount} от {user_id}'.format(amount=amount, user_id=user_id))
			c.execute("SELECT balance FROM us WHERE id=%d" % user_id)
			bal = c.fetchone()[0]
			c.execute("UPDATE us SET balance=%d WHERE id=%d" % (int(bal) + amount, user_id))
			conn.commit()
			vk.messages.send(
				user_id=user_id,
				message=f'✅Баланс пополнен на {amount} VkCoin\n 💳Баланс: {int(bal) + amount}',
				random_id=random.randint(1, 1000000000)
			)



		merchant.run_longpoll(tx=[1])  # Запускаем LongPoll
	except:
		print('ErrorMotherFucker')