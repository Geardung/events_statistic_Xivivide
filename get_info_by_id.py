import datetime
from html import entities
from models import *
import os





def main():  

    if not os.path.exists("./out"): os.mkdir("./out")
    if not Eventers.select():
        print("В базе данных нет ивентёров")
        return
    
    while True:
        id = int(input("Введите ID ивентёра: "))
        eventer = Eventers.select().where((Eventers.discord_id == id)).first()
        if eventer: break
        else: print("!ДАННЫЙ ИВЕНТЁР НЕ НАЙДЕН ПО ID!\nПОВТОР ВВОДА")
    
    
    otchet_from = input("Создать отчёт с (пример 22.07.22) включительно: ")
    otchet_to =  input("До (пример 22.07.22) не включительно: ") 
    
    texts = {
        "summary": f'Отчёт по ивентёру <@{id}>\nОбщая информация за период **с** <t:{int(datetime.datetime.strptime(otchet_from, "%d.%m.%y").timestamp())}:D>(включительно) **до** <t:{int(datetime.datetime.strptime(otchet_to, "%d.%m.%y").timestamp())}:D>(не включительно):\n\n',
        "events_list": 'Список **ивентов** за данный период:\n'
    }
    
    full = {
        "count": 0,
        "duration": 0,
        "summary_krugs": 0,
        "summary_prizes": 0,
        "summary_points": 0
    }
    
    eventer_events = Events.select().where((Events.eventer_id == eventer) &
                                           (Events.start_time >= datetime.datetime.strptime(otchet_from, "%d.%m.%y").timestamp()) &
                                           (Events.end_time <= datetime.datetime.strptime(otchet_to, "%d.%m.%y").timestamp()))
    
    if not eventer_events: 
        print("У ивентёра нет ивентов в базе за данный промежуток!")
        return
    
    for index, event in enumerate(eventer_events):
        event:Events
        if event.eventEx_id.type != "event": continue
        
        texts["events_list"] += f'```\n{index+1}) {event.eventEx_id.name} ({event.eventEx_id.points} баллов)\nКругов: {event.krugs}. Длительность: {event.duration}. Выдано: {event.all_prize}\n```\n'
        
        full["count"] += 1
        full["duration"] += event.duration
        full["summary_krugs"] += event.krugs
        full["summary_prizes"] += event.all_prize
        full["summary_points"] += event.krugs * event.eventEx_id.points
        
    texts["summary"] += f'Всего провел(а) ивентов за период: {full["count"]}\nОбщая длительность: {full["duration"]}\nОбщее кол-во кругов: {full["summary_krugs"]}\nОбщее количество выданных наград: {full["summary_prizes"]}\nОбщее количество баллов за данный период: {full["summary_points"]}\n\n'
    
    texts["summary"] += texts["events_list"]
    
    
    with open(f"./out/{id}.txt", "w", encoding="utf-8") as f: 
        f.write(texts["summary"])
        f.close()
    
if __name__ == "__main__":
    main()