import gpiod
import time

# Настройка GPIO
chip = gpiod.Chip('gpiochip0')
led_pins = [9, 10, 22, 27, 17, 4, 3, 2]
dac_pins = [8, 11, 7, 1, 0, 5, 12, 6]
comp_pin = 14
troyka_pin = 13
maxVolt = 3.3

# Запрашиваем линии DAC как выходы
dac_lines = [chip.get_line(pin) for pin in dac_pins]
for line in dac_lines:
    line.request(consumer='dac_example', type=gpiod.LINE_REQ_DIR_OUT)

# Запрашиваем линии для светодиодов как выходы
led_lines = [chip.get_line(pin) for pin in led_pins]
for line in led_lines:
    line.request(consumer='led_example', type=gpiod.LINE_REQ_DIR_OUT)

# Запрашиваем компаратор как вход
comp_line = chip.get_line(comp_pin)
comp_line.request(consumer='comp_example', type=gpiod.LINE_REQ_DIR_IN)

# Запрашиваем линию для Troyka-модуля как выход
troyka_line = chip.get_line(troyka_pin)
troyka_line.request(consumer='troyka_example', type=gpiod.LINE_REQ_DIR_OUT)
troyka_line.set_value(1)

def tobin(N):
    return [int(bit) for bit in bin(N)[2:].zfill(8)]

def num2dac(value):
    signal = tobin(value)
    for i, line in enumerate(dac_lines):
        line.set_value(signal[i])
    return signal

def adc():
    Volt = 0
    for step in range(8):
        buff = 2 ** (7 - step)
        num2dac(Volt + buff)
        time.sleep(0.005)
        compValue = comp_line.get_value()

        if compValue == 1:
            Volt += buff

        # Обновляем светодиоды
        led_signal = tobin(Volt)
        for i, line in enumerate(led_lines):
            line.set_value(led_signal[i])

    return Volt, (3.3 / 256 * Volt)

try:
    while True:
        print(adc())

finally:
    # Выключаем DAC и светодиоды
    for line in dac_lines + led_lines:
        line.set_value(0)
    troyka_line.set_value(0)
    
    # Освобождаем линии
    for line in dac_lines + led_lines + [comp_line, troyka_line]:
        line.release()
