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

from . import zigbee
from lib import logger as LogManager
logger = LogManager.Logger("InputHandler")

class InputHandler(object):
  def __init__(self):
    self.init_handler()

  def __getattr__(self, name):
    if name in self._map:
        return self._map[name]
    return self.__getattribute__(name)
  
  def ping_response(self, data):
    payload = data['payload'] if 'payload' in data else []
    if not isinstance(payload, list) or len(payload) != 15:
      return data
    rsp = {
      'serapi': 'SystemPingResponse',
      'macFlags': payload[0],
      'services': payload[1],
      'fwVersion': payload[2],
      'profile': self.list_to_number(payload[3:5]),
      'shortAddress': self.list_to_number(payload[5:7]),
      'ieeeAddress': payload[6:]
    }
    return rsp

  def multi_read_parser(self, data):
    payload = data['payload'] if 'payload' in data else []
    if not isinstance(payload, list) or len(payload) < 7:
      return data
    mode = payload[0]
    mrfCode = None
    if mode & (1 << 6):
      mrfCode = self.list_to_number(payload[1:3])
      payload = payload[3:]
    else:
      payload = payload[1:]
    cmdId = payload[5]
    rsp = {
      'mode': mode,
      'sourceAddress': self.list_to_number(payload[:2]),
      'sourceEndpoint': payload[2],
      'clusterId': self.list_to_number(payload[3:5]),
      'cmdId': cmdId
    }
    if mrfCode:
      rsp['manufacturerCode'] = mrfCode

    _payload = payload[6:] if len(payload) >= 7 else []
    if cmdId == 0x0b:
      rsp['serapi'] = 'DefaulResponse'
    elif cmdId == 0x01:
      rsp = self.read_attributes_response(rsp, _payload)
      rsp['serapi'] = 'ReadAttributesResponse'
    elif cmdId == 0x04:
      rsp['serapi'] = 'WriteAttributesResponse'
    elif cmdId == 0x07:
      rsp['serapi'] = 'ConfigureReportingResponse'
    elif cmdId == 0x09:
      rsp['serapi'] = 'ReadReportingConfigurationResponse'
    elif cmdId == 0x0a:
      rsp = self.read_attributes_response(rsp, _payload, False)
      rsp['serapi'] = 'ReportAttributeMessage'
    elif cmdId == 0x0d:
      rsp['serapi'] = 'DiscoverAttributeResponse'
    else:
      rsp['serapi'] = 'UnknownResponse'

    return rsp

  def read_attributes_response(self, current, payload, contains_success = True):
    if not isinstance(payload, list) or len(payload) == 0:
      current['attributes'] = []
      return current
    num_attrs = payload[0]
    if num_attrs == 0 or len(payload) == 1:
      current['attributes'] = []
      return current
    
    payload = payload[1:]
    attrs = []
    for attr_iter in range(num_attrs):
      if len(payload) < 3:
        break
      attr = {}
      attr_id = self.list_to_number(payload[:2])
      attr_data_type_index = 3
      attr_data_index = 4
      if contains_success:
        success = payload[2]
        if success != 0:
          payload = payload[3:]
          continue
      else:
        attr_data_type_index = 2
        attr_data_index = 3
      data_type = hex(payload[attr_data_type_index]).lower()
      if not zigbee.has_code(data_type):
        break
      bytes = zigbee.get_size_from_code(data_type)
      attr[hex(attr_id)] = zigbee.zigbee_parse(data_type,
                              payload[attr_data_index:attr_data_index + bytes])
      payload = payload[attr_data_index + bytes:]
      attrs.append(attr)

    current['attributes'] = attrs
    return current

  def network_address_response(self, data):
    payload = data['payload'] if 'payload' in data else []
    if not isinstance(payload, list) or len(payload) < 1:
      return data
    if payload[0] != 0 or len(payload) < 11:
      return data
    rsp = {
      'serapi': 'NetworkAddressResponse',
      'ieeeAdress': payload[1:9],
      'shortAddress': self.list_to_number(payload[9:11])
    }
    payload = payload[11:]
    if len(payload) == 0 or payload[0] == 0:
      return rsp
    rsp['devicesAssociated'] = []
    numAssocDev = payload[0]
    rsp['startIndex'] = payload[1]
    if numAssocDev * 2 != len(payload) - 2:
      return rsp
    payload = payload[2:]
    for addr in range(numAssocDev):
      rsp['devicesAssociated'].append(payload[addr:addr+2])
      payload = payload[addr+3:]
    return rsp

  def parse(self, data):
    cmdId = str(data['cmdId']) if 'cmdId' in data else None
    if not cmdId:
      return data

    handler = None
    if cmdId in self._map:
      handler = self._map[cmdId]['handler']
    
    if callable(handler):
      return handler(data)
    else:
      logger.error("Handler is not defined for cmdId {}".format(hex(int(cmdId))))
      return data

  def init_handler(self):
    self._map = {
      str(0x1000): {
        'name': 'SystemPingResponse',
        'handler': self.ping_response
      },
      str(0x1012): {
        'name': 'NetworkAddressResponse',
        'handler': self.network_address_response
      },
      str(0x1031): {
        'name': [
          'DefaulResponse',
          'ReadAttributesResponse',
          'WriteAttributesResponse',
          'ConfigureReportingResponse',
          'ReadReportingConfigurationResponse',
          'ReportAttributeMessage',
          'DiscoverAttributeResponse'
        ],
        'handler': self.multi_read_parser
      }
    }
  
  def list_to_number(self, listObj):
    return zigbee.list_to_number(listObj)

