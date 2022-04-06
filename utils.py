def str_bool(str_bool: str) -> bool:

    state = str_bool.strip().lower()
    if state in {"t", "y", "true", "yes", "1"}:
        return True
    elif state in {"f", "n", "false", "no", "0", ""}:
        return False
    else:
        raise ValueError(f"Unsupported: {str_bool}")

def type_size(str_type: str) -> int:

    if str_type in {"int8", "u8", "s8", "uint8"}:
        return 1
    elif str_type in {"short", "int16", "uint16", "u16", "s16"}:
        return 2
    elif str_type in {"float", "int32", "uint32", "u32", "s32", "f32"}:
        return 4
    elif str_type in {"int64", "uint64"}:
        return 8
    else:
        raise ValueError(f"Unsupported type: {str_type}")

def byte_order(str_byte_order: str) -> None:
    print("byte_order")
