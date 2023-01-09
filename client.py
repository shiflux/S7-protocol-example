#!/usr/bin/env python
# encoding: utf-8

'''
S7 Client Example
'''

import time

import snap7

DELTA_TEMPERATURE = 2.0

class CustomS7Client:
    '''
    Wrapper of our S7 client
    '''

    def __init__(self, host: str='127.0.0.1', port: int=1102) -> None:
        '''
        input:
            host (str): tcp address to use, default 0.0.0.0
            port (int): tcp port to use, default 1102
        '''
        self._host = host
        self._port = port
        self._address = 1

    def start(self) -> None:
        '''
        Start client loop
        '''
        client = snap7.client.Client()
        client.connect('127.0.0.1', 0, 0, self._port)
        while True:
            data = client.db_read(self._address, 0, 8)
            machine_status = snap7.util.get_bool(data, 0, 0)
            set_point = snap7.util.get_int(data, 2)
            current_temperature = snap7.util.get_real(data, 4)
            print(f'Current temperature {current_temperature:.2f}')
            if not machine_status and current_temperature>set_point+DELTA_TEMPERATURE:
                command = bytearray(2)
                snap7.util.set_bool(command, 0, 0, True)
                client.db_write(self._address, 0, command)
                print('Sent machine ON')
            elif machine_status and current_temperature<set_point-DELTA_TEMPERATURE:
                command = bytearray(2)
                snap7.util.set_bool(command, 0, 0, False)
                client.db_write(self._address, 0, command)
                print('Sent machine OFF')
            time.sleep(1)

if __name__ == "__main__":
    custom_client = CustomS7Client()
    custom_client.start()
