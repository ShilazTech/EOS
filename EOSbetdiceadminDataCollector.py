import eospy.cleos
import os
from eospy.keys import EOSKey
from Cryptodome.PublicKey import RSA
from Cryptodome import Random
import re
import time
import csv
from datetime import datetime
from datetime import timedelta
from pandas import read_csv
ce = eospy.cleos.Cleos(url='https://proxy.eosnode.tools')

def headdata(TrainingData, LastBlocknumber):
    to_account = "betdiceadmin"
    success=0
    StartBlocknumber=LastBlocknumber
    while success==0:
        rolladded = 0
        try:
            blst=ce.get_actions(to_account,-1,-10,30)
            lasttrxid="123"
            for key, trx in blst.items():
                if isinstance( trx, int):
                    break
                else:
                    trx=trx[0]
                gameid = str(trx["action_trace"]["act"]["name"])
                trx_id = trx["action_trace"]
                trxid = trx_id["trx_id"]
                data = trx["action_trace"]["act"]["data"]
                if "dicereceipt" == gameid:
                    roll_blocknumber=float(trx["block_num"])
                    roll_timestamp = trx["block_time"]
                    if roll_blocknumber>StartBlocknumber:
                        roll_timestamp = roll_timestamp.replace("T", " ")
                        roll_timestamp = datetime.strptime(roll_timestamp, "%Y-%m-%d %H:%M:%S.%f")
                        myFormat = "%Y-%m-%d %H:%M:%S"
                        roll_timestamp=roll_timestamp.strftime(myFormat)
                        index = roll_timestamp
                        data = trx["action_trace"]["act"]["data"]
                        betAsset=data["betAsset"]
                        betAsset=betAsset.split()
                        user_betvalue=float(betAsset[0])
                        user_currency=betAsset[1]
                        user_currency = [ord(c) for c in user_currency]
                        user_currency = sum(user_currency)
                        roll_reward=data["payoutAsset"]
                        roll_reward=roll_reward.split()
                        roll_reward = float(roll_reward[0])
                        roll_result=data["result"]
                        if roll_result=="W":
                            roll_result=1
                        else:
                            roll_result=0
                        roll_value=data["diceNumber"]
                        if roll_value<50:
                            roll_value=0
                        else:
                            roll_value=1
                        seedhash=data["hashSeed"]
                        roll_predicted=seedhash[-7:]
                        roll_predicted = roll_predicted.split(":")
                        roll_predicted=float(roll_predicted[1])
                        seedhash=seedhash[:83]
                        seedhash = [ord(c) for c in seedhash]
                        user_seed = sum(seedhash)
                        Gameseed=data["hashSeedHash"]
                        Gameseed = [ord(c) for c in Gameseed]
                        Gameseed = sum(Gameseed)
                        from_account=data["accountName"]
                        from_account = [ord(c) for c in from_account]
                        from_account = sum(from_account)
                        rolldata = [index,roll_blocknumber,from_account,roll_predicted, user_betvalue,user_currency, user_seed, Gameseed, roll_result, roll_reward, roll_value]
                        rolladded=rolladded+1
                        if trxid==lasttrxid:
                            x=1
                        else:
                            success=1
                            TrainingData.append(rolldata)
                            lasttrxid=trxid
        except:
            time.sleep(0.5)
    return  TrainingData,rolladded,roll_blocknumber
def whl(headers,count,getdata,datafileT,datafileP,datasize,action):
    TrainingData = []
    TrainingData.append(headers)
    while action == 1 and getdata == 1:
        if len(TrainingData) > datasize:  ## Resizing Block
            TrainingData = TrainingData[len(TrainingData) - datasize:len(TrainingData)]
            TrainingData = [headers] + TrainingData
        if getdata == 1:  ## Data collection and writer block
            print("     ")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("COUNT Number ", count)
            if count == 0:
                LastBlocknumber = 0
            TrainingData, rolladded, LastBlocknumber= headdata(TrainingData, LastBlocknumber)
            print("Roll Added           ", rolladded)
            print("Length Training Data ", len(TrainingData))
            with open(datafileT, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerows(TrainingData)
        count = count + 1
headers=["index","roll_blocknumber","from_account","roll_predicted", "user_betvalue","user_currency", "user_seed", "Gameseed", "roll_result", "roll_reward", "roll_value"]
datafileT = "your training datafile"
count = 0
getdata = 1
datasize = 200
action = 1
whl(headers,count,getdata,datafileT,datafileP,datasize,action)