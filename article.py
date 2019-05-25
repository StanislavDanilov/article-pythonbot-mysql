import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import pymysql.cursors
import requests
import random


def get_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='lucking1A*',
                                 db='firstbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
    

def random_mode():
    #Получаем рандомное число в районе от 1 до 200
    return random.choice(["Live", "Dead"])


def add_to_database(functionMode, x):
    #Создаем новую сессию
    connection = get_connection()
    #Наш запрос
    cursor = connection.cursor()
    sql = "INSERT INTO mode (Id_User, Mode) VALUES (%s, %s) ON DUPLICATE KEY UPDATE Mode = %s"
    #Выполняем наш запрос и вставляем свои значения
    cursor.execute(sql, (x, functionMode, functionMode))
    connection.commit()
    return functionMode


def select_from_database(idUser):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT Mode FROM mode WHERE Id_User = %s"
    cursor.execute(sql, (idUser,ПП))
    #Получаем запрашиваемые данных и заносим их в переменные
    for i in cursor:
        modeSend = i['Mode']
    if cursor.fetchall() == ():
        modeSend = 'Вы еще не пробовали'
    connection.close()
    return modeSend


vk_session = vk_api.VkApi(token="5af39fde0a7c747fa023f66538c8d7c12059b6ca910d0bb0cbd299df119061571a947454c953b0699d0d2")
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, "181744434")
#Проверка действий 
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        #Проверяем не пустое ли сообщение нам пришло
        if event.obj.text == 'Попытка':
            if event.from_user:
                idUser  = event.obj.from_id
                vk.messages.send(
                                    user_id=event.obj.from_id,
                                    random_id=get_random_id(),
                                    message="Ваш результат: " + str(add_to_database(random_mode(), idUser)))
        if event.obj.text == 'Последний результат':
            if event.from_user:
                idUser = event.obj.from_id
                vk.messages.send(
                                    user_id=event.obj.from_id,
                                    random_id=get_random_id(),
                                    message="Ваш прошлый результат: " + str(select_from_database(idUser)))