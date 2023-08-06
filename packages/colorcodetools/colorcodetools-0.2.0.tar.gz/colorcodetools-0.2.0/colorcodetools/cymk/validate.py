def is_cymk(cymk: str) -> bool:
    try:
        cymk_split = cymk.split("/")
    except:
        return False
    for e in cymk_split:
        try:
            int(e)
        except:
            return False
        if len(e) > 3:
            return False
        if int(e) > 100 or int(e) < 0:
            return False
    return True

def is_single_cymk(cymk: int) -> bool:
    if 100 >= cymk >= 0:
        return True
    else:
        return False
