"""! @brief Definición de la clase adc. ADC class definition"""
##
# @file adc.py
#
# @brief Define la clase correspondiente al adc ADS1115. 
# Definition of ADS115 class
#
# @section ADS1115 
#
# Funciones para lectura, interpretación y comunicaión con el adc ADS1115
# Functions for reading, interpretation and communication with ADS1115
#
# @section author Autor
# - Creado por Fernando Galassi el 11/08/2021
#
# Copyright (c) 2021 Crux Marine.  All rights reserved

from smbus2 import SMBus
from time import sleep
bus = SMBUS(1)

class ADS1115:
    """! Clase del ADC ADS1115
    Se define la clase utiliza para modelizar y utilizar al ADC.
    Class definition for ADS1115
    """
    def __init__(self, address = 0x48, channels = 3):
        """! Class constructor 
        @param address ADC I²C address. Dafault value 0x48
        @param channels Number of busy channels of the ADC. Default value 3
        @return An instance of ADS1115 class.
        """
        ## Address del ADC
        self.address = address
        ## Cantidad de canales ocupados del ADC
        self.channels = channels
    
    def read(self):
        """! Function for reading the ADC's channels.
        @return A list of measurements results
        """
        raw = []
        for n in self.channels:
            # Falso switch case para ver numero de canal a leer
            if n == 0:
                reg_config = [0xC1, 0x03]
                # Wake up al ADC
                bus.write_i2c_block_data(self.address, 0x01, reg_config)

                # Espera para el power up del ADC (por HDD dice ser 25 us)
                sleep(0.00005)

                # Lectura del dato
                dato = bus.read_i2c_block_data(self.address, 0x00, 2)

                # Conversion del dato. Complemento A2
                raw[n] = dato[0] * 256 + dato[1]
                if raw[n] > 32767:
                    raw[n] -= 65535

            elif n == 1:
                reg_config = [0xD1, 0x03]
                # Wake up al ADC
                bus.write_i2c_block_data(self.address, 0x01, reg_config)

                # Espera para el power up del ADC (por HDD dice ser 25 us)
                sleep(0.00005)

                # Lectura del dato
                dato = bus.read_i2c_block_data(self.address, 0x00, 2)

                # Conversion del dato. Complemento A2
                raw[n] = dato[0] * 256 + dato[1]
                if raw[n] > 32767:
                    raw[n] -= 65535
            elif n == 2:
                reg_config = [0xE1, 0x03]
                # Wake up al ADC
                bus.write_i2c_block_data(self.address, 0x01, reg_config)

                # Espera para el power up del ADC (por HDD dice ser 25 us)
                sleep(0.00005)

                # Lectura del dato
                dato = bus.read_i2c_block_data(self.address, 0x00, 2)

                # Conversion del dato. Complemento A2
                raw[n] = dato[0] * 256 + dato[1]
                if raw[n] > 32767:
                    raw[n] -= 65535
            elif n == 3:
                reg_config = [0xF1, 0x03]
                # Wake up al ADC
                bus.write_i2c_block_data(self.address, 0x01, reg_config)

                # Espera para el power up del ADC (por HDD dice ser 25 us)
                sleep(0.00005)

                # Lectura del dato
                dato = bus.read_i2c_block_data(self.address, 0x00, 2)

                # Conversion del dato. Complemento A2
                raw[n] = dato[0] * 256 + dato[1]
                if raw[n] > 32767:
                    raw[n] -= 65535
        return raw
