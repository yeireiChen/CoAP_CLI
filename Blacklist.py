import RestCoAP
import time
import sys
import core.nodeinfo as NodeInfo
from BlackPost import BlackPost



def changeChannel(border, mList):
 moteList = mList[:]
 moteList.append(border)
 querytmp = "first=18&two=19&three=20"
 query = "asn="
 blackEndASN = NodeInfo.getASN()

 if blackEndASN is not 0:
  	# running 15 slotframe
  blackEndASN += 9060
  if blackEndASN % 10 is 0:
   blackEndASN += 1

 query = query + str(blackEndASN) + "&" + querytmp
 print(query)

 for node in moteList:
  time.sleep(0.2)
  BlackPost(node,query).start()




