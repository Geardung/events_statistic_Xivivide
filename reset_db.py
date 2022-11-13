from models import *

#for table in [EventEx, Eventers, Events, Passwords]:
#    table.drop_table(cascade=True)
    

for table in [EventEx, Eventers, Events, Passwords]:
    
    table.create_table()
    
    if table != EventEx: continue
    
   #import psycopg2 #import the Postgres library

   ##connect to the database
   #conn = psycopg2.connect(host='localhost',
   #                       dbname='eventsXIVIVIDE',
   #                       user='postgres',
   #                       password='228485')  
   ##create a cursor object 
   ##cursor object is used to interact with the database
   #cur = conn.cursor()
   ##open the csv file using python standard file I/O
   ##copy file into the table just created 
   #f = open('./util/eventex.csv','r')
   #cur.copy_from(f, 'EventEx', sep=',')
   #f.close()