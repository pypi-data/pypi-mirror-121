from colorcodetools.cymk.validate import is_cymk, is_single_cymk
from typing import Union
from colorcodetools.cymk.config import config

def invert_cymk(cymk: str) -> Union[bool, str]:
    check_hex: bool = is_cymk(cymk=cymk)
    if not check_hex:
        return False
    config_data = config()
    inverted_cymk: str = ''
    cymk = cymk.split("/")
    count: int = 0
    for e in list(cymk):
        if count != len(list(cymk)) - 1:
            inverted_cymk += config_data[e.lower()] + "/"
            count += 1
        else:
            inverted_cymk += config_data[e.lower()]
    return inverted_cymk

def invert_single_cymk(cymk: int) -> Union[bool, int]:
    check_cymk: bool = is_single_cymk(cymk)
    if not check_cymk:
        return False
    config_data = config()
    inverted_cymk: int = config_data[str(cymk).strip()]
    return inverted_cymk