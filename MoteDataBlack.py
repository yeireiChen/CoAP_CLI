import logging
log = logging.getLogger("moteData")

import struct
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

import core.nodeinfo as NodeInfo

Base = declarative_base()
nodeinfo = None


class MoteDataBlack(Base):
    __tablename__ = 'mote_dataBlackTest3'

    id = Column(Integer, primary_key=True)
    mote = Column(String(200))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __str__(self):
        output = []
        return '\n'.join(output)

    @classmethod
    def make_from_bytes(cls, mote, data, flag):
        
        packet_format = [
            "<xx",  # start_flag
            "B",    # packet_tcflow
            "B",    # channelSize
            "I",    # start_asn
            "I",    # end_asn
            "8B",   # channel
            "8H",   # channelTx
            "8H",   # channelTxAck
            "cc",   # parentAddress
            "xx",   # end_flag[2] 2
        ]
        
        packet_format_str = ''.join(packet_format)
        packet_item = struct.unpack(packet_format_str, data)
        #print "get here\n"
        #print(packet_item)
        #packet_item = struct.unpack("!2BBBII8B8B8B2c2x", data)
        
        if flag :
          # print str(mote)+" moteData localqu : "+str(packet_item[1])+" End ASN : "+str(packet_item[3])
          NodeInfo.updateASN(packet_item[3]) # update ASN, need return to node, want to control slotframe offset.
          #if NodeInfo.getNodeLQ(mote) is not None:
            #NodeInfo.updateNodeLQ(mote, packet_item[1])
          #return packet_item[1]
          return 1
        else :
          return packet_item
          #return 1
