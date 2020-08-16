#!/usr/bin/env python3

import os
import sys
import time

PSU_TYPE = [
    "MAINS",
    "BATTERY",
    "USB",
]

PSU_PROPS = [
    "STATUS",
    "CHARGE_TYPE",
    "HEALTH",
    "PRESENT",
    "ONLINE",
    "TECHNOLOGY",
    "CYCLE_COUNT",
    "VOLTAGE_MAX",
    "VOLTAGE_MIN",
    "VOLTAGE_MAX_DESIGN",
    "VOLTAGE_MIN_DESIGN",
    "VOLTAGE_NOW",
    "POWER_NOW",
    "ENERGY_FULL_DESIGN",
    "ENERGY_EMPTY_DESIGN",
    "ENERGY_FULL",
    "ENERGY_NOW",
    "CAPACITY",
    "CAPACITY_LEVEL",
    "TEMP",
    "MODEL_NAME",
    "MANUFACTURER",
    "SERIAL_NUMBER"
]

for psp in PSU_PROPS:
    psp = 'POWER_SUPPLY_PROP_' + psp
    val = 'if (!strcmp("%s", str_enum)) { return %s };' % (psp, psp)
    print(val)

for pst in PSU_TYPE:
    pst = 'POWER_SUPPLY_TYPE_' + pst
    val = 'if (!strcmp("%s", str_enum)) { return %s };' % (pst, pst)
    print(val)