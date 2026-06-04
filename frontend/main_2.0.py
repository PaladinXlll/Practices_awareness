import customtkinter as ctk
import tkinter as tk
from tkinter import font as tkfont, messagebox, simpledialog
from PIL import Image, ImageTk
import os

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
# DASHBOARD (ТАБЛИЦА НА CANVAS С ЧЁРНЫМИ ЛИНИЯМИ)
# ==========================================

class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#DCCB98")

        # Данные таблицы
        self.table_data = {}
        self.current_row = 1
        self.rows = 15
        self.cols = 8

        # Ширина столбцов
        self.widths = [200, 250, 250, 150, 150, 200, 200, 100]
        
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

        # Хранение ID элементов для анимации наведения
        self.button_rects = {}

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
                hover_color="#C8B57E",
                command=self.show_exit_dialog
            )
        else:
            exit_btn = ctk.CTkButton(
                top_bar,
                text="←",
                width=40,
                fg_color="transparent",
                hover_color="#C8B57E",
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
                hover_color="#C8B57E",
                command=self.add_row
            )
        else:
            add_btn = ctk.CTkButton(
                top_bar,
                text="+",
                width=40,
                fg_color="transparent",
                hover_color="#C8B57E",
                text_color="black",
                font=("Arial", 30),
                command=self.add_row
            )
        add_btn.pack(side="right", padx=15)

        # КНОПКА "Редактирование списка преподавателей"
        self.edit_text = ctk.CTkButton(
            top_bar,
            text="Редактирование списка преподавателей",
            font=("Advent Pro", 20, "bold"),
            fg_color="transparent",
            text_color="black",
            hover_color="#C8B57E",
            corner_radius=10,
            width=320,
            height=40,
            command=self.edit_teachers_list
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

        # Создаем фрейм для таблицы (нужен для scrollregion)
        self.table_frame = tk.Frame(self.canvas, bg="#E6D7A8")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        
        self.table_frame.bind("<Configure>", self.update_scrollregion)
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind_all("<MouseWheel>", self.mouse_wheel)

        # Рисуем таблицу
        self.draw_table()

    # ==========================================
    # МЕТОД ДЛЯ РЕДАКТИРОВАНИЯ СПИСКА ПРЕПОДАВАТЕЛЕЙ
    # ==========================================
    
    def edit_teachers_list(self):
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Редактирование преподавателей")
        edit_window.geometry("500x400")
        edit_window.configure(fg_color="#DCCB98")
        edit_window.resizable(False, False)
        
        header = ctk.CTkFrame(
            edit_window,
            height=50,
            fg_color="#986722",
            corner_radius=0
        )
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_label = ctk.CTkLabel(
            header,
            text="Редактирование списка преподавателей",
            font=("Advent Pro", 20, "bold"),
            text_color="white"
        )
        header_label.pack(expand=True)
        
        list_frame = ctk.CTkFrame(
            edit_window,
            fg_color="#E6D7A8",
            corner_radius=15
        )
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        teachers = ["Иванов И.И.", "Петров П.П.", "Сидоров С.С."]
        
        for i, teacher in enumerate(teachers):
            teacher_frame = ctk.CTkFrame(
                list_frame,
                fg_color="#E9DCB0",
                corner_radius=10,
                height=45
            )
            teacher_frame.pack(fill="x", padx=10, pady=5)
            teacher_frame.pack_propagate(False)
            
            teacher_label = ctk.CTkLabel(
                teacher_frame,
                text=teacher,
                font=("Advent Pro", 16),
                text_color="black"
            )
            teacher_label.pack(side="left", padx=15)
        
        close_btn = ctk.CTkButton(
            edit_window,
            text="Закрыть",
            width=120,
            height=35,
            fg_color="#986722",
            hover_color="#7A5C3B",
            text_color="white",
            corner_radius=10,
            command=edit_window.destroy
        )
        close_btn.pack(pady=15)

    # ==========================================
    # SCROLL
    # ==========================================

    def update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize_canvas(self, event):
        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width,
            height=max(event.height, self.table_frame.winfo_reqheight())
        )

    def mouse_wheel(self, event):
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==========================================
    # DIALOG
    # ==========================================

    def custom_dialog(self, title, text, confirm_text, command):
        dialog = ctk.CTkToplevel(self)
        dialog.geometry("250x185")
        dialog.resizable(False, False)
        dialog.title(title)
        dialog.grab_set()

        header = ctk.CTkFrame(dialog, height=40, fg_color="#C9A646", corner_radius=0)
        header.pack(fill="x")
        header_label = ctk.CTkLabel(header, text=title, font=("Advent Pro", 16), text_color="black")
        header_label.pack(expand=True)

        text_label = ctk.CTkLabel(dialog, text=text, font=("Advent Pro", 14), text_color="#444444", wraplength=200)
        text_label.pack(expand=True)

        buttons = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons.pack(fill="x")

        confirm_btn = ctk.CTkButton(
            buttons, text=confirm_text, width=125, height=45, corner_radius=0,
            fg_color="#D8CCA3", hover_color="#C8B57E", text_color="#555555",
            command=lambda: [command(), dialog.destroy()]
        )
        confirm_btn.pack(side="left")

        cancel_btn = ctk.CTkButton(
            buttons, text="Отмена", width=125, height=45, corner_radius=0,
            fg_color="#D8CCA3", hover_color="#C8B57E", text_color="#777777",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right")

    def show_exit_dialog(self):
        self.custom_dialog("Выход", "Вы точно хотите\nвыйти?", "Выход", self.master.destroy)

    # ==========================================
    # РИСОВАНИЕ ТАБЛИЦЫ
    # ==========================================

    def draw_table(self):
        self.canvas.delete("all")
        self.button_rects.clear()
        
        total_width = sum(self.widths)
        total_height = (self.rows + 1) * self.row_height
        
        self.canvas.config(scrollregion=(0, 0, total_width, total_height))
        
        # Рисуем фон
        self.canvas.create_rectangle(0, 0, total_width, total_height, fill="#E6D7A8", outline="")
        
        # ==========================================
        # ЗАГОЛОВКИ (теперь цвет как у ячеек #E9DCB0)
        # ==========================================
        x = 0
        for i, (col, width) in enumerate(zip(self.columns, self.widths)):
            # Фон заголовка теперь #E9DCB0 (как у ячеек)
            self.canvas.create_rectangle(
                x, 0, x + width, self.row_height,
                fill="#E9DCB0", outline="black", width=1
            )
            
            if i == 0:
                if self.filter_img:
                    self.canvas.create_image(
                        x + 25, self.row_height // 2,
                        image=self.filter_img, anchor="center",
                        tags=("filter_icon",)
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
                self.canvas.create_rectangle(
                    x, y, x + width, y + self.row_height,
                    fill="#E9DCB0", outline="black", width=1
                )
                
                if col_idx == 0:
                    if self.info_img:
                        self.canvas.create_image(
                            x + 25, y + self.row_height // 2,
                            image=self.info_img, anchor="center",
                            tags=(f"info_{row}",)
                        )
                        data = self.table_data.get(row, {}).get(col, "")
                        self.canvas.create_text(
                            x + width // 2 + 20, y + self.row_height // 2,
                            text=data, font=("Advent Pro", 16), fill="black"
                        )
                    else:
                        self.canvas.create_text(
                            x + 25, y + self.row_height // 2,
                            text="ⓘ", font=("Advent Pro", 20, "bold"), fill="black",
                            tags=(f"info_{row}",)
                        )
                        data = self.table_data.get(row, {}).get(col, "")
                        self.canvas.create_text(
                            x + width // 2 + 20, y + self.row_height // 2,
                            text=data, font=("Advent Pro", 16), fill="black"
                        )
                elif col == "":
                    pass
                else:
                    data = self.table_data.get(row, {}).get(col, "")
                    self.canvas.create_text(
                        x + width // 2, y + self.row_height // 2,
                        text=data, font=("Advent Pro", 16), fill="black"
                    )
                
                x += width
        
        # ==========================================
        # КНОПКИ (РЕДАКТИРОВАТЬ/УДАЛИТЬ)
        # ==========================================
        button_col_x = sum(self.widths[:-1])
        button_col_width = self.widths[-1]
        
        for row in range(1, self.rows + 1):
            y = row * self.row_height
            center_y = y + self.row_height // 2
            center_x = button_col_x + button_col_width // 2
            
            edit_rect = self.canvas.create_rectangle(
                center_x - 32, center_y - 18, center_x - 8, center_y + 18,
                outline="", fill="", width=2
            )
            
            if self.edit_img:
                edit_btn = self.canvas.create_image(
                    center_x - 20, center_y,
                    image=self.edit_img, anchor="center",
                    tags=(f"edit_{row}",)
                )
            else:
                edit_btn = self.canvas.create_text(
                    center_x - 20, center_y,
                    text="✎", font=("Advent Pro", 18), fill="black",
                    tags=(f"edit_{row}",)
                )
            
            delete_rect = self.canvas.create_rectangle(
                center_x + 8, center_y - 18, center_x + 32, center_y + 18,
                outline="", fill="", width=2
            )
            
            if self.delete_img:
                delete_btn = self.canvas.create_image(
                    center_x + 20, center_y,
                    image=self.delete_img, anchor="center",
                    tags=(f"delete_{row}",)
                )
            else:
                delete_btn = self.canvas.create_text(
                    center_x + 20, center_y,
                    text="🗑", font=("Advent Pro", 18), fill="black",
                    tags=(f"delete_{row}",)
                )
            
            self.button_rects[edit_btn] = edit_rect
            self.button_rects[delete_btn] = delete_rect
        
        # Привязываем события для обводки
        for btn_id, rect_id in self.button_rects.items():
            self.canvas.tag_bind(btn_id, "<Enter>", lambda e, r=rect_id: self.on_hover_enter(r))
            self.canvas.tag_bind(btn_id, "<Leave>", lambda e, r=rect_id: self.on_hover_leave(r))
        
        self.canvas.tag_bind("edit", "<Button-1>", self.on_edit_click)
        self.canvas.tag_bind("delete", "<Button-1>", self.on_delete_click)
        self.canvas.tag_bind("filter_icon", "<Button-1>", self.on_filter_click)
        self.canvas.tag_bind("info", "<Button-1>", self.on_info_click)
        
        # Обводка для значка информации
        info_items = self.canvas.find_withtag("info")
        for info_id in info_items:
            bbox = self.canvas.bbox(info_id)
            if bbox:
                x1, y1, x2, y2 = bbox
                rect = self.canvas.create_rectangle(
                    x1 - 5, y1 - 5, x2 + 5, y2 + 5,
                    outline="", fill="", width=2
                )
                self.canvas.tag_bind(info_id, "<Enter>", lambda e, r=rect: self.on_hover_enter(r))
                self.canvas.tag_bind(info_id, "<Leave>", lambda e, r=rect: self.on_hover_leave(r))
        
        # Обводка для значка фильтра
        filter_items = self.canvas.find_withtag("filter_icon")
        for filter_id in filter_items:
            bbox = self.canvas.bbox(filter_id)
            if bbox:
                x1, y1, x2, y2 = bbox
                rect = self.canvas.create_rectangle(
                    x1 - 5, y1 - 5, x2 + 5, y2 + 5,
                    outline="", fill="", width=2
                )
                self.canvas.tag_bind(filter_id, "<Enter>", lambda e, r=rect: self.on_hover_enter(r))
                self.canvas.tag_bind(filter_id, "<Leave>", lambda e, r=rect: self.on_hover_leave(r))

    def on_hover_enter(self, rect_id):
        self.canvas.itemconfig(rect_id, outline="#986722", fill="")

    def on_hover_leave(self, rect_id):
        self.canvas.itemconfig(rect_id, outline="", fill="")

    # ==========================================
    # ОБРАБОТЧИКИ КЛИКОВ
    # ==========================================

    def on_edit_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        for tag in tags:
            if tag.startswith("edit_"):
                row = int(tag.split("_")[1])
                self.edit_row(row)
                break

    def on_delete_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        for tag in tags:
            if tag.startswith("delete_"):
                row = int(tag.split("_")[1])
                self.delete_row(row)
                break

    def on_filter_click(self, event):
        messagebox.showinfo("Фильтр", "Функция фильтрации будет добавлена позже")

    def on_info_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        for tag in tags:
            if tag.startswith("info_"):
                row = int(tag.split("_")[1])
                self.show_info(row)
                break

    # ==========================================
    # ПОКАЗ ИНФОРМАЦИИ
    # ==========================================

    def show_info(self, row):
        info_window = ctk.CTkToplevel(self)
        info_window.geometry("467x610")
        info_window.title("Информация")
        info_window.configure(fg_color="#D4B45F")
        info_window.resizable(False, False)

        header = ctk.CTkFrame(info_window, width=467, height=108, fg_color="#C9A646", corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        icon_label = ctk.CTkLabel(header, text="ⓘ", font=("Advent Pro", 30), text_color="black")
        icon_label.place(x=18, y=18)

        title_entry = ctk.CTkEntry(header, width=280, height=50, fg_color="#C9A646", border_width=0, text_color="black", font=("Advent Pro", 22))
        title_entry.place(x=70, y=20)
        title_entry.insert(0, self.table_data.get(row, {}).get("Название", ""))
        title_entry.configure(state="readonly")

        close_btn = ctk.CTkButton(header, text="✕", width=25, height=25, fg_color="transparent", hover_color="#B89435", text_color="black", font=("Advent Pro", 24), command=info_window.destroy)
        close_btn.place(x=420, y=10)

        form_frame = ctk.CTkFrame(info_window, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        for col in self.columns[:-1]:
            label = ctk.CTkLabel(form_frame, text=f"{col}:", font=("Advent Pro", 14, "bold"), text_color="black")
            label.pack(anchor="w", pady=(10, 2))
            value_label = ctk.CTkLabel(form_frame, text=self.table_data.get(row, {}).get(col, ""), font=("Advent Pro", 14), text_color="#333333", wraplength=400, justify="left")
            value_label.pack(anchor="w", pady=(0, 5))

    # ==========================================
    # РЕДАКТИРОВАНИЕ СТРОКИ
    # ==========================================

    def edit_row(self, row):
        if row not in self.table_data:
            self.table_data[row] = {col: "" for col in self.columns[:-1]}
        
        dialog = ctk.CTkToplevel(self)
        dialog.geometry("500x600")
        dialog.title(f"Редактирование строки {row}")
        dialog.configure(fg_color="#DBC685")
        dialog.resizable(False, False)

        header = ctk.CTkFrame(dialog, height=50, fg_color="#986722", corner_radius=0)
        header.pack(fill="x")
        header_label = ctk.CTkLabel(header, text=f"Редактирование строки {row}", font=("Advent Pro", 20, "bold"), text_color="white")
        header_label.pack(expand=True)

        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        entries = {}
        for col in self.columns[:-1]:
            label = ctk.CTkLabel(form_frame, text=f"{col}:", font=("Advent Pro", 16), text_color="black")
            label.pack(anchor="w", pady=(0, 5))
            entry = ctk.CTkEntry(form_frame, width=450, font=("Advent Pro", 14), fg_color="#E9DCB0", border_color="#986722")
            entry.pack(pady=(0, 15))
            entry.insert(0, self.table_data[row].get(col, ""))
            entries[col] = entry

        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 0))

        def save():
            for col in self.columns[:-1]:
                self.table_data[row][col] = entries[col].get()
            self.draw_table()
            dialog.destroy()

        save_btn = ctk.CTkButton(buttons_frame, text="Сохранить", font=("Advent Pro", 14, "bold"), fg_color="#986722", hover_color="#7a5518", command=save)
        save_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(buttons_frame, text="Отмена", font=("Advent Pro", 14, "bold"), fg_color="#986722", hover_color="#7a5518", command=dialog.destroy)
        cancel_btn.pack(side="left", padx=5)

    # ==========================================
    # УДАЛЕНИЕ СТРОКИ
    # ==========================================

    def delete_row(self, row):
        dialog = ctk.CTkToplevel(self)
        dialog.geometry("300x180")
        dialog.title("Подтверждение")
        dialog.configure(fg_color="#DBC685")
        dialog.resizable(False, False)

        header = ctk.CTkFrame(dialog, height=50, fg_color="#986722", corner_radius=0)
        header.pack(fill="x")
        header_label = ctk.CTkLabel(header, text="Подтверждение удаления", font=("Advent Pro", 18, "bold"), text_color="white")
        header_label.pack(expand=True)

        text_label = ctk.CTkLabel(dialog, text=f"Вы уверены, что хотите удалить строку {row}?", font=("Advent Pro", 14), text_color="black")
        text_label.pack(expand=True)

        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)

        def confirm_delete():
            if row in self.table_data:
                for col in self.columns[:-1]:
                    self.table_data[row][col] = ""
            self.draw_table()
            dialog.destroy()

        delete_btn = ctk.CTkButton(buttons_frame, text="Удалить", font=("Advent Pro", 14, "bold"), fg_color="#986722", hover_color="#7a5518", command=confirm_delete)
        delete_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(buttons_frame, text="Отмена", font=("Advent Pro", 14, "bold"), fg_color="#986722", hover_color="#7a5518", command=dialog.destroy)
        cancel_btn.pack(side="left", padx=5)

    # ==========================================
    # ДОБАВЛЕНИЕ СТРОКИ
    # ==========================================

    def add_row(self):
        for row in range(1, self.rows + 1):
            if row not in self.table_data:
                self.edit_row(row)
                return
            empty = True
            for col in self.columns[:-1]:
                if self.table_data[row].get(col, ""):
                    empty = False
                    break
            if empty:
                self.edit_row(row)
                return
        
        self.rows += 1
        self.table_data[self.rows] = {col: "" for col in self.columns[:-1]}
        self.draw_table()
        self.edit_row(self.rows)


# ==========================================
# ЗАПУСК
# ==========================================

if __name__ == "__main__":
    app = App()
    app.mainloop()