import logging
log = logging.getLogger("NodeLocalQueue")
import sys

import time
from coapthon.client.helperclient import HelperClient
from MoteDataBlack import MoteDataBlack
import Blacklist as Blacklist

port = 5683
nodeName = None
return_flag = 1
local_queue_numbers = None
nodeName = ""


def message_callback(response):
  global return_flag, local_queue_numbers, nodeName
  """
  :type response: coapthon.messages.response.Response
  """
  if response is not None:
    print("")
    print("Got new message -> {0}".format(nodeName))
    packet_content = ":".join("{:02x}".format(ord(c)) for c in response.payload)
    print(packet_content)
    print("Payload length: {0}".format(len(response.payload)))
    print("=================================")
    print(">")
    try :
      #mote, data, flag
      #local_queue_numbers = MoteData.make_from_bytes(response.source[0], response.payload, 1)
      print("got here")
      #print(response.source[0])
      data = MoteDataBlack.make_from_bytes(response.source[0],response.payload, 0)
      Blacklist.save_data(nodeName,data)
      #sent = Blacklist.checkChannel()
      #print(data)
    except :
      local_queue_numbers = 1
      print("Unexpected error: {0}".format(sys.exc_info()[0]))
      print("")
    return_flag = 0

def getNodeBlack(node,path):
  global nodeName, return_flag, local_queue_numbers
  return_flag = 1 # to initialized value.
  
  global nodeName
  nodeName = node
  src = path
  print nodeName
  coap_client = HelperClient(server=(nodeName, port))
  try:
    #coap_client = HelperClient(server=(node, port))
    start = time.time()
    coap_client.get(path=src, callback=message_callback, timeout=60)

    while (return_flag) :
      elapsed = time.time() - start
      print 'Watting time : %2.2f\r' % elapsed,
      if elapsed > 60 :
        coap_client.close()
        coap_client.get(path=src, callback=message_callback, timeout=60)
        start = time.time()

    coap_client.close()
    elapsed = time.time() - start
    print "\n%s  successful delivery, %.2f seconds." %(nodeName, elapsed-1)
    #print "Got the local queue : %s " %(str(local_queue_numbers))
    #return int(local_queue_numbers)
  except:
    if coap_client is not None:
      coap_client.close()
    print nodeName+" did not successfully send out."
