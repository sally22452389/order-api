import re

def is_valid_name(name: str) -> bool:
    """檢查名字是否只包含英文字母和空格

    :param name: 名字字串

    :return: 符合回傳 True, 否則回傳 False
    """
    return re.match(r"^[A-Za-z\s]+$", name) is not None

def is_capitalize_first_letter(name: str) -> bool:
    """檢查每個單字字首是否為大寫

    :param name: 名字字串

    :return: 所有單字字首都是大寫回傳 True, 否則回傳 False
    """
    return all(word.istitle() for word in name.split())