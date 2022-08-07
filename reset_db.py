from models import *

for table in [EventEx, Eventers, Events]:
    table.drop_table(cascade=True)
    

for table in [EventEx, Eventers, Events]:
    table.create_table()