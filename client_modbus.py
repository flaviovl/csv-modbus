from mapper_csv import main as run
from pymodbus.client.sync import ModbusTcpClient as SyncModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.register_read_message import ReadHoldingRegistersResponse


def read_holding_registers(
    address, size, client
) -> ReadHoldingRegistersResponse | None:

    response: ReadHoldingRegistersResponse
    response = client.read_holding_registers(address, size, unit=1)

    if response.isError():
        print("Error reading holding registers")
        return None
    return response


def modbus_client(ip, port):
    client = SyncModbusClient(ip, port)
    client.connect()

    return client


def decodec_modbus(decoder):
    return {
        "frequency_a": decoder.decode_32bit_float(),
        "UrmsA": decoder.decode_32bit_float(),
        "UrmsB": decoder.decode_32bit_float(),
        "UrmsC": decoder.decode_32bit_float(),
        "IrmsA": decoder.decode_32bit_float(),
        "IrmsB": decoder.decode_32bit_float(),
        "IrmsC": decoder.decode_32bit_float(),
        "active_power_a": decoder.decode_32bit_float(),
        "active_power_b": decoder.decode_32bit_float(),
        "active_power_c": decoder.decode_32bit_float(),
        "total_active_power": decoder.decode_32bit_float(),
        "reactive_power_a": decoder.decode_32bit_float(),
        "reactive_power_b": decoder.decode_32bit_float(),
        "reactive_power_c": decoder.decode_32bit_float(),
        "total_reactive_power": decoder.decode_32bit_float(),
        "apparent_power_a": decoder.decode_32bit_float(),
        "apparent_power_b": decoder.decode_32bit_float(),
        "apparent_power_c": decoder.decode_32bit_float(),
        "total_apparent_power": decoder.decode_32bit_float(),
        "power_factor_a": decoder.decode_32bit_float(),
        "power_factor_b": decoder.decode_32bit_float(),
        "power_factor_c": decoder.decode_32bit_float(),
        "total_power_factor": decoder.decode_32bit_float(),
        "dht_voltage_a": decoder.decode_32bit_float(),
        "dht_voltage_b": decoder.decode_32bit_float(),
        "dht_voltage_c": decoder.decode_32bit_float(),
        "dht_current_a": decoder.decode_32bit_float(),
        "dht_current_b": decoder.decode_32bit_float(),
        "dht_current_c": decoder.decode_32bit_float(),
    }


def main(ip, port, index, size):

    client_mb = modbus_client(ip, port)
    response = read_holding_registers(index, size, client_mb)
    payload_decoder = BinaryPayloadDecoder.fromRegisters(
        response.registers, byteorder=Endian.Big, wordorder=Endian.Little
    )
    
    decoded_data = decodec_modbus(payload_decoder)
    # decoder = BinaryModbusDecoder.fromRegisters(response.registers)

    # for name, value in iteritems(decoded_data):
    #     print("%s\t" % name, value)


if __name__ == "__main__":
    ip: str = "164.41.20.228"
    port: int = 1001

    minutely = run()
    index, size = minutely[1]
    print(f"index: {index}, size: {size}")
    
    main(ip, port, index, size)
