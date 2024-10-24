import time
import gpiod

# Определяем номера линий GPIO для светодиодов (LED) и AUX
pins_LED = [2, 3, 4, 17, 27, 22, 10, 9]
pins_AUX = [21, 20, 26, 16, 19, 25, 23, 24]
values_zero = [0, 0, 0, 0, 0, 0, 0, 0]
values_ones = [1, 1, 1, 1, 1, 1, 1, 1]

# Имя чипа GPIO, обычно gpiochip0
chip_name = 'gpiochip4'

# Открываем чип GPIO
chip = gpiod.Chip(chip_name)

# Получаем линии для светодиодов (вывод)
lines_LED = chip.get_lines(pins_LED)
lines_LED.request(consumer="my-gpiod-app", type=gpiod.LINE_REQ_DIR_OUT)

# Получаем линии для AUX (ввод с pull-up)
lines_AUX = chip.get_lines(pins_AUX)
lines_AUX.request(consumer="my-gpiod-app", type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

# Устанавливаем начальные значения на светодиоды
lines_LED.set_values(values_ones)

while True:
    # Читаем значения с линий AUX
    aux_values = lines_AUX.get_values()

    # Переключаем состояние светодиодов в зависимости от входов AUX
    led_values = []
    for i in range(8):
        if aux_values[i] == 0:
            led_values.append(values_zero[i])
        else:
            led_values.append(values_ones[i])
    
    # Устанавливаем новые значения для светодиодов
    lines_LED.set_values(led_values)

    time.sleep(0.1)  # Небольшая задержка для снижения нагрузки на процессор
