"""! @brief Módulo de funciones varias. Auxiliary functions module"""
##
# @file functions.py
#
# @brief Módulo de funciones varias. auxiliary functions module. 
#
# @section FUNCIONES 
#
# Funciones varias
# Auxiliary functions
#
# @section author Autor
# - Creado por Fernando Galassi el 11/08/2021
#
# Copyright (c) 2021 Crux Marine.  All rights reserved

def log_sd(measures):
    """! Function to perform SD logging
    @param measures List of dict with measures of all the sensors
    """
    for elem in measures:
        for dicc in elem:
            for k,v in dicc.items():
                f = open("/media/SD/data.txt", 'a')
                dato = k + ": " + v + "\n"
                f.write(dato)
                f.close()

def int2bin(integer, digits):
    """! Function to perform A2's complement an formatting
    @param integer Integer to operate
    @param digits Number of digits to format
    @return A2's complement result
    """
    if integer >= 0:
        return bin(integer)[2:].zfill(digits)
    else:
        return bin(2**digits + integer)[2:]
