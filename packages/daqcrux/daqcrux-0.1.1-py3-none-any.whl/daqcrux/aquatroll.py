"""! @brief Definición de la clase aquatroll. Aquatroll class definition"""
##
# @file aquatroll.py
#
# @brief Define la clase correspondiente al sensor AQUATROLL 500. 
# Aquatroll class definition
#
# @section AQUATROLL 
#
# Funciones para lectura e interpretación de los mensajes generados por el/los sensores AQUATROLL.
# Functions for reading and iterpreting AQUATROLL
#
# @section author Autor
# - Creado por Fernando Galassi el 12/08/2021
#
# Copyright (c) 2021 Crux Marine.  All rights reserved

import time
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

class troll :
    """! Clase del sensor Hyperion Valeport. Hyperion sensor class definition
    """
    
    def __init__(self, address = 1, ids = {1,2,3,4}):
        """! Class constructor
        @param address Modbus address. Default value 1
        @param ids Dict of sensors attached on the probe.
        @return An instance of troll class.
        """
        # Tiene que recibir los ID de los sensores que posee para que el constructor pueda
        ## Address del sensor. Sensor's address
        self.address = address
        ## Diccionario con los id de los sensores montados en la sonda. Sensor's id
        self.ids = ids

    def check_sensors(self, channel):
        """! Function to map the sensors attached on the probe
        @param channel An instance of modbus channel
        """
        
        # Wake up.
        check = channel.read_holding_registers(6983, 14, unit=0x01)
        time.sleep(2)
        # Measurement
        check = channel.read_holding_registers(6983, 14, unit=0x01)

    def read(self, channel):
        """! Function to read the sensor
        @param channel An instance modbus channel
        @return List of results
        """
        
        ## Resultado de la medición. Measurement result
        measure = []
        # Wake up
        value = channel.read_holding_registers(((self.ids[0]-1)*7) + 5450, 2, self.address)
        time.sleep(2)

        # Measuerement
        value = channel.read_holding_registers(((self.ids[0]-1)*7) + 5450, 2, self.address)
        decoder = BinaryPayloadDecoder.fromRegisters(value.registers, byteorder = Endian.Big)
        measure.append(decoder.decode_32bit_float())
        time.sleep(2)
        value = channel.read_holding_registers(((self.ids[1]-1)*7) + 5450, 2, self.address)
        decoder = BinaryPayloadDecoder.fromRegisters(value.registers, byteorder = Endian.Big)
        measure.append(decoder.decode_32bit_float())
        time.sleep(2)
        value = channel.read_holding_registers(((self.ids[2]-1)*7) + 5450, 2, self.address)
        decoder = BinaryPayloadDecoder.fromRegisters(value.registers,byteorder=Endian.Big)
        measure.append(decoder.decode_32bit_float())
        time.sleep(2)
        value = channel.read_holding_registers(((self.ids[3]-1)*7) + 5450, 2, self.address)
        decoder = BinaryPayloadDecoder.fromRegisters(value.registers,byteorder=Endian.Big)
        measure.append(decoder.decode_32bit_float())
        return measure
