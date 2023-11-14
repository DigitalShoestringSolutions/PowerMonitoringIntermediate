
########### PACKAGES ####
# pymodbus==2.5.3
# pyserial==3.5
# six==1.16.0

# @decoded by ANAND on Jun 2023
#########################

# configuration of address in datasheet pg 48 here:
# https://docs.rs-online.com/02cb/0900766b814cca5d.pdf

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
import time
from datetime import datetime
import os
import tomli
import logging
import logging.handlers



logger = logging.getLogger('main.measure.sensor')


########### HOBUT MFM 850 LTHN  Register Map####
# 0x0006 = v1
# 0x0008 = v2
# 0x000A = v3
# 0x000C = I1
# 0x000E = I2
# 0x0010 = I3
# 0x0012 = kW sum
# 0x001E = Hz
#########################

class ModbusPower:

    def __init__(self, adapter_addr, adapter_port=502):
        self.client = ModbusTcpClient(adapter_addr, port=adapter_port, framer=ModbusFramer)

    def register_read(self, addr, count, slave):
        res = self.client.read_input_registers(address=addr, count=int(count), unit=int(slave))
        decoder = BinaryPayloadDecoder.fromRegisters(res.registers, Endian.Big, wordorder=Endian.Little)
        reading = decoder.decode_32bit_float()
        return reading

    def action_push(self, slave_id, machine_name, voltage):
        readings = {}

        readings['reading1'] = self.register_read(0x000C, 4, slave_id)
        time.sleep(0.5)

        readings['reading2'] = float(voltage)
        time.sleep(0.5)

        readings['reading3'] = readings['reading1'] * readings['reading2']
        time.sleep(0.5)

        readings['reading4'] = self.register_read(0x001E, 4, slave_id)
        time.sleep(0.5)

        readings['reading5'] = self.register_read(0x005A, 4, slave_id)
        time.sleep(0.5)

        readings['devStat'] = 2



        return readings


