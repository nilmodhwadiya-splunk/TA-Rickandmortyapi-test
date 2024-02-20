
# encoding = utf-8

import os
import sys
import time
import datetime
import json


def validate_input(helper, definition):
    pass

# Base_url = https://rickandmortyapi.com/api
# endpoint = /character

def main_request(helper,base_url,page_no):
    url = base_url + f'?page={page_no}'

    response = helper.send_http_request(url, 'GET', parameters=None, payload=None,headers=None, cookies=None, verify=True, cert=None,timeout=None, use_proxy=True)
    
    r_json = response.json()
    
    r_status = response.status_code
    if r_status != 200:
        response.raise_for_status()
        
    return r_json
    
    

def get_pages(response):
    
    return response["info"]["pages"]
   
    
def data_json(response):
    
    allData = []
    
    for res in response["results"]:
        obj = {
            "name" : res["name"],
            "no_ep":len(res["episode"]),
            "id":res["id"]
            }
            
        allData.append(obj)
        
    return allData
    
def checkpoint_Handler(helper,response):
    final_result = []
    
    for item in response["results"]:
        state = helper.get_check_point(str(item["id"]))
        if state is None:
            final_result.append(item)
            helper.save_check_point(str(item["id"]), "Indexed")
        #helper.delete_check_point(str(item["id"])) # i am using it only for testing
        
    return final_result

def collect_events(helper, ew):

    opt_base_url = helper.get_arg('base_url')
    opt_endpoint = helper.get_arg('endpoint')

    baseURL = opt_base_url+opt_endpoint

    
    response = main_request(helper,baseURL,1)
    
    for page in range(1,get_pages(response)+1):
        response = main_request(helper,baseURL,page)
        data = data_json(response)
        
        r = checkpoint_Handler(helper,response)

        event = helper.new_event(json.dumps(r), time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
        ew.write_event(event)
