from __future__ import division
import RestCoAP
import time
import sys
import core.nodeinfo as NodeInfo
from BlackPost import BlackPost
from nodeBlack import getNodeBlack
from MoteDataBlack import MoteDataBlack

counter = 200
limit = 0.7
sent = 0 #for reset channelSequence
lock = 0
phyRange = 11
nodeDataDic = {}
#channelData= [[0 for i in range(3)] for j in range(16)]
channel = [] #15,20,22
badChannel = []
channelIndex=4
channelTxIndex=12
channelAckIndex=20
channelSize = 0
channelPayload = ""
objectSave_callback = None

last = [[0 for i in range(3)] for j in range(16)]

def getChannelChanged():
  global sent

  return sent

def getChannelSize():
  global channelSize

  channelSize = len(channel)

  return channelSize

def checkChannel():
  global sent,txLast,AckLast,last
  avgData = [[0 for i in range(3)] for j in range(16)]
  for keys in nodeDataDic.keys(): #nodes
    nodeData = nodeDataDic[keys]
    for channels in channel:  #channels
      avgData[channels -phyRange][1] += nodeData[channels -phyRange][1];
      avgData[channels -phyRange][2] += nodeData[channels -phyRange][2];

  for i in channel:
    tempTx = avgData[i -phyRange][1]
    tempAck = avgData[i -phyRange][2]
    lastTx = avgData[i -phyRange][1] - last[i -phyRange][1]
    lastAck = avgData[i -phyRange][2] - last[i -phyRange][2]
    temp = tempAck / tempTx;
    if(tempTx>=counter) and (limit>temp):
      print "Chek-----is badChannel-----{} : txCount_{},AckCount_{},lastTx_{},lastAck{}.__{:.2f}\n".format(i,tempTx,tempAck,lastTx,lastAck,temp)
      badChannel.append(i)
      #channel.remove(i)
      sent = 1
    else:
      print "Chek-----             -----{} : txCount_{},AckCount_{},lastTx_{},lastAck{}..__{:.2f}\n".format(i,tempTx,tempAck,lastTx,lastAck,temp)

    last[i -phyRange][1] = avgData[i -phyRange][1]
    last[i -phyRange][2] = avgData[i -phyRange][2]

  for i in badChannel: #remove badChannel in good channel list
    if i in channel:
      channel.remove(i)

  return sent




def save_data(node,data):
  global channelSize,objectSave_callback
  print(data)
  channelSize = data[1]
  print("channelsize is ",data[1])

  storeData = []
  if node in nodeDataDic.keys():
    tempData = nodeDataDic[node]
    for i in range(channelSize):
      tempChannel = data[channelIndex+i]
      if tempChannel not in channel:
        channel.append(tempChannel)

      tempData[tempChannel -phyRange][0] = tempChannel
      tempData[tempChannel -phyRange][1] = data[channelTxIndex+i]
      #print "got here\n"
      #print (data[channelTxIndex+i])
      tempData[tempChannel -phyRange][2] = data[channelAckIndex+i]

      #store to DB
      channel_data = MoteDataBlack(
                      mote = node,
                      start_asn = data[2], #2
                      end_asn = data[3], #3
                      channel = tempChannel,
                      txCount = data[channelTxIndex+i],
                      txAckCount = data[channelAckIndex+i],
                    )
      storeData.append(channel_data)

    for i in storeData:
      objectSave_callback(i)

  else:
    channelData = [[0 for i in range(3)] for j in range(16)]
    for i in range(channelSize):
      tempChannel = data[channelIndex+i]
      if tempChannel not in channel:
        channel.append(tempChannel)
        
      channelData[tempChannel -phyRange][0] = tempChannel
      channelData[tempChannel -phyRange][1] = data[channelTxIndex+i]
      channelData[tempChannel -phyRange][2] = data[channelAckIndex+i]

      #store to DB
      channel_data = MoteDataBlack(
                      mote = node,
                      start_asn = data[2], #2
                      end_asn = data[3], #3
                      channel = tempChannel,
                      txCount = data[channelTxIndex+i],
                      txAckCount = data[channelAckIndex+i],
                    )
      storeData.append(channel_data)

    nodeDataDic[node] = channelData

    for i in storeData:
      objectSave_callback(i)


def getBlackelist(object_callback): #object_callback
  #print(channelData)
  global objectSave_callback
  objectSave_callback = object_callback

  moteList = NodeInfo.getnodeList()[:]
  #moteList.append(NodeInfo.getMainKey())

  for node in moteList:
    time.sleep(0.2)
    getNodeBlack(node,"/res/blacklist")

  for item in nodeDataDic.keys():
    #print(nodeDataDic[item])
    print("{} : {}".format(item,nodeDataDic[item]))


def makePayload():
 global channelPayload
 channelPayload = str(len(channel))
 for i in range(len(channel)):
 	channelPayload = channelPayload +" "+str(channel[i])
 

def changeChannel():
 global channelPayload,sent 
 makePayload()

 sent = 0
 query = "blacklist?asn="
 blackEndASN = NodeInfo.getASN()

 if blackEndASN is not 0:
  	# running 15 slotframe
  blackEndASN += 9060
  if blackEndASN % 10 is 0:
   blackEndASN += 1

 query = query + str(blackEndASN)
 #print(query)
 #print(channelPayload)

 moteList = NodeInfo.getnodeList()[:]
 moteList.append(NodeInfo.getMainKey())

 threads = []
 counterIn = 0
 for node in moteList:
  time.sleep(0.2)
  threads.append(BlackPost(node,query,channelPayload))
  threads[counterIn].start()
  counterIn+=1
  #BlackPost(node,query,channelPayload).start()

 for i in range(len(threads)):
  threads[i].join()

def changeTemp():
 #print(NodeInfo.getnodeList())
 moteList = NodeInfo.getnodeList()[:]
 moteList.append(NodeInfo.getMainKey())
 querytmp = "first=11&two=13&three=15"
 query = "asn="
 blackEndASN = NodeInfo.getASN()

 if blackEndASN is not 0:
  	# running 60 slotframe/90s
  blackEndASN += 9060
  if blackEndASN % 10 is 0:
   blackEndASN += 1

 query = query + str(blackEndASN) + "&" + querytmp
 print(query)

 for node in moteList:
  time.sleep(0.2)
  BlackPost(node,query).start()





