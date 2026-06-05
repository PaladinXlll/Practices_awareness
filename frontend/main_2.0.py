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

        # КНОПКА "Редактирование списка преподавателей"
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
        self.save_img = None
        
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
            hover_color=self.hover_color,
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
            fg_color="#D8CCA3", hover_color=self.hover_color, text_color="#555555",
            command=lambda: [command(), dialog.destroy()]
        )
        confirm_btn.pack(side="left")

        cancel_btn = ctk.CTkButton(
            buttons, text="Отмена", width=125, height=45, corner_radius=0,
            fg_color="#D8CCA3", hover_color=self.hover_color, text_color="#777777",
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
                        # Кнопка сохранения
                        save_btn = tk.Button(
                            self.canvas,
                            image=self.save_img,
                            bg=btn_bg,
                            bd=0,
                            cursor="hand2",
                            command=lambda r=row: self.save_row(r)
                        )
                        save_btn.image = self.save_img
                        
                        # Эффект наведения
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
                    else:
                        # Кнопка редактирования
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
                        
                        # Эффект наведения
                        def on_enter_edit(e, btn=edit_btn):
                            btn.config(bg=self.hover_color)
                        def on_leave_edit(e, btn=edit_btn):
                            btn.config(bg=btn_bg)
                        
                        edit_btn.bind("<Enter>", on_enter_edit)
                        edit_btn.bind("<Leave>", on_leave_edit)
                        
                        self.canvas.create_window(
                            x + width // 2 - 20, y + self.row_height // 2,
                            window=edit_btn, width=34, height=34
                        )
                    
                    # Кнопка удаления
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
                    
                    # Эффект наведения
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
        if row not in self.table_data:
            self.table_data[row] = {col: "" for col in self.columns[:-1]}
        
        self.editing_row = row
        self.draw_table()

    def save_row(self, row):
        """Сохранить изменения в строке"""
        for (r, col), entry in self.edit_entries.items():
            if r == row:
                self.table_data[row][col] = entry.get()
        
        self.editing_row = None
        self.edit_entries.clear()
        self.draw_table()
        messagebox.showinfo("Сохранение", f"Изменения в строке {row} сохранены!")

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

        close_btn = ctk.CTkButton(header, text="✕", width=25, height=25, fg_color="transparent", hover_color=self.hover_color, text_color="black", font=("Advent Pro", 24), command=info_window.destroy)
        close_btn.place(x=420, y=10)

        form_frame = ctk.CTkFrame(info_window, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        for col in self.columns[:-1]:
            label = ctk.CTkLabel(form_frame, text=f"{col}:", font=("Advent Pro", 14, "bold"), text_color="black")
            label.pack(anchor="w", pady=(10, 2))
            value_label = ctk.CTkLabel(form_frame, text=self.table_data.get(row, {}).get(col, ""), font=("Advent Pro", 14), text_color="#333333", wraplength=400, justify="left")
            value_label.pack(anchor="w", pady=(0, 5))

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
            if self.editing_row == row:
                self.editing_row = None
            self.draw_table()
            dialog.destroy()

        delete_btn = ctk.CTkButton(buttons_frame, text="Удалить", font=("Advent Pro", 14, "bold"), fg_color="#986722", hover_color=self.hover_color, command=confirm_delete)
        delete_btn.pack(side="left", padx=5)
        cancel_btn = ctk.CTkButton(buttons_frame, text="Отмена", font=("Advent Pro", 14, "bold"), fg_color="#986722", hover_color=self.hover_color, command=dialog.destroy)
        cancel_btn.pack(side="left", padx=5)

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