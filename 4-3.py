import gpiod
import time

# Установим пин для использования
chip = gpiod.Chip('gpiochip0')
line_24 = chip.get_line(24)
line_9 = chip.get_line(9)

# Конфигурируем линии как выходы
config = gpiod.LineRequest()
config.consumer = 'pwm_example'
config.request_type = gpiod.LINE_REQ_DIR_OUT

line_24.request(config)
line_9.request(config)

def set_pwm_duty_cycle(line, duty_cycle, frequency=100):
    period = 1 / frequency
    active_time = duty_cycle / 100 * period
    inactive_time = period - active_time

    line.set_value(1)
    time.sleep(active_time)
    line.set_value(0)
    time.sleep(inactive_time)

try:
    print("Введите заполнение ШИМ (%):")

    while True:
        a = int(input())
        duty_cycle = int(a)

        # Включение ШИМ на обе линии
        set_pwm_duty_cycle(line_9, duty_cycle)
        set_pwm_duty_cycle(line_24, duty_cycle)

finally:
    # Очищаем линии
    line_24.set_value(0)
    line_9.set_value(0)
    line_24.release()
    line_9.release()
