from pymongo import MongoClient, database 
import subprocess 
import threading 
import pymongo 
from datetime import datetime, timedelta 
import time 
import certifi

DBName = "test" #Use this to change which Database we're accessing 
connectionURL = "mongodb+srv://connorkoch0511:SixersFan@cecs327assignment7.j3sdksp.mongodb.net/?retryWrites=true&w=majority" #Put your database URL here 
sensorTable = "traffic data" #Change this to the name of your sensor data table 

def QueryToList(query): 
    queryData = [] 
    for line in query: 
        queryData.append(line) 
    return queryData 

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
        client = MongoClient(cluster, tlsCAFile=certifi.where()) 
        db = client[DBName] 
        print("Database collections: ", db.list_collection_names()) 

        #We first ask the user which collection they'd like to draw from. 
        sensorTable = db[sensorTable] 
        print("Table:", sensorTable) 
        #We convert the cursor that mongo gives us to a list for easier iteration. 
        timeCutOff = datetime.now() - timedelta(minutes=5) #Set how many minutes you allow 

        oldDocuments = QueryToList(sensorTable.find({"time":{"$gte":timeCutOff}})) 
        currentDocuments = QueryToList(sensorTable.find({"time":{"$lte":timeCutOff}})) 

        print("Current Docs:",currentDocuments) 
        print("Old Docs:",oldDocuments) 

        #Parse the documents that you get back for the sensor data that you need 

        RoadA = 0
        RoadB = 0 
        RoadC = 0


        for document in oldDocuments:
            if(list(document['payload'].keys())[2] == 'Traffic Sensor 91'):
                RoadA += document['payload']['Traffic Sensor 91']
            elif(list(document['payload'].keys())[2] == 'Traffic Sensor 92'):
                RoadB += document['payload']['Traffic Sensor 92']
            elif(list(document['payload'].keys())[2] == 'Traffic Sensor 93'):
                RoadC += document['payload']['Traffic Sensor 93']
        
        RoadA = RoadA / len(oldDocuments)
        RoadB = RoadB / len(oldDocuments)
        RoadC = RoadC / len(oldDocuments)

        #Return that sensor data as a list 
        return [int(RoadA), int(RoadB), int(RoadC)] 

    except Exception as e: 
        print("Please make sure that this machine's IP has access to MongoDB.") 
        print("Error:",e) 
        exit(0) 