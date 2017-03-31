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

from lib import logger as LogManager
logger = LogManager.Logger("OutputHandler")

class OutputHandler(object):
  def __init__(self):
    self.init_handler()
  
  def __getattr__(self, name):
    if name in self._map:
        return self._map[name]
    return self.__getattribute__(name)
  
  def generate(self, request_string, **kwargs):
    handler = None
    if request_string in self._map:
      handler = self._map[request_string]['handler']
    
    if callable(handler):
      return handler(**kwargs)
    else:
      logger.error("Handler is not defined for {}".format(request_string))
      return {}
      
  def ping_request(self, **kwargs):
    return {'cmdId': self.SystemPing['cmdId']}
  
  def short_network_request(self, **kwargs):
    str_cmd = 'ShortNetworkAddressRequest'
    reqs = self.ShortNetworkAddressRequest['requirements']
    if not self._has_requiriments(str_cmd, kwargs, reqs):
      return {}
    payload = self._int_to_array(kwargs['ieeeAddress'], 8)
    if 'startIndex' in kwargs:
      payload +=  [1] + self._int_to_array(kwargs['startIndex'], 1)
    else:
      payload +=  [0, 0]
    return {'cmdId': self.ShortNetworkAddressRequest['cmdId'], 
            'payload': payload}

  def cluster_commands(self, **kwargs):
    str_cmd = 'ClusterCommands'
    reqs = self.ClusterCommands['requirements']
    if not self._has_requiriments(str_cmd, kwargs, reqs):
      return {}
    payload = []
    payload += self._int_to_array(kwargs['mode'], 1)
    if 'manufacturerCode' in kwargs:
      payload[0] = payload[0] | 1 << 6
      payload += self._int_to_array(kwargs['manufacturerCode'], 2)
    payload += self._int_to_array(kwargs['destinationAddress'], 2)
    payload += self._int_to_array(kwargs['destinationEndpoint'], 1)
    payload += self._int_to_array(kwargs['clusterId'], 2)
    payload += self._int_to_array(kwargs['commandId'], 1)
    if 'payload' in kwargs and isinstance(kwargs['payload'], list):
      payload += kwargs['payload']
    return {'cmdId': self.ClusterCommands['cmdId'], 'payload': payload}
  
  def read_attributes(self, **kwargs):
    str_cmd = 'ReadAttributes'
    reqs = self.ReadAttributes['requirements']
    if not self._has_requiriments(str_cmd, kwargs, reqs):
      return {}
    payload = []
    payload += self._int_to_array(kwargs['mode'], 1)
    if 'manufacturerCode' in kwargs:
      payload[0] = payload[0] | 1 << 6
      payload += self._int_to_array(kwargs['manufacturerCode'], 2)
    payload += self._int_to_array(kwargs['destinationAddress'], 2)
    payload += self._int_to_array(kwargs['destinationEndpoint'], 1)
    payload += self._int_to_array(kwargs['clusterId'], 2)
    payload.append(0)
    payload += [len(kwargs['attributesList'])]
    for attr in kwargs['attributesList']:
      payload += self._int_to_array(attr, 2)
    return {'cmdId': self.ReadAttributes['cmdId'], 'payload': payload}

  def _has_requiriments(self, request_string, obj, required_list):
    for req in required_list:
      if req not in obj:
        logger.error("{} is required for {}".format(req, request_string))
        return False
    return True

  def init_handler(self):
    self._map = {
      'SystemPing': {
        'cmdId': 0x0000,
        'handler': self.ping_request,
        'description': 'Ping device to verify if it is active and to check its capability'
      },
      'ClusterCommands': {
        'cmdId': 0x0030,
        'handler': self.cluster_commands,
        'requirements': [
          'mode',
          'destinationAddress',
          'destinationEndpoint',
          'clusterId',
          'commandId'
        ],
        'description': 'General format for sending commands to a cluster'
      },
      'ReadAttributes': {
        'cmdId': 0x0030,
        'handler': self.read_attributes,
        'requirements': [
          'mode',
          'destinationAddress',
          'destinationEndpoint',
          'clusterId',
          'attributesList'
        ],
        'description': 'General format for sending commands to a cluster'
      },
      'ShortNetworkAddressRequest': {
        'cmdId': 0x0012,
        'handler': self.short_network_request,
        'requirements': [
          'ieeeAddress'
        ],
        'description': 'Request a device short network address and its Childrens (ShortAddress) list'      
      }
    }
  
  def _int_to_array(self, val, num_bytes):
    d = [(val >> pos * 8) & 0xff for pos in range(num_bytes)]
    return d[::-1]
    
