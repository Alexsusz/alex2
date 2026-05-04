import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import random

# --- 1. Предопределённые цитаты ---
quotes = [
    {"text": "Жизнь — это то, что происходит, пока вы строите планы.", "author": "Джон Леннон", "topic": "Жизнь"},
    {"text": "Лучшее время для посадки дерева — 20 лет назад. Следующее лучше — сегодня.", "author": "Малый хладрон", "topic": "Мотивация"},
    {"text": "Настоящее искусство — это способность видеть магию в обычных вещах.", "author": "Альберт Эйнштейн", "topic": "Искусство"},
    # добавьте свои цитаты сюда
]

# --- 2. Путь к файлу истории в текущей папке ---
history_filename = 'history.json'  # В той же папке, где скрипт

def load_history():
    if os.path.exists(history_filename):
        with open(history_filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history():
    with open(history_filename, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- 3. Создание окна и интерфейса ---
root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("700x600")

# Переменные
all_quotes = quotes.copy()
history = load_history()

# Текущая цитата
current_quote_var = tk.StringVar()

label_quote = tk.Label(root, textvariable=current_quote_var, wraplength=650, font=("Arial", 14), justify='center')
label_quote.pack(pady=10)

# История
tk.Label(root, text="История:", font=("Arial", 12)).pack()
history_box = tk.Listbox(root, height=12, width=80)
history_box.pack(padx=10, pady=5)

# --- 4. Генерация цитаты ---
def generate_quote():
    global all_quotes
    if not all_quotes:
        messagebox.showwarning("Нет цитат", "Нет доступных цитат для выбора.")
        return
    selected = random.choice(all_quotes)
    display_text = f"\"{selected['text']}\" — {selected['author']} (тема: {selected['topic']})"
    current_quote_var.set(display_text)
    # добавляем в историю
    history.append(selected)
    refresh_history()

def refresh_history():
    history_box.delete(0, tk.END)
    for q in reversed(history):
        text = f"\"{q['text']}\" — {q['author']} (тема: {q['topic']})"
        history_box.insert(tk.END, text)

btn_generate = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
btn_generate.pack(pady=10)

# --- 5. Фильтрация ---
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0)
author_filter = tk.Entry(filter_frame)
author_filter.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Фильтр по теме:").grid(row=0, column=2)
topic_filter = tk.Entry(filter_frame)
topic_filter.grid(row=0, column=3, padx=5)

def apply_filter():
    global all_quotes
    auth = author_filter.get().strip().lower()
    top = topic_filter.get().strip().lower()
    all_quotes = [q for q in quotes if
                  (not auth or auth in q['author'].lower()) and
                  (not top or top in q['topic'].lower())]
    if not all_quotes:
        messagebox.showinfo("Нет цитат", "Нет цитат по заданным фильтрам.")
    generate_after_filter()

def generate_after_filter():
    if all_quotes:
        generate_quote()
        refresh_history()

def reset_filter():
    global all_quotes
    all_quotes = quotes.copy()
    generate_after_filter()

btn_filter = tk.Button(filter_frame, text="Применить фильтр", command=apply_filter)
btn_filter.grid(row=0, column=4, padx=5)

btn_reset = tk.Button(filter_frame, text="Сбросить фильтр", command=reset_filter)
btn_reset.grid(row=0, column=5, padx=5)

# --- 6. Добавление новой цитаты ---
def add_quote():
    text = simpledialog.askstring("Добавить цитату", "Введите текст цитаты:")
    if not text or not text.strip():
        messagebox.showwarning("Ошибка", "Текст не может быть пустым.")
        return
    author = simpledialog.askstring("Автор", "Введите автора:")
    if not author or not author.strip():
        messagebox.showwarning("Ошибка", "Автор не может быть пустым.")
        return
    topic = simpledialog.askstring("Тема", "Введите тему:")
    if not topic or not topic.strip():
        messagebox.showwarning("Ошибка", "Тема не может быть пустой.")
        return
    new_entry = {"text": text.strip(), "author": author.strip(), "topic": topic.strip()}
    quotes.append(new_entry)
    messagebox.showinfo("Успех", "Цитата добавлена.")
    global all_quotes
    all_quotes.append(new_entry)

btn_add = tk.Button(root, text="Добавить цитату", command=add_quote)
btn_add.pack(pady=5)

# --- 7. Кнопка "Сохранить" ---
def save_button_callback():
    save_history()
    messagebox.showinfo("Сохранено", f"История успешно сохранена в {history_filename}")

save_btn = tk.Button(root, text="Сохранить", command=save_button_callback)
save_btn.pack(pady=5)

# --- 8. Автоматическое сохранение при закрытии ---
import atexit
def on_close():
    save_history()
    root.destroy()

atexit.register(on_close)
root.protocol("WM_DELETE_WINDOW", on_close)

# --- 9. Первое отображение ---
generate_quote()

# Запуск GUI
root.mainloop()
