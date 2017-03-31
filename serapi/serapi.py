#!/usr/bin/env python

__author__ = "Juan Delgado and Juan Escobar"
__copyright__ = """
This software is owned by Compacta and/or its client and is protected
under applicable copyright laws. All rights are reserved. We grant You,
and any third parties, a license to use this software solely and
exclusively on Compacta products. You, and any third parties must reproduce
the copyright and warranty notice and any other legend of ownership on each
copy or partial copy of the software.

THIS SOFTWARE IS PROVIDED "AS IS". COMPACTA MAKES NO WARRANTIES, WHETHER
EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE,
ACCURACY OR LACK OF NEGLIGENCE. COMPACTA SHALL NOT, UNDER ANY CIRCUMSTANCES,
BE LIABLE FOR ANY DAMAGES, INCLUDING, BUT NOT LIMITED TO, SPECIAL,
INCIDENTAL OR CONSEQUENTIAL DAMAGES FOR ANY REASON WHATSOEVER.

Copyright Compacta International, Ltd 2011. All rights reserved
"""
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Juan Escobar"
__email__ = "jjescof@smartenit.com"
__status__ = "Development"

import threading
from . import controller
from . import outputhandler
from . import inputhandler
from lib import logger as LogManager
logger = LogManager.Logger("SerAPI")

class State:
  SOP = 1
  CMDID = 2
  LEN = 3
  PAYLOAD = 4
  CRC = 5

class SerApi(object):
  def __init__ (self, port):
    self.ctrl = controller.Controller(port)
    self.ctrl.setOnRead(self.onData)
    self.ctrl.open()
    self._state = State.SOP
    self._pkt = {}
    self._onPkt = None
    self._output_handler = outputhandler.OutputHandler()
    self._input_handler = inputhandler.InputHandler()
    #self._interCharGapTimer = threading.Timer()
    
    self._bytesCnt = 0

  @property  
  def state(self):
    return self._state

  @state.setter
  def state(self, newState):
    self._state = newState
  
  @property
  def packet(self):
    return self._pkt

  @property
  def onPacket(self):
    return self._onPkt

  def send(self, **kwargs):
    if 'cmdId' not in kwargs:
      logger.error("cmdId is not specified")
      return
    sendData = {}
    sendData['cmdId'] = kwargs['cmdId']
    sendData['payload'] = kwargs['payload'] if 'payload' in kwargs else None
    self._send(sendData)

  def _send(self, sendData):
    lenData = len(sendData['payload']) if sendData['payload'] else 0
    cmdId = [ 0xff & (sendData['cmdId'] >> 8), sendData['cmdId'] & 0xff]
    packet = [0x02] + cmdId + [lenData]
    if lenData != 0:
      packet += sendData['payload']
    packet.append(self._calculate_crc(packet[1:]))
    self.ctrl.write(packet)
    
  def setOnPacket(self, callback):
    """Set callback function to pass the new packet.

    Args:
        callback: Method to handle received packet.

    """
    if callable(callback):
      self._onPkt = callback
    else:
      logger.error("Callback parameter is not a function")
      self._onPkt = None

  def onData(self, data):
    for byte in data:
      if self.state == State.SOP and byte == 0x02:
        self.state = State.CMDID
        continue

      elif self.state == State.CMDID:
        if self._bytesCnt == 0:
          self._pkt['cmdId'] = byte << 8
          self._bytesCnt += 1
        else:
          self._pkt['cmdId'] = self._pkt['cmdId'] | byte
          self._bytesCnt = 0
          self.state = State.LEN
        continue

      elif self.state == State.LEN:
        self._pkt['len'] = byte
        self.state = State.PAYLOAD if byte > 0 else State.CRC
        self._pkt['payload'] = []
        continue

      elif self.state == State.PAYLOAD:
        self._pkt['payload'].append(byte)
        self._bytesCnt += 1
        if self._bytesCnt >= self._pkt['len']:
          self.state = State.CRC
          self._bytesCnt = 0
          continue

      elif self.state == State.CRC:
        self.state = State.SOP
        self._pkt['crc'] = byte
        parsed = self._input_handler.parse(self._pkt)
        if self.onPacket:
          self.onPacket(parsed)
        if parsed == self._pkt:
          logger.debug("Packet received: {}".format(self._pkt_to_json(self._pkt)))
        else:
          logger.debug("Packet received: {}".format(parsed))
        self._pkt = {}

      else:
        self.state = State.SOP
        self._pkt = {}

  def send_request(self, request_string, **kwargs):
    req_body = self._output_handler.generate(request_string, **kwargs)
    self.send(**req_body)    

  def _calculate_crc (self, payload):
    crc = 0
    for byte in payload:
      crc ^= byte
    return (crc & 0xFF)
    
  def _pkt_to_json(self, pkt):
    json = {}
    if 'len' in pkt:
      json['len'] = pkt['len']
    if 'payload' in pkt:
      json['payload'] = map(hex, pkt['payload'])
    if 'cmdId' in pkt:
      json['cmdId'] = hex(pkt['cmdId'])
    if 'crc' in pkt:
      json['crc'] = hex(pkt['crc'])
    
    return json

