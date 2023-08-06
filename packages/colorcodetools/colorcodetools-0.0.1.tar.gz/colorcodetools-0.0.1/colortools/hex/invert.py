from validate import is_hex
from typing import Union
import json

def invert_hex(hexcode: str, prefix: bool = True) -> Union[bool, str]:
    check_hex: bool = is_hex(hexcode=hexcode)
    if not check_hex:
        return False
    with open('config.json', 'r') as configFile:
        config_data = json.load(configFile)
        configFile.close()
    hexcode: str = hexcode.replace('#', '')
    if prefix:
        inverted_hex: str = '#'
    else:
        inverted_hex: str = ''
    count: int = 0
    for e in list(hexcode):
        if count < 6:
            inverted_hex += config_data[e.lower()]
            count += 1
        else:
            inverted_hex += e
    return inverted_hex