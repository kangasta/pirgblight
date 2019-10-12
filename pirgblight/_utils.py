def rgb_tuple_to_json(rgb):
    r,g,b = rgb

    return {
        "red": r,
        "green": g,
        "blue": b,
    }

def json_to_rgb_tuple(json_in):
    return (
        json_in.get('red', 0),
        json_in.get('green', 0),
        json_in.get('blue', 0),
    )