# -*- encoding: utf-8 -*-

from __future__ import print_function

import os
import sys
import subprocess
import datetime
import re
import csv

TIMESTAMP_FOLDER = '/Users/daiki/Box/MyMemo/timestamp/'  # must be changed
BORDER_TIME_FOR_DAYS = '03:00:00'

latest_updated_date_filename = 'latest_updated_date.txt'

pmset_command = 'pmset -g log|grep -e " Wake  " -e " Sleep  "'
border_dt = datetime.datetime.strptime(BORDER_TIME_FOR_DAYS, '%H:%M:%S')

today_str = datetime.datetime.today().strftime('%Y-%m-%d')

if os.path.exists(TIMESTAMP_FOLDER + latest_updated_date_filename):
    with open(TIMESTAMP_FOLDER + latest_updated_date_filename, 'r') as f:
        latest_data = f.read()
        if today_str == latest_data:
            sys.exit(0)

histories = subprocess.check_output(pmset_command, shell=True)

times = re.findall('(\d+-\d+-\d+) (\d+:\d+:\d+) .\d+ ([SW])', histories)

month_strs = list()
data = dict()
wake = 'first_wake'
sleep = 'last_sleep'

first_date_str = None
previous_date_str = None
wake_flag = False
last_sleep_time_str = None
for time in times:
    date_str, time_str, s_w = time

    time_dt = datetime.datetime.strptime(time_str, '%H:%M:%S')
    if time_dt < border_dt:
        date_dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        date_dt -= datetime.timedelta(days=1)
        date_str = date_dt.strftime('%Y-%m-%d')
        h_str, rest = time_str.split(':', 1)
        time_str = str(int(h_str) + 24) + ':' + rest
    month_str = date_str[:7]
    month_strs = month_strs + [month_str] \
        if month_str not in month_strs else month_strs

    if previous_date_str is not None and last_sleep_time_str is not None \
            and date_str != previous_date_str:
        if previous_date_str not in data:
            data[previous_date_str] = dict()
        data[previous_date_str][sleep] = last_sleep_time_str
    previous_date_str = date_str

    if s_w == 'W':
        wake_flag = True
        first_date_str = \
            date_str if first_date_str is None else first_date_str
        if date_str == first_date_str:
            continue
        if date_str in data:
            if wake in data[date_str]:
                continue
        else:
            data[date_str] = dict()
        data[date_str][wake] = time_str
    elif s_w == 'S':
        if wake_flag:
            last_sleep_time_str = time_str
            wake_flag = False

for month_str in month_strs:
    if os.path.exists(TIMESTAMP_FOLDER + month_str + '.txt'):
        with open(TIMESTAMP_FOLDER + month_str + '.txt', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                row[1] = row[1].replace(' ', '')
                row[2] = row[2].replace(' ', '')
                if row[0] in data:
                    if wake not in data[row[0]]:
                        data[row[0]][wake] = row[1]
                    if sleep not in data[row[0]]:
                        data[row[0]][sleep] = row[2]
                else:
                    data[row[0]] = dict()
                    data[row[0]][wake] = row[1]
                    data[row[0]][sleep] = row[2]
    date_list = list(data.keys())
    date_list = sorted(date_list,
                       key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    with open(TIMESTAMP_FOLDER + month_str + '.txt', 'w') as f:
        for date in date_list:
            if date.startswith(month_str):
                f.write(date + ', ' +
                        data[date].get(wake, '') + ', ' +
                        data[date].get(sleep, '') + '\n')

with open(TIMESTAMP_FOLDER + latest_updated_date_filename, 'w') as f:
    f.write(today_str)
