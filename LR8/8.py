import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap

with open("/home/denis/Desktop/get/LR8/data.txt","r") as f:
    data_array=np.array(f.read().split(), dtype=int) # Чтение данных из файлов data.txt

with open("/home/denis/Desktop/get/LR8/settings.txt","r") as f:
    data_settings=np.array(f.read().split(), dtype=float) # Чтение данных из файлов settings.txt

data_time=np.linspace(0,data_settings[0]*1000,data_array.size) # Перевод номеров отсчётов в секунды

data_array=data_array*data_settings[1] # Перевод показаний АЦП в Вольты

fig,ax = plt.subplots(figsize=(16,12),dpi=100)

ax.grid(which='major',color='gray') # Главная сетка

ax.minorticks_on()
ax.grid(which='minor',color='gray',linestyle=':') # Дополнительная сетка

ax.scatter(data_time[0:data_time.size:15],data_array[0:data_array.size:15],marker='D',c='darkgreen',s=30) # Настройка маркеров

ax.plot(data_time,data_array,label="Зависимость напряжения от времени",color='darkgreen',linewidth=1.5) # Пострение линии графика

ax.legend(fontsize=14) # Создание легенды

plt.xlim(data_time.min(), data_time.max() + 0.2) # Настройка максимума и минимума оси X
plt.ylim(data_array.min(), data_array.max() + 0.1) # Настройка максимума и минимума оси Y

ax.set_title("/n".join(wrap('Процесс зарядки и разрядки конденсатора в RC цепи',60))) # Название графика
ax.set_ylabel("напряжение,В") # Название оси Y
ax.set_xlabel("время,с") # Название оси X

# Вывод текста в области графика
plt.text( data_time.max() / 2 + 3.33, data_array.max()/ 2 + 0.25, 'Время заряда: 13.2756 сек.' , size='large', color='black') 
plt.text(data_time.max() / 2 + 3.33, data_array.max()/ 2 + 0.35, 'Время разряда: 10.7131 cек.' , size='large', color='black')

plt.show() # Отображение графика
fig.savefig('graph.svg') # Сохранение графика в файл в формате .svg