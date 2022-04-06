from collections import OrderedDict
from csv import DictReader
from typing import Dict, List, Tuple, Union

from config import devices_config
from constants import register_map_columns
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


def modbus_decoder_map(raw_map_block, template) -> List[OrderedDict[str, Union[str, int]]]:
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


def build_range_map(registers: List[Tuple[int, int]], max_reg_request=100) -> List[Tuple[int, int]]:

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


def group_reg_request(valid_map_block, group, max_reg_request):
    map_group_full = buid_group_map(valid_map_block, group)
    map_group_request = [(line["address"], line["size"]) for line in map_group_full]
    return build_range_map(map_group_request, max_reg_request)


def run():
    path_file = devices_config["MD30"]["path_file"]
    max_reg_request: int = devices_config["MD30"]["max_reg_request"]

    group_minutely: str = "minutely"
    group_quartely: str = "quartely"
    group_monthly: str = "monthly"

    raw_map_block: List[OrderedDict[str, str]] = csv_map_parser(path_file)
    valid_map_block: List[OrderedDict[str, str | int]] = modbus_decoder_map(raw_map_block, register_map_columns)

    group_request_minutely = group_reg_request(valid_map_block, group_minutely, max_reg_request)
    group_request_quartely = group_reg_request(valid_map_block, group_quartely, max_reg_request)
    group_request_monthly = group_reg_request(valid_map_block, group_monthly, max_reg_request)

    registers: Dict[str, List[Tuple[int, int]]] = {
        "Minutely": group_request_minutely,
        "Quartely": group_request_quartely,
        "Monthly": group_request_monthly,
    }
    return registers
    # return {"Minutely": group_request_minutely, "Quartely": group_request_quartely, "Monthly": group_request_monthly,}
    
# ======================================================================================================================


if __name__ == "__main__":
    run()
