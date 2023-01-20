import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
from pymongo_get_database import get_database

def get_record_count(keyword, n, j):
    #Published is the date when the article got saved in the database.
    data = {
        "Published": {
            "$lt": datetime.datetime.today() - datetime.timedelta(days=n) ,
            "$gt": datetime.datetime.today() - datetime.timedelta(days=j)
        }
    }
    dbname = get_database()
    return len(list(dbname[keyword].find(data)))

topics = ['tesla', 'apple', 'microsoft', 'nasa', 'amazon', 'BBC', 'cloud', 'fiat'] 

recordDay5 = []
recordDay4 = []
recordDay3 = []
recordDay2 = []
recordDay1 = []
for topic in topics :
    recordDay5.append(get_record_count(topic, 0, 1)) #Count records of each topic the 5 day
    recordDay4.append(get_record_count(topic, 1, 2)) #Count records of each topic the 4 day
    recordDay3.append(get_record_count(topic, 2, 3)) #Count records of each topic the 3 day
    recordDay2.append(get_record_count(topic, 3, 4)) #Count records of each topic the 2 day
    recordDay1.append(get_record_count(topic, 4, 5)) #Count records of each topic the 1 day


# create data
df = pd.DataFrame([
    ['Day 5', recordDay5[0], recordDay5[1], recordDay5[2], recordDay5[3], recordDay5[4], recordDay5[5], recordDay5[6], recordDay5[7]],
    ['Day 4', recordDay4[0], recordDay4[1], recordDay4[2], recordDay4[3], recordDay4[4], recordDay4[5], recordDay4[6], recordDay4[7]],
    ['Day 3', recordDay3[0], recordDay3[1], recordDay3[2], recordDay3[3], recordDay3[4], recordDay3[5], recordDay3[6], recordDay3[7]],
    ['Day 2', recordDay2[0], recordDay2[1], recordDay2[2], recordDay2[3], recordDay2[4], recordDay2[5], recordDay2[6], recordDay2[7]],
    ['Day 1', recordDay1[0], recordDay1[1], recordDay1[2], recordDay1[3], recordDay1[4], recordDay1[5], recordDay1[6], recordDay1[7]]
    ],
    columns=['Topics',  topics[0], topics[1], topics[2], topics[3], topics[4], topics[5], topics[6], topics[7]])
# view data
print(df)
ax = df.plot(x='Topics', stacked=True, kind='bar', figsize=(12, 8), rot='horizontal')

# .patches is everything inside of the chart
for rect in ax.patches:
    # Find where everything is located
    height = rect.get_height()
    width = rect.get_width()
    x = rect.get_x()
    y = rect.get_y()
    
    # The height of the bar is the data value and can be used as the label
    label_text = f'{height}'  # f'{height:.2f}' to format decimal values
    
    # ax.text(x, y, text)
    label_x = x + width / 2
    label_y = y + height / 2

    # plot only when height is greater than specified value
    if height > 0:
        ax.text(label_x, label_y, label_text, ha='center', va='center', fontsize=8)
    
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)    
ax.set_ylabel("Count", fontsize=18)
ax.set_xlabel("Day", fontsize=18)

plt.savefig('plot.png')
plt.show()