
import json
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase, PostgresqlDatabase

with open("./config.json", "r", encoding="utf-8") as config: config = json.loads(config.read())

db = PostgresqlDatabase(
    database=config["postgreSQL"]["db"],
    user=config["postgreSQL"]["user"],
    password=config["postgreSQL"]["password"],
    host=config["postgreSQL"]["host"],
    port=config["postgreSQL"]["port"])


class BaseModel(Model):
    class Meta:
        database = db


class EventEx(BaseModel):
    
    name = TextField()
    
    points = IntegerField()
    
    type = TextField()
    
    min_players_day =  IntegerField()
    
    min_players_night = IntegerField()
    
    
class Eventers(BaseModel):
    
    discord_id = TextField()
    
    discord_tag = TextField()
    
    cookies = IntegerField(default = 0)
    
    points = IntegerField(default = 0)


    
class Events(BaseModel):
    
    eventEx_id = ForeignKeyField(EventEx, null=True)
    
    eventer_id = ForeignKeyField(Eventers)
    
    krugs = IntegerField()
    
    duration = IntegerField()
    
    peoples = IntegerField()
    
    all_prize = IntegerField()
    
    start_time = IntegerField()
    
    end_time = IntegerField()
    
    points_summary = IntegerField(null=True)
    
class Passwords(BaseModel):
    
    password = TextField()
    
    accesstype = TextField()