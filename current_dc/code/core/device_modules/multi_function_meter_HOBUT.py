import traceback
import asyncio
import logging

logger = logging.getLogger(__name__)

# Total
# 0x0012 = kW sum
# 0x0014 = kVA sum
# 0x0016 = kVAR sum
# 0x001E = Hz
# 0x0018 = PF

# Per phase
# 0x0006 = v1 (phase)
# 0x0008 = v2
# 0x000A = v3
# 0x000C = I1
# 0x000E = I2
# 0x0010 = I3
# 0x0054 = THD V1
# 0x0056 = THD V2
# 0x0058 = THD V3
# 0x005A = THD I1
# 0x005C = THD I2
# 0x005E = THD I3


class HOBUT_850_LTHN:
    def __init__(self, config, variables):
        self.register_voltage = config.get("register_voltage", 0x0006)
        self.register_current = config.get("register_current", 0x000C)
        self.register_thd_V = config.get("register_thd_V", 0x0054)
        self.register_thd_I = config.get("register_thd_I", 0x005A)

        self.slave_id = config.get("slave_id")

        self.modbus = None

        self.current_in = variables['I_in']
        self.voltage_in = variables['V_in']
        self.thd_v_in = variables['thd_v']
        self.thd_i_in = variables['thd_i']

    def initialise(self, interface):
        self.modbus = interface

    async def sample(self):
        try:
            readings = {}

            readings[self.current_in] = await self.read_modbus_register(self.register_current)
            readings[self.voltage_in] = await self.read_modbus_register(self.register_voltage)
            readings[self.thd_v_in] = await self.read_modbus_register(self.register_thd_V)
            readings[self.thd_i_in] = await self.read_modbus_register(self.register_thd_I)

            return readings
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e

    async def read_modbus_register(self, register):
        result = self.modbus.read_register(register, 4, self.slave_id)
        if asyncio.iscoroutine(result):
            return await result
        else:
            return result
