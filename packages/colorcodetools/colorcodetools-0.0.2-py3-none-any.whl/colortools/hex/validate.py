def is_hex(hexcode: str) -> bool:
    if hexcode.startswith('#'):
        hex_check: str = hexcode.replace('#', '')
    else:
        hex_check: str = hexcode
    if len(hex_check) != 8 and len(hex_check) != 6 and len(hex_check) != 3:
        return False
    for e in list(hex_check):
        if e >= "g":
            return False
    return True