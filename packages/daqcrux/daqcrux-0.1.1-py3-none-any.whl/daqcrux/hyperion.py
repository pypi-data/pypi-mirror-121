"""! @brief Definición de la clase hyperion. Hyperion class definition"""
##
# @file hyperion.py
#
# @brief Define la clase correspondiente al sensor HYPERION.
# Hyperion class definition
#
# @section HYPERION 
#
# Funciones para lectura e interpretación de los mensajes generados por el/los sensores Hyperion
# Functions for reading and iterpreting Valeport Hyperion sensors
#
# @section author Autor
# - Creado por Fernando Galassi el 12/08/2021
#
# Copyright (c) 2021 Crux Marine.  All rights reserved

class optical :
    """! Clase del sensor Hyperion Valeport. Hyperion class definition
    """
    
    def __init__(self, address = 15, register = 4000, nregisters = 2):
        """! Class constructor
        @param address Sensor's modbus address. Default value is 15
        @param register Starting register to read. Default value is 4000.
        @param nregisters Number of registers to read. Default value is 2.
        @return An instance of optical class.
        """
        ## Sensor Address
        self.address = address
        ## Starting register to read
        self.register = register
        ## Number of registers to read
        self.nregisters = nregisters

    def read(self, channel):
        """! Function to perform reading
        @param channel Instance of modbus channel
        @return Measurement result
        """
        ## Resultado de la medición. Measure result
        measure = channel.read(self.register, self.nregisters, self.address)
        return measure


