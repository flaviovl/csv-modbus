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

def main():

    path_file = "maps/full_md30_true.csv"
    # path_file = "maps/med_md30.csv"
    # localhost =

    raw_map_block: List[OrderedDict[str, str]] = []
    raw_map_block = csv_map_parser(path_file)


# ====================================================================================================


if __name__ == "__main__":
    main()
