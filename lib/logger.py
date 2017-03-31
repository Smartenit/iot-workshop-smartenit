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

import datetime

def get_current_time():
  return datetime.datetime.now().strftime('%b %d %H:%M:%S.%f')

class Logger(object):
  def __init__ (self, tag):
    self._tag = tag
  
  @property
  def tag(self):
    return self._tag
  
  @tag.setter
  def tag(self, tag):
    self._tag = tag
  
  def log(self, verbosity, msg):
    print(get_current_time() + " " + self._tag + "[" + verbosity + "] " + msg)
  
  def info(self, msg):
    self.log("INFO", msg)
  
  def debug(self, msg):
    self.log("DEBUG", msg)
  
  def error(self, msg):
    self.log("ERROR", msg)

