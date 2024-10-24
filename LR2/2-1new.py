import time
import gpiod

# Указываем имя чипа и линии
chip = gpiod.Chip('gpiochip4')

# Определяем линии для пинов
pins = [2, 3, 4, 17, 27, 22, 10, 9]
lines = chip.get_lines(pins)

# Устанавливаем режим вывода для пинов
lines.request(consumer="my_script", type=gpiod.LINE_REQ_DIR_OUT)

# Определяем значения
values_zeros = [0] * len(pins)
values_ones = [1] * len(pins)

# Инициализируем пины в нулевое состояние
lines.set_values(values_zeros)

step = 0

while step < 3:
    i = 0
    lines.set_values([1 if idx == i else 0 for idx in range(len(pins))])
    
    i = 0
    while i < 7:
        values = [0] * len(pins)
        values[i] = 1
        lines.set_values(values)
        time.sleep(0.1)

        values[i] = 0
        values[i + 1] = 1
        lines.set_values(values)
        time.sleep(0.1)

        i += 1
        time.sleep(0.1)

    # Отключаем последний пин
    values = [0] * len(pins)
    lines.set_values(values)
    step += 1

# Возвращаем все пины в нулевое состояние
lines.set_values(values_zeros)
chip.close()
