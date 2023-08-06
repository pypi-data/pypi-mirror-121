"""! @brief Definición de la clase ais. AIS class definition"""
##
# @file ais.py
#
# @brief Define la clase correspondiente al Transreceptor AIS.
# AIS transreciever class definition.
#
# @section AIS 
#
# Funciones para lectura y escritura de los mensajes AIS generados
# AIS functions for r/w messages   
#
# @section author Autor
# - Creado por Fernando Galassi el 11/08/2021
#
# Copyright (c) 2021 Crux Marine.  All rights reserved

import serial

class SRT:
    """! Clase del transreceptor AIS SRT. AIS transreciever class
    """

    def __init__(self, port = "/dev/ttyUSB2", baud = 38400, t_out = 0.5):
        """! Constructor de la clase
        @param port Sensor connection port. Default value USB2.
        @param baud Baudrate of serial communication. Default value 38400.
        @param t_out Time out of serial communication. Default value 0.5 seconds.
        @return A class intantiation of AIS SRT.
        """
        ## Definición del Serial
        self.ais = serial.Serial(port, baud, t_out)

    def read(self):
        """! AIS function for reading
        @return Result of reading
        """
        data = self.ais.readline()
        data = data.decode("ascii", errors = 'ignore')
        return data

    def write(self, sentence):
        """! AIS function for writing 
        @param sentence Sentence to be send
        """
        self.ais.write(str.encode(sentence))
        