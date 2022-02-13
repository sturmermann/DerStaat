# - *- coding: utf- 8 - *-
print('Игровой бот запущен')
from random import randint
import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.upload import VkUpload
import pickle
import time
from threading import Thread
import math
from PIL import Image, ImageColor
from PIL import ImageDraw

class prov():
    def __init__(self):
        self.master = ''

class chat1():
    def __init__(self, id):
        global userlist
        self.id = id
        self.settings = [1,1,1]
        try:
            data = vk.messages.getConversationMembers( peer_id = 2000000000 + self.id )
            for i in data.get('items'):
                o = True
                for j in userlist:
                    if i.get('member_id') == j.id:
                        o = False
                        break
                if o == True:
                    userlist.append(player(i.get('member_id')))
        except:
            pass

class player():
    def __init__(self, id):
        self.id = id
        self.name = "Пользователь"
        self.capital = 6000
        self.power = 0
        self.glory = 0
        self.fabric = [0, 0, 0]
        self.clan = ''

class fabric():
    def __init__(self, price, income):
        self.price = price
        self.income = income

class clan():
    def __init__(self, master):
        self.name = "Новый Клан" 
        self.mastername = "Лидер"
        self.slavesname = "Послушники"
        self.id = idgenerator()
        self.master = master 
        self.slaves = []
        self.land = []
        self.color = ()
        self.password = passwordgenerate()
        self.tax = 0
        self.provision = 0

def idgenerator():
    alphabet = list("abcdefghijklmnopqrstuvwxyz0123456789")
    id = ""
    for i in range(4):
        id += alphabet[randint(0, len(alphabet) - 1)] 
    while True:
        yeah = 1
        for i in clanlist:
            if i.id == id:
                yeah = 0
                id = ""
                for i in range(4):
                    id += alphabet[randint(0, len(alphabet) - 1)] 
                break 
        if yeah == 1:
            break
    return id 

def passwordgenerate():
    alphabet = list("abcdefghijklmnopqrstuvwxyz0123456789")
    id = ""
    for i in range(8):
        id += alphabet[randint(0, len(alphabet) - 1)] 
    return id 

def war(peer_id, aid, bid):
    o = True
    for i in userlist:
        if i.id == aid:
            aid = i
            for j in userlist:
                if j.id == bid:
                    bid = j
                    o = False
                    break
            break
    if o == True:
        messagenormal(peer_id, 'Либо вы ввели неправильные данные, либо вы не зарегестрированны в системе. Для второго достаточно написать в лс группы')
        return 
    if aid.power == bid.power:
        messagenormal(peer_id, f'Ничья. \n Стороны потеряли по {aid.power} военной мощи')
        try:
            messagenormal(bid.id, f'На вас напал @id{aid.id}. Ничья. Вся армия потеряна')
        except Exception as e:
            print(e.__class__)
        aid.power = 0
        bid.power = 0

    elif aid.power > bid.power:
        aid.power -= bid.power
        k = bid.power 
        bid.power = 0 

        if bid.clan != '' and bid.clan.master.id != bid.id:
            if bid.clan.master.power > aid.power:
                messagenormal(peer_id, f'При поддержки своего клана победил защищающийся. \n Стороны потеряли по {aid.power + k} боевой мощи.\n Слава победы будет разделена между защищающимся и главой его клана')
                bid.clan.master.glory += aid.power * 2
                bid.glory += k * 2 
                bid.clan.master.power -= aid.power
                aid.power = 0 
                return
        messagenormal(peer_id, f'Победил нападающий. \n Защитнику никто помочь не смог. \n Стороны потеряли по {k} военной мощи(+ возможны дополнительные потери от сражений с владельцем клана). \n Нападающий получил {k * 2 + int((bid.capital * 0.35)/10)} славы. \n Нападающий отобрал у защищающегося {int(bid.capital * 0.35)} Гансов Гюнтеров')
        try:
            messagenormal(bid.id, f'Вы проиграли в сражении с @id{aid.id}. \n Потеряно {int(bid.capital * 0.35)} Гансов Гюнтеров и вся армия')
        except Exception as e:
            print(e.__class__)
        aid.glory += k * 2 + int((bid.capital * 0.35)/10)
        if aid.clan != '' and aid.clan.master.id != aid.id:
            aid.clan.master.capital += int( int(bid.capital * 0.35)  * (aid.clan.tax/100) )
            aid.capital += int(bid.capital * 0.35) - int( int(bid.capital * 0.35)  * (aid.clan.tax/100) )
        else:
            aid.capital += int(bid.capital * 0.35)
        bid.capital -= int(bid.capital * 0.35)
            
    elif bid.power > aid.power:
        messagenormal(peer_id, f'Победил защищающийся. \n Стороны потеряли по {aid.power} военной мощи.')
        try:
            messagenormal(bid.id, f'На вас напал @id{aid.id}. Победа. \n Получено {aid.power *2} славы. \n Потеряно {aid.power} боевой мощи')
        except Exception as e:
            print(e.__class__)
        bid.glory += aid.power * 2
        bid.power -= aid.power
        aid.power = 0

def upload_photo(upload, photo):
    response = upload.photo_messages(photo)[0]
    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment
def messagenormal(peer_id, text, ment = 1):
    vk.messages.send(
            peer_id = peer_id,
            random_id = get_random_id(),
            message = text,
            disable_mentions = ment 
        )
def messageattachment(peer_id, text, attachment, ment = 1):
    vk.messages.send(
            peer_id = peer_id,
            random_id = get_random_id(),
            message = text,
            attachment = upload_photo(upload, attachment),
            disable_mentions = ment 
        )

def textnord(text):
    textnormal = ''
    for i in text:
        if i != ' ':
            textnormal += i
    return textnormal

def information(user):
    income = 0 
    id = user.id
    if user.id > 0:
        txt = f"Информация о @id{id}({user.name}) \n"
        txt += f"У @id{id}({user.name}) на счету {user.capital} Гансов Гюнтеров. \nУ @id{id}({user.name}) во владении {user.power} военной мощи. \nУ @id{id}({user.name}) {user.glory} славы. \n"
        if user.clan != '':
            txt += f"@id{id}({user.name}) состоит в клане с мудрым именем {user.clan.name} .\n"
            txt += f"@id{id}({user.name}) выплачивает своему клану {user.clan.tax}% своих доходов. \n @id{id}({user.name}) получает от клана {user.clan.provision} гг/полминуты в качестве безусловной выплаты. \n"
        else:
            txt += f"@id{id}({user.name}) социофоб. \n"
        txt += f"@id{id}({user.name}) владеете следующим количеством фабрик:\n"
    else:
        id = id * -1
        txt = f"Информация о @club{id}({user.name}) \n"
        txt += f"У @club{id}({user.name}) на счету {user.capital} Гансов Гюнтеров. \nУ @club{id}({user.name}) во владении {user.power} военной мощи. \nУ @club{id}({user.name}) {user.glory} славы. \n"
        if user.clan != '':
            txt += f"@club{id}({user.name}) состоит в клане с мудрым именем {user.clan.name} . \n"
            txt += f"@club{id}({user.name}) выплачивает своему клану {user.clan.tax}% своих доходов. \n @club{id}({user.name}) получает от клана {user.clan.provision} гг/полминуты в качестве безусловной выплаты. \n" 
        else:
            txt += f"@club{id}({user.name}) социофоб. \n"
        txt += f"@club{id}({user.name}) владеете следующим количеством фабрик:\n"
    for i in range(3):
        txt += f" Фабрик ценой в {fabriclist[i].price} гг и доходом в {fabriclist[i].income} гг/полминуты - {user.fabric[i]} \n"
        income += fabriclist[i].income * user.fabric[i]
    txt += f"Общий доход равен {income} гг/полминуты"
    return txt 

def finduser(from_id, create = True):
    if from_id == False:
        return False
    user = 0
    o = True 
    for i in userlist:
        if i.id == from_id:
            user = i
            o = False
            break
    if o == True and create == True:
        user = player(from_id)
        userlist.append(user)
    if o == True and create == False:
        return False
    return user 

def findid(string):
    if '[' in string.lower() and '|' in string.lower():
        string = string[string.index('[')+1:string.index('|')]
        if 'club' in string.lower():
            string = '-' + string[string.index('b') + 1:]
        elif 'id' in string.lower():
            string = string[string.index('d') + 1:]
        else:
            return False
        try:
            string = int(string)
        except Exception as e:
            print(e.__class__)
            return False
        return string
    else:
        return False

def findcount(string, zero = False):
    count = ""
    for i in string:
        if i.isdigit():
            count += i
    if len(count) == 0:
        if zero == True:
            return 'no' 
        else:
            return False
    return int(count)

def surpise(event, user, text):
    user1 = user 
    if ":" not in text and event.message.get('reply_message') == None and  len(event.message.get('fwd_messages')) == 0:
        return False
    if event.message.get('reply_message') != None or len(event.message.get('fwd_messages')) != 0:
        count = findcount(text)
    else:
        count = findcount(text[:text.index(':')])
    if count == False:
        return False
    if count > user1.capital:
        return False
    if event.message.get('reply_message') != None:
        user2 = finduser(event.message.get('reply_message').get('from_id'))
    elif len(event.message.get('fwd_messages')) != 0:
        user2 = finduser(event.message.get('fwd_messages')[0].get('from_id'), create = False)
        if user2 == False:
            messagenormal(event.message.get('peer_id'),'К сожалению данный игрок не зарегестрирован в системе. Для регестрации достаточно написать в личные сообщения группы, или в беседу с присутсвием данного бота.')
            return
    else:
        found = findid(text[text.index(':'):])
        if found == False:
            return False
        user2 = finduser(found, create = False)
        if user2 == False:
            return False
    user1.capital -= count
    user2.capital += count
    if user1.id > 0:
        try:
            messagenormal(user2.id, f"Вам было передано {count} гг от @id{user1.id}({user1.name})")
        except Exception as e:
            print(e.__class__)
    else:
        try:
            messagenormal(user2.id, f"Вам было передано {count} гг от @club{user1.id * -1}({user1.name})")
        except Exception as e:
            print(e.__class__)
    if user2.id > 0:
        messagenormal(event.message.get('peer_id'), f'Успешно передано {count} гг @id{user2.id}({user2.name})')
    else:
        messagenormal(event.message.get('peer_id'), f'Успешно передано {count} гг @club{user2.id * -1}({user2.name})')

def fabricbuy(event, user, text):
    count = 1 
    if ':' in text:
        number = findcount(text[:text.index(':')], zero = True)
        count = findcount(text[text.index(':'):])
        if count == False:
            return False
    else:
        number = findcount(text, zero = True)
    if number == 'no':
        return False
    if number > 2:
        return False
    for i in range(3):
        if number == i:
            if user.capital >= fabriclist[i].price * count:
                user.capital -= fabriclist[i].price * count
                user.fabric[i] += count
                messagenormal(event.message.get('peer_id'), f'Покупка {count} фабрик(и) номер {i} успешно совершена. \n Оставшийся капитал - {user.capital}')
            else:
                return False
            break
def fabricsell(event, user, text):
    count = 1 
    if ':' in text:
        number = findcount(text[:text.index(':')], zero = True)
        count = findcount(text[text.index(':'):])
        if count == False:
            return False
    else:
        number = findcount(text, zero = True)
    if number == 'no':
        return False
    if number > 2:
        return False
    if user.fabric[number] < count:
        return False
    if user.clan != '' and user.clan.master.id != user.id:
        user.clan.master.capital += int(int(fabriclist[number].price * 0.7 * count) * (user.clan.tax/100))
        user.capital +=  int(fabriclist[number].price * 0.7 * count) - int(int(fabriclist[number].price * 0.7 * count) * (user.clan.tax/100))
        user.fabric[number] -= count
    else:
        user.capital += int(fabriclist[number].price * 0.7 * count)
        user.fabric[number] -= count
    messagenormal(event.message.get('peer_id'), f'Продажа {count} фабрик(и) номер {number} успешно совершена. \n Ваш капитал - {user.capital}')

def greatest(users, event):
    values = []
    owner = []
    maximumuser = []
    for i in users:
        owner.append(i)
        values.append(i.glory)
    for i in range(10):
        if len(owner) == 0:
            break
        index = values.index(max(values))
        maximumuser.append(owner[index])
        values.pop(index)
        owner.pop(index)
    txt = "Список самых славных воинов: \n"
    for i in range(len(maximumuser)):
        if maximumuser[i].id < 0:
            txt += f"{i + 1} - @public{maximumuser[i].id * -1}(Со счетом: {maximumuser[i].glory}) \n"
        else:
            txt += (f"{i + 1} - @id{maximumuser[i].id}(Со счетом: {maximumuser[i].glory}) \n")
    messagenormal(event.message.get('peer_id'), txt)

def gamecasino(event, user, text):
    found = findcount(text)
    if found == False:
        return False
    if found > user.capital:
        return False
    if randint(0,1) == 1:
        user.capital += int(found * 1.25)
        messagenormal(event.message.get('peer_id'), f'Поздравляю с выигрышом! Ты выиграл {int(found * 1.25)} Гансов Гюнтеров')
    else:
        user.capital -= int(found * 1)
        messagenormal(event.message.get('peer_id'), f'К сожалению ты проиграл {int(found)} Гансов Гюнтеров')

def clancreate(event, user, text):
    if user.clan != '':
        return False 
    clam = clan(user)
    user.clan = clam 
    clanlist.append(user.clan)
    pickle.dump(clanlist, open('кланыд', 'wb'))
    messagenormal(event.message.get('peer_id'), 'Клан успешно создан')

def clanrename(event, user, text): 
    if user.clan == '':
        return False 
    if ':' not in text:
        return False
    if user.clan.master.id != user.id:
        return False
    name = event.message.get('text')[event.message.get('text').index(':') + 1:] 
    if len(name) == 0 or len(name) > 110:
        return False 
    user.clan.name = name
    messagenormal(event.message.get('peer_id'), f'Название изменено на \"  {user.clan.name}  \" ')

def myclan(event, user, text):
    if user.clan == '':
        return False
    #firstvds
    txt = ""
    txt += f"ID клана: {user.clan.id} \n"
    txt += f"Имя клана: {user.clan.name} \n"
    txt += f"Налог равен {user.clan.tax}% \n"
    txt += f"Клан предоставляет обеспечение в размере {user.clan.provision} гг \n"
    txt += f"{user.clan.mastername} клана: @id{user.clan.master.id}({user.clan.master.name}) \n"
    txt += f"{user.clan.slavesname} клана: "
    for i in user.clan.slaves:
        txt += f"@id{i.id}({i.name}), "
    messagenormal(event.message.get('peer_id'), txt)

def delclan(event, user, text):
    if user.clan == '':
        return False 
    if user.clan.master == user:
        for i in user.clan.slaves:
            i.clan = ""
        clanlist.remove(user.clan)
        del user.clan 
        user.clan = ''
    else:
        user.clan.slaves.remove(user)
        user.clan = ""
    messagenormal(event.message.get('peer_id'), 'Вы вышли из клана/удалили клан')

def newid(event, user, text):
    if user.clan == '':
        return False 
    if user.clan.master.id != user.id:
        return False
    b = idgenerator()
    user.clan.id = b 
    messagenormal(event.message.get('peer_id'), 'Айди успешно сменён')

def changename(event, user, text):
    if ':' not in text:
        return False
    name = event.message.get('text')[event.message.get('text').index(':') + 1:] 
    if len(name) == 0 or len(name) > 50:
        return False 
    user.name = name
    messagenormal(event.message.get('peer_id'), f'Имя изменено на {user.name}')

def masternamechange(event, user, text):
    if user.clan == '':
        return False
    if user.clan.master.id != user.id:
        return False 
    if ':' not in text:
        return False
    name = event.message.get('text')[event.message.get('text').index(':') + 1:] 
    if len(name) == 0 or len(name) > 50:
        return False 
    user.clan.mastername = name
    messagenormal(event.message.get('peer_id'), f'Звание лидера изменено на {user.clan.mastername}')

def slavenamechange(event, user, text):
    if user.clan == '':
        return False
    if user.clan.master.id != user.id:
        return False 
    if ':' not in text:
        return False
    name = event.message.get('text')[event.message.get('text').index(':') + 1:] 
    if len(name) == 0 or len(name) > 50:
        return False 
    user.clan.slavesname = name
    messagenormal(event.message.get('peer_id'), f'Звание рядовых изменено на {user.clan.slavesname}')

def newpassword(event, user, text):
    if user.clan == '':
        return False
    if user.clan.master.id != user.id:
        return False 
    user.clan.password = passwordgenerate()
    messagenormal(event.message.get('peer_id'), f'Пароль успешно изменен')

def whatpassword(event, user, text):
    if user.clan == '':
        return False
    if user.clan.master.id != user.id:
        return False 
    messagenormal(event.message.get('peer_id'), f'Ваш пароль -- {user.clan.password}')

def enter(event, user, text):
    if user.clan != '':
        return False
    if ':' not in text or '^' not in text:
        return False 
    id = text[text.index(':')+1:text.index('^')]
    for i in clanlist:
        if i.id == id:
            if text[text.index('^')+1:] == i.password:
                i.slaves.append(user)
                user.clan = i
                messagenormal(event.message.get('peer_id'), f'Поздравлю с успешным вступлением в клан {user.clan.name}!')
                try:
                    messagenormal(user.clan.master.id, f'К вам в клан вступил @id{user.id}({user.name})')
                except:
                    pass
                return True 
            return False
    return False

def kickclan(who, event, user, text):
    for i in user.clan.slaves: 
        if i.id == who:
            user.clan.slaves.remove(i)
            i.clan = ""
            messagenormal(event.message.get('peer_id'), f'{i.name} успешно изгнан из клана {user.clan.name}')
            return True 
    messagenormal(event.message.get('peer_id'), 'Читай Биборан, Масленок!')

def changetax(event, user, text):
    if user.clan == '':
        return False
    if user.clan.master.id != user.id:
        return False
    if ':' not in text:
        return False
    count = findcount(text[text.index(':'):], zero = True)
    if count == 'no':
        return False
    if count > 100:
        return False
    user.clan.tax = count
    messagenormal(event.message.get('peer_id'), f'Теперь ставка налогов равна {user.clan.tax}%')

def changebod(event, user, text):
    if user.clan == '':
        return False
    if user.clan.master.id != user.id:
        return False
    if ':' not in text:
        return False
    count = findcount(text[text.index(':'):], zero = True)
    if count == 'no':
        return False
    user.clan.provision = count
    messagenormal(event.message.get('peer_id'), f'Теперь ставка БОД клана равна {user.clan.provision}')

def revolution(event, user, text):
    if user.clan == '':
        return False
    if user.clan.master.id == user.id:
        return False
    if user.power > user.clan.master.power:
        user.power -= user.clan.master.power
        user.clan.master.power = 0 
        for i in range(3):
            user.fabric[i] += math.ceil(user.clan.master.fabric[i] * 0.2)
            user.clan.master.fabric[i] -= math.ceil(user.clan.master.fabric[i] * 0.2)
        messagenormal(event.message.get('peer_id'), 'Слава Революции! Фаланга Победила!')
        user.capital += int(user.clan.master.capital * 0.5)
        user.clan.master.capital -= int(user.clan.master.capital * 0.5)
        user.clan.master.clan = ''
        user.clan.master = user
        user.clan.slaves.remove(user)
    else:
        user.clan.master.power -= user.power 
        user.power = 0 
        for i in range(3):
            user.clan.master.fabric[i] += math.ceil(user.fabric[i] * 0.2)
            user.fabric[i] -= math.ceil(user.fabric[i] * 0.2)
        messagenormal(event.message.get('peer_id'), f'Фашисты, коммунисты, либералы и прочие слуги интернационального капитала вновь проиграли. Славься {user.clan.name}, Славься {user.clan.mastername}')
        user.clan.master.capital += int(user.capital * 0.5)
        user.capital -= int(user.capital * 0.5)
        user.clan.slaves.remove(user)
        user.clan = ''
    
def spying(who_id, event, user, text):
    user_victim = finduser(who_id)
    if user_victim.clan == '':
        messagenormal(event.message.get('peer_id'), "Читай биборан, масленок!") 
        return
    if user.capital < 250000: #250000
        messagenormal(event.message.get('peer_id'), "Читай биборан, масленок!") 
        return
    user.capital -= 250000
    if randint(1, 100) <= len(user_victim.clan.slaves) + 1:
        messagenormal(event.message.get('peer_id'), f"Шпионаж прошёл успешно. Айди клана: {user_victim.clan.id}")
    else:
        messagenormal(event.message.get('peer_id'), f"Повезёт в следующий раз")

def findclan(id):
    for i in clanlist:
        if i.id == id:
            return i
    return False 

def attack(event, user, text):
    profit = 0
    if ':' not in text:
        return False 
    our_clan = findclan(text[text.index(':')+1:])
    if our_clan == False:
        return False 
    messagenormal(event.message.get('peer_id'), f"Битва начинается!")
    if user.power <= our_clan.master.power:
        our_clan.master.power -= user.power
        user.power = 0 
        messagenormal(event.message.get('peer_id'), f"Зубы сломаны о первую преграду")
        try:
            messagenormal(our_clan.master.id, f"На Вас напал @id{user.id}({user.name}). Ожидаемо, он програли")
        except:
            pass
        return
    user.power -= our_clan.master.power
    our_clan.master.power = 0 
    for i in our_clan.slaves:
        if user.power <= i.power:
            i.power -= user.power
            user.power = 0  
            messagenormal(event.message.get('peer_id'), f"Атака Провалилась")
            try:
                messagenormal(our_clan.master.id, f"На Вас напал @id{user.id}({user.name}). Ожидаемо, он програли")
            except:
                pass
            return 
        user.power -= i.power 
        i.power = 0
    messagenormal(event.message.get('peer_id'), f"Великая победа для нашей нации")
    try:
        messagenormal(our_clan.master.id, f"На Вас напал @id{user.id}({user.name}). Ваш клан уничтожены, а у вас отобрана половина состояния")
    except:
        pass
    profit += int(our_clan.master.capital * 0.5)
    our_clan.master.capital -= int(our_clan.master.capital * 0.5)
    for i in our_clan.slaves:
        profit += int(i.capital * 0.8)
        i.capital -= int(i.capital * 0.8)
        i.clan = ''
    for i in range(3):
        user.fabric[i] += math.ceil(our_clan.master.fabric[i] * 0.5)
        our_clan.master.fabric[i] -= math.ceil(our_clan.master.fabric[i] * 0.5)
    our_clan.master.clan = ''
    clanlist.remove(our_clan)
    del our_clan 
    if user.clan != '' and user.clan.master.id != user.id:
        user.clan.master.capital += int(profit * user.clan.tax/100)
        user.capital += profit - int(profit * user.clan.tax/100)
    else:
        user.capital += profit
    return 

def capture(event, user, text):
    a = provinces[random(0,3)][random(0,3)]
    while a.master != '':
        a = provinces[random(0,3)][random(0,3)]
    a.master == user.clan
'''
for i in range(4):
    alllist[4].append([])
    for a in range(4):
        alllist[4][i].append(prov())
print(alllist[4])
alllist = pickle.dump([[],pickle.load(open('фабрикид', 'rb')), [], []], open('всё','wb'))
alllist.append([])
'''
help = open(file = 'помощь.txt', encoding='utf-8', mode = 'r').read()
alllist = pickle.load(open('всё', 'rb'))
clanlist = alllist[0]
fabriclist = alllist[1]
userlist = alllist[2]
chates = alllist[3]
provinces = alllist[4]
vk_session = vk_api.VkApi(token = 'f806a2b025b45208ca55a67968afda989493ad503b7498a3e4e7bb61df25cfd0fb85c5b9aa0a2b1fbfc5d')
longpoll = VkBotLongPoll(vk_session, 201700275)
vk = vk_session.get_api()
upload = VkUpload(vk)
def massn():
    while True:
        #try:
            for event in longpoll.listen():
                if event.from_chat:
                    o = True
                    for i in chates:
                        if i.id == event.chat_id:
                            o = False
                            break
                    if o == True:
                        chates.append( chat1(event.chat_id) )
                        messageattachment(event.message.get('peer_id'), "Беседа успешно создана. Пожалуйста настройте бота при помощи команд //ботофлуд, //ботопостыодин и //ботопостыдва. Подробнее см. !помощь в личных сообщениях", 'happy.jpg')
                if event.type == VkBotEventType.MESSAGE_NEW and event.message.get('text') != "":
                    text = textnord(event.message.get('text')).lower()
                    user = finduser(event.message.get('from_id'))
                    if user.clan != '' and user.clan.master.id != user.id:
                        payment = len(text) * 10 
                        user.clan.master.capital += int(payment * (user.clan.tax/100))
                        payment -= int(payment * (user.clan.tax/100))
                        user.capital += payment
                    else:
                        user.capital += len(text) * 10
                    if event.from_chat:
                        for i in chates:
                            if i.id == event.chat_id:
                                chat = i
                                break
                        if "//ботофлуд" in text or '//ботопостыодин' in text or '//ботопостыдва' in text or '//какиенастройки' in text:
                            try: 
                                members = vk.messages.getConversationMembers(peer_id = event.message.get('peer_id'))
                            except Exception as e: 
                                messagenormal(event.message.get('peer_id'), 'Для работы бота требуется выдать ему права администратора')
                                continue
                            b = True
                            for i in members['items']:
                                if i['member_id'] == user.id: 
                                    if i['is_admin'] == False:
                                        b = 0 
                                    break
                            if b == False:
                                continue
                            num = findcount(text)
                            if "//ботофлуд" in text:
                                if num == False:
                                    chat.settings[0] = 0
                                else:
                                    chat.settings[0] = 1
                            elif '//ботопостыодин' in text:
                                if num == False:
                                    chat.settings[1] = 0
                                else:
                                    chat.settings[1] = 1
                            elif '//ботопостыдва' in text:
                                if num == False:
                                    chat.settings[2] = 0
                                else:
                                    chat.settings[2] = 1
                            else:
                                messagenormal(event.message.get('peer_id'), f'В беседе действуют следующие настройки(где 1 - разрешено). \n Работа бота - {chat.settings[0]} \n Рассылка постов первого порядка - {chat.settings[1]} \n Рассылка постов второго порядка - {chat.settings[2]}')
                            if text != '//какиенастройки':
                                messageattachment(event.message.get('peer_id'), 'Настройки беседы успешно изменены', 'happy.jpg')
                        elif chat.settings[0] == 0: 
                            continue 
                    if text.lower() == "!ктоя":
                        messagenormal(event.message.get('peer_id'), information(user))
                    elif "!ктоты" in text.lower():
                        if event.message.get('reply_message') != None:
                            messagenormal(event.message.get('peer_id'), information(finduser(event.message.get('reply_message').get('from_id'))))
                        elif len(event.message.get('fwd_messages')) != 0:
                            useer2 = finduser(event.message.get('fwd_messages')[0].get('from_id'), create = False)
                            if useer2 == False:
                                messagenormal(event.message.get('peer_id'),'К сожалению данный игрок не зарегестрирован в системе. Для регестрации достаточно написать в личные сообщения группы, или в беседу с присутсвием данного бота.')
                            else:
                                messagenormal(event.message.get('peer_id'), information(useer2))
                        else:
                            find = finduser(findid(text))
                            if find != False:
                                messagenormal(event.message.get('peer_id'), information(find))
                            else:
                                messagenormal(event.message.get('peer_id'), "Читай биборан, масленок!")
                    elif text.lower() == "!помощь":
                        messagenormal(event.message.get('peer_id'), help)
                    elif "!армиякупить" in text.lower():
                        count = findcount(text)
                        if count == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                        else:
                            if count > user.capital:
                                messagenormal(event.message.get('peer_id'), "Читай биборан, масленок!")
                            else:
                                user.power += count
                                user.capital -= count
                                messagenormal(event.message.get('peer_id'), f"Успешно преобретено {count} боевой мощи. \n Теперь у вас на счету {user.power} боевой мощи. \n Капитал состовляет {user.capital} Гансов Гюнтеровю")
                    elif text.lower() == '!менюфабрик':
                        txt = "Вы можете преобрести следующие фабрики (при помощи команды !купитьф + номер фабрики):\n"
                        for i in range(3):
                            txt += f"Фабрика ценой в {fabriclist[i].price} гг и доходом в {fabriclist[i].income} гг/полминуты - под номером {i} \n"
                        messagenormal(event.message.get('peer_id'), txt)
                    elif "!купитьф" in text.lower():
                        if fabricbuy(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif "!продатьф" in text.lower():
                        if fabricsell(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif "!армияпродать" in text.lower():
                        count = findcount(text)
                        if count == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                        else:
                            if count > user.power:
                                messagenormal(event.message.get('peer_id'), "Читай биборан, масленок!")
                            else:
                                user.power -= count
                                if user.clan != '' and user.clan.master.id != user.id:
                                    user.clan.master.capital += int(int(count * 0.7) * (user.clan.tax/100))
                                    user.capital += int(count * 0.7) - int(int(count * 0.7) * (user.clan.tax/100))
                                else:
                                    user.capital += int(count * 0.7)
                                messagenormal(event.message.get('peer_id'), f"Успешно продано {count} боевой мощи. \n Теперь у вас на счету {user.power} боевой мощи. \n Капитал состовляет {user.capital} Гансов Гюнтеровю")
                    elif "!даровать" in text.lower():
                        if surpise(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif "!напасть" in text.lower():
                        if event.message.get('reply_message') != None:
                            war(event.message.get('peer_id'), event.message.get('from_id'), event.message.get('reply_message').get('from_id'))
                        elif len(event.message.get('fwd_messages')) != 0:
                            war(event.message.get('peer_id'), event.message.get('from_id'), event.message.get('fwd_messages')[0].get('from_id'))
                        else:
                            found = findid(text)
                            if found != False:
                                war(event.message.get('peer_id'), event.message.get('from_id'), found)
                            else:
                                messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif text.lower() == "!олимпславы":
                        greatest(userlist, event)
                    elif '!игратьказино' in text:
                        if gamecasino(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif text == '!максимумфабрик':
                        messagenormal(event.message.get('peer_id'), f'При текущих финансах вы можете купить до {int(user.capital/50000)} фабрик типа 2') 
                    elif  text.lower() == '!создатьклан':
                        if clancreate(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif '!имяклана' in text.lower():
                        if clanrename(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif text.lower() == '!мойклан':
                        if myclan(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif text.lower() == '!удалитьклан':
                        if delclan(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif text.lower() == '!новыйайди':
                        if newid(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif '!сменитьимя' in text.lower():
                        if changename(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif '!имялидера' in text.lower():
                        if masternamechange(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif '!имярядового' in text.lower():
                        if slavenamechange(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif text.lower() == '!новыйпароль':
                        if newpassword(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif text.lower() == '!парольклана':
                        if whatpassword(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif '!вступитьвклан' in text.lower():
                        if enter(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif '!выгнать' in text.lower():
                        if user.clan == '':
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                            continue 
                        if user.clan.master.id != user.id:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                            continue
                        if event.message.get('reply_message') != None:
                            kickclan(event.message.get('reply_message').get('from_id'), event, user, text)
                        elif len(event.message.get('fwd_messages')) != 0:
                            kickclan(event.message.get('fwd_messages')[0].get('from_id'), event, user, text)
                        else:
                            found = findid(text)
                            if found != False:
                                kickclan(found, event, user, text)
                            else:
                                messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif '!налоги' in text.lower():
                        if changetax(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок')
                    elif '!выплаты' in text.lower():
                        if changebod(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок')
                    elif '!революция' in text.lower():
                        if revolution(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок')
                    elif '!шпионаж' in text.lower():
                        if event.message.get('reply_message') != None:
                            spying(event.message.get('reply_message').get('from_id'), event, user, text)
                        elif len(event.message.get('fwd_messages')) != 0:
                            spying(event.message.get('fwd_messages')[0].get('from_id'), event, user, text)
                        else:
                            found = findid(text)
                            if found != False:
                                spying(found, event, user, text)
                            else:
                                messagenormal(event.message.get('peer_id'), 'Читай биборан, масленок!')
                    elif '!штурм' in text.lower():
                        if attack(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Иногда я думаю, что делаю что-то не так со своей жизнью')
                    elif '!захватить' in text.lower():
                        if capture(event, user, text) == False:
                            messagenormal(event.message.get('peer_id'), 'Иногда я думаю, что делаю что-то не так со своей жизнью')
                    else:
                        if event.from_user:
                            if text.lower() == "!userlist":
                                messagenormal(event.message.get('peer_id'), userlist)
                            elif text.lower() == "!chates":
                                messagenormal(event.message.get('peer_id'), f'{chates}/')
                            elif 'накруткагансовгюнтеров561347' in text.lower():
                                text = text.split(':')
                                for i in userlist:
                                    if i.id == int(text[1]):
                                        i.capital += int(text[2])
                                        break
                            elif '/!/рассылкатекста1489:' in text:
                                att = []
                                for i in event.message.get('attachments'):
                                    type = i.get('type')
                                    owner_id = i.get(i.get('type')).get('owner_id')
                                    id = i.get(i.get('type')).get('id')
                                    access_key = i.get(i.get('type')).get('access_key')
                                    att.append(f'{type}{owner_id}_{id}_{access_key}') 
                                for i in chates:
                                    if i.settings[1] == 1:
                                        vk.messages.send(
                                            peer_id = 2000000000 + i.id,
                                            random_id = get_random_id(),
                                            message = event.message.get('text')[event.message.get('text').index(':') + 1:],
                                            attachment = att,
                                            disable_mentions = 1
                                            ) 
                                messagenormal(event.message.get('peer_id'), 'Расслыка прошла успешно')
                            elif '/!/рассылкатекста1588' in text:
                                att = []
                                for i in event.message.get('attachments'):
                                    type = i.get('type')
                                    owner_id = i.get(i.get('type')).get('owner_id')
                                    id = i.get(i.get('type')).get('id')
                                    access_key = i.get(i.get('type')).get('access_key')
                                    att.append(f'{type}{owner_id}_{id}_{access_key}') 
                                for i in chates:
                                    if i.settings[2] == 1:
                                        vk.messages.send(
                                            peer_id = 2000000000 + i.id,
                                            random_id = get_random_id(),
                                            message = event.message.get('text')[event.message.get('text').index(':') + 1:],
                                            attachment = att,
                                            disable_mentions = 1
                                            ) 
                                messagenormal(event.message.get('peer_id'), 'Расслыка прошла успешно')
                            else:
                                messageattachment(event.message.get('peer_id'), "По тем или иным причинам команда не может быть выполнена(скорее всего такой просто не существует, так что юзай !помощь)", 'sad.jpg')
                        elif event.from_chat:
                            if text.lower() == "!олимпбеседы":
                                chatuser = []
                                try:
                                    for i in vk.messages.getConversationMembers( peer_id = event.chat_id + 2000000000).get('items'):
                                        chatuser.append(finduser(i.get('member_id')))
                                    greatest(chatuser, event)
                                except Exception as e:
                                    messagenormal(event.message.get('peer_id'), 'Для корректной работы команды боту требуются права администратора')
                            else:
                                pass
                        else:
                            pass
                pickle.dump(alllist, open('всё', 'wb'))
        #except Exception as e:
            #print(e.__class__)

def fabricswork():
    a = 0 
    while True:
        #try:
            a += 1 
            for i in userlist:
                for j in range(len(i.fabric)):
                    if i.clan != '' and i.clan.master.id != i.id:
                        i.clan.master.capital += int(i.fabric[j] * fabriclist[j].income * (i.clan.tax / 100))
                        i.capital += (i.fabric[j] * fabriclist[j].income) - int(i.fabric[j] * fabriclist[j].income * (i.clan.tax / 100))
                    else:
                        i.capital += i.fabric[j] * fabriclist[j].income
                if i.clan != '':
                    if i.clan.master.capital - i.clan.provision >= 0:
                        i.capital += i.clan.provision
                        i.clan.master.capital -= i.clan.provision
            if a % 50 == 0:
                print(f' Круг номер {a} прошёл')
            time.sleep(30)
        #except Exception as e:
            #print(f'Проблема с фабриками {e}')

Thread(target = fabricswork).start()
Thread(target = massn).start()

while True:
    pass
