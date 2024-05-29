import re


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
    return calculate_long_position(D, PE, PL, R)


def process_message(message):
    sections = {
        'position_type': [],
        'entry': [],
        'take_profit': [],
        'stop_loss': [],
        'risk_percent': []
    }

    current_section = None

    lines = message.split('\n')
    for line in lines:
        line = line.strip()  # Удаляем лишние пробелы в начале и в конце строки
        if line.lower().startswith('position type:'):
            position_type = line.split(':')[1].strip().lower()
            if position_type in ['long', 'short']:
                sections['position_type'].append(position_type)
        elif 'entry' in line.lower():
            current_section = 'entry'
        elif 'take - profit' in line.lower():
            current_section = 'take_profit'
        elif 'stop loss' in line.lower():
            current_section = 'stop_loss'
        elif 'risk -' in line.lower():
            current_section = 'risk_percent'

        if current_section and '✔' not in line:
            # Ищем числа в строке и добавляем их в соответствующий раздел
            numbers = re.findall(r'\d+\.?\d*', line)  # Учитываем десятичные числа
            sections[current_section].extend(numbers)

    for section_name, section_data in sections.items():
        file_name = f'{section_name}.txt'
        with open(file_name, 'w') as file:
            for item in section_data:
                file.write(item + '\n')

