import RestCoAP
import time
import sys
import core.nodeinfo as NodeInfo
from BlackPost import BlackPost


channel = [15,18,20,22]
blacklist = []
channelPayload = ""

def makePayload():
 global channelPayload
 channelPayload = str(len(channel))
 for i in range(len(channel)):
 	channelPayload = channelPayload +" "+str(channel[i])
 


def changeChannel():
 global channelPayload
 makePayload()
 
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





