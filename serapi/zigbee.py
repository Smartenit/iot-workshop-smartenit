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

import os, json

_current_path = os.path.dirname(__file__)
json_file = {}
with open(_current_path + "/zigbee-types.json", "r") as json_data:
    json_file = json.load(json_data)
    json_data.close()

def has_code(code):
  if 'parse' not in json_file:
    return False
  if code not in json_file['parse']:
    return False
  return True

def get_size_from_code(code):
  if 'parse' not in json_file:
    return 0
  if code not in json_file['parse']:
    return 0
  if 'bytes' not in json_file['parse'][code]:
    return 0
  return json_file['parse'][code]['bytes']

def zigbee_parse(code, array):
  if 'parse' not in json_file:
    return None
  if code not in json_file['parse']:
    return None
  if 'parser' not in json_file['parse'][code]:
    return None
  parser = json_file['parse'][code]['parser']
  if parser == 'boolean':
    return bool(array[0]) if len(array) > 0 else False
  elif parser == 'unsigned_integer':
    return list_to_number(array)
  elif parser == 'signed_integer':
    return list_to_signed_numer(array)
  else:
    return None

def list_to_number(listObj):
  invert = listObj[::-1]
  result = 0
  for x in range(0, len(listObj)):
    result += invert[x] << x * 8
  return result  

def list_to_signed_numer(listObj):
  value = list_to_number(listObj)
  bitWidth = len(listObj) * 8
  return value - int((value << 1) & 2**bitWidth)
