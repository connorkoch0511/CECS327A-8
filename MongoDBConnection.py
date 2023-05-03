from pymongo import MongoClient, database 

import subprocess 

import threading 

import pymongo 

from datetime import datetime, timedelta 

import time 

 
 

DBName = "test" #Use this to change which Database we're accessing 

connectionURL = "mongodb+srv://connorkoch0511:SixersFan@cecs327assignment7.j3sdksp.mongodb.net/?retryWrites=true&w=majority" #Put your database URL here 

sensorTable = "test.traffic data" #Change this to the name of your sensor data table 

 
 

def QueryToList(query): 

    queryData = [] 

    for line in query: 

        queryData.append(line) 

    return queryData 

 
 

  #pass; #TODO: Convert the query that you get in this function to a list and return it 

  #HINT: MongoDB queries are iterable 

 
 

def QueryDatabase() -> list: 

    global DBName 

    global connectionURL 

    global currentDBName 

    global running 

    global filterTime 

    global sensorTable 

    cluster = None 

    client = None 

    db = None 

    try: 

        cluster = connectionURL 

        client = MongoClient(cluster) 

        db = client[DBName] 

        print("Database collections: ", db.list_collection_names()) 

 
 

        #We first ask the user which collection they'd like to draw from. 

        sensorTable = db[sensorTable] 

        print("Table:", sensorTable) 

        #We convert the cursor that mongo gives us to a list for easier iteration. 

        timeCutOff = datetime.now() - timedelta(minutes=0) #TODO: Set how many minutes you allow 

 
 

        oldDocuments = QueryToList(sensorTable.find({"time":{"$gte":timeCutOff}})) 

        currentDocuments = QueryToList(sensorTable.find({"time":{"$lte":timeCutOff}})) 

 
 

        print("Current Docs:",currentDocuments) 

        print("Old Docs:",oldDocuments) 

 
 

        #TODO: Parse the documents that you get back for the sensor data that you need 

        for document in oldDocuments: 

            print(document['payload']) 

        #Return that sensor data as a list 

 
 

        return oldDocuments 

 
 
 

    except Exception as e: 

        print("Please make sure that this machine's IP has access to MongoDB.") 

        print("Error:",e) 

        exit(0) 

 
 
 

 