import json
import re


def json_to_dict(filename):
    with open(filename, mode='r') as f:
        data = json.load(f)

    return data


def dict_to_json(d, filename='out.json'):
    with open(filename, mode='w') as f:
        json.dump(d, f)


def is_name_valid(s: str, dots_allowed: int = 1) -> bool:
    try:
        ss = str(s)
        dot_count = ss.count('.')
        valid = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
        if dot_count <= dots_allowed:
            substrs = ss.split('.')
            res = True
            for substr in substrs:
                res = res and (valid.match(substr) is not None)
            return res
        return False
    except:
        return False


def is_type_valid(s: str) -> bool:
    try:
        return str(s) in ('block', 'primitive')
    except:
        return False


def is_number_valid(n: int) -> bool:
    try:
        return int(n) == n and n >= 0
    except:
        return False
