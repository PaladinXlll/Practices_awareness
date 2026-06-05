import tkinter as tk
from tkinter import font as tkfont, simpledialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import os

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

# Переменная для отслеживания полноэкранного режима
is_fullscreen = False

# Словарь для хранения изображений
images = {}

# Данные таблицы (15 строк, 3 столбца)
table_data = [["", "", ""] for _ in range(15)]
table_data[0][0] = "ФИО"

# ==========================================
# КАСТОМНЫЙ ДИАЛОГ ВВОДА
# ==========================================
class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt, initialvalue=""):
        self.prompt = prompt
        self.initialvalue = initialvalue
        self.result = None
        super().__init__(parent, title)
    
    def body(self, master):
        master.configure(bg='#DBC685')
        
        label = tk.Label(master, text=self.prompt, bg='#DBC685', fg='#000000', font=("Advent Pro", 12))
        label.pack(padx=10, pady=5)
        
        self.entry = tk.Entry(master, width=40, bg='#E9DCB0', fg='#000000', 
                               font=("Advent Pro", 12), relief="solid", bd=1)
        self.entry.insert(0, self.initialvalue)
        self.entry.pack(padx=10, pady=5)
        self.entry.select_range(0, tk.END)
        
        return self.entry
    
    def buttonbox(self):
        box = tk.Frame(self, bg='#DBC685')
        box.pack()
        
        ok_btn = tk.Button(box, text="OK", width=10, command=self.ok,
                          bg='#986722', fg='white', font=("Advent Pro", 10, "bold"),
                          relief="flat", activebackground='#7a5518', activeforeground='white')
        ok_btn.pack(side="left", padx=5, pady=10)
        
        cancel_btn = tk.Button(box, text="Отмена", width=10, command=self.cancel,
                               bg='#986722', fg='white', font=("Advent Pro", 10, "bold"),
                               relief="flat", activebackground='#7a5518', activeforeground='white')
        cancel_btn.pack(side="left", padx=5, pady=10)
        
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
    
    def apply(self):
        self.result = self.entry.get()

# ==========================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ТАБЛИЦЕЙ
# ==========================================

def edit_row(row):
    """Редактирование всей строки (первая строка недоступна)"""
    if row == 0:
        return
    
    current_name = table_data[row][0]
    current_info = table_data[row][1]
    
    dialog1 = CustomDialog(root, "Редактирование ФИО", 
                          f"Введите ФИО для строки {row+1}:",
                          current_name)
    new_name = dialog1.result
    
    dialog2 = CustomDialog(root, "Редактирование информации", 
                          f"Введите информацию для строки {row+1}:",
                          current_info)
    new_info = dialog2.result
    
    if new_name is not None:
        table_data[row][0] = new_name
    if new_info is not None:
        table_data[row][1] = new_info
    
    draw_table()

def delete_row(row):
    """Удаление строки (первая строка недоступна)"""
    if row == 0:
        return
    
    if messagebox.askyesno("Подтверждение", f"Удалить строку {row+1}?", 
                           parent=root):
        for col in range(2):
            table_data[row][col] = ""
        draw_table()

def add_row():
    """Добавление новой строки"""
    for i in range(1, len(table_data)):
        if table_data[i][0] == "" and table_data[i][1] == "":
            dialog1 = CustomDialog(root, "Добавление ФИО", 
                                  f"Введите ФИО для строки {i+1}:", "")
            new_name = dialog1.result
            
            dialog2 = CustomDialog(root, "Добавление информации", 
                                  f"Введите информацию для строки {i+1}:", "")
            new_info = dialog2.result
            
            if new_name is not None:
                table_data[i][0] = new_name
            if new_info is not None:
                table_data[i][1] = new_info
            draw_table()
            return
    
    dialog1 = CustomDialog(root, "Добавление ФИО", "Введите ФИО для новой строки:", "")
    new_name = dialog1.result
    
    dialog2 = CustomDialog(root, "Добавление информации", "Введите информацию для новой строки:", "")
    new_info = dialog2.result
    
    if new_name is not None or new_info is not None:
        table_data.append([new_name or "", new_info or "", ""])
        draw_table()

# ==========================================
# ФУНКЦИЯ ПЕРЕКЛЮЧЕНИЯ ПОЛНОЭКРАННОГО РЕЖИМА
# ==========================================
def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)
    root.update_idletasks()
    update_layout()

def on_button_click(event):
    """Обработка кликов по кнопкам (редактировать/удалить)"""
    x = event.x
    y = event.y
    
    width = main_canvas.winfo_width()
    height = main_canvas.winfo_height()
    
    if width <= 1 or height <= 1:
        return
    
    col1_width = width * 0.25
    col2_width = width * 0.70
    col3_width = width * 0.05
    
    rows = len(table_data)
    row_height = height / rows
    
    row = int(y // row_height)
    if row >= rows or row == 0:
        return
    
    col3_start_x = col1_width + col2_width
    col3_center_x = col3_start_x + (col3_width / 2)
    
    if abs(x - (col3_center_x - 15)) < 15:
        edit_row(row)
    elif abs(x - (col3_center_x + 15)) < 15:
        delete_row(row)

def draw_table():
    """Рисует таблицу и кнопки с чёрной рамкой вокруг всей таблицы и подсветкой всех иконок"""
    width = main_canvas.winfo_width()
    height = main_canvas.winfo_height()
    
    if width <= 1 or height <= 1:
        return
    
    main_canvas.delete("all")
    
    # Рисуем фон с закругленными углами
    radius = min(20, width // 10, height // 10)
    main_canvas.create_polygon(
        radius, 0,
        width - radius, 0,
        width, radius,
        width, height - radius,
        width - radius, height,
        radius, height,
        0, height - radius,
        0, radius,
        fill='#E9DCB0',
        outline='',
        smooth=True
    )
    
    col1_width = width * 0.25
    col2_width = width * 0.70
    col3_width = width * 0.05
    
    rows = len(table_data)
    row_height = height / rows
    
    x1 = col1_width
    x2 = col1_width + col2_width
    
    # Рисуем ВНЕШНЮЮ ЧЁРНУЮ РАМКУ вокруг всей таблицы
    main_canvas.create_rectangle(
        0, 0, width, height,
        outline="black", width=2, fill=""
    )
    
    main_canvas.create_line(x1, 0, x1, height, fill="black", width=1)
    main_canvas.create_line(x2, 0, x2, height, fill="black", width=1)
    
    for i in range(rows + 1):
        y = i * row_height
        main_canvas.create_line(0, y, width, y, fill="black", width=1)
    
    for row in range(rows):
        y_center = (row * row_height) + (row_height / 2)
        
        if row == 0:
            font_style = ("Advent Pro", 25, "bold")
        else:
            font_style = ("Advent Pro", 18)
        
        if table_data[row][0]:
            main_canvas.create_text(
                col1_width / 2,
                y_center,
                text=table_data[row][0],
                font=font_style,
                fill="black",
                anchor="center"
            )
        
        if table_data[row][1]:
            main_canvas.create_text(
                col1_width + (col2_width / 2),
                y_center,
                text=table_data[row][1],
                font=font_style,
                fill="black",
                anchor="center"
            )
    
    if not images:
        try:
            edit_img = Image.open("frontend/assets/edit.png")
            edit_img = edit_img.resize((25, 25))
            images["edit"] = ImageTk.PhotoImage(edit_img)
        except:
            images["edit"] = None
        
        try:
            delete_img = Image.open("frontend/assets/delete.png")
            delete_img = delete_img.resize((25, 25))
            images["delete"] = ImageTk.PhotoImage(delete_img)
        except:
            images["delete"] = None
    
    if images["edit"] and images["delete"]:
        col3_center_x = x2 + (col3_width / 2)
        
        for row in range(1, rows):
            y_center = (row * row_height) + (row_height / 2)
            
            # Кнопка редактирования
            edit_btn = main_canvas.create_image(
                col3_center_x - 15, y_center, 
                image=images["edit"], anchor="center"
            )
            
            # Подсветка для кнопки редактирования (маленький квадрат)
            main_canvas.tag_bind(edit_btn, "<Enter>", lambda e, btn=edit_btn, x=col3_center_x - 15, y=y_center: highlight_button(btn, x, y))
            main_canvas.tag_bind(edit_btn, "<Leave>", lambda e, btn=edit_btn: unhighlight_button(btn))
            main_canvas.tag_bind(edit_btn, "<Button-1>", lambda e, r=row: edit_row(r))
            
            # Кнопка удаления
            delete_btn = main_canvas.create_image(
                col3_center_x + 15, y_center, 
                image=images["delete"], anchor="center"
            )
            
            # Подсветка для кнопки удаления (маленький квадрат)
            main_canvas.tag_bind(delete_btn, "<Enter>", lambda e, btn=delete_btn, x=col3_center_x + 15, y=y_center: highlight_button(btn, x, y))
            main_canvas.tag_bind(delete_btn, "<Leave>", lambda e, btn=delete_btn: unhighlight_button(btn))
            main_canvas.tag_bind(delete_btn, "<Button-1>", lambda e, r=row: delete_row(r))

def highlight_button(btn_id, x, y):
    """Подсветка кнопки - маленький квадрат за кнопкой"""
    # Удаляем предыдущую подсветку если есть
    if hasattr(main_canvas, "current_highlight"):
        main_canvas.delete(main_canvas.current_highlight)
    
    # Рисуем маленький квадрат-подсветку за кнопкой (размер под иконку 25x25)
    main_canvas.current_highlight = main_canvas.create_rectangle(
        x - 14, y - 14, x + 14, y + 14,
        fill="#C8B57E", outline=""
    )
    # Опускаем подсветку под кнопку
    main_canvas.tag_lower(main_canvas.current_highlight, btn_id)

def unhighlight_button(btn_id):
    """Убираем подсветку кнопки"""
    if hasattr(main_canvas, "current_highlight"):
        main_canvas.delete(main_canvas.current_highlight)
        main_canvas.current_highlight = None

def update_layout(event=None):
    """Обновляет размеры элементов при изменении окна"""
    width = root.winfo_width()
    height = root.winfo_height()
    
    # Обновляем размер козырька
    canopy.configure(width=width)
    
    # Обновляем размер контейнера между козырьком и линией
    teachers_container.configure(width=width)
    teachers_container.place(x=0, y=99, width=width)
    
    # Обновляем размер полосы
    bar.configure(width=width)
    bar.place(x=0, y=150.5, width=width)
    
    # Обновляем размер основного канваса
    new_width = max(10, width - 40)
    new_height = max(10, height - 187)
    
    main_canvas.configure(width=new_width, height=new_height)
    main_canvas.place(x=20, y=167, width=new_width, height=new_height)
    
    draw_table()

# ==========================================
# КОЗЫРЕК (НОВЫЙ ИЗ CUSTOMTKINTER)
# ==========================================

canopy = ctk.CTkFrame(
    root,
    height=99,
    fg_color="#986722",
    corner_radius=0
)
canopy.pack(fill="x")
canopy.pack_propagate(False)

# ==========================================
# КОНТЕЙНЕР ДЛЯ ЛОГОТИПОВ
# ==========================================

header_frame = ctk.CTkFrame(
    canopy,
    fg_color="transparent"
)
header_frame.pack(fill='both', expand=True)

logo_frame = ctk.CTkFrame(
    header_frame,
    fg_color="transparent"
)
logo_frame.pack(side="left", padx=20, pady=10)

logo1 = ctk.CTkLabel(
    logo_frame,
    text="PRACTICES",
    text_color="white",
    font=("Bayon", 32, "bold")
)
logo1.pack(anchor="w")

logo2 = ctk.CTkLabel(
    logo_frame,
    text="AWARENESS",
    text_color="white",
    font=("Bayon", 32, "bold")
)
logo2.pack(anchor="w", padx=(90, 0))

# ==========================================
# ЛОГОТИП КАРТИНКА
# ==========================================

try:
    logo_path = "frontend/assets/logo.png"
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
        # Подсветка для логотипа
        logo_label.bind("<Enter>", lambda e: logo_label.config(bg='#7a5518'))
        logo_label.bind("<Leave>", lambda e: logo_label.config(bg='#986722'))
except Exception as e:
    print(f"Ошибка загрузки логотипа: {e}")

# ==========================================
# КОНТЕЙНЕР МЕЖДУ КОЗЫРЬКОМ И ЛИНИЕЙ
# ==========================================
teachers_container = tk.Frame(root, bg='#DBC685', height=51.5)
teachers_container.place(x=0, y=99, width=1280)
teachers_container.pack_propagate(False)

teachers_inner = tk.Frame(teachers_container, bg='#DBC685')
teachers_inner.pack(side="left", padx=20)

# Картинка main.png с подсветкой
try:
    icon_path = "frontend/assets/main.png"
    if os.path.exists(icon_path):
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((24, 24))
        main_icon = ImageTk.PhotoImage(icon_image)
        
        icon_label = tk.Label(
            teachers_inner,
            image=main_icon,
            bg='#DBC685',
            bd=0
        )
        icon_label.image = main_icon
        icon_label.pack(side="left", padx=(0, 10))
        # Подсветка для main.png
        icon_label.bind("<Enter>", lambda e: icon_label.config(bg='#C8B57E'))
        icon_label.bind("<Leave>", lambda e: icon_label.config(bg='#DBC685'))
except Exception as e:
    print(f"Ошибка загрузки main.png: {e}")

# Текст "Список преподавателей"
try:
    advent_font = tkfont.Font(family="Advent Pro", size=25, weight="normal")
except:
    advent_font = ("Arial", 20, "normal")

teachers_label = tk.Label(
    teachers_inner,
    text="Список преподавателей",
    fg="#000000",
    bg='#DBC685',
    font=advent_font
)
teachers_label.pack(side="left")

# Кнопка "Добавить" (create.png) с подсветкой
try:
    create_path = "frontend/assets/create.png"
    if os.path.exists(create_path):
        create_image = Image.open(create_path)
        create_image = create_image.resize((39, 39))
        create_icon = ImageTk.PhotoImage(create_image)
        
        create_button = tk.Button(
            teachers_container,
            image=create_icon,
            bg='#DBC685',
            bd=0,
            command=add_row
        )
        create_button.image = create_icon
        create_button.pack(side="right", padx=20)
        # Подсветка для кнопки добавления
        create_button.bind("<Enter>", lambda e: create_button.config(bg='#C8B57E'))
        create_button.bind("<Leave>", lambda e: create_button.config(bg='#DBC685'))
except Exception as e:
    print(f"Ошибка загрузки create.png: {e}")

# ==========================================
# ПОЛОСА НА РАССТОЯНИИ 150.5px ОТ ВЕРХА
# ==========================================
bar = tk.Frame(root, bg='#986722', height=0)
bar.place(x=0, y=150.5, width=1280)
bar.pack_propagate(False)

# ==========================================
# ОСНОВНОЙ КАНВАС С ТАБЛИЦЕЙ
# ==========================================
main_canvas = tk.Canvas(
    root,
    width=1248,
    height=744,
    bg='#E9DCB0',
    highlightthickness=0
)
main_canvas.place(x=20, y=167)

main_canvas.bind("<Button-1>", on_button_click)

# ==========================================
# УПРАВЛЕНИЕ
# ==========================================
def close_window(event):
    root.destroy()

root.bind('<Escape>', close_window)
root.bind('<F11>', toggle_fullscreen)
root.bind('<Configure>', update_layout)

root.after(100, draw_table)
root.after(100, update_layout)

root.mainloop()