def json_to_dict(filename):
    import json

    with open(filename, mode='r') as f:
        data = json.load(f)

    return data


def dict_to_json(d, filename='out.json'):
    import json

    with open(filename, mode='w') as f:
        json.dump(d, f)


def get_or_re(d, key):
    if key not in d.keys():
        raise RuntimeError(f'Key {key} not found in dictionary.')
    return d[key]

