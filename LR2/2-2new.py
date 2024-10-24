import time
import gpiod

# Определяем номера линий GPIO (пины)
pins = [8, 11, 7, 1, 0, 5, 12, 6]
number = [1, 0, 0, 0, 0, 0, 1, 0]

# Имя чипа GPIO, обычно это gpiochip0
chip_name = 'gpiochip4'

# Открываем чип GPIO
chip = gpiod.Chip(chip_name)

# Получаем линии по номерам GPIO
lines = chip.get_lines(pins)

# Устанавливаем линии на вывод
lines.request(consumer="my-gpiod-app", type=gpiod.LINE_REQ_DIR_OUT)

# Устанавливаем значения на линии
lines.set_values(number)

# Задержка 20 секунд
time.sleep(20)

# Освобождаем линии
lines.release()
