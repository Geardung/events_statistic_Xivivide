from datetime import datetime
import os, json
from models import *


def get_aver_ex_events():
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