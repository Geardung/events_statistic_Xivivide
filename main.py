from datetime import datetime
import os, json
from models import *

lolkek = {
    "event": "Ивент",
    "close": "Клоз",
    "undefined": "хз"
}

def add_event():
    pass


if  __name__ == "__main__":


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
                to_parse_txt = to_parse_txt.read().replace("Akane\nБОТ", "").split("Изображение")
                for event_txt in to_parse_txt:
                    print("_________________________")
                    for event_line_txt in event_txt.splitlines()[1:]:
                        print(event_line_txt)
                        
                        if event_line_txt.startswith(" — "): pass
                        
                        elif event_line_txt.startswith("Провeдённый"): 
                            if "ивент!" in event_line_txt.split(" "): event_type = "event"
                            elif "клоз!" in event_line_txt.split(" "): event_type = "close"
                            else: event_type = "undefined"
                            cc = lolkek[event_type]
                            
                        elif event_line_txt.startswith(":tochka1:Ведущий:"): 
                            
                            eventer_tag = event_line_txt.split(":tochka1:Ведущий: ")[1]
                            eventer = Eventers.select().where(Eventers.discord_tag == eventer_tag).first()
                            
                            if not eventer:
                                print(f"Eventer не найден по дискорд тэгу!\n{eventer_tag}")
                                inp_discord_id = int(input("Введите его айди: "))
                                
                                eventer:Eventers = Eventers.select().where((Eventers.discord_id == inp_discord_id)).first()
                                
                                if not eventer:
                                    eventer = Eventers.create(discord_tag = eventer_tag, discord_id = inp_discord_id)
                                    eventer.save()
                                    
                                    with open("./list.json", "r", encoding="utf-8") as f: 
                                        config = json.loads(f.read())
                                        f.close()
                                
                                    config["eventers"].append(
                                        {
                                            "discord_id": inp_discord_id,
                                            "discord_tag": eventer_tag
                                        }
                                    )
                                    
                                    with open("./list.json", "w", encoding="utf-8") as f: 
                                        f.write(json.dumps(config, indent=4, ensure_ascii=False))
                                        f.close()
                                
                                    
                                else:
                                    eventer.discord_tag = eventer_tag
                                    eventer.save()
                            
                            else: print("Ивентёр найден")
                        
                        elif event_line_txt.startswith(":tochka1:Время:"): 
                            
                            a = event_line_txt.split(" ")
                            format = '%d_%m_%Y %I:%M %p'
                            
                            start_ts = datetime.strptime(file.split(".")[0] + f' {a[2]} {a[3]}', format).timestamp()
                            end_ts   = datetime.strptime(file.split(".")[0] + f' {a[5]} {a[6]}', format).timestamp()
                            start = datetime.strptime(file.split(".")[0] + f' {a[2]} {a[3]}', format)
                            end   = datetime.strptime(file.split(".")[0] + f' {a[5]} {a[6]}', format)
                            duration = (end - start).seconds/60
                            
                        elif event_line_txt.startswith(":tochka1:Участвовало"):
                            
                            if "-" in event_line_txt: peoples = int(event_line_txt.split(" ")[-1].split("-")[0])
                            elif len(event_line_txt.split(" ")[-1]) > 2: 
                                input("Press to continue...")
                                continue              
                            else: peoples = int( event_line_txt.split(" ")[-1])
                                                      
                        elif event_line_txt.startswith(f":tochka1:{cc}:"): 
                            
                            event_name = event_line_txt.split(f":tochka1:{cc}: ")[-1][:-1]
                            
                            event_ex = EventEx.select().where((EventEx.name == event_name)).first()
                            
                            if not event_ex:
                                
                                print("Ивент не найден!")
                                points = int(input("Введите кол-во баллов за ивент: "))
                                day = int(input("Введите кол-во человек днем: "))
                                night = int(input("Введите кол-во человек ночью: "))
                                
                                event_ex = EventEx.create(name = event_name, points = points, min_players_day = day, min_players_night = night, type = event_type)
                                with open("./list.json", "r", encoding="utf-8") as f: 
                                
                                    config = json.loads(f.read())
                                    f.close()
                                    
                                
                                config["events"].append(
                                    {
                                        "name": event_name,
                                        "points": points,
                                        "min_players_day": day,
                                        "min_players_night": night,
                                        "type": event_type
                                    }
                                )
                                
                                with open("./list.json", "w", encoding="utf-8") as f: 
                                    f.write(json.dumps(config, indent=4, ensure_ascii=False))
                                    f.close()
                                
                        elif event_line_txt.startswith(":tochka1:Количество кругов:"): 
                            krugs = int( event_line_txt.split(" ")[-1])
                            if krugs > 8: krugs = 8
                            
                        elif event_line_txt.startswith(":tochka1:Вознаграждение:"): prize = int(event_line_txt.split(" ")[1])
                    
                    
                    
                    if not Events.select().where((Events.eventer_id == eventer) & (Events.end_time == end_ts)).first():
                        Events.create(eventer_id = eventer, eventEx_id = event_ex, krugs=krugs, all_prize=prize, peoples = peoples,
                                      duration = duration, start_time = start_ts, end_time = end_ts, points_summary = event_ex.points*krugs).save()

    else: print("IDI Nahuy, vnutri papki \"in\" ничего нет")