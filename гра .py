import tkinter as tk
import random
from functools import partial
from tkinter import messagebox

symbols = ['🍎', '🍌', '🍇', '🍒', '🍓', '🍍', '🥝', '🍑']
symbols *= 2
random.shuffle(symbols)

opened = []
buttons = []
matched = []

def on_click(i):
    global opened
    if i in matched or i in opened:
        return
    buttons[i].config(text=symbols[i], state="disabled")
    opened.append(i)
    if len(opened) == 2:
        first, second = opened
        if symbols[first] == symbols[second]:
            matched.extend(opened)
            opened = []
            if len(matched) == len(symbols):
                messagebox.showinfo("Перемога!", "Ви відкрили всі пари!")
        else:
            root.after(1000, hide_pair)

def hide_pair():
    global opened
    for i in opened:
        buttons[i].config(text="?", state="normal")
    opened = []

root = tk.Tk()
root.title("Memory Game - Гра на пам'ять")

frame = tk.Frame(root)
frame.pack()

for i in range(4):
    for j in range(4):
        index = i * 4 + j
        btn = tk.Button(
            frame,
            text="?",
            width=6,
            height=3,
            command=partial(on_click, index),
            font=("Arial", 20)
        )
        btn.grid(row=i, column=j, padx=5, pady=5)
        buttons.append(btn)

root.mainloop()