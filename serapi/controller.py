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

import serial, threading, time
from lib import logger as LogManager
logger = LogManager.Logger("JenCtrl")

CONST_BAUD_RATE = 115200
MAX_SIZE_OUT_BUFFER = 1024

class Controller(object):
  def __init__ (self, port):
    self._portName = port
    self._serial = serial.Serial()
    self._serial.baudrate = CONST_BAUD_RATE
    self._serial.port = port
    self._onRead = None
    self._thread = threading.Thread(target=self._read, name='JenCtrlRead')
    self._thread.setDaemon(False)
    self._parentThread = threading.currentThread()
  
  @property
  def portName(self):
    return self._portName
  
  @property
  def onRead(self):
    return self._onRead

  def setOnRead(self, callback):
    """Set callback function to pass the received data.

    Args:
        callback: Method to handle received data.

    """
    if callable(callback):
      self._onRead = callback
    else:
      logger.error("Callback parameter is not a function")
      self._onRead = None
  
  @property
  def serial(self):
    return self._serial
  
  def open(self):
    """Open serial port and start to receive data asychronously.

    """
    try:
      self.serial.open()
      if not self._thread.is_alive():
        self._thread.start()
    except serial.serialutil.SerialException:
      logger.error('Could not open {} port'.format(self.portName))

  def isOpen(self):
    """Open serial port and start to receive data asychronously.
    
    Returns:
            True if port is opened, False otherwise.

    """
    return self.serial.is_open

  def close(self):
    """Close the serial port connection.

    """
    logger.info('Closing {} port'.format(self.portName))
    self.serial.close()
  
  def write(self, data):
    """Write data to the serial port.

    Args:
        data: List containing the message, for instance [2, 0, 0,0]

    """
    if self.isOpen():
      if self.serial.out_waiting > MAX_SIZE_OUT_BUFFER:
        logger.info("Flushing output buffer")
        self.serial.reset_output_buffer()
      logger.debug("[TX] {}".format(map(hex, data)))
      self.serial.write(bytearray(data))
    else:
      logger.error("Cannot write when the serial port has not been opened'")
  
  def _read(self):
    """Private method to handle received data from the serial port.
    
    If callback function is set, it will be called with all data in the input
    buffer

    """
    while True:
      if not self._parentThread.is_alive():
        logger.debug("Parent thread is not running")
        self.close()
        return
      if not self.isOpen():
        logger.error("Serial port is closed, cannot read data")
        return
      if self.serial.in_waiting > 0:
        rsp = map(ord, self.serial.read(self.serial.in_waiting))
        logger.debug("[RX] {}".format(map(hex, rsp)))
        if self.onRead:
          self.onRead(rsp)
      time.sleep(0.1)

