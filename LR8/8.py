import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap
import os

data_file_path = "/home/denis/Desktop/get/LR8/data.txt"
settings_file_path = "/home/denis/Desktop/get/LR8/settings.txt"
save_folder = os.path.dirname(data_file_path) 

with open(data_file_path, "r") as f:
    data_array = np.array(f.read().split(), dtype=int)

with open(settings_file_path, "r") as f:
    data_settings = np.array(f.read().split(), dtype=float)


data_time = np.linspace(0, data_settings[0] * 1000, data_array.size)
data_array = data_array * data_settings[1]
charging_time = data_time[np.argmax(data_array)] 
#discharging_time = data_time[1] - charging_time
discharging_time = data_time[-1] - charging_time  

# Построение графика
fig, ax = plt.subplots(figsize=(16, 12), dpi=100)

ax.grid(which='major', color='gray')
ax.minorticks_on()
ax.grid(which='minor', color='gray', linestyle=':')

ax.scatter(data_time[0:data_time.size:5], data_array[0:data_array.size:5], marker='D', c='blue', s=30)
ax.plot(data_time, data_array, label="Зависимость напряжения от времени", color='red', linewidth=1.5)

ax.legend(fontsize=14)

plt.xlim(data_time.min(), data_time.max() + 0.2)
plt.ylim(data_array.min(), data_array.max() + 0.1)

ax.set_title("\n".join(wrap('Процесс зарядки и разрядки конденсатора в RC цепи', 60)))
ax.set_ylabel("напряжение, В")
ax.set_xlabel("время, с")

plt.text(data_time.max() / 2 + 3.33, data_array.max() / 2 + 0.25, f'Время заряда: {charging_time:.2f} сек.', size='large', color='black')
plt.text(data_time.max() / 2 + 3.33, data_array.max() / 2 + 0.35, f'Время разряда: {discharging_time:.2f} сек.', size='large', color='black')

graph_file_path = os.path.join(save_folder, 'graph.svg')
fig.savefig(graph_file_path)

plt.show()
