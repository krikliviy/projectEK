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
import tkinter as tk
from functools import partial

root = tk.Tk()
root.title("Memory Game - Зворотній режим з перезапуском")

timer_label = tk.Label(root, text=f"Час: 30 с", font=("Arial", 14))
timer_label.pack(pady=5)

correct_label = tk.Label(root, text="Правильних пар: 0", font=("Arial", 14))
correct_label.pack(pady=5)

frame = tk.Frame(root)
frame.pack()

buttons = []

for i in range(4):
    for j in range(4):
        index = i * 4 + j
        btn = tk.Button(
            frame, text="?", width=6, height=3,
            font=("Arial", 20),
            command=partial(on_click, index)
        )
        btn.grid(row=i, column=j, padx=5, pady=5)
        buttons.append(btn)

def reset_game():
    global symbols, opened, matched, time_left, game_started, correct_count

    symbols = symbols_base * 2
    random.shuffle(symbols)
    opened.clear()
    matched.clear()
    time_left = 30
    correct_count = 0
    correct_label.config(text="Правильних пар: 0")
    timer_label.config(text=f"Час: {time_left} с")
    game_started = False

    for i, btn in enumerate(buttons):
        btn.config(text=symbols[i], state="disabled", bg="SystemButtonFace")

    root.after(2500, start_game)

reset_button = tk.Button(root, text="Перезапустити гру", font=("Arial", 14), command=reset_game)
reset_button.pack(pady=10)

reset_game()
root.mainloop()
