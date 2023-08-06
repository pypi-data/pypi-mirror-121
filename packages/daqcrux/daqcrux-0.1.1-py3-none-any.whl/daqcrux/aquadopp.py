"""! @brief Definición de la clase aquadopp. Aquadopp class definition"""
##
# @file aquadopp.py
#
# @brief Define la clase correspondiente al sensor AQUADOPP.
# Aquadopp class definition
#
# @section AQUADOPP_ADCP 
#
# Funciones para lectura e interpretación de los mensajes generados por el ADCP AQUADOPP.
# Functions for reading and iterpreting AQUADOPP
#
# @section author Autor
# - Creado por Fernando Galassi el 11/08/2021
#
# Copyright (c) 2021 Crux Marine.  All rights reserved

import serial

# Objeto Aquadopp
class adcp:
    """! Clase del sensor AQUADOPP. Class definition for AQUADOPP
    """
    
    def __init__(self, port = "/dev/ttyUSB1", baud = 9600, t_out = 0.5):
        """! Class constructor
        @param port Sensor connection port. Default value USB1.
        @param baud Baudrate of serial communication. Default value 9600.
        @param t_out Time out of serial communication. Default value 0.5 seconds.
        @return A class intantiation of AQUADOPP.
        """
        ## Puerto del sensor. Sensor's port
        self.puerto = port
        ## Baudrate de la comunicación con el sensor. Baudrate of serial communication
        self.baud_rate = baud
        ## Timeout de la comunicación con el sensor. Timeout of serial communication
        self.time_out = t_out
        #self.sensor = serial.Serial(port, baud, timeout=t_out)

    def read(self):
        """! Function to read the sensor
        @return A list of dict with measurements
        """
        data = self.sensor.readline()
        measure =[]
        if data[0:6] == '$PNORS':
            s = data.split(",")
            measure.append(adcp.decode_sensordata(s))
        elif data[0:6] == '$PNORC':
            s = data.split(",")
            measure.append(adcp.decode_currentvelocity(s))
        return measure

    def decode_sensordata(list):
        """! Function to parse "$PNORS" NMEA messages from AQUADOPP
        @param list List received from read function
        @return Dict of parsed message
        """
        pnors = {}

        if list[3] == 1:
            pnors["aquadopp"] = "Data Sensor"
            pnors["date"] = list[1][0:2] + "/" + list[1][2:4] + "/" + list[1][4:6]
            pnors["time"] = list[2][0:2] + ":" + list[1][2:4] + ":" + list[1][4:6]
            pnors["error"] = "yes" + "\n"
        else:
            pnors["aquadopp"] = "Data Sensor"
            pnors["date"] = list[1][0:2] + "/" + list[1][2:4] + "/" + list[1][4:6]
            pnors["time"] = list[2][0:2] + ":" + list[1][2:4] + ":" + list[1][4:6]
            pnors["status"] = list[4]
            pnors["baterry_voltage"] = list[5] + " V"
            pnors["sound_speed"] = list[6] + " m/s"
            pnors["heading"] = list[7] + " grados"
            pnors["pitch"] = list[8] + " grados"
            pnors["roll"] = list[9] + " grados"
            pnors["pressure"] = list[10]
            pnors["water_temperature"] = list[11]
            pnors["analog_in1"] = list[12] + " Cuentas"
            pnors["analog_in2"] = list[13][0:1] + " Cuentas"
            pnors["error"] = "No" + "\n"
        return pnors

        # Funcion para decodificar los mensajes NMEA del tipo '$PNORC' del AQUADOPP
    def decode_currentvelocity(list):
        """! Function to parse "$PNORC" NMEA messages from AQUADOPP
        @param list List received from read function
        @return Dict of parsed message
        """
        pnorc = {}
        pnorc["aquadopp"] = "Current velocity"
        pnorc["date"] = list[1][0:2] + "/" + list[1][2:4] + "/" + list[1][4:6]
        pnorc["time"] = list[2][0:2] + ":" + list[1][2:4] + ":" + list[1][4:6]
        pnorc["cell_number"] = list[3]
        pnorc["velocity_1"] = list[4]
        pnorc["velocity_2"] = list[5]
        pnorc["velocity_3"] = list[6]
        pnorc["speed"] = list[7]
        pnorc["current_direction"] = list[8]
        pnorc["amplitude_1"] = list[10] + " counts"
        pnorc["amplitude_2"] = list[11] + " counts"
        pnorc["amplitude_3"] = list[12] + " counts"
        pnorc["correlation_1"] = list[13] + " %"
        pnorc["correlation_2"] = list[14] + " %"
        pnorc["correlation_3"] = list[15][0:1] + " % " + "\n"

        return pnorc

