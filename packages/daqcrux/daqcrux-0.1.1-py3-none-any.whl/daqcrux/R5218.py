"""! @brief Definición de la clase R5218. R5218 class definition """
##
# @file R5218.py
#
# @brief Define la clase correspondiente al sensor 5218R.
# R5218 class definition
#
# @section 5218R_WAVE_TIDE 
#
# Funciones para lectura e interpretación de los mensajes generados por el MAREÓGRAFO 5218R
# Functions for reading and iterpreting 5218R wave and tide gauge
#
# @section author Autor
# - Creado por Fernando Galassi el 26/08/2021
#
# Copyright (c) 2021 Crux Marine.  All rights reserved

import serial

# Objeto 5218
class waveandtide:
    """! Clase del sensor 5218. 5218 sensor class definition.
    """
    def __init__(self, port = "/dev/ttyUSB3", baud = 9600, t_out = 0.5):
        """! Class constructor
        @param port Sensor connection port. Default value USB3.
        @param baud Baudrate of serial communication. Default value 9600.
        @param t_out Time out of serial communication. Default value 0.5 seconds.
        @return A class instantiation of waveandtide .
        """
        ## Puerto del sensor. Sensor's port
        self.puerto = port
        ## Baudrate de la comunicación con el sensor. Baudrate of communication
        self.baud_rate = baud
        ## Timeout de la comunicación con el sensor
        self.time_out = t_out
        ## Serial port
        self.sensor = serial.Serial(self.puerto, self.baud_rate, self.time_out)
        
        
    def config(self):
        """! Function to configurate the sensor 
        """  
        ## Señal de wake al sensor  
        self.send_command()
        self.send_command("Stop\r\n", 1)
        self.send_command("Set Passkey(1)\r\n")
        self.send_command("Enable Text(no)\r\n")
        self.send_command("Set Enable Decimalformat(yes)\r\n")
        self.send_command("Set Enable Polled Mode(yes)\r\n")
        self.send_command("Save\r\n")
        self.send_command("Reset\r\n")
        
    def send_command(self, command = "\r\n", retry = 1):
        """! Function to send commands to the sensors
        @param command Command to be send. Default value is '\r\n'
        @param retry Number of retrys. Deafault value is 1
        """
        ack = False
        while ack == False and retry >= 1 :
            ## Escritura del comando en el serial 
            self.sensor.write(command)
            ack = self.wait_ack()
            retry -= 1

    def wait_ack(self):
        """! Function to interpret sensor's answer
        """
        ack = self.sensor.readline()
        if '#' in ack:
            return True
        else :
            return False

    def read(self):
        """! Function to read sensor's answer
        @return Measurement result
        """
        ## Envio de wakeup al sensor
        ##self.send_command()
        ##self.send_command("Do Sample\r\n")
        measures = self.sensor.readline()
        measures = measures.decode("ascii", errors = 'ignore')
        measure = self.decode_measures(measures)
        return measure

    def decode_measures(self, measures):
        """! Function to interpret sensor's measurement
        @param measures Measure of sensor
        @return Dict of interpreted measure
        """
        data = measures.split('\t')
        waveandtide = {}
        waveandtide['pressure'] = data[2] 
        waveandtide['temperature'] = data[3] 
        waveandtide['tide_pressure'] = data[4]
        waveandtide['tide_level'] = data[5]
        waveandtide['sign_heigth'] = data[6]
        waveandtide['max_height'] = data[7]
        waveandtide['mean_period'] = data[8]
        waveandtide['peak_period'] = data[9]
        waveandtide['energy_period'] = data[10]
        waveandtide['steepness'] = data[11]
        waveandtide['mean_zero_cross'] = data[12]
        waveandtide['irregularity'] = data[13]
        waveandtide['cutoff_freq_high'] = data[14]
        return waveandtide

