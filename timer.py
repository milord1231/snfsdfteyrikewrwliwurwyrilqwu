import random
import sqlite3
import time
import vk_api
import vkcoin
import hashlib
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
conn = sqlite3.connect(r"timer.db")
c = conn.cursor()
sqlite3.connect(":memory:", check_same_thread=False)
connt = sqlite3.connect(r"all_inf.db")
t = connt.cursor()
sqlite3.connect(":memory:", check_same_thread=False)


def winner(id, summ):
	t.execute("SELECT balance FROM us WHERE id=%d" % (int(id)))
	bal = int(t.fetchone()[0])
	t.execute("UPDATE us SET balance=%d WHERE id=%d" % (bal + int(summ), int(id)))
	connt.commit()
	

while True:
	try:
		photos = [0, 'photo-195266217_457239019', 'photo-195266217_457239020', 'photo-195266217_457239021', 'photo-195266217_457239022', 'photo-195266217_457239023', 'photo-195266217_457239024']
		c.execute("SELECT time FROM chat_1 WHERE chat_id=%d" % 1)
		time1 = c.fetchone()[0]
		if time1 == 0:
			c.execute("SELECT chat_id FROM chat_1")
			chats = c.fetchall()
			for i in range(len(chats)):
				c.execute('SELECT stavki FROM chat_1 WHERE chat_id=%d' % int(chats[i][0]))
				stt = c.fetchone()[0]
				print(stt)
				st = stt.split(';')
				print(st)
				if stt != '0:0:0;':
					del st[0]

					print("LEN:", len(st))
					if len(st) != 1 and len(st) != 0:
						del st[-1]
					print(st)	
					vk.messages.send(
						chat_id=int(chats[i][0]),
						random_id=random.randint(1, 10000007777),
						message='Итак, результаты раунда...'
						)
					time.sleep(2)
					c.execute('SELECT stavki FROM chat_1 WHERE chat_id=%d' % int(chats[i][0]))
					res = c.fetchone()[0]
					print(f'\n{res}')
					bank = ''
					result = res.split(';')
					del result[0]
					del result[-1]
					st_1 = '•Ставки на ⚀ (1):\n'
					st_2 = '•Ставки на ⚁ (2):\n'
					st_3 = '•Ставки на ⚂ (3):\n'
					st_4 = '•Ставки на ⚃ (4):\n'
					st_5 = '•Ставки на ⚄ (5):\n'
					st_6 = '•Ставки на ⚅ (6):\n'
					st_7 = '•Ставки на нечётное:\n'
					st_8 = '•Ставки на чётное:\n'
					st_all = set()
					c.execute('SELECT win FROM chat_1 WHERE chat_id=%d' % int(chats[i][0]))
					win = int(c.fetchone()[0])
					if win == 1 or win == 3 or win == 5 or win == 8:
						win2 = 7
					else:
						win2 = 8
					print("WIN:", win2)
					for ell in result:
						el = ell.split(':')
						t.execute('SELECT name FROM us WHERE id=%d' % int(el[0]))
						name = t.fetchone()[0]
						winn = int(el[1])
						print('WINN:', winn)
						if winn == 1 or winn == 3 or winn == 5 or winn == 8:
							win3 = 7
						else:
							win3 = 8
						if int(el[1]) == 1:
							if int(el[1]) == win:
								st_1 += f"✅- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(+{int(el[2]) * 3} VkCoins)\n"
								winner(el[0], int(el[2])*3)
								st_all.add(1)
							else:
								st_1 += f"❌- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(-{int(el[2])} VkCoins)\n"
								st_all.add(1)
						elif int(el[1]) == 2:
							if int(el[1]) == win:
								st_2 += f"✅- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(+{int(el[2]) * 3} VkCoins)\n"
								st_all.add(2)
								winner(el[0], int(el[2])*3)
							else:
								st_2 += f"❌- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(-{int(el[2])} VkCoins)\n"
								st_all.add(2)
						elif int(el[1]) == 3:
							if int(el[1]) == win:
								st_3 += f"✅- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(+{int(el[2]) * 3} VkCoins)\n"
								st_all.add(3)
								winner(el[0], int(el[2])*3)
							else:
								st_3 += f"❌- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(-{int(el[2])} VkCoins)\n"
								st_all.add(3)
						elif int(el[1]) == 4:
							if int(el[1]) == win:
								st_4 += f"✅- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(+{int(el[2]) * 3} VkCoins)\n"
								st_all.add(4)
								winner(el[0], int(el[2])*3)
							else:
								st_4 += f"❌- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(-{int(el[2])} VkCoins)\n"
								st_all.add(4)
						elif int(el[1]) == 5:
							if int(el[1]) == win:
								st_5 += f"✅- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(+{int(el[2]) * 3} VkCoins)\n"
								st_all.add(5)
								winner(el[0], int(el[2])*3)
							else:
								st_5 += f"❌- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(-{int(el[2])} VkCoins)\n"
								st_all.add(5)
						elif int(el[1]) == 6:
							if int(el[1]) == win:
								st_6 += f"✅- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(+{int(el[2]) * 3} VkCoins)\n"
								st_all.add(6)
								winner(el[0], int(el[2])*3)
							else:
								st_6 += f"❌- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(-{int(el[2])} VkCoins)\n"
								st_all.add(6)
						elif win3 == 7:
							if win3 == win2:
								st_7 += f"✅- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(+{int(el[2]) * 2} VkCoins)\n"
								st_all.add(7)
								winner(el[0], int(el[2])*2)
							else:
								st_7 += f"❌- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(-{int(el[2])} VkCoins)\n"
								st_all.add(7)
						elif win3 == 8:
							if win3 == win2:
								st_8 += f"✅- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(+{int(el[2]) * 2} VkCoins)\n"
								st_all.add(8)
								winner(el[0], int(el[2])*2)
							else:
								st_8 += f"❌- @id{el[0]}({name}) поставил {el[2]} VkCoins\n(-{int(el[2])} VkCoins)\n"
								st_all.add(8)
					if st_all is set():
						bank = 'В этом раунде пока никто не поставил!'
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
						c.execute("SELECT hash FROM chat_1 WHERE chat_id=%d" % int(chats[i][0]))
						hash1 = (c.fetchone()[0])
						hash_object = hashlib.sha384(hash1.encode())
						hash2 = hash_object.hexdigest()
						vk.messages.send(
							chat_id=int(chats[i][0]),
							random_id=random.randint(1, 10000007777),
							message=f'🎲Результаты:\n\t--ВЫПАЛО ЧИСЛО {win}\n\n{bank}\n•Проверочное слово: {hash1}\n\n•Хэш: {hash2}',
							attachment=f'{photos[int(win)]}'
						)
				print(chats[i][0])
				rs = '0:0:0;'
				winsss = random.randint(1, 6)
				vk.messages.send(
					user_id=596624436,
					random_id=random.randint(0, 10000000000),
					message=f'Chat_id: {chats[i][0]}, WIN: {winsss}',
					attachment=f'{photos[int(winsss)]}'
				)
				c.execute("UPDATE chat_1 SET time=%d WHERE chat_id=%d" % (120, int(chats[i][0])))
				c.execute("UPDATE chat_1 SET win=%d WHERE chat_id=%d" % (winsss, int(chats[i][0])))
				c.execute('UPDATE chat_1 SET stavki=? WHERE chat_id=?', (rs, int(chats[i][0])))
				conn.commit()
				hash1_obj = hashlib.md5(f'{random.randint(1120, 1020020)}'.encode())
				hash2 = hash1_obj.hexdigest()
				c.execute('UPDATE chat_1 SET hash=? WHERE chat_id=?', (hash2, int(chats[i][0])))
				conn.commit()
				print('CHAT ID:', int(chats[i][0]))
		else:
			c.execute("SELECT chat_id FROM chat_1")
			chats = c.fetchall()
			for i in range(len(chats)):	
				print(chats[i][0])
				c.execute("UPDATE chat_1 SET time=%d WHERE chat_id=%d" % (time1 - 1, int(chats[i][0])))
				conn.commit()

		time.sleep(1)
	except:
		print('ERROR motherFucker')