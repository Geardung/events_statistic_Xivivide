from datetime import datetime
import os, json, sys
from models import *
from threading import Thread

lolkek = {
    "event": "Ивент",
    "close": "Клоз",
    "undefined": "хз"
}

def add_event():
    pass

def start_parsing(is_parser=False):
    if (not os.path.exists("./in")): os.mkdir("./in")
    
    if (not len(os.listdir("./in")) == 0):
        path = "./in/"
        
        for file in os.listdir(path):
            filepath = path+file
            
            if (not os.path.isfile(path+file)):
                print(path+file + " <- Не файл")
                continue
                
            elif (not file.split(".")[0].count("_") == 2 and not file.split(".")[-1] != "txt"): 
                print(filepath +" <--- Название файла неправильно <день>_<месяц>_<год>.txt")
                continue
            
            with open(filepath, "r", encoding="utf-8") as to_parse_txt:
                to_parse_txt = to_parse_txt.read()
                
                print("_________________________")
                
                data:dict = json.loads(to_parse_txt)
        
                for message in data["messages"]:
                    
                    eventer = None 
                    event_ex = None
                    krugs  = None
                    prize  = None
                    peoples  = None
                    duration  = None
                    start_ts  = None
                    end_ts  = None

                    if not message["author"]["id"] == "940974851101962270": continue

                    event_embed = message["embeds"][0]

                    #eventer = self.db_session.query(UserModel).filter_by(discord_id = int(event_embed["thumbnail"]["url"].split("/")[-2])).first()
                    try:
                        d_id = int(event_embed["thumbnail"]["url"].split("/")[-2])
                    except:
                        print(event_embed)
                        continue
                    
                    eventer = Eventers.select().where(Eventers.discord_id == d_id).first()

                    if not eventer: 
                        eventer = Eventers.create(discord_id=d_id, discord_tag="test")
                        eventer.save()

                    event_info = event_embed["description"]
                    
                    def printMSGurl(): print("https://discord.com/channels/876887982509002855/904020811625672714/" + str(message["id"]))

                    for info in event_info.split("\n"):

                        info:str

                        if   info.find(":tochka1:Ведущий: `") > -1: pass # Не требуется
                        elif info.find(":tochka1:Время: `") > -1: 
                            time = info[info.find("`")+1:-1]
                            #TIMESTAMP PARSING
                            format = '%Y-%m-%d %I:%M %p'
                            a = time.split(" ")
                            start = datetime.strptime(message["timestamp"].split("T")[0] + f' {a[1]} {a[2]}', format)
                            end   = datetime.strptime(message["timestamp"].split("T")[0] + f' {a[4]} {a[5]}', format)
                            start_ts = start.timestamp()
                            end_ts   = end.timestamp()
                            duration = (end - start).seconds/60


                        elif info.find(":tochka1:Ивент: `") > -1 or info.find(":tochka1:Клоз: `") > -1 :
                            #EVENT NAME PARSING
                            #event_example = self.db_session.query(EventExampleModel).filter_by(name = info[info.find("`")+1:-1][:-1])[-1]
                            event_ex = EventEx.select().where(EventEx.name == info[info.find("`")+1:-1][:-1]).first()
                            if not event_ex: 
                                print("EventEx not finded -> ", info[info.find("`")+1:-1][:-1])
                                
                                if is_parser: continue
                                else: event_ex = EventEx.create(id=EventEx.select().count()+1,name=info[info.find("`")+1:-1][:-1], points=int(input("Баллов: ")), type=input("Тип close\\event: "), min_players_day=int(input("Минимально днём: ")), min_players_night=int(input("Минимально ночью: "))).save()
                            
                            #all_events = self.db_session.query(EventModel).filter_by(event=event_example.id).all()
                            #if len(all_events) > count_e:
                            #    average_krugs = ( sum([x.krugs for x in all_events]) ) / all_events.count()
                            #    average_all_prize = ( sum([x.all_prize for x in all_events]) ) / all_events.count()

                        elif info.find(":tochka1:Участвовало людей: `") > -1:
                            #EVENT PEOPLE PARSING
                            try: peoples = int(info[info.find("`")+1:-1])
                            except:
                                #await otchetEmbedsend(message["id"], "Ивентёр не добавлен в базу данных User", events_channel)
                                try: peoples = int(info[info.find("`")+1:-1][0])
                                except:
                                    #await otchetEmbedsend(message["id"], "Ивентёр не добавлен в базу данных User", events_channel)
                                    print("Люди вписаны неправильно блять -> ", info[info.find("`")+1:-1])
                                    printMSGurl()
                                    continue
                            
                            if peoples > 100: peoples = 1

                            
                        elif info.find(":tochka1:Количество кругов: `") > -1:
                            #EVENT KRUGS PARSING
                            try: krugs = int(info[info.find("`")+1:-1])
                            except:
                                #await otchetEmbedsend(message["id"], "Ивентёр не добавлен в базу данных User", events_channel)
                                print("Количество кругов вписаны неправильно блять")
                                printMSGurl()
                                continue
                            
                        elif info.find(":tochka1:Вознаграждение:  `") > -1:
                            #EVENT PRIZE PARSING
                            try: prize = int(info[info.find("`")+1:-9])
                            except:
                                #await otchetEmbedsend(message["id"], "Ивентёр не добавлен в базу данных User", events_channel)
                                print("Вознаграждение вписаны неправильно блять ->", info[info.find("`")+1:-9])
                                printMSGurl()
                                
                                continue
                            
                            if prize > 1111110: prize = 1
                    
                    
                    #if not ( eventer and event_ex and krugs and prize and peoples and duration and start_ts and end_ts ): 
                    if None in [eventer, event_ex, krugs, prize, peoples, duration, start_ts, end_ts]:
                        
                        print("\n", eventer ,  event_ex ,  krugs ,  prize ,  peoples ,  duration ,  start_ts ,  end_ts, "\n")
                        #
                        #input()
                        
                        continue
                    
                    #if 0 in [eventer, event_ex, krugs, prize, peoples, duration, start_ts, end_ts]:
                    #    
                    #    print("\n", eventer ,  event_ex ,  krugs ,  prize ,  peoples ,  duration ,  start_ts ,  end_ts, "\n")
                    #    printMSGurl()
                    #    input()
                    #    
                    #    continue
                    
                    
                    mnozhitel = 1
                    
                    if not Events.select().where((Events.eventer_id == eventer) & (Events.end_time == end_ts)).first():
                        print(eventer ,  event_ex ,  krugs ,  prize ,  peoples ,  duration ,  start_ts ,  end_ts)
                        Events.create(eventer_id = eventer, eventEx_id = event_ex, krugs=krugs, all_prize=prize, peoples = peoples,
                                  duration = duration, start_time = start_ts, end_time = end_ts, points_summary = event_ex.points*krugs*mnozhitel).save()

                    

                    
    else: print("IDI Nahuy, vnutri papki \"in\" ничего нет")
    
if __name__ == "__main__":
    
    if len(sys.argv) < 2: start_parsing()
    elif sys.argv[1] == "parser": Thread(target=start_parsing, args=[True]).start()