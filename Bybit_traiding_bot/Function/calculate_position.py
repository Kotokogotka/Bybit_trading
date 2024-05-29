def calculate_long_position(D, PE, PL, R):
    SL = PE - PL  # длина стопа
    V = D / SL / 100
    Result = V * R
    return Result


def calculate_short_position(D, PE, PL, R):
    SL = PL - PE  # длина стопа
    V = D / SL / 100
    Result = V * R
    return Result


def calculate_position_size(position_type, D, PE, PL, R):
    if position_type == 'short':
        return calculate_short_position(D, PE, PL, R)
    else:
        return calculate_long_position(D, PE, PL, R)