##Please read before executing this script
##This is sample script for Posting meraki statistics in to Spark room
##Before executing this script remember to replace the Variables below begins ("REPLACE-WITH..) with corresponding value as directed/applicable.
## In this script we accomplish following
## Section 1) Reporting network information - Get network information from Meraki and post in SPARK Room
## Section 2) Reporting Client information - Get Client device traffic statistics ( Sent/Received Data)
##enjoy !!

#!/usr/bin/python
import json
import requests
import mysql.connector
import datetime


## Section 1:: Reporting network information 
##URL to request meraki

neturl = "https://n67.meraki.com/api/v0/organizations/191019/networks"

## Create a Meraki API Key. Signup and Refer to the steps in the link below.
## developers.meraki.com
netheaders = {
    'content-type': "application/json",
    'x-cisco-meraki-api-key': "REPLACE-WITH-YOUR-APIKEY", ##<<< Replace with your Meraki API key
    'cache-control': "no-cache"
    }

##URL for incoming Webhook in spark
##Spark rooms https://developer.ciscospark.com/resource-webhooks.html
sparkurl = "https://api.ciscospark.com/v1/webhooks/incoming/REPLACE-WITH-YOUR-WEBHOOK" ##<<< Replace with your incoming webhook URL from Spark

## Get your Bearer here https://developer.ciscospark.com/getting-started.html
sparkheader = {
    'content-type': "application/json; charset=utf-8",
    'authorization': "Bearer REPLACE-WITH-YOUR-BEARER", ##<<< Replace with your Bearer from Spark
    'cache-control': "no-cache"
    }


##GET request to Meraki to request network information
response = requests.request("GET", neturl, headers=netheaders)
s = json.loads(response.text)

## Create a room in Spark and save room-id for future use https://developer.ciscospark.com/endpoint-rooms-post.html
## In this section we post the network information to Spark Room
for network in s:
    ##write to mysql
    time = datetime.datetime.now()
    string = str(time) + network ['name'] + network['id'] 
    print time
    print network ['name']
    print network['id'] + '\n'
    payload = { 'roomId': "REPLACE-WITH-YOUR-ROOMID", ##<<< Replace with your Spark Room-ID
               'text': string}
    spark = requests.request("POST", sparkurl, data=json.dumps(payload), headers=sparkheader)



## Section 2:: Reporting network information 
## URL to request the Client information 
url = "https://n67.meraki.com/api/v0/devices/Q2BN-CNZX-RLTY/clients?timespan=36000"
querystring = {"timespan":"36000"}
headers = {
    'content-type': "application/json",
     'x-cisco-meraki-api-key': "REPLACE-WITH-YOUR-APIKEY", ##<<< Replace with your Meraki API key
    'cache-control': "no-cache"
    }

##URL for incoming Webhook in spark
##Spark rooms https://developer.ciscospark.com/resource-webhooks.html
sparkurl = "https://api.ciscospark.com/v1/webhooks/incoming/REPLACE-WITH-YOUR-WEBHOOK" ##<<< Replace with your incoming webhook URL from Spark

## Get your Bearer here https://developer.ciscospark.com/getting-started.html
sparkheader = {
    'content-type': "application/json; charset=utf-8",
    'authorization': "Bearer REPLACE-WITH-YOUR-BEARER", ##<<< Replace with your Bearer from Spark
    'cache-control': "no-cache"
    }

##GET request to Meraki to request Client Data
response = requests.request("GET", url, headers=headers, params=querystring)
s = json.loads(response.text)

for client in s:
    ##write to mysql
    time = datetime.datetime.now()
    data = client['usage']
    string = str(time) + " " + "Clientname" + " " +client['description'] + " " + "ClientId" + client['id'] +" "+ "SentData" + str(data['sent']) +" "+"RecvData"+str(data['recv']) 
    print time
    print  client['description']
    print str(data['sent']) + '\n'
    print str(data['recv']) + '\n'
    payload = { 'roomId': "REPLACE-WITH-YOUR-ROOMID", ##<<< Replace with your Spark Room-ID
               'text': string}
    spark = requests.request("POST", sparkurl, data=json.dumps(payload), headers=sparkheader)
    