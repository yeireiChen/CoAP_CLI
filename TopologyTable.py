import RestCoAP
from SlotOperation import PostQuery
from NodeLocalQueue import getNodeLocalQueue
import core.nodeinfo as NodeInfo
import core.channelinfo as ChannelInfo
import core.schedule as SchedulePost
import operator
import re

node_list = []          # save the node to list. 
node_Name_list = []     # save the node name to list, not class.
global_counter = 0      # save global queue.
testing_flag = 0        # testing flag.
# slot_offset = 10          # default timeslot_offset.
# channel_offset = 0      # default channelslot_offset.
channel_offset_numbers = 16 # the number is channel offset of total numbers.
g_init_flag = None      # to get node local queue on first search.
topology_list = []
border_router_ID = None
temp_list = []
scheduleTable = {}


def set_table(host, topology_List):
  global node_list, g_init_flag
  # print node_list
  # if len(node_list) == 0 :
  #   g_init_flag = 1 
  # else :
  #   g_init_flag = 0

  dictTemp = {}

  for item in topology_List:
    #print item
    if item[0] in dictTemp:
      dictTemp[item[0]].append(item[1])
    else:
      dictTemp[item[0]] = [item[1]]

  topology_print(dictTemp, host)

def topology_print(dictTemp, host):
  global global_counter, node_list, node_Name_list, topology_list, temp_list
  topology_list = []
  get_queue = 0

  global_counter = 0 # initialize
  for mainKey in dictTemp.keys():
    if mainKey in host:
      print mainKey # host
      topology_list += [mainKey]
      border_router_ID = mainKey

      if len(temp_list) is 0:
        #hostNode = SlotOperation(nodeKey=mainKey)
        # node_list.append(hostNode)
        #node_Name_list.append(hostNode.getName())
        ChannelInfo.initial_channel_list(True)

      NodeInfo.setMainKey(mainKey)
      #print node_Name_list
        
      global_counter += 1
      for childKey in dictTemp.get(mainKey):

        # host's child is other node's parent.
        if childKey in dictTemp.keys():

          topology_list += ["--"+" 1 "+childKey]

          get_queue = parentAndChild(childKey, dictTemp, 1)

          temp_local_queue = NodeInfo.getNodeLQ(childKey)
          if temp_local_queue is None :
            temp_local_queue = getNodeLocalQueue(childKey)
          
          NodeInfo.setNodeInfo(childKey, mainKey, temp_local_queue, get_queue+temp_local_queue)

          
          global_counter += temp_local_queue
          sumCounter = get_queue+temp_local_queue

          dictTemp.pop(childKey)
 
        # only child
        else: 

          temp_local_queue = NodeInfo.getNodeLQ(childKey)
          if temp_local_queue is None:
            temp_local_queue = getNodeLocalQueue(childKey)
          
          NodeInfo.setNodeInfo(childKey, mainKey, temp_local_queue, temp_local_queue) # save the local queue and global queue.
          
          global_counter += temp_local_queue

          topology_list += ["--"+" 1 "+childKey]

  if operator.eq(temp_list, topology_list) : 
    pass
  else :
    temp_list = topology_list
    # post scheduling to all nodes.
    SchedulePost.StartSchedule(NodeInfo.getNodeTable())

  print ""
  print '\n'.join(topology_list)
  print ""

  return node_list


def parentAndChild(parentKey, dictTemp, temp_counter):
  global global_counter, slot_offset, node_list, channel_offset, topology_list
  local_queue = 0
  get_queue = 0
  save_counter = temp_counter
  for childKey in dictTemp.get(parentKey):
    
    # child still is another child's parent.
    if childKey in dictTemp.keys(): 
      temp_counter += 1

      temp_str = ""
      for index in range(0,temp_counter):
        temp_str = temp_str+"--"
      topology_list += [temp_str+" "+str(temp_counter)+" "+childKey]
      
      get_queue = parentAndChild(childKey, dictTemp, temp_counter)
      # no other child, restore uplayer of numbers.
      temp_counter = save_counter 

      temp_local_queue = NodeInfo.getNodeLQ(childKey)

      if temp_local_queue is None:
        temp_local_queue = getNodeLocalQueue(childKey)
      
      NodeInfo.setNodeInfo(childKey, parentKey, temp_local_queue, get_queue+temp_local_queue)

      global_counter += temp_local_queue
      sumCounter = get_queue+temp_local_queue

      local_queue = local_queue + sumCounter # return upper layer.

    # end of child.
    else :
      temp_str = ""
      for index in range(0,temp_counter+1):
        temp_str = temp_str+"--"
      topology_list += [temp_str+" "+str(temp_counter+1)+" "+childKey]

      temp_local_queue = NodeInfo.getNodeLQ(childKey)

      if temp_local_queue is None :
        temp_local_queue = getNodeLocalQueue(childKey)
      
      NodeInfo.setNodeInfo(childKey, parentKey,temp_local_queue, temp_local_queue)

      local_queue = local_queue + temp_local_queue # to save it.
      global_counter += temp_local_queue

  return local_queue

def slotPostControl(parentKey, childKey, send_count):
  # first need to check the child have been changed parent ?
  parent_flag = 1
  
  #print childKey+"** post to "+parentKey+" send_count : "+str(send_count)

  while (parent_flag != 0):
    parent_flag, channel_offset = ChannelInfo.check_parent_changed(childKey, parentKey)

    if parent_flag is 0 :
      slot_offset, channel_offset = ChannelInfo.peek_get_channel_list(childKey, parentKey, send_count)
      if slot_offset == 0 :
        # a new slot setting.
        #print "add channel and slot."
        slot_offset, channel_offset = ChannelInfo.set_channel_list(childKey, parentKey, 1)
        if childKey not in scheduleTable:
          scheduleTable[childKey] = str(slot_offset)+" "+str(channel_offset)+" TX "
        else :
          scheduleTable[childKey] += str(slot_offset)+" "+str(channel_offset)+" TX "

        if parentKey not in scheduleTable:
          scheduleTable[parentKey] = str(slot_offset)+" "+str(channel_offset)+" RX "
        else :
          scheduleTable[parentKey] += str(slot_offset)+" "+str(channel_offset)+" RX "

        #PostQuery(childKey, parentKey, slot_offset, channel_offset, 0, 1)

      else :
        # already setting, not chaned.
        if ChannelInfo.peek_set_channel_list(childKey, parentKey, slot_offset, channel_offset, send_count) :
          print "got same slot and channel."
          # nothing
    else :
      print "Hello~"
      # need to edit, trigger topology was changed.
#       remove_slot(childKey, parent_flag ,channel_offset)


# def remove_slot(childKey, del_slot, del_channel):
#   print "remove slot."+childKey+" "+str(del_slot)+" "+str(del_channel)
#   old_parentKey = ChannelInfo.remove_channel_list(del_slot, del_channel)
#   PostQuery(childKey, old_parentKey, 0, 0, del_slot, 2)

#   if cmp(old_parentKey, NodeInfo.getMainKey()) is 0 :
#     return 1
#   else :
#     next_old_parentKey, next_old_slot, next_old_channel = ChannelInfo.peek_next_parent_channel_list(old_parentKey, del_slot, del_channel)
#     remove_slot(old_parentKey, next_old_slot, next_old_channel)

def startPostScheduling():
  while (len(scheduleTable) > 0):
    for nodeKey in scheduleTable:
      payload_data = scheduleTable[nodeKey]
      temp_payload = cut_payload(payload_data, 64)
      flag = False
      for i in temp_payload:
        print nodeKey+" payload : "+i
        flag = RestCoAP.postPayloadToNode(nodeKey, "slotframe", i)
      if flag is True:
        scheduleTable.pop(nodeKey)
      break

  return 0

def cut_payload(payload, length):
    payloadArr = re.findall('.{'+str(length)+'}', payload)
    payloadArr.append(payload[(len(payloadArr)*length):])
    return payloadArr

def cal_timeslot(now_time_slot, numbers):
  max_numbers = 151
  now_time_slot_offset = now_time_slot + numbers

  if now_time_slot_offset > max_numbers :
    return 1
  else :
    return 0
