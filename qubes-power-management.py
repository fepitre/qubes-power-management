#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import time

SYS_CLASS_POWER_SUPPLY = '/sys/class/power_supply'


class QubesPowerManagementCli:
    def __init__(self):
        self.initialized = False
        self.ac_name = 'DUMMY_AC'
        self.battery_name = 'DUMMY_BAT'

    @staticmethod
    def unload_psu_module():
        result = subprocess.run('rmmod dummy_psu', shell=True,
                                stderr=subprocess.DEVNULL)
        return result.returncode == 0

    def load_psu_module(self, model_name=None, manufacturer=None,
                        serial_number=None):
        cmd = [
            'insmod', 'dummy_psu.ko',
            'ac_name="%s"' % self.ac_name,
            'battery_name="%s"' % self.battery_name
        ]
        if model_name:
            cmd.append('battery_model_name="%s"' % model_name)
        if manufacturer:
            cmd.append('battery_manufacturer="%s"' % manufacturer)
        if serial_number:
            cmd.append('battery_serial_number="%s"' % serial_number)
        cmd = ' '.join(cmd)
        result = subprocess.run(cmd, shell=True, cwd='/home/user/dummy-psu/')
        return result.returncode == 0

    @staticmethod
    def set_psp_value(name, key, value):
        param_path = SYS_CLASS_POWER_SUPPLY + '/%s/%s' % (name, key)
        if os.path.exists(param_path):
            with open(param_path, 'w') as param_fd:
                param_fd.write(value)

    def update_psu(self, psu):
        psp_names = [prop for prop in psu.keys() if prop not in (
            'model_name', 'manufacturer', 'serial_number', 'name')]
        if 'capacity' in psp_names:
            psu_name = self.battery_name
        else:
            psu_name = self.ac_name
        for prop in psp_names:
            self.set_psp_value(psu_name, prop, psu[prop])


def main():
    cli = QubesPowerManagementCli()
    cli.unload_psu_module()

    try:
        process = subprocess.Popen(
            ['qrexec-client-vm', 'dom0', 'qubes.PowerSupply'],
            stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                psu = json.loads(output.decode('utf-8'))
                # Currently we cannot write to string properties
                # only load module with them
                if not cli.initialized:
                    psu_name = psu.get('name', None)
                    if 'capacity' in psu.keys():
                        if psu_name:
                            cli.battery_name = psu_name
                        cli.load_psu_module(
                            model_name=psu.get('model_name', None),
                            manufacturer=psu.get('manufacturer', None),
                            serial_number=psu.get('serial_number', None))
                        cli.initialized = True
                        cli.update_psu(psu)
                    else:
                        if psu_name:
                            cli.ac_name = psu_name
                else:
                    cli.update_psu(psu)

            time.sleep(1)
        rc = process.poll()
        return rc
    except KeyboardInterrupt:
        print('\n')
    finally:
        cli.unload_psu_module()


if __name__ == '__main__':
    sys.exit(main())
