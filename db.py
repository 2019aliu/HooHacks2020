import pymongo
import os

CONNECTION_STRING = "mongodb+srv://admin:admin@covid2020-k5vfm.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
globalData = client.get_database('global')
globalConfirmed = globalData.get_collection('global_confirmed')

print(globalConfirmed.find_one({'Country/Region': 'US'})['3/28/20'])

os.system('''mongoexport --host COVID2020-shard-0/covid2020-shard-00-00-k5vfm.mongodb.net:27017,covid2020-shard-00-01-k5vfm.mongodb.net:27017,covid2020-shard-00-02-k5vfm.mongodb.net:27017 --ssl --username admin --password admin --authenticationDatabase admin --db global --collection global_confirmed --type csv --out time_series_covid19_confirmed_global.csv --fields=Province/State,Country/Region,Lat,Long,1/22/20,1/23/20,1/24/20,1/25/20,1/26/20,1/27/20,1/28/20,1/29/20,1/30/20,1/31/20,2/1/20,2/2/20,2/3/20,2/4/20,2/5/20,2/6/20,2/7/20,2/8/20,2/9/20,2/10/20,2/11/20,2/12/20,2/13/20,2/14/20,2/15/20,2/16/20,2/17/20,2/18/20,2/19/20,2/20/20,2/21/20,2/22/20,2/23/20,2/24/20,2/25/20,2/26/20,2/27/20,2/28/20,2/29/20,3/1/20,3/2/20,3/3/20,3/4/20,3/5/20,3/6/20,3/7/20,3/8/20,3/9/20,3/10/20,3/11/20,3/12/20,3/13/20,3/14/20,3/15/20,3/16/20,3/17/20,3/18/20,3/19/20,3/20/20,3/21/20,3/22/20,3/23/20,3/24/20,3/25/20,3/26/20,3/27/20,3/28/20''')