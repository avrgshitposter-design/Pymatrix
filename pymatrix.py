import os
import random
import time
import shutil
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

# Настройки
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()"
width, height = shutil.get_terminal_size()
columns = width
min_speed = 0.03
max_speed = 0.15
max_trail = 8  # длина хвоста

# Для каждой колонки создаем:
# - текущее положение
# - скорость
# - список символов в хвосте
drops = []
for _ in range(columns):
    drops.append({
        'pos': random.randint(-height, 0),
        'speed': random.uniform(min_speed, max_speed),
        'trail': []
    })

try:
    while True:
        for i, drop in enumerate(drops):
            # Добавляем новый символ в колонку
            char = random.choice(chars)
            drop['trail'].append((drop['pos'], char))

            # Ограничиваем длину хвоста
            if len(drop['trail']) > max_trail:
                drop['trail'] = drop['trail'][-max_trail:]

            # Отрисовываем хвост
            for idx, (y, c) in enumerate(drop['trail']):
                if 0 <= y < height:
                    fade = idx / max_trail
                    if fade < 0.3:
                        color = Fore.RED + Style.BRIGHT
                    elif fade < 0.7:
                        color = Fore.RED
                    else:
                        color = Fore.RED + Style.DIM
                    print(f"\033[{y+1};{i+1}H{color}{c}")

            # Увеличиваем позицию
            drop['pos'] += 1

            # Случайный сброс колонки для динамики
            if drop['pos'] > height + random.randint(0, 20):
                drop['pos'] = random.randint(-height//2, 0)
                drop['trail'] = []
                drop['speed'] = random.uniform(min_speed, max_speed)

        time.sleep(0.03)  # глобальная пауза между кадрами

except KeyboardInterrupt:
    print(Style.RESET_ALL)
    print("\nCMatrix остановлен.")
