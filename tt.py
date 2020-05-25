import bs4

from selenium.webdriver.support.select import Select
from keyboard import press
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from twilio.rest import Client


import requests
import json
import pandas as pd
import dateutil.parser
import pytz
from datetime import datetime, timedelta

import sys
import time
import os



no_open_slots = True
postcodelist = ['SN11BE']
i=0
while no_open_slots:
    timezone = pytz.timezone('Europe/London')

    dt_now = datetime.now(timezone)

    tomorrow_start = datetime(dt_now.year, dt_now.month, dt_now.day, tzinfo=timezone) + timedelta(1)
    print(tomorrow_start)
    lastdate_end = tomorrow_start + timedelta(days=14)
    print(lastdate_end)
    tomorrow_start = tomorrow_start.isoformat()
    lastdate_end = lastdate_end.isoformat()
    #startdate = startdate.text



    for ipostcode in postcodelist:
        time.sleep(10)
        print(ipostcode)
        URL = "https://groceries.asda.com/api/v3/slot/view"
        i=i+1
        print(str(i) + ":"+ ipostcode)
        #cookies = chrome_cookies(URL)

        # defining a params dict for the parameters to be sent to the API
        payload = {"requestorigin":"gi","data":{"service_info":{"fulfillment_type":"DELIVERY","enable_express":False},"start_date":tomorrow_start,"end_date":lastdate_end,"reserved_slot_id":"","request_window":"P4D","service_address":{"postcode":ipostcode},"customer_info":{"account_id":"6591325788"},"order_info":{"order_id":"21484574043","restricted_item_types":[],"volume":0,"weight":0,"sub_total_amount":0,"line_item_count":0,"total_quantity":0}}}
        # sending get request and saving the response as response object
        print(payload)
        r = requests.post(url = URL, json=payload)
        data = r.json()
        data = data['data']['slot_days']
        print(data)
        ##json_file = open('Response_A.json', 'r', encoding='utf-8')
        ##data = json.load(json_file)
        ##data = data['data']['slot_days']
        list1=['UNAVAILABLE',"FULLY_BOOKED"]
        list_of_dicts = []

        for dict_1 in data:

            slots_list = dict_1['slots']

            for dict_2 in slots_list:

                if 'status' in dict_2['slot_info']:
                    #if dict_2['slot_info']['status'] in list1:
                    if dict_2['slot_info']['status'] == 'AVAILABLE':
                        new_dict = {}
                        new_dict['start_time'] = dict_2['slot_info']['start_time']
                        new_dict['end_time'] = dict_2['slot_info']['end_time']
                        new_dict['status'] = dict_2['slot_info']['status']
                        list_of_dicts.append(new_dict)

        df = pd.DataFrame(list_of_dicts, columns=['start_time', 'end_time', 'status'])
        df['start_time'] = df['start_time'].apply(lambda x: dateutil.parser.parse(x).date())

        groups = df.groupby('start_time')

        list_of_counts = [(group.strftime('%Y-%m-%d'), len(values)) for group, values in groups]
        total_values = sum([i for _, i in list_of_counts])

        print(list_of_counts)

##        print('\nTotal Values: ', total_values)
##
##        print('Total Values Per Day:\n')
##        for day, count in list_of_counts:
##            print('{} - {}'.format(day, count))

        if total_values > 0:
            print('ASDA SLOTS OPEN')

            no_open_slots = False


print('\nEntries With Status: UNAVAILABLE\n')
    ##for dict_ in list_of_dicts:



    ##for dict_ in list_of_dicts:
    ##    print(dict_)


    # extracting data in json format
    #data = r.json()

##    fullstring = r.text
##    substring = "UNAVAILABLE"
##    counter = fullstring.count(substring)
    #print(counter)

    ##jsonpath_expression = parse('data.slot_days.slots.slot_info.status')
    ##for match in jsonpath_expression.find(r):
    ##    print(f'Employee id: {match.value}')
