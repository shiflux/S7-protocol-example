#!/usr/bin/env python
# encoding: utf-8

'''
S7 Server Example
'''

import ctypes
import time

import snap7

class CustomS7Server:
    '''
    Wrapper of our S7 server
    '''

    def __init__(self, host: str='0.0.0.0', port: int=1102) -> None:
        '''
        input:
            host (str): tcp address to use, default 0.0.0.0
            port (int): tcp port to use, default 1102
        '''
        self._host = host
        self._port = port
        self._address = 1

        # our db_data will contain the following registries
        # DB1.DBX0.0    ->  Machine ON
        # DB1.DBW2      ->  Setpoint
        # DB1.DBD4      ->  Current temperature

        # allocate 4 words = 8 bytes:
        #   - BOOLeans are containted in 1 word -> 2 bytes
        #   - INTegers are 2 bytes
        #   - REALs are 4 bytes
        self.db_data = (ctypes.c_ubyte*8)()

        # initialize Machine ON to False
        self.machine_on = False
        snap7.util.set_bool(self.db_data, 0, 0, self.machine_on)
        # initialize Setpoint to 10
        self.setpoint = 10
        snap7.util.set_int(self.db_data, 2, self.setpoint)
        # initialize Current temperature to 0
        self.current_temperature = 0.0
        snap7.util.set_real(self.db_data, 4, self.current_temperature)

    def start(self) -> None:
        '''
        Start server loop
        '''
        server = snap7.server.Server()
        server.register_area(snap7.types.srvAreaDB, self._address, self.db_data)
        server.start(self._port)
        while True:
            event = server.pick_event()
            if event:
                if event.EvtCode == 262144 and event.EvtRetCode == 0: # write command executed
                    if event.EvtParam1 == 132: # DB write
                        # address = event.EvtParam2
                        start_address = event.EvtParam3
                        write_length = event.EvtParam4
                        if start_address == 0:
                            self.machine_on = snap7.util.get_bool(self.db_data, start_address, 0)
                            print(f'Machine {"ON" if self.machine_on else "OFF"} command received')
                        elif start_address + write_length >= 2:
                            self.setpoint = snap7.util.get_int(self.db_data, start_address)
                            print(f'New setpoint {self.setpoint}')
                print(server.event_text(event))
            else:
                if self.machine_on:
                    self.current_temperature = max(self.current_temperature-0.05, 0)
                else:
                    self.current_temperature = min(self.current_temperature+0.05, 20)
                snap7.util.set_real(self.db_data, 4, self.current_temperature)
                time.sleep(.1)

if __name__ == "__main__":
    custom_server = CustomS7Server()
    custom_server.start()
