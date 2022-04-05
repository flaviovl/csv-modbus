from collections import OrderedDict
from csv import DictReader
from typing import Dict, List, NewType, Tuple, Union

from utils import str_bool


def csv_map_parser(file_path) -> List[OrderedDict[str, str]]:
    raw_map_block: List[OrderedDict[str, str]] = []

    with open(file_path, "r", encoding="utf8") as file_handle:
        csv_reader = DictReader(file_handle, delimiter=",", skipinitialspace=True)

        for line in csv_reader:
            raw_line = OrderedDict()
            for key, value in line.items():
                raw_line[key.lower()] = value
            raw_map_block.append(raw_line)
    return raw_map_block


def modbus_decoder_map(
    raw_map_block, template
) -> List[OrderedDict[str, Union[str, int]]]:
    valid_map_block: List[OrderedDict[str, Union[str, int]]] = []

    for line in raw_map_block:
        line["address"] = int(line["address"])
        line["size"] = int(line["size"])
        line["active"] = str_bool(line["active"])

        if line["active"]:
            valid_line = OrderedDict()
            for column in line:
                if column in template:
                    valid_line[column] = line[column]
            valid_map_block.append(valid_line)

    return valid_map_block


def buid_group_map(map_block, group: str) -> List[OrderedDict[str, Union[str, int]]]:
    group_map: List[OrderedDict[str, Union[str, int]]] = []

    for line in map_block:
        if line["group"] == group:
            # line.__delitem__("group")
            group_map.append(line)

    return group_map


def build_range_map(
    registers: List[Tuple[int, int]], max_reg_request: int = 100
) -> List[Tuple[int, int]]:

    register_ranges: List[Tuple[int, int]] = []
    register_start: int = registers[0][0]
    size_request: int = registers[0][1]
    current: int = registers[0][0]
    register_counter: int = 0

    for addr, size in registers[1:]:
        if addr == current + size and register_counter < max_reg_request:
            size_request += size
            register_counter += 1
            # continue

        else:
            register_ranges.append((register_start, size_request))
            register_start = addr
            size_request = size
            register_counter = 0

        current = addr

    register_ranges.append((register_start, size_request))
    return register_ranges


def print_registers(text, regs):
    print("---" * 30)
    print(text)
    print("")
    print("Tuple(addr_initial, size):", regs)


def main():

    path_file = "maps/full_md30_true.csv"
    # path_file = "maps/med_md30.csv"
    # localhost =

    raw_map_block: List[OrderedDict[str, str]] = []

    register_minutely: List[OrderedDict[str, Union[str, int]]] = []
    register_quartely: List[OrderedDict[str, Union[str, int]]] = []
    register_monthly: List[OrderedDict[str, Union[str, int]]] = []

    address_minutely: List[Tuple[int, int]] = []
    address_quartely: List[Tuple[int, int]] = []
    address_monthly: List[Tuple[int, int]] = []

    template = ["register", "address", "size", "type", "group"]
    group_minutely: str = "minutely"
    group_quartely: str = "quartely"
    group_monthly: str = "monthly"

    max_reg_request: int = 100

    raw_map_block = csv_map_parser(path_file)
    valid_map_block = modbus_decoder_map(raw_map_block, template)

    register_minutely = buid_group_map(valid_map_block, group_minutely)
    register_quartely = buid_group_map(valid_map_block, group_quartely)
    register_monthly = buid_group_map(valid_map_block, group_monthly)

    address_minutely = [(line["address"], line["size"]) for line in register_minutely]  # type: ignore
    address_quartely = [(line["address"], line["size"]) for line in register_quartely]  # type: ignore
    address_monthly = [(line["address"], line["size"]) for line in register_monthly]    # type: ignore

    group_request_minutely = build_range_map(address_minutely, max_reg_request)
    group_request_quartely = build_range_map(address_quartely, max_reg_request)
    group_request_monthly = build_range_map(address_monthly, max_reg_request)

# ==================================================================================================
    print_registers("Group de Request Minutely:", group_request_minutely)
    print_registers("Group de Request Quartely:", group_request_quartely)
    print_registers("Group de Request Monthly:", group_request_monthly)
    print("---" * 30)
# ==================================================================================================


if __name__ == "__main__":
    main()
