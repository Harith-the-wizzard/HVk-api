import datetime
import vk_api
import time
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
import codecs
import asyncio

def send_message(peer_id, message, vk):
    vk.messages.send(peer_id=peer_id, message=message, random_id=get_random_id())

def buff(peer_id, message, vk, mess_id):
    vk.messages.send(peer_id=peer_id, message=message, random_id=get_random_id(), forward_messages = mess_id)

async def send(peer_id, message, vk, mess_id, i):
    await asyncio.sleep(10*i)
    buff(peer_id, message, vk, mess_id)
    i=i-1
    return i

test=2000000000

with codecs.open('text.txt', encoding='utf-8') as text:
    trash=text.read()
    trash=trash.split('|')
    token=trash[0].split(':')
    token=token[1]
    chat_all=trash[1].split(':')
    chat_all=int(chat_all[1])+test
    chat_arch=trash[2].split(':')
    chat_arch=int(chat_arch[1])+test
    chat_buff=trash[3].split(':')
    chat_buff=chat_buff[1]
    text_all=trash[4].split('::')
    text_all=text_all[1]
    text_arch=trash[5].split('::')
    text_arch=text_arch[1]
    text_price=trash[6].split('::\r\n')
    text_price=text_price[1]
    text_price=text_price.split('\r\n')
    text.close()

chat_buff=chat_buff.split(', ')
for i in range(len(chat_buff)):
    chat_buff[i]=int(chat_buff[i])+test

price={}
tim={}
rep={}
forw=''
d=0
o=0

for i in text_price:
    i=i.split(' - ')
    i[0]=i[0].lower()
    i[1]=i[1].lower()
    price[i[0]]=i[1]

mess=''

reseruct=True
clean=True
fire=True
kd=True

dt=0
t_all=0
t_arch=0
t_clean=0
t_fire=0
t_reseruct=0
j=0

m_id=621215551
# Мой ID 621215551 Притулы 267369151
try:
    vk_session = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
except Exception as e:
    print(e)
kol=-183040898

t=0
znach=0



while True:
    try:
        timer=time.time_ns()//1000000000
        a=vk.messages.search(q='паладин пытается Вас воскресить!', peer_id=kol)
        b=vk.messages.search(q='на Вас наложено очищение огнем!', peer_id=kol)
        for i in b['items']:

            if (i['text']=='Очищение огнём') and i['from_id']==m_id:
                t=i['date']
                if timer-t>=900:
                    clean=True
                else:
                    clean=False
                    t_fire=timer+900-(timer-t)
                break
        for i in a['items']:
            if 'Воскрешение' == i['text'] and i['from_id']==m_id:
                t=i['date']
                if timer-t>=21600:
                    reseruct=True
                else:
                    reseruct=False
                    t_reseruct=timer+21600-(timer-t)
                break
        for i in b['items']:

            if (i['text']=='Очищение') and i['from_id']==m_id:
                t=i['date']
                if timer-t>=900:
                    clean=True
                else:
                    clean=False
                    t_clean=timer+900-(timer-t)
                break
        response = vk.users.get()
        print('Автобот успешно запущен.')
        for event in longpoll.listen():
            timer=time.time_ns()//1000000000
            if t_all-timer<=0: # Таймер для общего чата
                t_all=time.time()+10800
                send_message(chat_all, text_all, vk)

            if t_arch-timer<=0: #Таймер для архива
                t_arch=time.time()+3600
                send_message(chat_arch, text_arch, vk)

            if t_clean-timer<=0: # Таймер для очищений
                clean=True

            if t_reseruct-timer<=0: # Таймер для возрождения
                reseruct=True

            if event.type == VkEventType.MESSAGE_NEW:
                if event.peer_id==chat_all:

                    message=vk.messages.getById(message_ids=event.message_id)
                    v_id=message['items'][0]['from_id'] # Сличение. Проверка, что это Смотр.
                    if v_id==kol:
                        if 'получено' in event.text: # Проверка того, что в сообщении есть получено.
                            text=event.text
                            text=text.split(' ')
                            f_id=text[0].split('|')
                            f_id=f_id[0].split('[id')
                            f_id=int(f_id[1])
                            if m_id==f_id: # Сличение по ID с зашитым значением.
                                text=event.text
                                text=text.split(' получено: ')
                                text=text[1]
                                text=text.split(' от ')
                                text=text[0]
                                text=text[1:]
                                try:
                                    if text.find('*')==True: # Проверка по наличию множества предметов.
                                        text=text.split('*')
                                        kolvo=int(text[0])
                                        text=text[1].lower()
                                        pr=price[text].split(' ')
                                        mn=int(pr[0])*kolvo
                                        gear='Передать '+str(mn)+' '+pr[1]
                                    else:
                                        text=text.lower()
                                        pr=price[text].split(' ')
                                        mn=int(pr[0])
                                        gear='Передать '+str(mn)+' '+pr[1]
                                except Exception as e:
                                    continue
                                text=event.text
                                text=text.split(' от игрока ')
                                text=text[1].split('!')
                                text=text[0]
                                p_id=text.split('|')
                                p_id=p_id[0].split('id')
                                p_id=int(p_id[1])
                                giver=vk.messages.search(q='Передать', peer_id=chat_all)
                                for i in giver['items']:
                                    if int(i['from_id'])==p_id:
                                        forw=i['id']
                                        break
                                sender=vk.messages.search(q='Передать', peer_id=chat_all)
                                for i in sender['items']:
                                    if int(i['from_id'])==m_id:
                                        dt=int(i['date'])
                                        break
                                if timer-dt>10:
                                    buff(chat_all, gear, vk, forw)
                                else:
                                    j = j + 1
                                    j = asyncio.run(send(chat_all, gear, vk, forw, j))
                if event.peer_id in chat_buff:
                    if '.' == event.text:
                        send_message(event.peer_id, '/', vk)
                    if '/барыга воскреси' == event.text.lower() and reseruct==True:
                        buff(kol, 'Воскрешение', vk, event.message_id)
                        rep={'m_id':event.message_id, 'p_id':event.peer_id}
                    if '/барыга воскреси' == event.text.lower() and reseruct==False:
                        pr=t_reseruct-timer
                        h=pr//3600
                        m=pr%3600
                        m=m//60
                        s=m%60
                        mes='Я ещё в кд ' + str(h)+ ' часов ' + str(m) + ' минут ' + str(s) + ' секунд'
                        buff(event.peer_id, mes, vk, event.message_id)

                    if '/барыга огонь' == event.text.lower() and clean==True:
                        buff(kol, 'Очищение огнём', vk, event.message_id)
                        rep={'m_id':event.message_id, 'p_id':event.peer_id}
                    if '/барыга огонь' == event.text.lower() and clean==False:
                        pr=t_fire-timer
                        m=pr//60
                        s=pr%60
                        mes='Я ещё в кд ' + str(m) + ' минут ' + str(s) + ' секунд'
                        buff(event.peer_id, mes, vk, event.message_id)

                    if '/барыга очищение' == event.text.lower() and clean==True:
                        buff(kol, 'Очищение', vk, event.message_id)
                        rep={'m_id':event.message_id, 'p_id':event.peer_id}
                    if '/барыга очищение' == event.text.lower() and clean==False:
                        pr=t_clean-timer
                        m=pr//60
                        s=pr%60
                        mes='Я ещё в кд ' + str(m) + ' минут ' + str(s) + ' секунд'
                        buff(event.peer_id, mes, vk, event.message_id)

                    if '/барыга хочу' in event.text.lower() and 'воды' in event.text:
                        check=vk.messages.search(q='Передать', peer_id=event.peer_id)
                        text=event.text
                        id=event.message_id
                        text=text.split(' ')
                        text=int(text[2])
                        if text==1:
                            mes='Передать первозданная вода'
                        else:
                            mes='Передать первозданная вода - ' + str(text) + ' штук'
                        for i in check['items']:
                            if 'Передать' in i['text'] and i['from_id']==m_id and timer-i['date']<=10:
                                kd=False
                                j=j+1
                                j=asyncio.run(send(event.peer_id, mes, vk, event.message_id, j))
                                break
                            else:
                                kd=True
                                break
                        if kd==True:
                            buff(event.peer_id, mes, vk, id)
                if event.from_group and event.peer_id==-183040898:
                    if 'на Вас наложено очищение огнем!' in event.text:
                        t_fire = timer + 900
                        clean = False
                        buff(rep['p_id'], 'Очишение огнём успешно!', vk, rep['m_id'])
                    if 'паладин пытается Вас воскресить!' in event.text:
                        t_reseruct=timer+21600
                        reseruct = False
                        buff(rep['p_id'], 'Воскрешение успешно!', vk, rep['m_id'])
                    if 'на Вас наложено очищение!' in event.text:
                        t_clean = timer+900
                        clean=False
                        buff(rep['p_id'], 'Очищение успешно!', vk, rep['m_id'])
                    if 'цель уже получала очищение огнем' in event.text:
                        buff (rep['p_id'], 'Цель уже была очищена огнём. Не могу пока что очистить', vk, rep['m_id'])
                    if 'этому персонажу не требуется воскрешение.' in event.text:
                        buff(rep['p_id'], 'А ну не балуй. Ты итак живой, я не буду тебя воскрешать.', vk, rep['m_id'])
                    if 'нельзя воскресить игроков меньше 30-го уровня.' in event.text:
                        buff(rep['p_id'], 'Прости, но ты ещё слишком юн, чтобы я мог тебя воскресить.', vk, rep['m_id'])
                    if 'воскрешение работает только на игроков уровнем ниже, чем использующий умение паладин.' in event.text:
                        buff(rep['p_id'], 'Удивительно, но я слишком молод, чтобы суметь тебя воскресить.', vk, rep['m_id'])







    except Exception as e:
        err_time=datetime.datetime.now()
        err=open('logs.txt', 'a')
        err_log=str(err_time)+' '+str(e)+'\n'
        err.write(err_log)
        err.close()
        print('Ошибка! Загляните в логи и передайте их Хариту')
