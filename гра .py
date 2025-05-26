import random
from tkinter import messagebox

# Базовий набір символів (фрукти)
symbols_base = ['🍎', '🍌', '🍇', '🍒', '🍓', '🍍', '🥝', '🍑']

# Список відкритих карток
opened = []

# Список карток, які вже співпали
matched = []

# Початковий час для гри (в секундах)
time_left = 30

# Чи запущена гра
game_started = False

# Лічильник правильних пар
correct_count = 0

# Функція, що викликається при натисканні на картку
def on_click(i):
    global opened, game_started, correct_count

    # Ігнорувати натискання, якщо гра ще не почалась або картка вже відкрита/знайдена
    if not game_started or i in matched or i in opened:
        return

    # Показуємо символ картки
    buttons[i].config(text=symbols[i], state="disabled", bg="white")
    opened.append(i)

    # Перевірка, чи відкрито дві картки
    if len(opened) == 2:
        first, second = opened
        if symbols[first] == symbols[second]:
            # Якщо символи співпали — додаємо до знайдених
            matched.extend(opened)
            correct_count += 1
            correct_label.config(text=f"Правильних пар: {correct_count}")
            opened.clear()

            # Якщо всі пари знайдено — перемога
            if len(matched) == len(symbols):
                messagebox.showinfo("Перемога!", "Ви відкрили всі пари!")
                end_game()
        else:
            # Якщо не співпали — сховати пари через 1 секунду
            root.after(1000, hide_pair)

# Функція ховає символи, якщо пари не співпали
def hide_pair():
    global opened
    for i in opened:
        buttons[i].config(text="?", state="normal", bg="SystemButtonFace")
    opened.clear()

# Оновлення таймера
def update_timer():
    global time_left
    if not game_started:
        return

    time_left -= 1
    timer_label.config(text=f"Час: {time_left} с")

    if time_left == 0:
        # Якщо час вийшов — поразка
        messagebox.showinfo("Час вийшов", "Ви програли!")
        reset_game()
    else:
        # Запланувати наступне оновлення таймера через 1 сек
        root.after(1000, update_timer)

# Функція початку гри
def start_game():
    global game_started
    game_started = True

    # Скидаємо вигляд усіх кнопок
    for btn in buttons:
        btn.config(text="?", state="normal", bg="SystemButtonFace")

    update_timer()

# Функція завершення гри
def end_game():
    global game_started
    game_started = False
import tkinter as tk  # Імпортуємо бібліотеку для графічного інтерфейсу
from functools import partial  # Імпортуємо partial для передачі параметрів у функцію при натисканні кнопки

# Створюємо головне вікно гри
root = tk.Tk()
root.title("Memory Game - Зворотній режим з перезапуском")  # Встановлюємо заголовок вікна

# Створюємо текстову мітку для таймера (початкове значення 30 с)
timer_label = tk.Label(root, text=f"Час: 30 с", font=("Arial", 14))
timer_label.pack(pady=5)  # Додаємо відступ зверху і знизу (pady)

# Створюємо мітку, яка показує кількість правильних пар, знайдених гравцем
correct_label = tk.Label(root, text="Правильних пар: 0", font=("Arial", 14))
correct_label.pack(pady=5)

# Створюємо контейнер (рамку), в якому будуть кнопки гри (картки)
frame = tk.Frame(root)
frame.pack()  # Додаємо рамку до головного вікна

# Список для збереження всіх кнопок гри (16 штук для поля 4x4)
buttons = []

# Цикл для створення 4x4 кнопок (всього 16)
for i in range(4):
    for j in range(4):
        index = i * 4 + j  # Обчислюємо унікальний індекс для кожної кнопки
        btn = tk.Button(
            frame, text="?", width=6, height=3,  # Початковий текст "?" і розміри кнопки
            font=("Arial", 20),  # Шрифт і розмір тексту на кнопці
            command=partial(on_click, index)  # Передаємо функцію on_click з параметром index
        )
        btn.grid(row=i, column=j, padx=5, pady=5)  # Розміщуємо кнопку у відповідній комірці сітки
        buttons.append(btn)  # Додаємо кнопку до списку buttons


# Функція для скидання гри та її перезапуску
def reset_game():
    global symbols, opened, matched, time_left, game_started, correct_count

    # Створюємо новий список символів і перемішуємо їх
    symbols = symbols_base * 2  # Повторюємо кожен символ 2 рази, бо кожен має пару
    random.shuffle(symbols)  # Перемішуємо символи випадковим чином

    opened.clear()   # Очищаємо список відкритих карток
    matched.clear()  # Очищаємо список знайдених пар
    time_left = 30   # Повертаємо таймер на 30 секунд
    correct_count = 0  # Обнуляємо рахунок правильних пар

    # Оновлюємо текстові мітки
    correct_label.config(text="Правильних пар: 0")
    timer_label.config(text=f"Час: {time_left} с")

    game_started = False  # Гра ще не почалась

    # Встановлюємо нові значення на кнопки і блокуємо їх на 2.5 секунди
    for i, btn in enumerate(buttons):
        btn.config(text=symbols[i], state="disabled", bg="SystemButtonFace")  # Показуємо картки на старті

    # Через 2.5 секунди запускаємо гру (картки сховаються)
    root.after(2500, start_game)


# Кнопка для ручного перезапуску гри (натискається користувачем)
reset_button = tk.Button(root, text="Перезапустити гру", font=("Arial", 14), command=reset_game)
reset_button.pack(pady=10)  # Відступ зверху і знизу


# Запускаємо перший запуск гри автоматично при відкритті вікна
reset_game()
# Запускаємо основний цикл роботи графічного інтерфейсу
root.mainloop()

