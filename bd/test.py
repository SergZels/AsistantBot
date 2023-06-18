'''
import matplotlib.pyplot as plt
import numpy as np

labels = ['G1', 'G2', 'G3', 'G4', 'G5']
men_means = [2200, 314, 3440, 3665, 2700]
women_means = [1125,4433,9987,9878,6]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()

rects1 = ax.bar(x - width/2, men_means, width, label='Men')
rects2 = ax.bar(x + width/2, women_means, width, label='Women')

ax.set_ylabel('Виручка')
ax.set_title('Графік якийсь там')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=2) # це відступ від тексту до цифри
ax.bar_label(rects2, padding=2)

fig.tight_layout()

plt.show()
'''
'''
from bdnew import botBDnew
from bdnew import Credet
from bdnew import Stat
from bdnew import db
import datetime


now = datetime.datetime.now()
r = Stat(cashAM =10, cashPM = 20, date = "2022-10-22")
r.save()
rec= Stat.select().where((Stat.date.year == now.year) & (Stat.date.month == now.month))
print(rec.sql())
# print(dir(rec))

queru = Stat.raw('SELECT * FROM Stat')
print(queru)
# res=  Stat.select().where(SQL('SELECT * FROM Stat'))
res = db.execute_sql('SELECT * FROM Stat;')
print(res.fetchall()[0])

from peewee import *
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "botBDTest.db")
db = SqliteDatabase(db_path)

class User(Model):
    name = TextField()
    old = IntegerField()
'''
import datetime
from datetime import date

now = datetime.datetime.now()
now = date(2023,1,2)
month = now.month
if month >1:
    now = now.replace(month=now.month-1) 
else: now = now.replace(month=12,year=now.year-1) 


print(now)