"""! @brief Definición de la clase airmar. Airmar class definition"""
##
# @file airmar.py
#
# @brief Define la clase correspondiente al sensor AIRMAR 220WX
# AIRMAR 220WX class definition
#
# @section AIRMAR_220WX 
#
# Funciones para lectura e interpretación de los mensajes generados por la estación meteorológica
# AIRMAR 220WX.
# Functions for reading and iterpreting AIRMAR 220WX
#
# @section author Autor
# - Creado por Fernando Galassi el 11/08/2021
#
# Copyright (c) 2021 Crux Marine.  All rights reserved

import serial

class WX220:
    """! Clase del sensor AIRMAR 220WX. Class definition for AIRMAR 220WX
    """

    def __init__(self, port = "/dev/ttyUSB0", baud = 9600, t_out = 0.5):
        """! Class constructor
        @param port Sensor connection port. Default value USB0.
        @param baud Baudrate of serial communication. Default value 9600.
        @param t_out Time out of serial communication. Default value 0.5 seconds.
        @return A class intantiation of AIRMAR WX220.
        """
        ## Puerto del sensor. Sensor's port
        self.puerto = port
        ## Baudrate de la comunicación con el sensor. Baudrate of serial communication
        self.baud_rate = baud
        ## Timeout de la comunicación con el sensor. Timeout of serial communication
        self.time_out = t_out
        # self.sensor = serial.Serial(port, baud, timeout=t_out)

    def read(self):
        """! Function to read the sensor
        @return A list of dict with measurements
        """
        measure = []
        data = self.sensor.readline()
        # Falso switch case donde pregunto  que tipo de dato es
        if data[0:6] == '$GPGGA':
            s = data.split(",")
            measure.append(WX220.decode_globalposition(s))
        elif data[0:6] == '$GPZDA':
            s = data.split(",")
            measure.append(WX220.decode_datetime(s))
        elif data[0:6] == '$WIMDA':
            s = data.split(",")
            measure.append(WX220.decode_meteordata(s))
        elif data[0:6] == '$WIMWV':
            s = data.split(",")
            measure.append(WX220.decode_windvelocity(s))
        return measure

    def decode_globalposition(list):
        """! Function to parse "$GPGGA" NMEA messages from AIRMAR 220WX
        @param list List received from read function
        @return Dict of parsed message
        """
        gpgga = {}
        gpgga["airmar_220wx_gpgga"] = list[0]
        gpgga["time"] = list[1][0:2] + ":" + list[1][2:4] + ":" + list[1][4:6]
        gpgga["latitude"] = list[2] + list[3]
        gpgga["latitude_orientation"] = list[3]
        gpgga["longitude"] = list[4] + list[5]
        gpgga["longitude_orientation"] = list[5]
        gpgga["gps_quality"] = list[6] + "\n"
        return gpgga

    def decode_datetime(list):
        """! Function to parse "$GPZDA" NMEA messages from AIRMAR 220WX
        @param list List received from read function
        @return Dict of parsed message
        """
        gpzda = {}
        gpzda["airmar_220wx_gpzda"] = list[0]
        gpzda["time"] = list[1][0:2] + ":" + list[1][2:4] + ":" + list[1][4:6]
        gpzda["date"] = list[2] + "/" + list[3] + "/" + list[4] + "\n"
        return gpzda

    def decode_meteordata(list):
        """! Function to parse "$WIMDA" NMEA messages from AIRMAR 220WX
        @param list List received from read function
        @return Dict of parsed message
        """
        wimda = {}
        wimda["airmar_220wx_wimda"] = list[0]
        wimda["barometric_pressure"] = list[3]
        wimda["air_temperature"] = list[5]
        wimda["relative_humidity"] = list[9]
        wimda["dew_point"] = list[11]
        wimda["wind_direction"] = list[13]
        wimda["wind_speed"] = list[17] + "\n"
        return wimda

    def decode_windvelocity(list):
        """! Function to parse "$WIMWV" NMEA messages from AIRMAR 220WX
        @param list List received from read function
        @return Dict of parsed message
        """
        wimwv = {}
        wimwv["airmar_220wx_wimwv"] = list[0]
        wimwv["wind_angle"] = list[1]
        wimwv["wind_speed"] = list[3] + "\n"
        return wimwv
