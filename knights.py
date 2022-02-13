#endless hallucination  / 1 day irl = 1 year in game
# 1. Добавление информационных команд +
# 2. Смена ника +
# 3. Добавление работы с феодом { постройка зданий, рост населения +, улучшение зданий, работа зданий, создание глобального рынка, потребление населения, создание армии }
# 4. Костомизация профиля
# 5. Добавление карты с провинциями, ресурсами, ростом населения
# 6. Добавление возможности просмотреть карту, захвата провинций
# 7. Поработать с гильдиями
# ЦЕНЫ НА ЗАВОД!
# Завод у гильдий!
### +сохранения 
# import requests
import requests
import random 
import pickle
from threading import Thread
import time

token = ""  # access_token

bynameList = []
playerCount = -1

def bynameGenerator():
    pass # may be later. Idk should i restrict names so all of them will be originally 

def idGenerator():
    global playerCount
    playerCount += 1 
    return playerCount 


class player():
    def __init__(self, vkId):
        self.vkItsd = vkId # vk id
        self.inGameId = idGenerator() # an original in game id
        self.money = 100 # money
        self.symbols = 0 # 1 reichsmark = 50 symbols, so it make sense to save the remainder of characters not converted to marks
        self.fame = 0 # fame 
        self.byname = "Новичок" 
        self.description = "Здесь пока что пусто" 
        self.picture = "" #Picture of profile
        self.mayorship = "" #province that owned by this player 
        self.guild = "" #guild in what player take part / guild can also be as !HITLER! some goverment 
        self.domain = domain(self)
        playerDict[vkId] = self

class domain():
    def __init__(self, player):
        self.owner = player
        self.buildings = []
        self.spots = 15
        self.population = 1000
        self.army = 0
        self.storage = {} 
        domainList.append(self)
        #self.blood =

class manufactory():
    def __init__(self, player, good, needToWork, efficiency, whither):
        self.name = f"Мануфактура номер {len(whither.buildings)+1} {good}"
        self.owner = player
        self.good = good
        self.needToWork = needToWork
        self.level = 1
        self.efficiencyBase = efficiency
        whither.buildings.append(self)

class good():
    def __init__(self, label, types, primordial, cost, needToProduce):
        self.label = label 
        self.type = types
        self.primordial = primordial
        self.cost = cost 
        self.needToProduce = needToProduce

def sendMessage(peerId, randomId, text, attachment=""):
    return requests.get(f"https://api.vk.com/method/messages.send?message={text}&attachment={attachment}&peer_id={peerId}&access_token={token}&v=5.131&random_id={randomId}")

def textOrderisation(text):
    textN = ""
    for i in text:
        if i != " ":
            textN+= i
    return textN.lower()

def findingNumbers(text):
    textN = ""
    return int(textN) 

def findPlayer(vkId, create = True):
    answer = playerDict.get(vkId, False)
    if answer == False:
        if create:
            answer = player(vkId)
            print(playerDict)
        else:
            return False
    return answer 

def pong(update):
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], "pong")

def help(update):
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], "Привет!")

def changeByname(update, user, text):
    if "\"" in text and "\"" in text[text.index("\"") + 1:]:
        a = update["object"]["message"]["text"][update["object"]["message"]["text"].index("\"") + 1:]
        name = a[:a.index("\"")]
        if len(name.replace(" ", "")) > 0 and len(name) < 51:  
            user.byname = name

def changeDescription(update, user, text):
    if "\"" in text and "\"" in text[text.index("\"") + 1:]:
        a = update["object"]["message"]["text"][update["object"]["message"]["text"].index("\"") + 1:]
        desc = a[:a.index("\"")]
        if len(desc.replace(" ", "")) > 0 and len(desc) < 401:  
            user.description = desc

def changePicture(update,user):
    if len(update["object"]["message"]["attachments"]) < 1 or update["object"]["message"]["attachments"][0]["type"] != "photo":
        print(9)
        user.picture = ""
        return  sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], "Ваше изображение удалено")
    print("bb")
    typeSS = update["object"]["message"]["attachments"][0]["type"]
    ownerId = update["object"]["message"]["attachments"][0]["photo"]["owner_id"]
    accessKey = update["object"]["message"]["attachments"][0]["photo"].get("access_key","")
    mediaId = update["object"]["message"]["attachments"][0]["photo"]["id"]
    if accessKey != "":
        user.picture = f"{typeSS}{ownerId}_{mediaId}_{accessKey}"
    else:
        user.picture = f"{typeSS}{ownerId}_{mediaId}"
    return  sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], "Ваше изображение обновлено")
    
    

def build(update,user,text):
    if user.money < 300:
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], "Недостаточно марок")
    if len(user.domain.buildings) >= user.domain.spots:
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], "Недостаточно места")
    user.money -= 100
    manufactory(user, "money", 1, user.domain)
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], "Постройка успешно создана")


def showInformation(update, user):
    text = ""
    text += f"Имя: {user.byname}, Порядковый номер: {user.inGameId} \n"
    text += f"Самопредставление: {user.description}\n"
    text += "Известен лишь своим друзьям" * (user.fame<200) + "Известен даже свинопасам" * (user.fame>=200) + f" ({user.fame})\n"
    text += f"Местный Орден придежрывает {user.money} райхсмарок на счету \n"
    text += f"Не состоит в гилдиях, не мэр \n"
    text += f"Владеет доменом на {user.domain.population} душ \n"
    text += f"В домене представлены следующие постройки: \n"
    for i in range(len(user.domain.buildings)):
        if user.domain.buildings[i].__class__.__name__ == "manufactory":
            text += f"    {i+1}.{user.domain.buildings[i].name}, производящая {user.domain.buildings[i].good}, {user.domain.buildings[i].level} уровня. Уровень эффективности равен {user.domain.buildings[i].efficiencyBase} \n"
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], text, user.picture)

def showInformationAnother(update,text):
    informationTarget = False
    if update["object"]["message"].get("reply_message", False):
        informationTarget = findPlayer(update["object"]["message"]["reply_message"]["from_id"], create = False)
    elif len(update["object"]["message"]["fwd_messages"]):
        informationTarget = findPlayer(update["object"]["message"]["fwd_messages"][0]["from_id"], create=False)
    elif "]" in text and "@" in text and "|" in text:
        if "[club" in text:
            informationTarget = findPlayer(int(text[text.index("[club") + len("[club"):text.index("|")]), create=False)
        elif "[id" in text:
            informationTarget = findPlayer(int(text[text.index("[id") + len("[id"):text.index("|")]), create=False)
    if informationTarget == False:
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], "Человек не зарегестрирован в боте")
    return showInformation(update, informationTarget)

commands = {
    "ping":lambda:pong(update),
    "!ктоя":lambda:showInformation(update, user),
    "!ктоты":lambda:showInformationAnother(update, text),
    "!помощь":lambda:help(update),
    "!имя":lambda:changeByname(update, user, text),
    "!описание":lambda:changeDescription(update,user,text),
    "!изображение":lambda:changePicture(update,user),
    "!строить":lambda:build(update,user,text)
}
playerDict = {}
domainList = []

consumption = {             #good:quantity

} 

# goodsTypes = {
#     0:good("Зерновые", 0, 1, 25),
#     1:good("Золото", 1, 1, 25),
#     2:good("Хлеб", 2, 0, 25),
#     3:good("Райхсмарки", 3, 0, 25),
# }

def mainBot():
    global ts, update, user, text # without ts - problems; update,user.text - можно определить перечень commands в самой функции как альтернатива
    
    response = requests.get('https://api.vk.com/method/groups.getLongPollServer',
                   params={'access_token': token, "v":5.131, "group_id":208705301}).json()["response"] # getting an longPoll server ( google if you are interested )
    
    keyLongPoll = response["key"]
    ts = response["ts"]
    serverLongPoll = response["server"] 
    
    while (True):
        response = requests.get(f"{serverLongPoll}?act=a_check&key={keyLongPoll}&ts={ts}&wait=25&mode=2&version=5.131").json()
        if response["updates"]: 
            for update in response["updates"]:
                if update["type"] == "message_new":
                    text = textOrderisation(update["object"]["message"]["text"])
                    user = findPlayer(update["object"]["message"]["from_id"])
                    user.money += ((user.symbols + len(text)) // 50)
                    user.symbols = (user.symbols + len(text)) % 50
                    try:
                        for i in commands.keys():
                            if i in text:
                                commands[i]() 
                                break
                    except Exception as a:
                        print(a)
        ts = response["ts"]
        #print(response)

def changes():
    while True:
        try:
            for i in domainList:
                i.population = int(i.population * 1.02)
                for x in i.buildings:
                    if x.__class__.__name__ == "manufactory" and x.good == "money":
                        i.owner.money += int(100 * x.efficiencyBase)
            time.sleep(5)
        except Exception as a:
            print(a)

firstThread = Thread(target=mainBot)
secondThread = Thread(target=changes)

firstThread.start()
secondThread.start()
