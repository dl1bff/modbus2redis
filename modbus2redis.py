#!/usr/bin/env python

import json
import time
import sys
import redis

from pymodbus.client.sync import ModbusSerialClient




def process_u32x1(registers, prefix, redis_handle):
  if (len(registers) != 2):
    print "ERROR: invalid list length"
    return 1
  
  val = registers[0] * 65536 + registers[1];
  # print prefix + "=" + str(val)
  redis_handle.setex(name=prefix, time=30, value=str(val))
  return 0





def process_u32x3(registers, prefix, redis_handle):
  if (len(registers) != 6):
    print "ERROR: invalid list length"
    return 1

  for i in range(0, 3):
    j = list((registers[i*2], registers[i*2 + 1]))
    if (process_u32x1(j, prefix + "L" + str(i+1), redis_handle) != 0):
      return 1

  return 0
 



if len(sys.argv) != 2:
  print "Usage: " + sys.argv[0] + " <json_config_file>"
  sys.exit(1)


cf = json.loads( open (sys.argv[1], "r").read() )



client = ModbusSerialClient(method='rtu', port=cf["serial_config"]["device"],
	baudrate=cf["serial_config"]["baudrate"],
	parity=cf["serial_config"]["parity"] )


client.connect()

redis_handle = redis.Redis(host='127.0.0.1', port=6379, db=0)




reqlist = cf["reqlist"]




while 1==1:
	for i in range(0, len(reqlist)):
		job = reqlist[i]

		rr = client.read_holding_registers(job["address"], job["numreg"], unit=job["unit"])

		if (rr.isError()):
		  print "ERROR: read_holding_registers " + job["prefix"]
		else:
		  if getattr(sys.modules[__name__], job["func"])(rr.registers, job["prefix"], redis_handle) != 0:
		    print "ERROR: " + job["func"]
		    break 
                time.sleep(0.05)

	time.sleep(1)
