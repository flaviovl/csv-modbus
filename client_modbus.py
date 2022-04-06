from constants import parameters
from mapper_csv import main as run
from pymodbus.client.sync import ModbusTcpClient as SyncModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.register_read_message import ReadHoldingRegistersResponse

from config import devices_config


# --------------------------------------------------------------------------------------------------
def read_holding_registers(address, size, client) -> ReadHoldingRegistersResponse | None:

    response: ReadHoldingRegistersResponse
    response = client.read_holding_registers(address, size, unit=1)

    if response.isError():
        print("Error reading holding registers")
        return None
    return response
# --------------------------------------------------------------------------------------------------


def connect_modbus_client(ip_address, port, protocol) -> SyncModbusClient | None:
    
    if protocol == 0:                                 # TCP
        client = SyncModbusClient(ip_address, port)
        client.connect()

    elif protocol == 1:                               # UDP
        client = SyncModbusClient(ip_address, port)
        client.connect()

    else:
        client = None
        print("protocol not implemented")

    return client
# --------------------------------------------------------------------------------------------------


def simple_decoded(payload_decoder, index, size):
    """
        index => Endereço inicial da tabela modbus
        size => Quantos registradores deseja ler
    """
    payload_decoded = {}
    for address in range(index, index + size, 2):
        payload_decoded[f'{address}'] = round(payload_decoder.decode_32bit_float(), 2)

    # print(payload_decoded)
    return payload_decoded
# --------------------------------------------------------------------------------------------------


def main(index, size):
    
    protocol: int = devices_config["MD30"]["protocol"]
    ip_address: str = devices_config["MD30"]["ip_address"]
    port: int = devices_config["MD30"]["port"]
    
    client_mb = connect_modbus_client(ip_address, port, protocol)
    
    response = read_holding_registers(index, size, client_mb)
    
    payload_decoder = BinaryPayloadDecoder.fromRegisters(
        response.registers, byteorder=Endian.Big, wordorder=Endian.Little
    )
    
    # decoded_data = decodec_modbus(payload_decoder)
    decoded_data = simple_decoded(payload_decoder, index, size)

    print(decoded_data)
    measurements = dict(zip(parameters, decoded_data.values()))
    print(f'Measurements: {len(measurements)}')
    
    for param, value in measurements.items():
        print(f'{param}: {value}')    
# --------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    minutely = run()
    index, size = minutely[1]
    print(f"index: {index}, size: {size}")
    
    main(index, size)
