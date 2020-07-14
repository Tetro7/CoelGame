import os
import sys
import time
import random
from pynput import keyboard
import pyautogui

# Возбуждаемое исключение окончания игры
class GameOver(Exception):
    def __init__(self, text):
        self.txt = text

# Строка позволяющая обрабатывать события пользователя с клавиатуры
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

# Функция для очистки экрана cmd
clear = lambda: os.system('cls')

# Создаём изборажение игравого поля
a = [[' ' for i in range(21)] for j in range(12)]

# Класс для создания объекта ваганетки (в нём просто заданны все детальки для отрисовки ваганетки на поле)
class Telega:
	def __init__(self):	
		self.a_l = '\\'
		self.a_r = '/'
		self.b = '_'
		self.c = 'o'
		self.telega = [[' ' for i in range(5)] for i in range(2)]

# Созадём объект вагонетки и собираем её модель
gameObj = Telega()
gameObj.telega[0][0] = gameObj.a_l
gameObj.telega[0][1] = gameObj.b
gameObj.telega[0][2] = gameObj.b
gameObj.telega[0][3] = gameObj.b
gameObj.telega[0][4] = gameObj.a_r
gameObj.telega[1][1] = gameObj.c
gameObj.telega[1][3] = gameObj.c

# Массив с координатами, которые дают программе знать, откуда начать отрисовывать ваганетку
pologenie = [(9, 1), (9, 8), (9, 15)]
pos = 1 # Индикатор положения

# Создание текстур труб откуда будет сыпаться уголь и счётчик
a[0][0] = '\\'
a[0][3] = '\\'
a[0][8] = '|'
a[0][12] = '|'
a[0][17] = '/'
a[0][20] = '/'
a[11][0] = 'Coin:'
a[11][1] = 0
a[11][19] = 'HP:'
a[11][20] = 5


def scor():
	'''Функция осуществляет подсчёт собраных монеток'''

	if a[8][3] == 'O' and a[9][3] == '_':
		a[11][1] += 1 # Счётчик
		a[8][3] = ' '
	else:
		a[8][3] = ' '
		

	if a[8][10] == 'O' and a[9][10] == '_':
		a[11][1] += 1
		a[8][10] = ' '
	else:
		a[8][10] = ' '

	if a[8][17] == 'O' and a[9][17] == '_':
		a[11][1] += 1
		a[8][17] = ' '
	else:
		a[8][17] = ' '

def death():
	if a[8][3] == 'O' and a[9][3] == ' ':
		a[11][20] -= 1

	if a[8][10] == 'O' and a[9][10] == ' ':
		a[11][20] -= 1

	if a[8][17] == 'O' and a[9][17] == ' ':
		a[11][20] -= 1



def spawn():
	'''Функция осуществляет спавн монеток на поле'''

	indicator = random.randint(0, 1)
	if indicator == 1:
		coordinata = random.choice([3, 10, 17])
		a[2][coordinata] = 'O'

def goCoin():
	'''Функция передвигает монетки находящиеся на поле'''

	if a[5][3] == 'O':
		a[5][3] = ' '
		a[8][3] = 'O'

	if a[5][10] == 'O':
		a[5][10] = ' '
		a[8][10] = 'O'

	if a[5][17] == 'O':
		a[5][17] = ' '
		a[8][17] = 'O'


	if a[2][3] == 'O':
		a[2][3] = ' '
		a[5][3] = 'O'

	if a[2][10] == 'O':
		a[2][10] = ' '
		a[5][10] = 'O'

	if a[2][17] == 'O':
		a[2][17] = ' '
		a[5][17] = 'O'

	

def printTelega(pole, telega, x, y):
	'''Функция отрисовывает ваганетку на главном кадре'''

	for i in range(2):
		for j in range(5):
			pole[x + i][y + j] = telega.telega[i][j]

def delTelega(pole, telega, x, y):
	'''Функция удаляет ваганетку на главном кадре'''

	for i in range(2):
		for j in range(5):
			pole[x + i][y + j] = ' ' 	

def printPole():
	'''Функция, которая объединяет все функции рисования воедино и выполняет финальную сборку кадра,
	который видит пользователь'''

	X = 21 # Ширина поля
	Y = 12 # Высота поля
	global pos

	# Проверка помогает программе не выходит ьза пределлы кадра, чтобы не возбуждать исключение выхода за пределы списка
	if pos < 0:
		pos = 0
	if pos > 2:
		pos = 2

	# Код ниже сначало помещает телегу на основной кадр, после чего с помощью цикла кадр отрисовывается в консоле,
	# после выполняет функция подсчёта очков, а затем вагонетка стирается с поля
	printTelega(a, gameObj, pologenie[pos][0], pologenie[pos][1])
	for i in range(0,Y):
		for j in range(0,X):
			print(a[i][j], end=' ')
		print()
	death()
	scor()
	delTelega(a, gameObj, pologenie[pos][0], pologenie[pos][1])


def on_press(key):
	'''Функия, которая регестрирует нажатия пользователя'''

	global pos

	if key.char == 'a':
		pos -= 1
		return False
	if key.char == 'd':
		pos += 1
		return False
	if key.char == 'l':
		return False
	if key == keyboard.Key.esc:
		return False
	
    
def on_release(key):
	'''Функция служит для того, чтобы когда пользователь отпускал клавишу не срабатывало какое-либо событие'''
	return 0

clear()
print('В игре вы управляете ваганеткой, которая должна ловить золотые монетки, падающие из труб.')
print('Время в игре останавливается, если вы стоите на месте. Для перемещения вагонетки используйте клавиши A и D, а для возобновления течения времени нажимайте клавишу L')
print()
start = input('Напишите s, если вы хотите начать или нажмите Ctrl + Z, чтобы выйти из игры: ')

if start == 's':
	# Цикл, который собирает все функции вместе и является неким скелетом всей программы
	while True:
		try:
			if a[11][20] != 0:
				clear()
				goCoin()
				spawn()
				printPole()
				time.sleep(0.001)
				with keyboard.Listener(
    				on_press=on_press,
    				on_release=on_release) as listener:
					print('Press esc to exit')
					listener.join()
			else:
				clear()
				print('GameOver')
				print('Ваш счёт:', a[11][1])
				time.sleep(5)
				raise AttributeError
		except AttributeError:
			clear()
			print('Ваш счёт:', a[11][1])
			raise GameOver('GameOver')

    
    