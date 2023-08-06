"""! @brief Módulo de funciones utilizadas para el armado del mensaje 8 AIS.
AIS message 8 construction functions module
"""
##
# @file message.py
#
# @brief Módulo de funciones utilizadas para el armado del mensaje 8 AIS
# AIS message 8 construction functions module
#
# @section Message 
#
# Funciones para la codificación y armado del mensaje binario 8 AIS.
#
# @section author Autor
# - Creado por Fernando Galassi el 11/08/2021
#
# Copyright (c) 2021 Crux Marine.  All rights reserved

import functions
from datetime import datetime

def bintoascii (chain):
    """! Function to perform ASCII 6-bits codification
    @param chain Chain to codificate in ASCII 6-bits
    @return ASCII 6-bits character
    """
    if chain == '000000':
        return '0'
    elif chain == '000001':
        return '1'
    elif chain == '000010':
        return '2'
    elif chain == '000011':
        return '3'
    elif chain == '000100':
        return '4'
    elif chain == '000101':
        return '5'
    elif chain == '000110':
        return '6'
    elif chain == '000111':
        return '7'
    elif chain == '001000':
        return '8'
    elif chain == '001001':
        return '9'
    elif chain == '001010':
        return ':'
    elif chain == '001011':
        return ';'
    elif chain == '001100':
        return '<'
    elif chain == '001101':
        return '='
    elif chain == '001110':
        return '>'
    elif chain == '001111':
        return '?'
    elif chain == '010000':
        return '@'
    elif chain == '010001':
        return 'A'
    elif chain == '010010':
        return 'B'
    elif chain == '010011':
        return 'C'
    elif chain == '010100':
        return 'D'
    elif chain == '010101':
        return 'E'
    elif chain == '010110':
        return 'F'
    elif chain == '010111':
        return 'G'
    elif chain == '011000':
        return 'H'
    elif chain == '011001':
        return 'I'
    elif chain == '011010':
        return 'J'
    elif chain == '011011':
        return 'K'
    elif chain == '011100':
        return 'L'
    elif chain == '011101':
        return 'M'
    elif chain == '011110':
        return 'N'
    elif chain == '011111':
        return 'O'
    elif chain == '100000':
        return 'P'
    elif chain == '100001':
        return 'Q'
    elif chain == '100010':
        return 'R'
    elif chain == '100011':
        return 'S'
    elif chain == '100100':
        return 'T'
    elif chain == '100101':
        return 'U'
    elif chain == '100110':
        return 'V'
    elif chain == '100111':
        return 'W'
    elif chain == '101000':
        return '`'
    elif chain == '101001':
        return 'a'
    elif chain == '101010':
        return 'b'
    elif chain == '101011':
        return 'c'
    elif chain == '101100':
        return 'd'
    elif chain == '101101':
        return 'e'
    elif chain == '101110':
        return 'f'
    elif chain == '101111':
        return 'g'
    elif chain == '110000':
        return 'h'
    elif chain == '110001':
        return 'i'
    elif chain == '110010':
        return 'j'
    elif chain == '110011':
        return 'k'
    elif chain == '110100':
        return 'l'
    elif chain == '110101':
        return 'm'
    elif chain == '110110':
        return 'n'
    elif chain == '110111':
        return 'o'
    elif chain == '111000':
        return 'p'
    elif chain == '111001':
        return 'q'
    elif chain == '111010':
        return 'r'
    elif chain == '111011':
        return 's'
    elif chain == '111100':
        return 't'
    elif chain == '111101':
        return 'u'
    elif chain == '111110':
        return 'v'
    elif chain == '111111':
        return 'w'

def codification(binpayload):
    """! Function to slice binary chain in 6 bits.
    @param binpayload Binary payload to codificate
    @return Codificated payload
    """
    l = 6
    li = 0
    cod = ''
    for i in range(54):
        b = bintoascii(binpayload[li:l])
        li = l
        l += 6
        cod += b
    return cod

def checksum(sentence):
    """! Funtion to generate checksum
    @param sentence Sentence to get checksum
    @return Checksum 
    """
    i = 0
    checksum = 0
    st = sentence[1:]
    while i < len(st):
        checksum ^= ord(st[i])
        i += 1
    h_chcksm = hex(checksum)[2:]
    s_chcksm = h_chcksm
    if len(s_chcksm) == 1:
        new_chcksm = '0'+ s_chcksm
    else:
        new_chcksm = s_chcksm
    return new_chcksm.upper()

def mssg8_bin(data):
    """! Function to build AIS message 8 in binary from all the measuments of the sensors
    @param data List of dict with measuremnts resutls
    @return Binary payload
    """
    longitude = 0
    latitude = 0
    wind_speed = 0
    wind_direction = 0
    temperature = 0
    humidity = 0
    current_speed = 0
    current_direction = 0
    water_temperature = 0
    dew_point = 0
    barometric_pressure = 0
    water_level = 0
    utc = datetime.utcnow()
    # print(utc)
    day = utc.day
    date = f'{day:05b}'
    hora = utc.hour
    hour = f'{hora:05b}'
    minuto = utc.minute
    minute = f'{minuto:06b}'
    # Carga de valores que no se miden
    dac = f'{1:010b}'
    fid = f'{31:06b}'
    position_accuracy = f'{0:01b}'
    # Carga de valores N/A en variables que no puedo medir por el momento
    wind_gust = f'{127:07b}'
    wind_gust_dir = f'{511:09b}'
    pressure_trend = f'{3:02b}'
    visibility = f'{127:08b}'
    level_trend = f'{3:02b}'
    current_2_speed = f'{255:08b}'
    current_2_dir = f'{360:09b}'
    current_2_depth = f'{31:05b}'
    current_3_speed = f'{255:08b}'
    current_3_dir = f'{360:09b}'
    cdepth3 = f'{31:05b}'
    wave_direction = f'{360:09b}'
    swell_height = f'{255:08b}'
    swell_period = f'{63:06b}'
    swell_direction = f'{360:09b}'
    sea_state = f'{13:04b}'
    preciptation_type = f'{7:03b}'
    salinity = f'{510:09b}'
    ice = f'{3:02b}'
    spare_2 = f'{0:010b}'
    fill_bits = f'{0:04b}'

    for elem in data:
        for dicc in elem:
            for k,v in dicc.items():
                if k == "latitude":
                    data = len(v)
                    if v[data-1] == 'N':
                        latitude = v[:-1]
                        latitude = float(latitude)
                        latitude = latitude * 600
                        latitude = int(latitude)
                        latitude = f'{latitude:024b}'
                    else:
                        latitude = v[:-1]
                        latitude = float(latitude)
                        latitude = (-latitude) * 600
                        latitude = int(latitude)
                        latitude = functions.int2bin(latitude,24)
                elif k == "longitude":
                    data = len(v)
                    if v[data-1] == 'E':
                        longitude = v[:-1]
                        longitude = float(longitude)
                        longitude = longitude * 600
                        longitude= int(longitude)
                        longitude = f'{longitude:025b}'
                    else:
                        longitude = v[:-1]
                        longitude = float(longitude)
                        longitude = (-longitude) * 600
                        longitude = int(longitude)
                        longitude = functions.int2bin(longitude,25)
                elif k == "wind_speed":
                    wind_v = float(v)
                    if wind_v < 1 :
                        wind_v = 0
                    wind_v = int(wind_v)
                    wind_speed = f'{wind_v:07b}'
                elif k == "wind_direction":
                    wind_dir = float(v)
                    wind_dir = int(wind_dir)
                    wind_direction = f'{wind_dir:09b}'
                elif k == "air_temperature":
                    air_t = float(v)
                    air_t = air_t * 10
                    air_t = int(air_t)
                    temperature = f'{air_t:011b}'
                elif k == "relative_humidity":
                    r_humidity = float(v)
                    r_humidity = int(r_humidity)
                    humidity = f'{r_humidity:07b}'
                elif k == "dew_point":
                    d_point = float(v)
                    d_point = d_point * 10
                    d_point = int(d_point)
                    dew_point = f'{d_point:010b}'
                elif k == "barometric_pressure":
                    b_pressure = float(v)
                    b_pressure = b_pressure * 1000
                    b_pressure = int(b_pressure)
                    b_pressure = b_pressure * 401 / 1200 # Adaptacion a la norma del AIS
                    b_pressure = int(b_pressure)
                    barometric_pressure = f'{b_pressure:09b}'
                elif k == "velocity_1":
                    vel1 = float(v)
                    vel1 = vel1 * 1.944 * 100 # Pasaje de m/s a knots
                    if vel1 > 25:
                        vel1 = 251
                        current_speed = f'{vel1:08b}'
                    else:
                        vel1 = int(vel1)
                        current_speed = f'{vel1:08b}'
                elif k == "velocity_2":
                    vel2 = float(v)
                    vel2 = vel2 * 1.944 * 100 # Pasaje de m/s a knots
                    if vel2 > 25:
                        vel2 = 251
                        s_vel2 = f'{vel2:08b}'
                    else:
                        vel2 = int(vel2)
                        s_vel2 = f'{vel2:08b}'
                elif k == "velocity_3":
                    vel3 = float(v)
                    vel3 = vel3 * 1.944 * 100  # Pasaje de m/s a knots
                    if vel3 > 25:
                        vel3 = 251
                        s_vel3 = f'{vel3:08b}'
                    else:
                        vel3 = int(vel3)
                        s_vel3 = f'{vel3:08b}'
                elif k == "current_direction":
                    current_d = float(v)
                    current_d = int(current_d)
                    current_direction = f'{current_d:09b}'
                elif k == "water_temperatura":
                    water_t = float(v)
                    water_t = int(water_t)
                    if water_t < 0:
                        water_temperature = functions.int2bin(water_t,10)
                    else :
                        water_temperature = f'{water_t:010b}'
                elif k == "water_level":
                    water_l = float(v)
                    water_l = int(water_l)
                    water_l = (water_l / 100) - 10
                    water_level = f'{water_l:12b}'
                elif k == "sign_heitght" :
                    wave_h = float(v)
                    wave_h = int(wave_h)
                    wave_h = wave_h * 10
                    wave_height = f'{wave_h:08b}'
                elif k == "mean_period" :
                    wave_p = float(v)
                    wave_p = int(wave_p)
                    wave_period = f'{wave_p:06b}'

    payl = dac + fid + longitude + latitude + position_accuracy + date + hour + minute + wind_speed + wind_gust + wind_direction + wind_gust_dir + temperature + \
        humidity + dew_point + barometric_pressure + pressure_trend + visibility + water_level + level_trend + current_speed + current_direction + current_2_speed + \
        current_2_dir + current_2_depth + current_3_speed + current_3_dir + cdepth3 + wave_height + wave_period + wave_direction + swell_height + swell_period + \
        swell_direction + sea_state + water_temperature + preciptation_type + salinity + ice + spare_2 + fill_bits

    return payl

def make_message(measures, MMSI = 000000000):
    """! Function to complie all the measuremnts and create MEB type sentences to be send
    @param measures List of dict with measurements results
    @param MMSI AIS transreciever ID. Default value is 997090011
    @return Dict of sentences to be send
    """    
    mssg8 = {}
    mmsi = str(MMSI)
    # Binary payload build
    payload = mssg8_bin(measures)

    # 6-bits ASCII codification
    asciipyld = codification(payload)

    # Como el mensaje se debe cortar en dos sentencias, debo definir dos encabezados similares, pero con minimas
    # diferencias
    # Cada Header tiene los siguientes parametros:
    # X -> Representa la cantidad de sentencias a transmitir (1 ~ 9)
    # X -> Representa el orden de la sentencia (1 ~ 9)
    # X -> Identificador sequencial de sentencia (0 ~ 3)
    # X -> Canal AIS para enviar el mensaje
    # XXXXXXXXX -> MMSI de origen, parametro recibido
    # XX -> ID del mensaje
    # X -> Index ID del mensaje (2 ~ 7) (0 y 1 Están reservados)
    # X -> Comportamiento de broadcast
    # XXXXXXXXX -> MMSI de destino
    # X -> Flag de dato binario
    # X -> Status de sentencia (C ó R)
    # print("el largo del payload es: ",len(asciipyld))

    header1 = '!AIMEB,2,1,1,,' + mmsi + ',8,1,0,,1,C,'
    header2 = '!AIMEB,2,2,1,,,,,,,,C,'
    tail1 = ',0'
    tail2 = ',4'
    sentencia1 = header1 + asciipyld[0:39] + tail1
    sentencia2 = header2 + asciipyld[39:] + tail2

    # Checksum creation
    checksum1 = checksum(sentencia1)
    checksum2 = checksum(sentencia2)

    # Last addition
    mssg8[0] = sentencia1 + '*' + checksum1
    mssg8[1] = sentencia2 + '*' + checksum2

    return mssg8


