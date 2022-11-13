import datetime
from models import *
import os




def get_statistic_by_id(closer_id: int, start: str, end: str, password: str):
    """Подготавливает статистику на определённого ивентёра

    Args:
        closer_id (int): ID ивентёра, на которого нужно сделать статистику
        start (str): Дата в формате 30.12.22
        end (str): Дата в формате 30.12.22
        password (str): Пароль короче твой, который ты получил у Тэдэши#2468

    Returns:
        _type_: Сообщение в готовом виде для Discord`a
    """    
    
    
    if not password.lower() in [ x.password for x in Passwords.select().where((Passwords.accesstype == "closers") & (Passwords.password == password.lower()))]: return "Пароль неверный"
    
    if not os.path.exists("./out"): os.mkdir("./out")
    if not Eventers.select(): return "В базе данных нет ивентёров"
    
    while True:
        id = closer_id
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