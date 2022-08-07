import datetime
from models import *
import os


def main():
    text = ""
    eventers_info_text = "Статистика ивентёров: "
    all_eventers = Eventers.select()

    otchet_from = input("Создать отчёт с (пример 22.07.22) включительно: ")
    otchet_to =  input("До (пример 22.07.22) не включительно: ") 
    input("Press to continue")
    
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
            "summary_points": 0
        })
        
        for event in eventer_events:
            if event.eventEx_id.type != "event": continue
            
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
        
        if a: eventers_info_text += f' \n\nИвентёр {eventers_info[-1]["eventer_tag"]}\nВсего ивентов за период: {eventers_info[-1]["count_events"]}\nСуммарная длительность всех ивентов: {eventers_info[-1]["summary_duration"]} минут\nВсего кругов за все ивенты: {eventers_info[-1]["summary_krugs"]}\nВсего выдано серверной валюты: {eventers_info[-1]["summary_prizes"]}\nВсего получено баллов: {eventers_info[-1]["summary_points"]}'
    
    text += f'\n\n\nОбщая информация за период с **{otchet_from}(включительно) до {otchet_to}(не включительно)**:\n\nВсего проведено ивентов: {full_information_events["count"]}\nВсего затрачено на проведение ивентов: {full_information_events["duration"]} минут\nВсего кругов было проведено: {full_information_events["summary_krugs"]}\nВсего выдано серверной валюты: {full_information_events["summary_prizes"]}\nВсего получено баллов: {full_information_events["summary_points"]}\n'
    
    text += eventers_info_text
    
    nowtime = datetime.datetime.now().strftime("%d-%m-%Y %H-%M")
    
    with open(f"./out/{nowtime}.txt", "x", encoding="utf-8") as f: 
        f.write(text)
        f.close()
        

if __name__ == "__main__":
    main()