import os
import sys

# ==========================================
# ПУТИ ПРОЕКТА
# ==========================================

# Корень проекта (git/)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Добавляем корень проекта для импорта backend
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

# Папка frontend/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Папка frontend/assets/
ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")

# ==========================================
# ИМПОРТЫ
# ==========================================

import tkinter as tk
from tkinter import font as tkfont, simpledialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import threading

# Backend
from backend.db_teachers import (
    get_teachers,
    add_teacher,
    update_teacher,
    delete_teacher
)

from backend.db_teachers_event import get_teacher_events


# ==========================================
# ТЕМА ДЛЯ CUSTOMTKINTER
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ==========================================
# ГЛАВНОЕ ОКНО
# ==========================================

root = tk.Tk()
root.title("PRACTICES AWARENESS")
root.geometry("1280x910")
root.configure(bg='#DBC685')

is_fullscreen = False
images = {}
table_data = [["", "", ""] for _ in range(15)]
table_data[0][0] = "ФИО"

# Для хранения полей ввода
edit_entries = {}
editing_row = None


import subprocess

def open_main(event=None):
    root.destroy()

    subprocess.Popen([
        sys.executable,
        os.path.join(PROJECT_DIR, "frontend", "main_2.0.py")
    ])


def load_teachers_from_db():
    try:
        teachers = get_teachers()

        def update_ui():
            global table_data, editing_row, edit_entries

            # если сейчас идёт редактирование — закрываем его
            for row in list(edit_entries.keys()):
                try:
                    edit_entries[row]['fio'].destroy()
                    edit_entries[row]['practice'].destroy()
                except:
                    pass

            edit_entries.clear()
            editing_row = None

            # пересобираем таблицу заново (БД = источник истины)
            new_table = [["ФИО", "Практики", ""]]

            for teacher in teachers:
                fio = f"{teacher['surname']} {teacher['name']} {teacher['patronymic']}"

                new_table.append([
                    fio,
                    "",
                    teacher["teacher_id"]
                ])

            table_data = new_table

            draw_table()

        # обновление UI в главном потоке Tkinter
        root.after(0, update_ui)

    except Exception as e:
        print("Ошибка загрузки:", e)



def add_teacher_dialog(event=None):
    fio = simpledialog.askstring(
        "Добавить преподавателя",
        "Введите ФИО:\nФамилия Имя Отчество"
    )

    if not fio:
        return

    parts = fio.strip().split()

    if len(parts) < 3:
        messagebox.showerror(
            "Ошибка",
            "Введите ФИО полностью"
        )
        return

    surname = parts[0]
    name = parts[1]
    patronymic = " ".join(parts[2:])

    result = add_teacher(
        surname,
        name,
        patronymic
    )

    if result:
        threading.Thread(
            target=load_teachers_from_db,
            daemon=True
        ).start()

        messagebox.showinfo(
            "Успех",
            "Преподаватель добавлен"
        )
    else:
        messagebox.showerror(
            "Ошибка",
            "Не удалось добавить преподавателя"
        )








HOVER_COLOR = "#B8A87C"
HOVER_SIZE = 14

# ==========================================
# ФУНКЦИИ ДЛЯ ПОДСВЕТКИ
# ==========================================

def on_enter_button_widget(widget, original_bg):
    """Подсветка для обычных tk виджетов"""
    widget.config(bg=HOVER_COLOR)

def on_leave_button_widget(widget, original_bg):
    """Убирает подсветку с обычных tk виджетов"""
    widget.config(bg=original_bg)

# Глобальный словарь для хранения подсветок на Canvas
current_hover_rect = None

def on_enter_canvas_button(event, btn_id, x, y):
    """Подсветка для кнопок на Canvas"""
    global current_hover_rect
    
    # Удаляем старую подсветку
    if current_hover_rect:
        try:
            main_canvas.delete(current_hover_rect)
        except:
            pass
    
    # Создаём новую подсветку
    current_hover_rect = main_canvas.create_rectangle(
        x - HOVER_SIZE, y - HOVER_SIZE, x + HOVER_SIZE, y + HOVER_SIZE,
        fill=HOVER_COLOR, outline=""
    )
    main_canvas.tag_lower(current_hover_rect, btn_id)

def on_leave_canvas_button(event):
    """Убирает подсветку с кнопок на Canvas"""
    global current_hover_rect
    if current_hover_rect:
        try:
            main_canvas.delete(current_hover_rect)
        except:
            pass
        current_hover_rect = None

# ==========================================
# ФУНКЦИИ ТАБЛИЦЫ
# ==========================================

def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)

def draw_checkmark(x, y, size=18):
    """Рисует зелёную галочку"""
    return main_canvas.create_line(
        x - size/2, y,
        x - size/4, y + size/3,
        x + size/2, y - size/3,
        fill="#2E7D32", width=3, capstyle="round", joinstyle="round"
    )

def save_edit(row):
    global editing_row, current_hover_rect

    if current_hover_rect:
        try:
            main_canvas.delete(current_hover_rect)
        except:
            pass
        current_hover_rect = None

    if row in edit_entries:

        fio = edit_entries[row]['fio'].get().strip()
        practice = edit_entries[row]['practice'].get().strip()

        teacher_id = table_data[row][2]

        parts = fio.split()

        if len(parts) < 3:
            messagebox.showerror(
                "Ошибка",
                "Введите ФИО полностью:\nФамилия Имя Отчество"
            )
            return

        surname = parts[0]
        name = parts[1]
        patronymic = " ".join(parts[2:])

        success = update_teacher(
            int(teacher_id),
            surname,
            name,
            patronymic
        )

        if not success:
            messagebox.showerror(
                "Ошибка",
                "Не удалось сохранить изменения"
            )
            return

        table_data[row][0] = fio
        table_data[row][1] = practice

        edit_entries[row]['fio'].destroy()
        edit_entries[row]['practice'].destroy()

        del edit_entries[row]

        editing_row = None

        threading.Thread(
    target=load_teachers_from_db,
    daemon=True
    ).start()

        print("Изменения сохранены")

def clear_row(row):
    global editing_row, current_hover_rect

    if current_hover_rect:
        try:
            main_canvas.delete(current_hover_rect)
        except:
            pass
        current_hover_rect = None

    # если редактируем строку — закрываем редактор
    if row in edit_entries:
        edit_entries[row]['fio'].destroy()
        edit_entries[row]['practice'].destroy()
        del edit_entries[row]
        editing_row = None

    teacher_id = table_data[row][2]

    if teacher_id:
        delete_teacher(int(teacher_id))

    # 🔥 ВАЖНО: перезагружаем данные из БД
    threading.Thread(
        target=load_teachers_from_db,
        daemon=True
    ).start()

def start_edit(row):
    """Начинает редактирование"""
    global editing_row, current_hover_rect
    
    # Убираем подсветку
    if current_hover_rect:
        try:
            main_canvas.delete(current_hover_rect)
        except:
            pass
        current_hover_rect = None
    
    # Если уже редактируем другую строку, сохраняем её
    if editing_row is not None and editing_row != row:
        save_edit(editing_row)
    
    # Если уже редактируем эту строку, выходим
    if editing_row == row:
        return
    
    editing_row = row
    
    # Получаем координаты
    width = main_canvas.winfo_width()
    height = main_canvas.winfo_height()
    
    if width <= 1 or height <= 1:
        return
    
    col1_width = width * 0.25
    col2_width = width * 0.70
    rows = len(table_data)
    row_height = height / rows
    
    y_center = (row * row_height) + (row_height / 2)
    
    # Поле для ФИО
    entry_fio = tk.Entry(main_canvas, bg='#E9DCB0', fg='black', 
                          font=("Advent Pro", 16), relief="solid", bd=1)
    entry_fio.insert(0, table_data[row][0])
    entry_fio.place(x=5, y=y_center - row_height/2 + 5,
                    width=col1_width - 10, height=row_height - 10)
    
    # Поле для практики
    entry_practice = tk.Entry(main_canvas, bg='#E9DCB0', fg='black',
                               font=("Advent Pro", 16), relief="solid", bd=1)
    entry_practice.insert(0, table_data[row][1])
    entry_practice.place(x=col1_width + 5, y=y_center - row_height/2 + 5,
                         width=col2_width - 10, height=row_height - 10)
    
    edit_entries[row] = {
        'fio': entry_fio,
        'practice': entry_practice
    }
    
    # Обновляем кнопки
    update_buttons()

def update_table_display():
    """Обновляет только текст в таблице"""
    width = main_canvas.winfo_width()
    height = main_canvas.winfo_height()
    
    if width <= 1 or height <= 1:
        return
    
    col1_width = width * 0.25
    col2_width = width * 0.70
    rows = len(table_data)
    row_height = height / rows
    
    # Удаляем только текстовые элементы
    for item in main_canvas.find_withtag("text_item"):
        main_canvas.delete(item)
    
    # Рисуем текст заново
    for row in range(rows):
        y_center = (row * row_height) + (row_height / 2)
        
        # Пропускаем строку, которая редактируется
        if row == editing_row:
            continue
        
        if row == 0:
            font_style = ("Advent Pro", 25, "bold")
        else:
            font_style = ("Advent Pro", 18)
        
        if table_data[row][0]:
            main_canvas.create_text(
                col1_width / 2, y_center,
                text=table_data[row][0],
                font=font_style, fill="black", anchor="center",
                tags="text_item"
            )
        
        if table_data[row][1]:
            main_canvas.create_text(
                col1_width + (col2_width / 2), y_center,
                text=table_data[row][1],
                font=font_style, fill="black", anchor="center",
                tags="text_item"
            )

def update_buttons():
    """Обновляет только кнопки в таблице"""
    width = main_canvas.winfo_width()
    height = main_canvas.winfo_height()
    
    if width <= 1 or height <= 1:
        return
    
    col1_width = width * 0.25
    col2_width = width * 0.70
    col3_width = width * 0.05
    rows = len(table_data)
    row_height = height / rows
    
    x2 = col1_width + col2_width
    col3_center_x = x2 + (col3_width / 2)
    
    # Удаляем старые кнопки
    for item in main_canvas.find_withtag("button_item"):
        main_canvas.delete(item)
    
    # Рисуем новые кнопки
    for row in range(1, rows):
        y_center = (row * row_height) + (row_height / 2)
        
        # ЧЁРНЫЙ КРЕСТИК
        if images.get("delete"):
            delete_btn = main_canvas.create_image(
                col3_center_x + 15, y_center,
                image=images["delete"], anchor="center",
                tags="button_item"
            )
            main_canvas.tag_bind(delete_btn, "<Button-1>", lambda e, r=row: clear_row(r))
            main_canvas.tag_bind(delete_btn, "<Enter>", 
                lambda e, btn=delete_btn, x=col3_center_x + 15, y=y_center: on_enter_canvas_button(e, btn, x, y))
            main_canvas.tag_bind(delete_btn, "<Leave>", on_leave_canvas_button)
        
        # КАРАНДАШ или ГАЛОЧКА
        if row == editing_row:
            save_btn = draw_checkmark(col3_center_x - 15, y_center, 18)
            main_canvas.addtag_withtag("button_item", save_btn)
            main_canvas.tag_bind(save_btn, "<Button-1>", lambda e, r=row: save_edit(r))
            main_canvas.tag_bind(save_btn, "<Enter>", 
                lambda e, btn=save_btn, x=col3_center_x - 15, y=y_center: on_enter_canvas_button(e, btn, x, y))
            main_canvas.tag_bind(save_btn, "<Leave>", on_leave_canvas_button)
        else:
            if images.get("edit"):
                edit_btn = main_canvas.create_image(
                    col3_center_x - 15, y_center, 
                    image=images["edit"], anchor="center",
                    tags="button_item"
                )
                main_canvas.tag_bind(edit_btn, "<Button-1>", lambda e, r=row: start_edit(r))
                main_canvas.tag_bind(edit_btn, "<Enter>", 
                    lambda e, btn=edit_btn, x=col3_center_x - 15, y=y_center: on_enter_canvas_button(e, btn, x, y))
                main_canvas.tag_bind(edit_btn, "<Leave>", on_leave_canvas_button)

def draw_table():
    """Рисует таблицу (один раз)"""
    width = main_canvas.winfo_width()
    height = main_canvas.winfo_height()
    
    if width <= 1 or height <= 1:
        root.after(50, draw_table)
        return
    
    main_canvas.delete("all")
    
    # Фон
    radius = min(20, width // 10, height // 10)
    main_canvas.create_polygon(
        radius, 0, width - radius, 0, width, radius,
        width, height - radius, width - radius, height,
        radius, height, 0, height - radius, 0, radius,
        fill='#E9DCB0', outline='', smooth=True
    )
    
    col1_width = width * 0.25
    col2_width = width * 0.70
    rows = len(table_data)
    row_height = height / rows
    
    x1 = col1_width
    x2 = col1_width + col2_width
    
    # Рамки
    main_canvas.create_rectangle(0, 0, width, height, outline="black", width=2)
    main_canvas.create_line(x1, 0, x1, height, fill="black", width=1)
    main_canvas.create_line(x2, 0, x2, height, fill="black", width=1)
    
    for i in range(rows + 1):
        y = i * row_height
        main_canvas.create_line(0, y, width, y, fill="black", width=1)
    
    update_table_display()
    update_buttons()

def update_layout(event=None):
    """Обновление размера окна"""
    width = root.winfo_width()
    height = root.winfo_height()
    
    canopy.configure(width=width)
    teachers_container.configure(width=width)
    teachers_container.place(x=0, y=99, width=width)
    bar.configure(width=width)
    bar.place(x=0, y=150.5, width=width)
    
    new_width = max(10, width - 40)
    new_height = max(10, height - 187)
    
    main_canvas.configure(width=new_width, height=new_height)
    main_canvas.place(x=20, y=167, width=new_width, height=new_height)
    
    draw_table()

# ==========================================
# ЗАГРУЗКА КАРТИНОК
# ==========================================

try:
    edit_img = Image.open(os.path.join(ASSETS_DIR, "edit.png"))
    edit_img = edit_img.resize((25, 25))
    images["edit"] = ImageTk.PhotoImage(edit_img)
except:
    pass

try:
    delete_img = Image.open(os.path.join(ASSETS_DIR, "delete.png"))
    delete_img = delete_img.resize((25, 25))
    images["delete"] = ImageTk.PhotoImage(delete_img)
except:
    # Создаём чёрный крестик если нет картинки
    from PIL import ImageDraw
    img = Image.new('RGBA', (25, 25), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.line([(5, 5), (20, 20)], fill='black', width=3)
    draw.line([(20, 5), (5, 20)], fill='black', width=3)
    images["delete"] = ImageTk.PhotoImage(img)

# ==========================================
# ИНТЕРФЕЙС
# ==========================================

canopy = ctk.CTkFrame(root, height=99, fg_color="#986722", corner_radius=0)
canopy.pack(fill="x")
canopy.pack_propagate(False)

header_frame = ctk.CTkFrame(canopy, fg_color="transparent")
header_frame.pack(fill='both', expand=True)

logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
logo_frame.pack(side="left", padx=20, pady=10)

logo1 = ctk.CTkLabel(logo_frame, text="PRACTICES", text_color="white", font=("Bayon", 32, "bold"))
logo1.pack(anchor="w")

logo2 = ctk.CTkLabel(logo_frame, text="AWARENESS", text_color="white", font=("Bayon", 32, "bold"))
logo2.pack(anchor="w", padx=(90, 0))

# Логотип
try:
    logo_path = os.path.join(ASSETS_DIR, "logo.png")

    if os.path.exists(logo_path):
        image = Image.open(logo_path)
        image = image.resize((145, 145))

        logo_img = ImageTk.PhotoImage(image)

        logo_label = tk.Label(
            header_frame,
            image=logo_img,
            bg="#986722",
            bd=0
        )

        logo_label.image = logo_img
        logo_label.pack(side="right", padx=20, pady=10)

        logo_label.bind(
            "<Enter>",
            lambda e: on_enter_button_widget(logo_label, "#986722")
        )

        logo_label.bind(
            "<Leave>",
            lambda e: on_leave_button_widget(logo_label, "#986722")
        )

except Exception as e:
    print("Ошибка загрузки logo.png:", e)

# Контейнер с надписью
teachers_container = tk.Frame(root, bg='#DBC685', height=51.5)
teachers_container.place(x=0, y=99, width=1280)
teachers_container.pack_propagate(False)

teachers_inner = tk.Frame(teachers_container, bg='#DBC685')
teachers_inner.pack(side="left", padx=20)

# Иконка
try:
    icon_path = os.path.join(ASSETS_DIR, "main.png")
    if os.path.exists(icon_path):
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((24, 24))
        main_icon = ImageTk.PhotoImage(icon_image)
        icon_label = tk.Label(teachers_inner, image=main_icon, bg='#DBC685', bd=0)
        icon_label.image = main_icon
        icon_label.pack(side="left", padx=(0, 10))
        icon_label.bind("<Button-1>", open_main)

        # Подсветка для иконки
        icon_label.bind("<Enter>", lambda e: on_enter_button_widget(icon_label, "#DBC685"))
        icon_label.bind("<Leave>", lambda e: on_leave_button_widget(icon_label, "#DBC685"))
except:
    pass

# Текст
teachers_label = tk.Label(
    teachers_inner, text="Список преподавателей",
    fg="#000000", bg='#DBC685', font=("Advent Pro", 25)
)
teachers_label.pack(side="left")

# Кнопка добавления
try:
    create_path = os.path.join(ASSETS_DIR, "create.png")

    create_image = Image.open(create_path)
    create_image = create_image.resize((39, 39))

    create_icon = ImageTk.PhotoImage(create_image)

    create_button = tk.Label(
        teachers_container,
        image=create_icon,
        bg='#DBC685',
        bd=0
    )

    create_button.image = create_icon
    create_button.pack(side="right", padx=20)

    create_button.bind(
    "<Button-1>",
    add_teacher_dialog
    )

    create_button.bind(
        "<Enter>",
        lambda e: on_enter_button_widget(create_button, "#DBC685")
    )

    create_button.bind(
        "<Leave>",
        lambda e: on_leave_button_widget(create_button, "#DBC685")
    )

except Exception as e:
    print("Ошибка загрузки create.png:", e)

    
# Полоса
bar = tk.Frame(root, bg='#986722', height=0)
bar.place(x=0, y=150.5, width=1280)
bar.pack_propagate(False)

# Канвас
main_canvas = tk.Canvas(root, width=1248, height=744, bg='#E9DCB0', highlightthickness=0)
main_canvas.place(x=20, y=167)

# ==========================================
# ЗАПУСК
# ==========================================

def close_window(event):
    root.destroy()

root.bind('<Escape>', close_window)
root.bind('<F11>', toggle_fullscreen)
root.bind('<Configure>', update_layout)

root.after(100, draw_table)

threading.Thread(
    target=load_teachers_from_db,
    daemon=True
).start()

root.mainloop()