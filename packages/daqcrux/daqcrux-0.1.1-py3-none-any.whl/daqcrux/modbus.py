from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse

class modbus:
    """! Clase del canal modbus. Modbus channel class definition.
    """

    def __init__(self, method='rtu', port= '/dev/ttyUSB2', stopbits=1, bytesize=8, parity='N', baudrate=9600, timeout=0.5):
        """! Class constructor
        @param method Communication method. Default is RTU
        @param port Serial port. Default value is USB2.
        @param stopbits Stopbits number. Default value is 1
        @param bytesize Bytesize of communication. Default value is 8
        @param parity Parity of communication. Default value is NONE
        @param baudrate Baudreate of serial communication. Default value is 9600.
        @param timeout Communication timeout. Default value is 0.5 seconds.
        @return An instance modbus class.
        """
        ## Serial port
        self.client = ModbusClient(method, port, stopbits, bytesize, parity, baudrate, timeout)

    def read_input(self, register, nregisters, address):
        """! Function to read sensor's input registers 
        @param register Starting register to read
        @param nregisters Number of register to read
        @param address Sensor's modbus address
        @return Measurement result
        """
        ## Variable donde se almacena la lectura del sensor. Measure
        measure = self.client.read_input_registers(register, nregisters, unit = address)
        return measure.registers
        
    def read_holding_registers(self, register, nregisters, address):
        """! Function to read sensor's holding registers 
        @param register Starting register to read
        @param nregisters Number of register to read
        @param address Sensor's modbus address
        @return Measurement result
        """
        ## Variable donde se almacena la lectura del sensor. Measure
        measure = self.client.read_holding_registers(register, nregisters, unit = address)
        return measure.registers