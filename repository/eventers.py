import datetime
from models import *
import os




def get_statistic_by_id(eventer_id: int, start: str, end: str, password: str):
    """Подготавливает статистику на определённого ивентёра

    Args:
        eventer_id (int): ID ивентёра, на которого нужно сделать статистику
        start (str): Дата в формате 30.12.22
        end (str): Дата в формате 30.12.22
        password (str): Пароль короче твой, который ты получил у Тэдэши#2468

    Returns:
        _type_: Сообщение в готовом виде для Discord`a
    """    
    
    if not password in [x.password for x in Passwords.select().where((Passwords.accesstype=="eventers") & (Passwords.password == password))]: return "Пароль неверный"
    
    if not os.path.exists("./out"): os.mkdir("./out")
    if not Eventers.select(): return "В базе данных нет ивентёров"
    
    while True:
        id = eventer_id
        eventer = Eventers.select().where((Eventers.discord_id == id)).first()
        if eventer: break
        else: return "Нет ивентёра"
    
    
    otchet_from = start
    otchet_to = end
    
    
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
    
    if not eventer_events: return "У ивентёра нет ивентов в базе за данный промежуток!"
    
    for index, event in enumerate(eventer_events):
        event:Events
        if event.eventEx_id.type != "event": continue
        
        texts["events_list"] += f'''```\n{index+1}) {event.eventEx_id.name} ({event.eventEx_id.points} баллов)\nКругов: {event.krugs}. Длительность: {event.duration}. Выдано: {event.all_prize}\nЗапущен в: {datetime.datetime.fromtimestamp(event.start_time).strftime("%d.%m.%y %H:%M")}\n```\n'''
        
        full["count"] += 1
        full["duration"] += event.duration
        full["summary_krugs"] += event.krugs
        full["summary_prizes"] += event.all_prize
        full["summary_points"] += event.points_summary
        
    texts["summary"] += f'Всего провел(а) ивентов за период: {full["count"]}\nОбщая длительность: {full["duration"]}\nОбщее кол-во кругов: {full["summary_krugs"]}\nОбщее количество выданных наград: {full["summary_prizes"]}\nОбщее количество баллов за данный период: {full["summary_points"]}\n\n'
    
    texts["summary"] += texts["events_list"]
    
    return texts["summary"]



def get_statistic_all(start: str, end: str, password: str):
    """Подготавливает статистику на определённого ивентёра

    Args:
        eventer_id (int): ID ивентёра, на которого нужно сделать статистику
        start (str): Дата в формате 30.12.22
        end (str): Дата в формате 30.12.22
        password (str): Пароль короче твой, который ты получил у Тэдэши#2468

    Returns:
        _type_: Сообщение в готовом виде для Discord`a
    """    
    
    if not password in [x.password for x in Passwords.select().where((Passwords.accesstype=="eventers") & (Passwords.password == password))]: return "Пароль неверный"
    
    text = ""
    eventers_info_text = "Статистика ивентёров: "
    all_eventers = Eventers.select()

    otchet_from = start
    otchet_to =  end
    
    av = get_aver_ex_events()
    
    full_information_events = {
        "count": 0,
        "duration": 0,
        "summary_krugs": 0,
        "summary_prizes": 0,
        "summary_points": 0
    }

    eventers_info = []

    if not os.path.exists("./out"): os.mkdir("./out")
    if not all_eventers: return
    
    for eventer in all_eventers:
        
        eventer_events = Events.select().where((Events.eventer_id == eventer) &
                                               (Events.start_time >= datetime.datetime.strptime(otchet_from, "%d.%m.%y").timestamp()) &
                                               (Events.end_time <= datetime.datetime.strptime(otchet_to, "%d.%m.%y").timestamp()))
        
        a = False
        
        if not eventer_events: continue
        
        eventers_info.append({
            "eventer_tag": f"<@{eventer.discord_id}>",
            "count_events": 0,
            "summary_duration": 0,
            "summary_krugs": 0,
            "summary_prizes": 0,
            "summary_points": 0,
            "podozrtelno": 0
        })
        
        for event in eventer_events:
            if event.eventEx_id.type != "event": continue
            
            event_ex:EventEx = EventEx.select().where((EventEx.id == event.eventEx_id)).first()
            
            full_information_events["count"] += 1
            full_information_events["duration"] += event.duration
            full_information_events["summary_krugs"] += event.krugs
            full_information_events["summary_prizes"] += event.all_prize
            full_information_events["summary_points"] += event.points_summary
            
            eventers_info[-1]["count_events"] += 1
            eventers_info[-1]["summary_duration"] += event.duration
            eventers_info[-1]["summary_krugs"] += event.krugs
            eventers_info[-1]["summary_prizes"] += event.all_prize
            eventers_info[-1]["summary_points"] += event.points_summary
            a = True
            
            if av and av[event_ex.name]:
                
                if av[event_ex.name]["dur_all"]-10 < event.duration: eventers_info[-1]["podozrtelno"] += 1
                
                if av[event_ex.name]["prize_all"]-100 < event.all_prize: eventers_info[-1]["podozrtelno"] += 1
                
                #if av[event_ex.name]["dur_all"]-10 < event_ex.duration: eventers_info[-1]["podozrtelno"] += 1
            
        
        if not "event" in [x.type for x in [EventEx.get_by_id(x.eventEx_id) for x in eventer_events]]: continue
        
        if a: eventers_info_text += f' \n\nИвентёр {eventers_info[-1]["eventer_tag"]}\nВсего ивентов за период: {eventers_info[-1]["count_events"]}\nСуммарная длительность всех ивентов: {eventers_info[-1]["summary_duration"]} минут\nВсего кругов за все ивенты: {eventers_info[-1]["summary_krugs"]}\nВсего выдано серверной валюты: {eventers_info[-1]["summary_prizes"]}\nВсего получено баллов: {eventers_info[-1]["summary_points"]}\nВсего подозрительных ивентов за период: {eventers_info[-1]["podozrtelno"]}'
        else: eventers_info_text += f'\n\nИвентёр {eventers_info[-1]["eventer_tag"]} не провёл ни-одного ивента за этот период'
        
    text += f'Общая информация за период с <t:{int(datetime.datetime.strptime(otchet_from, "%d.%m.%y").timestamp())}:D>(включительно) до <t:{int(datetime.datetime.strptime(otchet_to, "%d.%m.%y").timestamp())}:D>(не включительно):\n\nВсего проведено ивентов: {full_information_events["count"]}\nВсего затрачено на проведение ивентов: {full_information_events["duration"]} минут\nВсего кругов было проведено: {full_information_events["summary_krugs"]}\nВсего выдано серверной валюты: {full_information_events["summary_prizes"]}\nВсего получено баллов: {full_information_events["summary_points"]}\n\n\n'
    
    text += eventers_info_text
    
    return text



def get_aver_ex_events(password):
    
    if not password in [x.password for x in Passwords.select().where((Passwords.accesstype=="eventers") & (Passwords.password == password))]: return "Пароль неверный"
    
    """Подготавливает статистику на определённого ивентёра

    Args:
        eventer_id (int): ID ивентёра, на которого нужно сделать статистику
        start (str): Дата в формате 30.12.22
        end (str): Дата в формате 30.12.22
        password (str): Пароль короче твой, который ты получил у Тэдэши#2468

    Returns:
        _type_: Сообщение в готовом виде для Discord`a
    """    
    events_exs = EventEx.select().where((EventEx.type=="event"))
    lol = {}
    for ev_ex in events_exs:

        ev_ex:EventEx

        events = Events.select().where((Events.duration>=15) & (Events.all_prize<=5000) & (Events.eventEx_id == ev_ex) & (Events.start_time>1661855743))

        if not events: continue

        info = {
            "events": 0,
            "krugs_all": 0,
            "dur_all": 0,
            "peoples_all": 0,
            "prize_all": 0,
        }


        for event in events:

            event:Events

            info["dur_all"] += event.duration
            info["events"] += 1
            info["krugs_all"] += event.krugs
            info["peoples_all"] += event.peoples
            info["prize_all"] += event.all_prize

        info["dur_all"] = info["dur_all"] / info["krugs_all"]
        info["peoples_all"] = info["peoples_all"] / info["krugs_all"]
        info["prize_all"] = info["prize_all"] / info["krugs_all"]
        
        lol[ev_ex.name] = info
        print(ev_ex.name,";", int(info["dur_all"]/info["krugs_all"]),";",int(info["peoples_all"]/info["events"]),";", int(info["prize_all"]/info["events"]),sep="")

    return lol