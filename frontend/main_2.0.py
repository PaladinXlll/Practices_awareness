import customtkinter as ctk
import tkinter as tk
from tkinter import font as tkfont, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw
import os
import copy

# ==========================================
# ПОИСК ШРИФТА ADVENT PRO
# ==========================================

def find_advent_pro_font():
    """Ищет файл шрифта Advent Pro Expanded Light в системе"""
    fonts_dir = "C:/Windows/Fonts"
    
    possible_names = [
        "AdventPro-ExpandedLight.ttf",
        "AdventPro-ExtraLight.ttf",
        "AdventPro-Light.ttf",
        "AdventPro-Regular.ttf",
        "AdventPro-Medium.ttf",
        "adventproexpandedlight.ttf",
        "adventproextralight.ttf",
        "adventprolight.ttf",
        "adventpro.ttf",
    ]
    
    for name in possible_names:
        path = os.path.join(fonts_dir, name)
        if os.path.exists(path):
            print(f"✓ Найден шрифт: {path}")
            return path
    
    if os.path.exists(fonts_dir):
        for file in os.listdir(fonts_dir):
            if "advent" in file.lower() and file.lower().endswith(('.ttf', '.ttc')):
                path = os.path.join(fonts_dir, file)
                print(f"✓ Найден шрифт: {path}")
                return path
    
    print("✗ Шрифт Advent Pro не найден, будет использоваться Arial")
    return None

ADVENT_FONT_PATH = find_advent_pro_font()

# ==========================================
# ТЕМА
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ==========================================
# ГЛАВНОЕ ОКНО
# ==========================================

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Practices Awareness")
        self.geometry("1280x910")
        self.minsize(900, 600)

        self.configure(fg_color="#E9DCB0")

        # ==========================================
        # HEADER
        # ==========================================

        header = ctk.CTkFrame(
            self,
            height=100,
            fg_color="#986722",
            corner_radius=0
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        # ==========================================
        # ЛОГОТИП СЛЕВА
        # ==========================================

        logo_frame = ctk.CTkFrame(
            header,
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
            image_path = "frontend/assets/logo.png"
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((145, 145))
                self.logo_image = ImageTk.PhotoImage(image)
                image_label = tk.Label(
                    header,
                    image=self.logo_image,
                    bg="#986722",
                    bd=0
                )
                image_label.pack(side="right", padx=20)
        except Exception as e:
            print("Ошибка загрузки картинки:", e)

        # ==========================================
        # DASHBOARD
        # ==========================================

        dashboard = DashboardFrame(self)
        dashboard.pack(fill="both", expand=True)


# ==========================================
# DASHBOARD (ТАБЛИЦА НА CANVAS)
# ==========================================

class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#DCCB98")

        # Данные таблицы
        self.table_data = {}
        self.current_row = 1
        self.rows = 15
        self.cols = 8
        
        # Хранилище для Entry виджетов при редактировании
        self.edit_entries = {}
        self.editing_row = None
        self.original_data = {}  # Хранилище исходных данных для отмены

        # Ширина столбцов
        self.base_widths = [200, 250, 250, 150, 150, 200, 200, 100]
        self.widths = self.base_widths.copy()
        
        # Заголовки
        self.columns = [
            "Название",
            "Место проведения",
            "Мероприятие",
            "Уровень",
            "Дата",
            "Контроль",
            "Документы",
            ""
        ]

        # Высота строки
        self.row_height = 50

        # Цвет ячейки
        self.cell_color = "#E9DCB0"
        
        # Цвет при наведении (как у кнопки выхода)
        self.hover_color = "#C8B57E"

        # ==========================================
        # ВЕРХНЯЯ ПАНЕЛЬ С КНОПКАМИ
        # ==========================================

        top_bar = ctk.CTkFrame(
            self,
            height=60,
            fg_color="#D6C189",
            corner_radius=0
        )

        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        # ИКОНКА ВЫХОДА
        exit_path = "frontend/assets/exit.png"
        if os.path.exists(exit_path):
            exit_image = Image.open(exit_path)
            self.exit_icon = ctk.CTkImage(
                light_image=exit_image,
                dark_image=exit_image,
                size=(32, 32)
            )
            exit_btn = ctk.CTkButton(
                top_bar,
                image=self.exit_icon,
                text="",
                width=40,
                fg_color="transparent",
                hover_color=self.hover_color,
                command=self.show_exit_dialog
            )
        else:
            exit_btn = ctk.CTkButton(
                top_bar,
                text="←",
                width=40,
                fg_color="transparent",
                hover_color=self.hover_color,
                text_color="black",
                font=("Advent Pro", 24),
                command=self.show_exit_dialog
            )
        exit_btn.pack(side="left", padx=(10, 5), pady=5)

        # ЗАГОЛОВОК
        title_label = ctk.CTkLabel(
            top_bar,
            text="Главная страница",
            font=("Advent Pro", 28, "bold"),
            text_color="black"
        )
        title_label.pack(side="left", padx=10)

        # КНОПКА СОЗДАНИЯ
        add_path = "frontend/assets/create.png"
        if os.path.exists(add_path):
            add_image = Image.open(add_path)
            self.add_icon = ctk.CTkImage(
                light_image=add_image,
                dark_image=add_image,
                size=(30, 30)
            )
            add_btn = ctk.CTkButton(
                top_bar,
                image=self.add_icon,
                text="",
                width=40,
                fg_color="transparent",
                hover_color=self.hover_color,
                command=self.add_row
            )
        else:
            add_btn = ctk.CTkButton(
                top_bar,
                text="+",
                width=40,
                fg_color="transparent",
                hover_color=self.hover_color,
                text_color="black",
                font=("Arial", 30),
                command=self.add_row
            )
        add_btn.pack(side="right", padx=15)

        # КНОПКА "Редактирование списка преподавателей" (заглушка для будущего функционала)
        self.edit_text = ctk.CTkButton(
            top_bar,
            text="Редактирование списка преподавателей",
            font=("Advent Pro", 20, "bold"),
            fg_color="transparent",
            text_color="black",
            hover_color=self.hover_color,
            corner_radius=10,
            width=320,
            height=40,
            command=self.show_placeholder_message  # Временная заглушка
        )
        self.edit_text.pack(side="right", padx=15, pady=10)


        # ==========================================
        # КОНТЕЙНЕР С ПРОКРУТКОЙ
        # ==========================================

        container = tk.Frame(self, bg="#DCCB98")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(
            container,
            bg="#E6D7A8",
            highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        y_scrollbar = ctk.CTkScrollbar(
            container,
            orientation="vertical",
            command=self.canvas.yview
        )
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = ctk.CTkScrollbar(
            self,
            orientation="horizontal",
            command=self.canvas.xview
        )
        x_scrollbar.pack(fill="x", padx=20, pady=(0, 10))

        self.canvas.configure(
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        # Загружаем иконки
        self.filter_img = None
        self.info_img = None
        self.edit_img = None
        self.delete_img = None
        self.save_img = None
        self.cancel_img = None  # Иконка отмены
        
        # Загрузка иконки фильтра
        filter_paths = ["frontend/assets/filter.png", "assets/filter.png", "filter.png"]
        for path in filter_paths:
            try:
                if os.path.exists(path):
                    filter_image = Image.open(path)
                    self.filter_img = ImageTk.PhotoImage(filter_image.resize((22, 22)))
                    break
            except:
                pass
        
        # Загрузка иконки информации
        info_paths = ["frontend/assets/info.png", "assets/info.png", "info.png"]
        for path in info_paths:
            try:
                if os.path.exists(path):
                    info_image = Image.open(path)
                    self.info_img = ImageTk.PhotoImage(info_image.resize((26, 26)))
                    break
            except:
                pass
        
        # Загрузка иконки редактирования
        edit_paths = ["frontend/assets/edit.png", "assets/edit.png", "edit.png"]
        for path in edit_paths:
            try:
                if os.path.exists(path):
                    edit_image = Image.open(path)
                    self.edit_img = ImageTk.PhotoImage(edit_image.resize((28, 28)))
                    break
            except:
                pass
        
        # Загрузка иконки удаления
        delete_paths = ["frontend/assets/delete.png", "assets/delete.png", "delete.png"]
        for path in delete_paths:
            try:
                if os.path.exists(path):
                    delete_image = Image.open(path)
                    self.delete_img = ImageTk.PhotoImage(delete_image.resize((28, 28)))
                    break
            except:
                pass
        
        # Создаём зелёную галочку для сохранения
        try:
            save_path = "frontend/assets/save.png"
            if os.path.exists(save_path):
                save_image = Image.open(save_path)
                self.save_img = ImageTk.PhotoImage(save_image.resize((28, 28)))
            else:
                self.save_img = self.create_checkmark_image()
        except:
            self.save_img = self.create_checkmark_image()
        
        # Создаём красный крестик для отмены
        self.cancel_img = self.create_cancel_image()

        # Создаем фрейм для таблицы
        self.table_frame = tk.Frame(self.canvas, bg="#E6D7A8")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        
        self.table_frame.bind("<Configure>", self.update_scrollregion)
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind_all("<MouseWheel>", self.mouse_wheel)

        # Рисуем таблицу
        self.draw_table()

    def create_checkmark_image(self):
        """Создаёт зелёную галочку программно"""
        img = Image.new('RGBA', (28, 28), (0, 0, 0, 0))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.line((5, 14, 11, 20), fill='#27AE60', width=3)
        draw.line((11, 20, 23, 8), fill='#27AE60', width=3)
        return ImageTk.PhotoImage(img)
    
    def create_cancel_image(self):
        """Создаёт красный крестик для отмены программно"""
        img = Image.new('RGBA', (28, 28), (0, 0, 0, 0))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        # Рисуем крестик
        draw.line((8, 8, 20, 20), fill='#E74C3C', width=3)
        draw.line((20, 8, 8, 20), fill='#E74C3C', width=3)
        return ImageTk.PhotoImage(img)

    # ==========================================
    # ГРАДИЕНТНЫЙ ФОН ДЛЯ ДИАЛОГОВ
    # ==========================================
    
    def create_gradient_background(self, width=300, height=45):
        """Создаёт градиентный фон для шапки"""
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        r1, g1, b1 = 0xD4, 0xB8, 0x5C
        r2, g2, b2 = 0x82, 0x6C, 0x1C
        
        for x in range(width):
            r = int(r1 + (r2 - r1) * x / (width - 1))
            g = int(g1 + (g2 - g1) * x / (width - 1))
            b = int(b1 + (b2 - b1) * x / (width - 1))
            draw.line([(x, 0), (x, height)], fill=(r, g, b))
        
        return ImageTk.PhotoImage(image)

    # ==========================================
    # ВРЕМЕННАЯ ЗАГЛУШКА ДЛЯ КНОПКИ ПРЕПОДАВАТЕЛЕЙ
    # ==========================================
    
    def show_placeholder_message(self):
        """Временное сообщение о том, что функционал будет добавлен позже"""
        messagebox.showinfo("В разработке", "Функционал редактирования преподавателей будет добавлен в следующей версии")

    # ==========================================
    # SCROLL
    # ==========================================

    def update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize_canvas(self, event):
        canvas_width = event.width
        base_table_width = sum(self.base_widths)
        
        if canvas_width > base_table_width:
            extra_width = canvas_width - base_table_width
            self.widths = []
            for w in self.base_widths:
                if w > 0:
                    new_w = w + int(extra_width * (w / base_table_width))
                    self.widths.append(new_w)
                else:
                    self.widths.append(w)
        else:
            self.widths = self.base_widths.copy()
        
        self.draw_table()
        
        total_width = sum(self.widths)
        total_height = (self.rows + 1) * self.row_height
        self.canvas.itemconfig(
            self.canvas_window,
            width=total_width,
            height=total_height
        )
        self.canvas.configure(scrollregion=(0, 0, total_width, total_height))

    def mouse_wheel(self, event):
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==========================================
    # СТИЛИЗОВАННЫЙ ДИАЛОГ ВЫХОДА
    # ==========================================

    def show_exit_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.title("Выход")
        dialog.configure(fg_color="#E6D5A8")
        dialog.grab_set()

        main_frame = ctk.CTkFrame(dialog, fg_color="#F0E6C8", corner_radius=0, border_width=0)
        main_frame.pack(fill="both", expand=True)

        header_container = tk.Frame(main_frame, height=45, bg="#F0E6C8")
        header_container.pack(fill="x")
        header_container.pack_propagate(False)

        header = tk.Canvas(header_container, height=45, highlightthickness=0, bd=0)
        header.pack(fill="x")

        def draw_header():
            width = header.winfo_width()
            if width > 10:
                gradient_img = self.create_gradient_background(width, 45)
                header.create_image(0, 0, image=gradient_img, anchor="nw")
                header.gradient_img = gradient_img
                header.create_text(width // 2, 22, text="Выход", fill="black", 
                                  font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
                                  anchor="center")

        header.after(100, draw_header)

        text_label = ctk.CTkLabel(
            main_frame,
            text="Вы точно хотите\nвыйти?",
            font=("Advent Pro Expanded Light", 20) if ADVENT_FONT_PATH else ("Arial", 20),
            text_color="#444444",
            wraplength=250,
            justify="center"
        )
        text_label.pack(expand=True, pady=20)

        buttons_frame = ctk.CTkFrame(main_frame, height=45, fg_color="#E0D0A0", corner_radius=0)
        buttons_frame.pack(fill="x", side="bottom")
        buttons_frame.pack_propagate(False)

        separator = ctk.CTkFrame(main_frame, height=2, fg_color="#7A6A45", corner_radius=0)
        separator.pack(fill="x", side="bottom")

        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Выход",
            height=45,
            corner_radius=0,
            fg_color="#E0D0A0",
            hover_color="#D4C490",
            text_color="#444444",
            font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
            border_width=0,
            command=self.master.destroy
        )
        confirm_btn.pack(side="left", fill="both", expand=True)

        v_separator = ctk.CTkFrame(buttons_frame, width=2, fg_color="#7A6A45", corner_radius=0)
        v_separator.pack(side="left", fill="y")

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Отмена",
            height=45,
            corner_radius=0,
            fg_color="#E0D0A0",
            hover_color="#D4C490",
            text_color="#444444",
            font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
            border_width=0,
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", fill="both", expand=True)

    # ==========================================
    # СТИЛИЗОВАННЫЙ ДИАЛОГ УДАЛЕНИЯ
    # ==========================================

    def delete_row(self, row):
        def confirm_delete():
            if row in self.table_data:
                for col in self.columns[:-1]:
                    self.table_data[row][col] = ""
            if self.editing_row == row:
                self.editing_row = None
            self.draw_table()
            dialog.destroy()

        dialog = ctk.CTkToplevel(self)
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.title("Удалить")
        dialog.configure(fg_color="#E6D5A8")
        dialog.grab_set()

        main_frame = ctk.CTkFrame(dialog, fg_color="#F0E6C8", corner_radius=0, border_width=0)
        main_frame.pack(fill="both", expand=True)

        header_container = tk.Frame(main_frame, height=45, bg="#F0E6C8")
        header_container.pack(fill="x")
        header_container.pack_propagate(False)

        header = tk.Canvas(header_container, height=45, highlightthickness=0, bd=0)
        header.pack(fill="x")

        def draw_header():
            width = header.winfo_width()
            if width > 10:
                gradient_img = self.create_gradient_background(width, 45)
                header.create_image(0, 0, image=gradient_img, anchor="nw")
                header.gradient_img = gradient_img
                header.create_text(width // 2, 22, text="Удалить", fill="black", 
                                  font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
                                  anchor="center")

        header.after(100, draw_header)

        text_label = ctk.CTkLabel(
            main_frame,
            text=f"Вы уверены, что хотите\nудалить строку {row}?",
            font=("Advent Pro Expanded Light", 20) if ADVENT_FONT_PATH else ("Arial", 20),
            text_color="#444444",
            wraplength=250,
            justify="center"
        )
        text_label.pack(expand=True, pady=20)

        buttons_frame = ctk.CTkFrame(main_frame, height=45, fg_color="#E0D0A0", corner_radius=0)
        buttons_frame.pack(fill="x", side="bottom")
        buttons_frame.pack_propagate(False)

        separator = ctk.CTkFrame(main_frame, height=2, fg_color="#7A6A45", corner_radius=0)
        separator.pack(fill="x", side="bottom")

        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Удалить",
            height=45,
            corner_radius=0,
            fg_color="#E0D0A0",
            hover_color="#D4C490",
            text_color="#444444",
            font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
            border_width=0,
            command=confirm_delete
        )
        confirm_btn.pack(side="left", fill="both", expand=True)

        v_separator = ctk.CTkFrame(buttons_frame, width=2, fg_color="#7A6A45", corner_radius=0)
        v_separator.pack(side="left", fill="y")

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Отмена",
            height=45,
            corner_radius=0,
            fg_color="#E0D0A0",
            hover_color="#D4C490",
            text_color="#444444",
            font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
            border_width=0,
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", fill="both", expand=True)

    # ==========================================
    # ДИАЛОГ ПОДТВЕРЖДЕНИЯ СОХРАНЕНИЯ
    # ==========================================

    def show_confirm_save_dialog(self, row):
        """Диалог подтверждения сохранения изменений"""
        dialog = ctk.CTkToplevel(self)
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.title("Подтверждение")
        dialog.configure(fg_color="#E6D5A8")
        dialog.grab_set()

        main_frame = ctk.CTkFrame(dialog, fg_color="#F0E6C8", corner_radius=0, border_width=0)
        main_frame.pack(fill="both", expand=True)

        header_container = tk.Frame(main_frame, height=45, bg="#F0E6C8")
        header_container.pack(fill="x")
        header_container.pack_propagate(False)

        header = tk.Canvas(header_container, height=45, highlightthickness=0, bd=0)
        header.pack(fill="x")

        def draw_header():
            width = header.winfo_width()
            if width > 10:
                gradient_img = self.create_gradient_background(width, 45)
                header.create_image(0, 0, image=gradient_img, anchor="nw")
                header.gradient_img = gradient_img
                header.create_text(width // 2, 22, text="Сохранение", fill="black", 
                                  font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
                                  anchor="center")

        header.after(100, draw_header)

        text_label = ctk.CTkLabel(
            main_frame,
            text="Сохранить изменения?",
            font=("Advent Pro Expanded Light", 20) if ADVENT_FONT_PATH else ("Arial", 20),
            text_color="#444444",
            wraplength=250,
            justify="center"
        )
        text_label.pack(expand=True, pady=20)

        buttons_frame = ctk.CTkFrame(main_frame, height=45, fg_color="#E0D0A0", corner_radius=0)
        buttons_frame.pack(fill="x", side="bottom")
        buttons_frame.pack_propagate(False)

        separator = ctk.CTkFrame(main_frame, height=2, fg_color="#7A6A45", corner_radius=0)
        separator.pack(fill="x", side="bottom")

        def save_and_close():
            self.save_row_changes(row)
            dialog.destroy()

        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Сохранить",
            height=45,
            corner_radius=0,
            fg_color="#E0D0A0",
            hover_color="#D4C490",
            text_color="#444444",
            font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
            border_width=0,
            command=save_and_close
        )
        confirm_btn.pack(side="left", fill="both", expand=True)

        v_separator = ctk.CTkFrame(buttons_frame, width=2, fg_color="#7A6A45", corner_radius=0)
        v_separator.pack(side="left", fill="y")

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Отмена",
            height=45,
            corner_radius=0,
            fg_color="#E0D0A0",
            hover_color="#D4C490",
            text_color="#444444",
            font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
            border_width=0,
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", fill="both", expand=True)

    # ==========================================
    # ДИАЛОГ ОТМЕНЫ РЕДАКТИРОВАНИЯ
    # ==========================================

    def show_cancel_edit_dialog(self, row):
        """Диалог подтверждения отмены редактирования"""
        dialog = ctk.CTkToplevel(self)
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.title("Отмена")
        dialog.configure(fg_color="#E6D5A8")
        dialog.grab_set()

        main_frame = ctk.CTkFrame(dialog, fg_color="#F0E6C8", corner_radius=0, border_width=0)
        main_frame.pack(fill="both", expand=True)

        header_container = tk.Frame(main_frame, height=45, bg="#F0E6C8")
        header_container.pack(fill="x")
        header_container.pack_propagate(False)

        header = tk.Canvas(header_container, height=45, highlightthickness=0, bd=0)
        header.pack(fill="x")

        def draw_header():
            width = header.winfo_width()
            if width > 10:
                gradient_img = self.create_gradient_background(width, 45)
                header.create_image(0, 0, image=gradient_img, anchor="nw")
                header.gradient_img = gradient_img
                header.create_text(width // 2, 22, text="Отмена", fill="black", 
                                  font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
                                  anchor="center")

        header.after(100, draw_header)

        text_label = ctk.CTkLabel(
            main_frame,
            text="Отменить изменения?",
            font=("Advent Pro Expanded Light", 20) if ADVENT_FONT_PATH else ("Arial", 20),
            text_color="#444444",
            wraplength=250,
            justify="center"
        )
        text_label.pack(expand=True, pady=20)

        buttons_frame = ctk.CTkFrame(main_frame, height=45, fg_color="#E0D0A0", corner_radius=0)
        buttons_frame.pack(fill="x", side="bottom")
        buttons_frame.pack_propagate(False)

        separator = ctk.CTkFrame(main_frame, height=2, fg_color="#7A6A45", corner_radius=0)
        separator.pack(fill="x", side="bottom")

        def cancel_and_close():
            self.cancel_edit(row)
            dialog.destroy()

        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Отменить",
            height=45,
            corner_radius=0,
            fg_color="#E0D0A0",
            hover_color="#D4C490",
            text_color="#444444",
            font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
            border_width=0,
            command=cancel_and_close
        )
        confirm_btn.pack(side="left", fill="both", expand=True)

        v_separator = ctk.CTkFrame(buttons_frame, width=2, fg_color="#7A6A45", corner_radius=0)
        v_separator.pack(side="left", fill="y")

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Продолжить",
            height=45,
            corner_radius=0,
            fg_color="#E0D0A0",
            hover_color="#D4C490",
            text_color="#444444",
            font=("Advent Pro Expanded Light", 20, "bold") if ADVENT_FONT_PATH else ("Arial", 20, "bold"),
            border_width=0,
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", fill="both", expand=True)

    # ==========================================
    # ОКНО ИНФОРМАЦИИ (с плашкой Преподаватели, но без списка)
    # ==========================================

    def show_info(self, row):
        WINDOW_W = 467
        WINDOW_H = 400
        HEADER_H = 108

        info_window = ctk.CTkToplevel(self)
        info_window.geometry(f"{WINDOW_W}x{WINDOW_H}")
        info_window.title("Информация")
        info_window.configure(fg_color="#D4B45F")
        info_window.resizable(False, False)

        # ---------------- HEADER ----------------
        header = tk.Canvas(
            info_window,
            height=HEADER_H,
            highlightthickness=0,
            bd=0
        )
        header.pack(fill="x")
        
        info_window.update_idletasks()
        real_width = info_window.winfo_width()

        # Градиентный фон для шапки
        left = (221, 194, 108)
        right = (186, 144, 48)

        for x in range(real_width):
            k = x / max(real_width - 1, 1)
            r = int(left[0] + (right[0] - left[0]) * k)
            g = int(left[1] + (right[1] - left[1]) * k)
            b = int(left[2] + (right[2] - left[2]) * k)
            color = f"#{r:02x}{g:02x}{b:02x}"
            header.create_line(x, 0, x, HEADER_H, fill=color)

        # Иконка
        header.create_text(
            34,
            32,
            text="ⓘ",
            font=("Advent Pro", 24) if ADVENT_FONT_PATH else ("Arial", 24),
            fill="black"
        )

        # Заголовок
        header.create_text(
            72,
            18,
            anchor="nw",
            text="Новые технологии -\nновая педагогика",
            font=("Advent Pro", 22) if ADVENT_FONT_PATH else ("Arial", 22),
            fill="black"
        )

        # Кнопка закрытия
        close_btn = header.create_text(
            real_width - 28,
            24,
            text="✕",
            font=("Advent Pro", 24) if ADVENT_FONT_PATH else ("Arial", 24),
            fill="black"
        )
        header.tag_bind(
            close_btn,
            "<Button-1>",
            lambda e: info_window.destroy()
        )

        # Линия под градиентом
        top_line = tk.Frame(
            info_window,
            height=2,
            bg="#A37C26"
        )
        top_line.pack(fill="x")

        # ---------------- BODY ----------------
        body = ctk.CTkFrame(
            info_window,
            fg_color="transparent"
        )
        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Получаем данные строки
        row_data = self.table_data.get(row, {})
        
        # Описание
        description_title = ctk.CTkLabel(
            body,
            text="Описание:",
            text_color="black",
            font=("Advent Pro", 22, "bold") if ADVENT_FONT_PATH else ("Arial", 22, "bold")
        )
        description_title.pack(anchor="w", pady=(0, 10))
        
        description_text = row_data.get("Описание", "Нет описания")
        description_value = ctk.CTkLabel(
            body,
            text=description_text,
            text_color="#333333",
            font=("Advent Pro", 18) if ADVENT_FONT_PATH else ("Arial", 18),
            wraplength=400,
            justify="left"
        )
        description_value.pack(anchor="w", pady=(0, 20))

        # Линия над преподавателями
        line = tk.Frame(
            info_window,
            height=2,
            width=real_width - 40,
            bg="#A37C26"
        )
        line.place(x=20, y=320)

        # Плашка "Преподаватели" (без списка)
        teachers_title = ctk.CTkLabel(
            info_window,
            text="Преподаватели:",
            text_color="black",
            fg_color="transparent",
            font=("Advent Pro", 22, "bold") if ADVENT_FONT_PATH else ("Arial", 22, "bold")
        )
        teachers_title.place(x=20, y=340)

    # ==========================================
    # РИСОВАНИЕ ТАБЛИЦЫ
    # ==========================================

    def draw_table(self):
        self.canvas.delete("all")
        self.edit_entries.clear()
        
        total_width = sum(self.widths)
        total_height = (self.rows + 1) * self.row_height
        
        self.canvas.config(scrollregion=(0, 0, total_width, total_height))
        
        # Рисуем фон
        self.canvas.create_rectangle(0, 0, total_width, total_height, fill="#E6D7A8", outline="")
        
        # ==========================================
        # ЗАГОЛОВКИ
        # ==========================================
        x = 0
        for i, (col, width) in enumerate(zip(self.columns, self.widths)):
            self.canvas.create_rectangle(
                x, 0, x + width, self.row_height,
                fill="#D9C998", outline="black", width=1
            )
            
            if i == 0:
                if self.filter_img:
                    # Создаём кнопку фильтра с эффектом наведения
                    filter_btn = tk.Button(
                        self.canvas,
                        image=self.filter_img,
                        bg="#D9C998",
                        bd=0,
                        cursor="hand2",
                        command=self.on_filter_click
                    )
                    filter_btn.image = self.filter_img
                    
                    # Эффект наведения
                    def on_enter(e, btn=filter_btn):
                        btn.config(bg=self.hover_color)
                    def on_leave(e, btn=filter_btn):
                        btn.config(bg="#D9C998")
                    
                    filter_btn.bind("<Enter>", on_enter)
                    filter_btn.bind("<Leave>", on_leave)
                    
                    self.canvas.create_window(
                        x + 25, self.row_height // 2,
                        window=filter_btn, width=28, height=28
                    )
                    
                    self.canvas.create_text(
                        x + width // 2 + 15, self.row_height // 2,
                        text=col, font=("Advent Pro", 16, "bold"), fill="#2B2B2B"
                    )
                else:
                    self.canvas.create_text(
                        x + width // 2, self.row_height // 2,
                        text=col, font=("Advent Pro", 16, "bold"), fill="#2B2B2B"
                    )
            else:
                self.canvas.create_text(
                    x + width // 2, self.row_height // 2,
                    text=col, font=("Advent Pro", 16, "bold"), fill="#2B2B2B"
                )
            x += width
        
        # ==========================================
        # ЯЧЕЙКИ И ДАННЫЕ
        # ==========================================
        for row in range(1, self.rows + 1):
            y = row * self.row_height
            x = 0
            
            for col_idx, (col, width) in enumerate(zip(self.columns, self.widths)):
                # Рисуем фон ячейки
                self.canvas.create_rectangle(
                    x, y, x + width, y + self.row_height,
                    fill=self.cell_color, outline="black", width=1
                )
                
                if col_idx == 0:
                    # Кнопка информации с эффектом наведения
                    btn_bg = self.cell_color
                    
                    if self.info_img:
                        info_btn = tk.Button(
                            self.canvas,
                            image=self.info_img,
                            bg=btn_bg,
                            bd=0,
                            cursor="hand2",
                            command=lambda r=row: self.show_info(r)
                        )
                        info_btn.image = self.info_img
                    else:
                        info_btn = tk.Button(
                            self.canvas,
                            text="ⓘ",
                            font=("Advent Pro", 16, "bold"),
                            bg=btn_bg,
                            fg="black",
                            bd=0,
                            cursor="hand2",
                            command=lambda r=row: self.show_info(r)
                        )
                    
                    # Эффект наведения
                    def on_enter(e, btn=info_btn):
                        btn.config(bg=self.hover_color)
                    def on_leave(e, btn=info_btn):
                        btn.config(bg=btn_bg)
                    
                    info_btn.bind("<Enter>", on_enter)
                    info_btn.bind("<Leave>", on_leave)
                    
                    self.canvas.create_window(
                        x + 25, y + self.row_height // 2,
                        window=info_btn, width=28, height=28
                    )
                    
                    # Текст или поле ввода
                    if self.editing_row == row:
                        entry = tk.Entry(
                            self.canvas,
                            font=("Advent Pro", 14),
                            bg=self.cell_color,
                            fg="black",
                            relief="flat",
                            bd=0,
                            highlightthickness=1,
                            highlightcolor="#986722",
                            highlightbackground="#986722"
                        )
                        entry.insert(0, self.table_data.get(row, {}).get(col, ""))
                        entry_id = self.canvas.create_window(
                            x + width // 2 + 20, y + self.row_height // 2,
                            window=entry, width=width - 80, height=self.row_height - 10
                        )
                        self.edit_entries[(row, col)] = entry
                    else:
                        data = self.table_data.get(row, {}).get(col, "")
                        self.canvas.create_text(
                            x + width // 2 + 20, y + self.row_height // 2,
                            text=data, font=("Advent Pro", 16), fill="black"
                        )
                        
                elif col == "":
                    # Кнопки редактирования/сохранения и удаления
                    btn_bg = self.cell_color
                    
                    if self.editing_row == row:
                        # Кнопка сохранения (слева)
                        save_btn = tk.Button(
                            self.canvas,
                            image=self.save_img,
                            bg=btn_bg,
                            bd=0,
                            cursor="hand2",
                            command=lambda r=row: self.show_confirm_save_dialog(r)
                        )
                        save_btn.image = self.save_img
                        
                        def on_enter_save(e, btn=save_btn):
                            btn.config(bg=self.hover_color)
                        def on_leave_save(e, btn=save_btn):
                            btn.config(bg=btn_bg)
                        
                        save_btn.bind("<Enter>", on_enter_save)
                        save_btn.bind("<Leave>", on_leave_save)
                        
                        self.canvas.create_window(
                            x + width // 2 - 20, y + self.row_height // 2,
                            window=save_btn, width=34, height=34
                        )
                        
                        # Кнопка отмены (справа)
                        cancel_btn = tk.Button(
                            self.canvas,
                            image=self.cancel_img,
                            bg=btn_bg,
                            bd=0,
                            cursor="hand2",
                            command=lambda r=row: self.show_cancel_edit_dialog(r)
                        )
                        cancel_btn.image = self.cancel_img
                        
                        def on_enter_cancel(e, btn=cancel_btn):
                            btn.config(bg=self.hover_color)
                        def on_leave_cancel(e, btn=cancel_btn):
                            btn.config(bg=btn_bg)
                        
                        cancel_btn.bind("<Enter>", on_enter_cancel)
                        cancel_btn.bind("<Leave>", on_leave_cancel)
                        
                        self.canvas.create_window(
                            x + width // 2 + 20, y + self.row_height // 2,
                            window=cancel_btn, width=34, height=34
                        )
                    else:
                        # Кнопка редактирования (по центру)
                        if self.edit_img:
                            edit_btn = tk.Button(
                                self.canvas,
                                image=self.edit_img,
                                bg=btn_bg,
                                bd=0,
                                cursor="hand2",
                                command=lambda r=row: self.start_edit(r)
                            )
                            edit_btn.image = self.edit_img
                        else:
                            edit_btn = tk.Button(
                                self.canvas,
                                text="✎",
                                font=("Advent Pro", 16),
                                bg=btn_bg,
                                fg="black",
                                bd=0,
                                cursor="hand2",
                                command=lambda r=row: self.start_edit(r)
                            )
                        
                        def on_enter_edit(e, btn=edit_btn):
                            btn.config(bg=self.hover_color)
                        def on_leave_edit(e, btn=edit_btn):
                            btn.config(bg=btn_bg)
                        
                        edit_btn.bind("<Enter>", on_enter_edit)
                        edit_btn.bind("<Leave>", on_leave_edit)
                        
                        self.canvas.create_window(
                            x + width // 2 - 15, y + self.row_height // 2,
                            window=edit_btn, width=34, height=34
                        )
                        
                        # Кнопка удаления (справа от редактирования)
                        if self.delete_img:
                            delete_btn = tk.Button(
                                self.canvas,
                                image=self.delete_img,
                                bg=btn_bg,
                                bd=0,
                                cursor="hand2",
                                command=lambda r=row: self.delete_row(r)
                            )
                            delete_btn.image = self.delete_img
                        else:
                            delete_btn = tk.Button(
                                self.canvas,
                                text="🗑",
                                font=("Advent Pro", 16),
                                bg=btn_bg,
                                fg="black",
                                bd=0,
                                cursor="hand2",
                                command=lambda r=row: self.delete_row(r)
                            )
                        
                        def on_enter_delete(e, btn=delete_btn):
                            btn.config(bg=self.hover_color)
                        def on_leave_delete(e, btn=delete_btn):
                            btn.config(bg=btn_bg)
                        
                        delete_btn.bind("<Enter>", on_enter_delete)
                        delete_btn.bind("<Leave>", on_leave_delete)
                        
                        self.canvas.create_window(
                            x + width // 2 + 20, y + self.row_height // 2,
                            window=delete_btn, width=34, height=34
                        )
                    
                else:
                    # Обычные ячейки
                    if self.editing_row == row:
                        entry = tk.Entry(
                            self.canvas,
                            font=("Advent Pro", 14),
                            bg=self.cell_color,
                            fg="black",
                            relief="flat",
                            bd=0,
                            highlightthickness=1,
                            highlightcolor="#986722",
                            highlightbackground="#986722"
                        )
                        entry.insert(0, self.table_data.get(row, {}).get(col, ""))
                        entry_id = self.canvas.create_window(
                            x + width // 2, y + self.row_height // 2,
                            window=entry, width=width - 20, height=self.row_height - 10
                        )
                        self.edit_entries[(row, col)] = entry
                    else:
                        data = self.table_data.get(row, {}).get(col, "")
                        self.canvas.create_text(
                            x + width // 2, y + self.row_height // 2,
                            text=data, font=("Advent Pro", 16), fill="black"
                        )
                
                x += width
        
        # Рисуем черные рамки поверх
        self.draw_borders()

    def draw_borders(self):
        """Рисует черные рамки таблицы"""
        total_width = sum(self.widths)
        total_height = (self.rows + 1) * self.row_height
        
        # Горизонтальные линии
        for row in range(self.rows + 2):
            y = row * self.row_height
            self.canvas.create_line(0, y, total_width, y, fill="black", width=1)
        
        # Вертикальные линии
        x = 0
        for width in self.widths:
            x += width
            self.canvas.create_line(x, 0, x, total_height, fill="black", width=1)

    def on_filter_click(self):
        messagebox.showinfo("Фильтр", "Функция фильтрации будет добавлена позже")

    # ==========================================
    # ОБРАБОТЧИКИ КЛИКОВ
    # ==========================================

    def start_edit(self, row):
        """Начать редактирование строки"""
        # Сохраняем исходные данные перед редактированием
        if row not in self.original_data:
            self.original_data[row] = copy.deepcopy(self.table_data.get(row, {}))
        
        if row not in self.table_data:
            self.table_data[row] = {col: "" for col in self.columns[:-1]}
        
        self.editing_row = row
        self.draw_table()

    def save_row_changes(self, row):
        """Сохранить изменения в строке"""
        for (r, col), entry in self.edit_entries.items():
            if r == row:
                self.table_data[row][col] = entry.get()
        
        # Удаляем сохраненные исходные данные
        if row in self.original_data:
            del self.original_data[row]
        
        self.editing_row = None
        self.edit_entries.clear()
        self.draw_table()
        messagebox.showinfo("Сохранение", f"Изменения в строке {row} сохранены!")

    def cancel_edit(self, row):
        """Отменить редактирование и восстановить исходные данные"""
        # Восстанавливаем исходные данные
        if row in self.original_data:
            if row in self.table_data:
                self.table_data[row] = copy.deepcopy(self.original_data[row])
            del self.original_data[row]
        
        self.editing_row = None
        self.edit_entries.clear()
        self.draw_table()

    # ==========================================
    # ДОБАВЛЕНИЕ СТРОКИ
    # ==========================================

    def add_row(self):
        for row in range(1, self.rows + 1):
            if row not in self.table_data:
                self.start_edit(row)
                return
            empty = True
            for col in self.columns[:-1]:
                if self.table_data[row].get(col, ""):
                    empty = False
                    break
            if empty:
                self.start_edit(row)
                return
        
        self.rows += 1
        self.table_data[self.rows] = {col: "" for col in self.columns[:-1]}
        self.draw_table()
        self.start_edit(self.rows)


# ==========================================
# ЗАПУСК
# ==========================================

if __name__ == "__main__":
    app = App()
    app.mainloop()