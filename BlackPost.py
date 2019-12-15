import threading
import RestCoAP
import re
import time

import logging
log = logging.getLogger("BlackPost")

class BlackPost(threading.Thread):
 def __init__(self, nodeKey, query, payload, node=None, group=None, target=None, verbose=None): 
 #def __init__(self, nodeKey, query, node=None, group=None, target=None, verbose=None):
  threading.Thread.__init__(self, group=group, target=target, name=nodeKey, verbose=verbose)
  self.nodeKey = nodeKey
  self.query = query
  self.payload = payload
  self.signal = False
  return

 def run(self):
  #self.signal = RestCoAP.postQueryToNode(self.nodeKey,"blacklist",self.query)
  self.signal = RestCoAP.postPayloadToNode(self.nodeKey,self.query,self.payload)
  if self.signal is True:
   self.stop()
  else:
   print "error"
      
 def stop(self):
  log.info("Stoping Post Payload to {0} .".format(self.nodeKey))