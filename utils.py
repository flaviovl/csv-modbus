def str_bool(str_bool: str) -> bool:

    state = str_bool.strip().lower()
    if state in {"t", "y", "true", "yes", "1"}:
        return True
    elif state in {"f", "n", "false", "no", "0", ""}:
        return False
    else:
        raise ValueError(f"Unsupported: {str_bool}")
