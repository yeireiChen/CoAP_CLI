from __future__ import division
import RestCoAP
import time
import sys
import core.nodeinfo as NodeInfo
from BlackPost import BlackPost
from nodeBlack import getNodeBlack

counter = 380
limit = 0.7
sent = 0
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

def checkChannel():
  global sent
  avgData = [[0 for i in range(3)] for j in range(16)]
  for keys in nodeDataDic.keys(): #nodes
    nodeData = nodeDataDic[keys]
    for channels in channel:  #channels
      avgData[channels -phyRange][1] += nodeData[channels -phyRange][1];
      avgData[channels -phyRange][2] += nodeData[channels -phyRange][2];

  for i in channel:
    tempTx = avgData[i -phyRange][1]
    tempAck = avgData[i -phyRange][2]
    temp = tempAck / tempTx;
    if(tempTx>=counter) and (limit>temp):
      print "Chek-----is badChannel-----{} : txCount_{},AckCount{}.\n".format(i,tempTx,tempAck)
      badChannel.append(i)
      #channel.remove(i)
      sent = 1
    else:
      print "Chek-----             -----{} : txCount_{},AckCount{}.\n".format(i,tempTx,tempAck)

  for i in badChannel: #remove badChannel in good channel list
    if i in channel:
      channel.remove(i)

  return sent




def save_data(node,data):
  global channelSize
  print(data)
  channelSize = data[1]
  print("channelsize is ",data[1])

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
  else:
    channelData = [[0 for i in range(3)] for j in range(16)]
    for i in range(channelSize):
      tempChannel = data[channelIndex+i]
      if tempChannel not in channel:
        channel.append(tempChannel)
        
      channelData[tempChannel -phyRange][0] = tempChannel
      channelData[tempChannel -phyRange][1] = data[channelTxIndex+i]
      channelData[tempChannel -phyRange][2] = data[channelAckIndex+i]
    nodeDataDic[node] = channelData


def getBlackelist():
  #print(channelData)
  moteList = NodeInfo.getnodeList()[:]
  #moteList.append(NodeInfo.getMainKey())

  for node in moteList:
    time.sleep(0.2)
    getNodeBlack(node,"/res/blacklist")

  for item in nodeDataDic.keys():
    print(nodeDataDic[item])


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
 for node in moteList:
  time.sleep(0.2)
  BlackPost(node,query,channelPayload).start()

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





