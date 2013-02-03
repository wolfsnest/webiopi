#   Copyright 2012-2013 Eric Ptak - trouch.com
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import time
from webiopi.bus import Bus, loadModule
from webiopi.rest import route

EXTRAS = {
    "TEMP": {"loaded": False, "module": "w1-therm"}
}

def loadExtraModule(type):
    if EXTRAS[type]["loaded"] == False:
        loadModule(EXTRAS[type]["module"])
        EXTRAS[type]["loaded"] = True

class OneWire(Bus):
    def __init__(self, slave=None, family=0, extra=None, name="1-Wire"):
        Bus.__init__(self, "ONEWIRE", "/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves", os.O_RDONLY)
        if self.fd > 0:
            os.close(self.fd)
            self.fd = 0

        self.family = family
        if  slave != None:
            addr = slave.split("-")
            if len(addr) == 1:
                self.slave = "%02x-%s" % (family, slave)
            elif len(addr) == 2:
                prefix = int(addr[0], 16)
                if family != prefix:
                    raise Exception("Slave address %s does not match family %02x" % (slave, family))
                self.slave = slave
        else:
            time.sleep(1)
            devices = self.deviceList()
            if len(devices) == 0:
                raise Exception("No device match family %02x" % family)
            self.slave = devices[0]

        loadExtraModule(extra)
        self.name = name
        
    def __str__(self):
        return "%s(slave=%s)" % (self.name, self.slave)
    
    def deviceList(self):
        devices = []
        with open(self.device) as f:
            lines = f.read().split("\n")
            if self.family > 0:
                prefix = "%02x-" % self.family
                for line in lines:
                    if line.startswith(prefix):
                        devices.append(line)
            else:
                devices = lines
        return devices;
    
    def read(self):
        with open("/sys/bus/w1/devices/%s/w1_slave" % self.slave) as file:
            data = file.read()
        return data

class OneWireTemperature(OneWire):
    def __init__(self, slave=None, family=0, name="1-Wire-Temp"):
        OneWire.__init__(self, slave, family, "TEMP", name)
        
    @route("GET", "temperature", "%.2f")
    def getTemperature(self):
        data = self.read()
        lines = data.split("\n")
        if lines[0].endswith("YES"):
            temp = lines[1][-5:]
            return int(temp) / 1000.0
