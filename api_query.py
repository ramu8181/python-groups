import urllib.request
import requests
import json
import re
import os
from prettytable import PrettyTable

def api_pretty_print(api_list):
          pretty = PrettyTable()
          pretty.field_names = ["SNo" , "ID", "Type", "Desc"]
          for i  in range(0, len(api_list)):
             post = requests.get(url=api_list[i], verify=False, headers={'accept': 'application/json'})
             dict_info =  json.loads(json.dumps(post.json(), indent=4))
             pretty.add_row([i,dict_info["properties"]["sender"],dict_info["properties"]["@type"],dict_info["properties"]["headline"]])
          print (pretty)

def convert_html_id():
       rest_list = []
       pattern = "\"id\":\s\"https://api.weather.gov/alerts.*"
       with urllib.request.urlopen("https://api.weather.gov/alerts?active=true&region=PA") as url:
           s = url.readlines()
           print(type(s))
           s = [x.decode('utf-8').strip() for x in s if x!='']
           for i in s:
              if (re.match(pattern,i)):
                 rest_list.append(i.split(" ")[1].replace("\"","").replace(",",""))
           return(rest_list)

if __name__=='__main__':
        api_list = convert_html_id()
        api_pretty_print(api_list)
