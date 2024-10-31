import gpiod
import time

dac_pins = [8, 11, 7, 1, 0, 5, 12, 6]
comp_pin = 14
troyka_pin = 13
maxVolt = 3.3

# Настраиваем GPIO
with gpiod.Chip('gpiochip0') as chip:
    dac_lines = [chip.get_line(pin) for pin in dac_pins]
    for line in dac_lines:
        line.request(consumer="my_script", type=gpiod.LINE_REQ_DIR_OUT)


# Запрос на доступ к выводам DAC как выходы
dac_lines = [chip.get_line(pin) for pin in dac_pins]
for line in dac_lines:
    line.request(consumer='dac_example', type=gpiod.LINE_REQ_DIR_OUT)

# Настраиваем компаратор как вход
comp_line = chip.get_line(comp_pin)
comp_line.request(consumer='comp_example', type=gpiod.LINE_REQ_DIR_IN)

# Настраиваем трофейный модуль (Troyka) как выход
troyka_line = chip.get_line(troyka_pin)
troyka_line.request(consumer='troyka_example', type=gpiod.LINE_REQ_DIR_OUT)
troyka_line.set_value(1)

levels = 2 ** len(dac_pins)

def tobin(N):
    return [int(bit) for bit in bin(N)[2:].zfill(8)]

def num2dac(value):
    signal = tobin(value)
    for i, line in enumerate(dac_lines):
        line.set_value(signal[i])
    return signal

try:
    while True:
        for value in range(256):
            signal = num2dac(value)
            voltage = value / levels * maxVolt
            time.sleep(0.001)
            compValue = comp_line.get_value()

            if compValue == 1:
                print("Искомое число = {:^3} -> {}, входное напряжение = {:.2f}".format(value, signal, voltage))
                break

finally:
    for line in dac_lines:
        line.set_value(0)
    troyka_line.set_value(0)
    for line in dac_lines + [comp_line, troyka_line]:
        line.release()
