#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime
import numpy as np
import pandas as pd

def pre_process_inflow_data():
    data = pd.read_excel('river_flow_data.xlsx', index_col=0)
    time = to_datetime(data['Time'])
    data['Time'] = time
    last_row = len(data) - 1
    data = data.drop(data.index[last_row])
    heads = data.columns[1:11]
    for h in heads:
        data[h] = data[h].astype(float)

    return data

def to_datetime(df_time):
    time_arr = np.flip(np.array(df_time))
    year = 2022  # first record year
    print('start date..............')
    print(time_arr[0])
    print('past date...............')
    print(time_arr[-1])
    counter = 0
    time_data = []
    for i in time_arr:
        counter = counter + 1
        time_i = i.split('/')
        if (len(time_i)) == 1:
            time_i = i.split('-')
        date = time_i[0]
        month_alp = time_i[1].replace('\xa0', '')
        months = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6', 'Jul': '7',
                  'Aug': '8', 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        month = months[month_alp]

        # 2020 was a leap year

        if year == 2020:
            days = 366
        else:
            days = 365

        if counter == days:
            counter = 0
            year = year + 1
            print('incrementing the year')
            print(year)

        date_time = datetime(year, int(month), int(date))
        time_data.append(date_time)

    time_array = np.flip(np.array(time_data))
    print('start date..............')
    print(time_array[0])
    print('past date...............')
    print(time_array[-1])
    return time_array

