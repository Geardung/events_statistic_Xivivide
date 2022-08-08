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
        "summary": f'Общая информация за период с <t:{datetime.datetime.strptime(otchet_from, "%d.%m.%y").timestamp()}:D>(включительно) до <t:{datetime.datetime.strptime(otchet_to, "%d.%m.%y").timestamp()}:D>(не включительно):\n\n',
        "events_list": 'Список **ивентов** за данный период:\n\n'
    }
    
    full_information_events = {
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
        
    
if __name__ == "__main__":
    main()