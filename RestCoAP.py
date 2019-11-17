import logging
log = logging.getLogger("REST_CoAP")
import sys


import core.nodeinfo as NodeInfo
import time
from coapthon.client.helperclient import HelperClient
# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"
port = 5683

def postPayloadToNode(node, resource, payload_data):
  resource = "res/"+resource
  log.info("{0} : {1}, payload -> {2}".format(node, resource, payload_data))
  try:
    coap_client = HelperClient(server=(node, port))
    start = time.time()
    coap_client.post(path=resource, payload=payload_data ,timeout=30)
    coap_client.close()
    elapsed = time.time() - start
    log.info("{} successful delivery, {:.2f} seconds. ".format(node, (elapsed-1)))
    return True
  except:
    coap_client.close()
    log.info("{0} did not successfully send out, retry again.".format(node))
    return False

def postQueryToNode(node,resource,query):
  query = "?"+query
  resource = "res/"+resource+query
  try:
    coap_client = HelperClient(server=(node, port))
    start = time.time()
    coap_client.post(path=resource, payload='' ,timeout=30)
    coap_client.close()
    elapsed = time.time() - start
    log.info("{} successful delivery, {:.2f} seconds. ".format(node, elapsed-1))
    return True
  except:
    coap_client.close()
    log.info("{0} did not successfully send out, retry again.".format(node))
    return False

def postToAllNode(List,resource,query):
  #query = "?"+query
  endASN = NodeInfo.getASN()
  if endASN is not 0:
    # running 15 slotframe
    endASN += 12080
    if endASN % 10 is 0:
      endASN += 1  
    query = "?asn="+str(endASN)+"&"+query
  resource = "res/"+resource+query
  log.info(List)
  mote_temp = List[:]
  mote_temp.append('fd00::201:1:1:1')
  #border = NodeInfo.getMainKey()
  #mote_temp.append(border)
  
  log.info(mote_temp);

  for node in mote_temp:
    try:
      coap_client = HelperClient(server=(node, port))
      start = time.time()
      coap_client.post(path=resource, payload='' ,timeout=30)
      coap_client.close()
      elapsed = time.time() - start
      log.info("{} successful delivery, {:.2f} seconds. ".format(node, elapsed-1))

    except:
      coap_client.close()
      log.info("{0} did not successfully send out, retry again.".format(node))
      pass

  return