import customtkinter as ctk
import tkinter as tk
from tkinter import font as tkfont, messagebox
from PIL import Image, ImageTk
import os
import threading

# Импорт функций для работы с базой данных
from db_events import get_events, add_event, update_event, delete_event
from db_reference import get_levels, get_types, get_controls

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

        # ЛОГОТИП СЛЕВА
        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=10)

        logo1 = ctk.CTkLabel(logo_frame, text="PRACTICES", text_color="white", font=("Bayon", 32, "bold"))
        logo1.pack(anchor="w")

        logo2 = ctk.CTkLabel(logo_frame, text="AWARENESS", text_color="white", font=("Bayon", 32, "bold"))
        logo2.pack(anchor="w", padx=(90, 0))

        # ЛОГОТИП КАРТИНКА
        try:
            image_path = "frontend/assets/logo.png"
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((145, 145))
                self.logo_image = ImageTk.PhotoImage(image)
                image_label = tk.Label(header, image=self.logo_image, bg="#986722", bd=0)
                image_label.pack(side="right", padx=20)
        except Exception as e:
            print("Ошибка загрузки картинки:", e)

        # DASHBOARD
        dashboard = DashboardFrame(self)
        dashboard.pack(fill="both", expand=True)


# ==========================================
# DASHBOARD (ТАБЛИЦА НА CANVAS)
# ==========================================

class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#DCCB98")

        # Данные таблицы и словари
        self.table_data = {}
        self.row_to_event_id = {}
        
        # Словари для справочников (Название -> ID)
        self.levels_map = {}
        self.types_map = {}
        self.controls_map = {}
        
        # Словари для обратного перевода (ID -> Название)
        self.levels_id_map = {}
        self.types_id_map = {}
        self.controls_id_map = {}
        
        # Списки имен для выпадающих меню
        self.levels_names = []
        self.types_names = []
        self.controls_names = []
        
        self.current_row = 1
        self.rows = 15
        self.cols = 8
        
        self.edit_entries = {}
        self.editing_row = None

        self.base_widths = [200, 250, 250, 150, 150, 200, 200, 100]
        self.widths = self.base_widths.copy()
        
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

        self.row_height = 50
        self.cell_color = "#E9DCB0"
        self.hover_color = "#C8B57E"

        # ==========================================
        # ВЕРХНЯЯ ПАНЕЛЬ С КНОПКАМИ
        # ==========================================

        top_bar = ctk.CTkFrame(self, height=60, fg_color="#D6C189", corner_radius=0)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        exit_path = "frontend/assets/exit.png"
        if os.path.exists(exit_path):
            exit_image = Image.open(exit_path)
            self.exit_icon = ctk.CTkImage(light_image=exit_image, dark_image=exit_image, size=(32, 32))
            exit_btn = ctk.CTkButton(top_bar, image=self.exit_icon, text="", width=40, fg_color="transparent", hover_color=self.hover_color, command=self.show_exit_dialog)
        else:
            exit_btn = ctk.CTkButton(top_bar, text="←", width=40, fg_color="transparent", hover_color=self.hover_color, text_color="black", font=("Advent Pro", 24), command=self.show_exit_dialog)
        exit_btn.pack(side="left", padx=(10, 5), pady=5)

        title_label = ctk.CTkLabel(top_bar, text="Главная страница", font=("Advent Pro", 28, "bold"), text_color="black")
        title_label.pack(side="left", padx=10)

        add_path = "frontend/assets/create.png"
        if os.path.exists(add_path):
            add_image = Image.open(add_path)
            self.add_icon = ctk.CTkImage(light_image=add_image, dark_image=add_image, size=(30, 30))
            add_btn = ctk.CTkButton(top_bar, image=self.add_icon, text="", width=40, fg_color="transparent", hover_color=self.hover_color, command=self.add_row)
        else:
            add_btn = ctk.CTkButton(top_bar, text="+", width=40, fg_color="transparent", hover_color=self.hover_color, text_color="black", font=("Arial", 30), command=self.add_row)
        add_btn.pack(side="right", padx=15)

        self.edit_text = ctk.CTkButton(top_bar, text="Редактирование списка преподавателей", font=("Advent Pro", 20, "bold"), fg_color="transparent", text_color="black", hover_color=self.hover_color, corner_radius=10, width=320, height=40, command=self.edit_teachers_list)
        self.edit_text.pack(side="right", padx=15, pady=10)

        # ==========================================
        # КОНТЕЙНЕР С ПРОКРУТКОЙ
        # ==========================================

        container = tk.Frame(self, bg="#DCCB98")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(container, bg="#E6D7A8", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        y_scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=self.canvas.yview)
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = ctk.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        x_scrollbar.pack(fill="x", padx=20, pady=(0, 10))

        self.canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Загрузка иконок
        self.filter_img = self._load_icon(["frontend/assets/filter.png", "assets/filter.png", "filter.png"], (22, 22))
        self.info_img = self._load_icon(["frontend/assets/info.png", "assets/info.png", "info.png"], (26, 26))
        self.edit_img = self._load_icon(["frontend/assets/edit.png", "assets/edit.png", "edit.png"], (28, 28))
        self.delete_img = self._load_icon(["frontend/assets/delete.png", "assets/delete.png", "delete.png"], (28, 28))
        
        save_path = "frontend/assets/save.png"
        if os.path.exists(save_path):
            self.save_img = ImageTk.PhotoImage(Image.open(save_path).resize((28, 28)))
        else:
            self.save_img = self.create_checkmark_image()

        self.table_frame = tk.Frame(self.canvas, bg="#E6D7A8")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        
        self.table_frame.bind("<Configure>", self.update_scrollregion)
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind_all("<MouseWheel>", self.mouse_wheel)

        # Запуск получения данных
        self.load_data()

    def _load_icon(self, paths, size):
        for path in paths:
            if os.path.exists(path):
                return ImageTk.PhotoImage(Image.open(path).resize(size))
        return None

    # ==========================================
    # МНОГОПОТОЧНОЕ ЧТЕНИЕ ДАННЫХ
    # ==========================================

    def load_data(self):
        """Запуск фонового потока для чтения данных из БД"""
        thread = threading.Thread(target=self._fetch_events_bg)
        thread.daemon = True
        thread.start()

    def _fetch_events_bg(self):
        """Работает в фоне: запрашивает данные из MySQL"""
        try:
            # Сначала стягиваем все справочники
            raw_levels = get_levels() or []
            raw_types = get_types() or []
            raw_controls = get_controls() or []

            # Затем сами мероприятия
            events = get_events() or []

            # Передаем всё в главный поток
            self.after(0, self._populate_table, events, raw_levels, raw_types, raw_controls)
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self.after(0, lambda: messagebox.showerror("Ошибка", f"Не удалось загрузить данные из БД:\n{e}"))

    def _populate_table(self, events, raw_levels, raw_types, raw_controls):
        """Работает в UI-потоке: заполняет локальные словари и рисует Canvas"""
        self.table_data.clear()
        self.row_to_event_id.clear()

        # Создаем маппинги (Название -> ID)
        self.levels_map = {str(item['name']): item['level_id'] for item in raw_levels}
        self.types_map = {str(item['name']): item['type_id'] for item in raw_types}
        self.controls_map = {str(item['name']): item['control_id'] for item in raw_controls}

        # Создаем обратные маппинги (ID -> Название)
        self.levels_id_map = {item['level_id']: str(item['name']) for item in raw_levels}
        self.types_id_map = {item['type_id']: str(item['name']) for item in raw_types}
        self.controls_id_map = {item['control_id']: str(item['name']) for item in raw_controls}

        # Списки имен для выпадающих меню
        self.levels_names = list(self.levels_map.keys()) if self.levels_map else ["Нет данных"]
        self.types_names = list(self.types_map.keys()) if self.types_map else ["Нет данных"]
        self.controls_names = list(self.controls_map.keys()) if self.controls_map else ["Нет данных"]

        # Если мероприятий нет
        if not events:
            self.rows = 15
            for r in range(1, 16):
                self.table_data[r] = {col: "" for col in self.columns[:-1]}
            self.draw_table()
            return

        self.rows = max(len(events), 15)
        
        for i, ev in enumerate(events, start=1):
            self.row_to_event_id[i] = ev.get('event_id')
            
            # Конвертируем числовые ID из БД в текстовые названия для показа
            level_name = self.levels_id_map.get(ev.get('level'), str(ev.get('level', "")))
            type_name = self.types_id_map.get(ev.get('type'), str(ev.get('type', "")))
            control_name = self.controls_id_map.get(ev.get('control'), str(ev.get('control', "")))

            self.table_data[i] = {
                "Название": ev.get('name', ""),
                "Место проведения": ev.get('place', ""),
                "Мероприятие": type_name,
                "Уровень": level_name,
                "Дата": str(ev.get('event_date', "")),
                "Контроль": control_name,
                "Документы": ev.get('document', "")
            }
        
        for i in range(len(events) + 1, self.rows + 1):
            self.table_data[i] = {col: "" for col in self.columns[:-1]}
            
        self.draw_table()

    def create_checkmark_image(self):
        img = Image.new('RGBA', (28, 28), (0, 0, 0, 0))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.line((5, 14, 11, 20), fill='#27AE60', width=3)
        draw.line((11, 20, 23, 8), fill='#27AE60', width=3)
        return ImageTk.PhotoImage(img)

    def edit_teachers_list(self):
        pass # Этот метод остается заглушкой

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
                    self.widths.append(w + int(extra_width * (w / base_table_width)))
                else:
                    self.widths.append(w)
        else:
            self.widths = self.base_widths.copy()
        
        self.draw_table()
        total_width = sum(self.widths)
        total_height = (self.rows + 1) * self.row_height
        self.canvas.itemconfig(self.canvas_window, width=total_width, height=total_height)
        self.canvas.configure(scrollregion=(0, 0, total_width, total_height))

    def mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def custom_dialog(self, title, text, confirm_text, command):
        dialog = ctk.CTkToplevel(self)
        dialog.geometry("250x185")
        dialog.resizable(False, False)
        dialog.title(title)
        dialog.grab_set()

        header = ctk.CTkFrame(dialog, height=40, fg_color="#C9A646", corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text=title, font=("Advent Pro", 16), text_color="black").pack(expand=True)
        ctk.CTkLabel(dialog, text=text, font=("Advent Pro", 14), text_color="#444444", wraplength=200).pack(expand=True)

        buttons = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons.pack(fill="x")
        ctk.CTkButton(buttons, text=confirm_text, width=125, height=45, corner_radius=0, fg_color="#D8CCA3", hover_color=self.hover_color, text_color="#555555", command=lambda: [command(), dialog.destroy()]).pack(side="left")
        ctk.CTkButton(buttons, text="Отмена", width=125, height=45, corner_radius=0, fg_color="#D8CCA3", hover_color=self.hover_color, text_color="#777777", command=dialog.destroy).pack(side="right")

    def show_exit_dialog(self):
        self.custom_dialog("Выход", "Вы точно хотите\nвыйти?", "Выход", self.master.destroy)

    # ==========================================
    # РИСОВАНИЕ ТАБЛИЦЫ С COMBOBOX
    # ==========================================

    def draw_table(self):
        self.canvas.delete("all")
        self.edit_entries.clear()
        
        total_width = sum(self.widths)
        total_height = (self.rows + 1) * self.row_height
        
        self.canvas.config(scrollregion=(0, 0, total_width, total_height))
        self.canvas.create_rectangle(0, 0, total_width, total_height, fill="#E6D7A8", outline="")
        
        # Заголовки
        x = 0
        for i, (col, width) in enumerate(zip(self.columns, self.widths)):
            self.canvas.create_rectangle(x, 0, x + width, self.row_height, fill="#D9C998", outline="black", width=1)
            
            if i == 0 and self.filter_img:
                filter_btn = tk.Button(self.canvas, image=self.filter_img, bg="#D9C998", bd=0, cursor="hand2", command=self.on_filter_click)
                filter_btn.bind("<Enter>", lambda e, btn=filter_btn: btn.config(bg=self.hover_color))
                filter_btn.bind("<Leave>", lambda e, btn=filter_btn: btn.config(bg="#D9C998"))
                self.canvas.create_window(x + 25, self.row_height // 2, window=filter_btn, width=28, height=28)
                self.canvas.create_text(x + width // 2 + 15, self.row_height // 2, text=col, font=("Advent Pro", 16, "bold"), fill="#2B2B2B")
            else:
                self.canvas.create_text(x + width // 2, self.row_height // 2, text=col, font=("Advent Pro", 16, "bold"), fill="#2B2B2B")
            x += width
        
        # Ячейки
        for row in range(1, self.rows + 1):
            y = row * self.row_height
            x = 0
            
            for col_idx, (col, width) in enumerate(zip(self.columns, self.widths)):
                self.canvas.create_rectangle(x, y, x + width, y + self.row_height, fill=self.cell_color, outline="black", width=1)
                
                # ПЕРВАЯ КОЛОНКА (С кнопкой ИНФО)
                if col_idx == 0:
                    btn_bg = self.cell_color
                    if self.info_img:
                        info_btn = tk.Button(self.canvas, image=self.info_img, bg=btn_bg, bd=0, cursor="hand2", command=lambda r=row: self.show_info(r))
                    else:
                        info_btn = tk.Button(self.canvas, text="ⓘ", font=("Advent Pro", 16, "bold"), bg=btn_bg, fg="black", bd=0, cursor="hand2", command=lambda r=row: self.show_info(r))
                    info_btn.bind("<Enter>", lambda e, btn=info_btn: btn.config(bg=self.hover_color))
                    info_btn.bind("<Leave>", lambda e, btn=info_btn: btn.config(bg=btn_bg))
                    self.canvas.create_window(x + 25, y + self.row_height // 2, window=info_btn, width=28, height=28)
                    
                    if self.editing_row == row:
                        entry = tk.Entry(self.canvas, font=("Advent Pro", 14), bg=self.cell_color, fg="black", relief="flat", bd=0, highlightthickness=1, highlightcolor="#986722", highlightbackground="#986722")
                        entry.insert(0, self.table_data.get(row, {}).get(col, ""))
                        self.canvas.create_window(x + width // 2 + 20, y + self.row_height // 2, window=entry, width=width - 80, height=self.row_height - 10)
                        self.edit_entries[(row, col)] = entry
                    else:
                        self.canvas.create_text(x + width // 2 + 20, y + self.row_height // 2, text=self.table_data.get(row, {}).get(col, ""), font=("Advent Pro", 16), fill="black")
                        
                # ПОСЛЕДНЯЯ КОЛОНКА (Кнопки Редактировать/Удалить)
                elif col == "":
                    btn_bg = self.cell_color
                    if self.editing_row == row:
                        save_btn = tk.Button(self.canvas, image=self.save_img, bg=btn_bg, bd=0, cursor="hand2", command=lambda r=row: self.save_row(r))
                        save_btn.bind("<Enter>", lambda e, btn=save_btn: btn.config(bg=self.hover_color))
                        save_btn.bind("<Leave>", lambda e, btn=save_btn: btn.config(bg=btn_bg))
                        self.canvas.create_window(x + width // 2 - 20, y + self.row_height // 2, window=save_btn, width=34, height=34)
                    else:
                        if self.edit_img:
                            edit_btn = tk.Button(self.canvas, image=self.edit_img, bg=btn_bg, bd=0, cursor="hand2", command=lambda r=row: self.start_edit(r))
                        else:
                            edit_btn = tk.Button(self.canvas, text="✎", font=("Advent Pro", 16), bg=btn_bg, fg="black", bd=0, cursor="hand2", command=lambda r=row: self.start_edit(r))
                        edit_btn.bind("<Enter>", lambda e, btn=edit_btn: btn.config(bg=self.hover_color))
                        edit_btn.bind("<Leave>", lambda e, btn=edit_btn: btn.config(bg=btn_bg))
                        self.canvas.create_window(x + width // 2 - 20, y + self.row_height // 2, window=edit_btn, width=34, height=34)
                    
                    if self.delete_img:
                        delete_btn = tk.Button(self.canvas, image=self.delete_img, bg=btn_bg, bd=0, cursor="hand2", command=lambda r=row: self.delete_row(r))
                    else:
                        delete_btn = tk.Button(self.canvas, text="🗑", font=("Advent Pro", 16), bg=btn_bg, fg="black", bd=0, cursor="hand2", command=lambda r=row: self.delete_row(r))
                    delete_btn.bind("<Enter>", lambda e, btn=delete_btn: btn.config(bg=self.hover_color))
                    delete_btn.bind("<Leave>", lambda e, btn=delete_btn: btn.config(bg=btn_bg))
                    self.canvas.create_window(x + width // 2 + 20, y + self.row_height // 2, window=delete_btn, width=34, height=34)
                    
                # ОСТАЛЬНЫЕ КОЛОНКИ (Текст или Combobox/Entry)
                else:
                    if self.editing_row == row:
                        current_val = self.table_data.get(row, {}).get(col, "")
                        
                        # Если это колонка со справочником -> ВЫПАДАЮЩИЙ СПИСОК
                        if col in ["Уровень", "Мероприятие", "Контроль"]:
                            if col == "Уровень":
                                combo_values = self.levels_names
                            elif col == "Мероприятие":
                                combo_values = self.types_names
                            else:
                                combo_values = self.controls_names

                            combo = ctk.CTkComboBox(
                                self.canvas,
                                values=combo_values,
                                font=("Advent Pro", 14),
                                fg_color="#F2F2F2",
                                text_color="black",
                                button_color="#986722",
                                button_hover_color=self.hover_color,
                                border_color="#986722",
                                corner_radius=0,
                                dropdown_font=("Advent Pro", 14)
                            )
                            
                            if current_val:
                                combo.set(current_val)
                            elif combo_values and combo_values[0] != "Нет данных":
                                combo.set(combo_values[0])
                            else:
                                combo.set("")
                                
                            self.canvas.create_window(x + width // 2, y + self.row_height // 2, window=combo, width=width - 20, height=self.row_height - 10)
                            self.edit_entries[(row, col)] = combo
                            
                        # Если это обычная колонка -> ОБЫЧНЫЙ ВВОД ТЕКСТА
                        else:
                            entry = tk.Entry(self.canvas, font=("Advent Pro", 14), bg=self.cell_color, fg="black", relief="flat", bd=0, highlightthickness=1, highlightcolor="#986722", highlightbackground="#986722")
                            entry.insert(0, current_val)
                            self.canvas.create_window(x + width // 2, y + self.row_height // 2, window=entry, width=width - 20, height=self.row_height - 10)
                            self.edit_entries[(row, col)] = entry
                    else:
                        self.canvas.create_text(x + width // 2, y + self.row_height // 2, text=self.table_data.get(row, {}).get(col, ""), font=("Advent Pro", 16), fill="black")
                x += width
        self.draw_borders()

    def draw_borders(self):
        total_width = sum(self.widths)
        total_height = (self.rows + 1) * self.row_height
        for row in range(self.rows + 2):
            y = row * self.row_height
            self.canvas.create_line(0, y, total_width, y, fill="black", width=1)
        x = 0
        for width in self.widths:
            x += width
            self.canvas.create_line(x, 0, x, total_height, fill="black", width=1)

    def on_filter_click(self):
        messagebox.showinfo("Фильтр", "Функция фильтрации будет добавлена позже")

    # ==========================================
    # СОХРАНЕНИЕ / ОБНОВЛЕНИЕ В БД
    # ==========================================

    def start_edit(self, row):
        if row not in self.table_data:
            self.table_data[row] = {col: "" for col in self.columns[:-1]}
        self.editing_row = row
        self.draw_table()

    def save_row(self, row):
        row_data = {}
        for (r, col), widget in self.edit_entries.items():
            if r == row:
                row_data[col] = widget.get()
        
        thread = threading.Thread(target=self._save_bg, args=(row, row_data))
        thread.daemon = True
        thread.start()

    def _save_bg(self, row, row_data):
        name = row_data.get("Название", "")
        place = row_data.get("Место проведения", "")
        date_val = row_data.get("Дата", "")
        document_val = row_data.get("Документы", "")
        description_val = ""

        # Преобразуем строковые названия из ComboBox обратно в числовые ID
        type_name = row_data.get("Мероприятие", "")
        level_name = row_data.get("Уровень", "")
        control_name = row_data.get("Контроль", "")

        type_id = self.types_map.get(type_name, type_name)
        level_id = self.levels_map.get(level_name, level_name)
        control_id = self.controls_map.get(control_name, control_name)

        event_id = self.row_to_event_id.get(row)

        try:
            if event_id:
                res = update_event(event_id, name, place, level_id, date_val, document_val, type_id, control_id, description_val)
            else:
                res = add_event(name, place, level_id, date_val, document_val, type_id, control_id, description_val)
            
            if res is not None and res is not False:
                self.after(0, self._save_success, row, row_data)
            else:
                self.after(0, lambda: messagebox.showerror("Ошибка", "База данных отклонила сохранение."))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка БД:\n{e}"))

    def _save_success(self, row, row_data):
        for col, val in row_data.items():
            self.table_data[row][col] = val
        self.editing_row = None
        self.edit_entries.clear()
        self.draw_table()
        messagebox.showinfo("Сохранение", f"Изменения сохранены!")
        self.load_data()

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
        ctk.CTkLabel(header, text="Подтверждение удаления", font=("Advent Pro", 18, "bold"), text_color="white").pack(expand=True)
        ctk.CTkLabel(dialog, text=f"Вы уверены, что хотите удалить строку?", font=("Advent Pro", 14), text_color="black").pack(expand=True)

        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)

        def confirm_delete():
            dialog.destroy()
            event_id = self.row_to_event_id.get(row)
            if event_id:
                thread = threading.Thread(target=self._delete_bg, args=(row, event_id))
                thread.daemon = True
                thread.start()
            else:
                self._delete_success(row)

        ctk.CTkButton(buttons_frame, text="Удалить", font=("Advent Pro", 14, "bold"), fg_color="#986722", hover_color=self.hover_color, command=confirm_delete).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Отмена", font=("Advent Pro", 14, "bold"), fg_color="#986722", hover_color=self.hover_color, command=dialog.destroy).pack(side="left", padx=5)

    def _delete_bg(self, row, event_id):
        try:
            res = delete_event(event_id)
            if res is not None and res is not False:
                self.after(0, self._delete_success, row)
            else:
                self.after(0, lambda: messagebox.showerror("Ошибка", "Не удалось удалить запись из БД"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка: {e}"))

    def _delete_success(self, row):
        if row in self.table_data:
            for col in self.columns[:-1]:
                self.table_data[row][col] = ""
        if self.editing_row == row:
            self.editing_row = None
        
        if row in self.row_to_event_id:
            del self.row_to_event_id[row]
            
        self.draw_table()
        self.load_data()

    # ==========================================
    # ИНФО И ДОБАВЛЕНИЕ
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

        ctk.CTkLabel(header, text="ⓘ", font=("Advent Pro", 30), text_color="black").place(x=18, y=18)
        title_entry = ctk.CTkEntry(header, width=280, height=50, fg_color="#C9A646", border_width=0, text_color="black", font=("Advent Pro", 22))
        title_entry.place(x=70, y=20)
        title_entry.insert(0, self.table_data.get(row, {}).get("Название", ""))
        title_entry.configure(state="readonly")
        ctk.CTkButton(header, text="✕", width=25, height=25, fg_color="transparent", hover_color=self.hover_color, text_color="black", font=("Advent Pro", 24), command=info_window.destroy).place(x=420, y=10)

        form_frame = ctk.CTkFrame(info_window, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        for col in self.columns[:-1]:
            ctk.CTkLabel(form_frame, text=f"{col}:", font=("Advent Pro", 14, "bold"), text_color="black").pack(anchor="w", pady=(10, 2))
            ctk.CTkLabel(form_frame, text=self.table_data.get(row, {}).get(col, ""), font=("Advent Pro", 14), text_color="#333333", wraplength=400, justify="left").pack(anchor="w", pady=(0, 5))

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