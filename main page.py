import customtkinter as ctk
import tkinter as tk
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
            font=("Arial", 32, "bold")
        )

        logo1.pack(anchor="w")

        logo2 = ctk.CTkLabel(
            logo_frame,
            text="AWARENESS",
            text_color="white",
            font=("Arial", 32, "bold")
        )

        logo2.pack(anchor="w", padx=(90, 0))

        # ==========================================
        # ЛОГОТИП СПРАВА
        # ==========================================

        try:

            image_path = "assets/logo.png"

            if os.path.exists(image_path):

                image = Image.open(image_path)
                image = image.resize((150, 150))

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
# DASHBOARD
# ==========================================

class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#DCCB98")

        self.row_entries = {}

        # ==========================================
        # ВЕРХНЯЯ ПАНЕЛЬ
        # ==========================================

        top_bar = ctk.CTkFrame(
            self,
            height=60,
            fg_color="#D6C189",
            corner_radius=0
        )

        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        # ==========================================
        # ИКОНКА ВЫХОДА
        # ==========================================

        exit_path = "assets/exit.png"

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
                font=("Arial", 24),
                command=self.show_exit_dialog
            )

        exit_btn.pack(side="left", padx=(10, 5), pady=5)

        # ==========================================
        # ЗАГОЛОВОК
        # ==========================================

        title_label = ctk.CTkLabel(
            top_bar,
            text="Главная страница",
            font=("Arial", 28, "bold"),
            text_color="black"
        )

        title_label.pack(side="left", padx=10)

        # ==========================================
        # КНОПКА СОЗДАНИЯ
        # ==========================================

        add_path = "assets/create.png"

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
                command=self.show_create_dialog
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
                command=self.show_create_dialog
            )

        add_btn.pack(side="right", padx=15)

        # ==========================================
        # ОБЛАСТЬ ТАБЛИЦЫ
        # ==========================================

        container = tk.Frame(self, bg="#DCCB98")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(
            container,
            bg="#E6D7A8",
            highlightthickness=0
        )

        self.canvas.pack(side="left", fill="both", expand=True)

        # ==========================================
        # ВЕРТИКАЛЬНЫЙ СКРОЛЛ
        # ==========================================

        y_scrollbar = ctk.CTkScrollbar(
            container,
            orientation="vertical",
            command=self.canvas.yview
        )

        y_scrollbar.pack(side="right", fill="y")

        # ==========================================
        # ГОРИЗОНТАЛЬНЫЙ СКРОЛЛ
        # ==========================================

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

        # ==========================================
        # ТАБЛИЦА
        # ==========================================

        self.table_frame = ctk.CTkFrame(
            self.canvas,
            fg_color="#E6D7A8",
            corner_radius=15
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.table_frame,
            anchor="nw"
        )

        self.table_frame.bind(
            "<Configure>",
            self.update_scrollregion
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_canvas
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_wheel
        )

        self.current_row = 1

        columns = [
            "Название",
            "Место проведения",
            "Мероприятие",
            "Уровень",
            "Дата",
            "Контроль",
            "Документы",
            ""
        ]

        widths = [250, 300, 300, 180, 180, 250, 250, 140]

        # ==========================================
        # ЗАГОЛОВКИ
        # ==========================================

        for i, col in enumerate(columns):

            header = ctk.CTkLabel(
                self.table_frame,
                text=col,
                font=("Arial", 18, "bold"),
                text_color="#2B2B2B",
                fg_color="#D9C998",
                corner_radius=0,
                height=45,
                width=widths[i]
            )

            header.grid(
                row=0,
                column=i,
                sticky="nsew",
                ipadx=10,
                ipady=10
            )

            self.table_frame.grid_columnconfigure(
                i,
                weight=1,
                minsize=widths[i]
            )

        # ==========================================
        # СТРОКИ
        # ==========================================

        for _ in range(10):
            self.create_row()

    # ==========================================
    # SCROLL
    # ==========================================

    def update_scrollregion(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_canvas(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            height=max(
                event.height,
                self.table_frame.winfo_reqheight()
            )
        )

    def mouse_wheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==========================================
    # СОЗДАНИЕ СТРОКИ
    # ==========================================

    def create_row(self):

        row = self.current_row
        columns_count = 8

        self.row_entries[row] = []

        for col in range(columns_count):

            cell_frame = ctk.CTkFrame(
                self.table_frame,
                fg_color="#E9DCB0",
                corner_radius=0,
                border_width=1,
                border_color="#7A6A45",
                width=200,
                height=50
            )

            cell_frame.grid(
                row=row,
                column=col,
                sticky="nsew"
            )

            # ==========================================
            # ПЕРВАЯ КОЛОНКА
            # ==========================================

            if col == 0:

                info_path = "assets/info.png"

                if os.path.exists(info_path):

                    info_image = Image.open(info_path)

                    self.info_icon = ctk.CTkImage(
                        light_image=info_image,
                        dark_image=info_image,
                        size=(26, 26)
                    )

                    info_button = ctk.CTkButton(
                        cell_frame,
                        image=self.info_icon,
                        text="",
                        width=28,
                        height=28,
                        fg_color="transparent",
                        hover_color="#D5C28E",
                        command=lambda r=row: self.show_info(r)
                    )

                else:

                    info_button = ctk.CTkButton(
                        cell_frame,
                        text="ⓘ",
                        width=28,
                        height=28,
                        fg_color="transparent",
                        hover_color="#D5C28E",
                        text_color="black",
                        font=("Arial", 18),
                        command=lambda r=row: self.show_info(r)
                    )

                info_button.pack(
                    side="left",
                    padx=(5, 2),
                    pady=5
                )

                entry = ctk.CTkEntry(
                    cell_frame,
                    fg_color="#E9DCB0",
                    border_width=0,
                    text_color="black",
                    font=("Arial", 18)
                )

                entry.pack(
                    side="left",
                    fill="both",
                    expand=True,
                    padx=(0, 5),
                    pady=5
                )

                self.row_entries[row].append(entry)

            # ==========================================
            # ПОСЛЕДНЯЯ КОЛОНКА
            # ==========================================

            elif col == columns_count - 1:

                # ==========================================
                # РЕДАКТИРОВАНИЕ
                # ==========================================

                edit_path = "assets/edit.png"

                if os.path.exists(edit_path):

                    edit_image = Image.open(edit_path)

                    self.edit_icon = ctk.CTkImage(
                        light_image=edit_image,
                        dark_image=edit_image,
                        size=(28, 28)
                    )

                    edit_btn = ctk.CTkButton(
                        cell_frame,
                        image=self.edit_icon,
                        text="",
                        width=34,
                        height=34,
                        fg_color="transparent",
                        hover_color="#D5C28E",
                        command=lambda r=row: self.edit_row(r)
                    )

                else:

                    edit_btn = ctk.CTkButton(
                        cell_frame,
                        text="✎",
                        width=34,
                        height=34,
                        fg_color="transparent",
                        hover_color="#D5C28E",
                        text_color="black",
                        font=("Arial", 18),
                        command=lambda r=row: self.edit_row(r)
                    )

                edit_btn.pack(
                    side="left",
                    padx=(5, 2),
                    pady=5
                )

                # ==========================================
                # УДАЛЕНИЕ
                # ==========================================

                delete_path = "assets/delete.png"

                if os.path.exists(delete_path):

                    delete_image = Image.open(delete_path)

                    self.delete_icon = ctk.CTkImage(
                        light_image=delete_image,
                        dark_image=delete_image,
                        size=(28, 28)
                    )

                    delete_btn = ctk.CTkButton(
                        cell_frame,
                        image=self.delete_icon,
                        text="",
                        width=34,
                        height=34,
                        fg_color="transparent",
                        hover_color="#D5C28E",
                        command=lambda r=row: self.delete_row(r)
                    )

                else:

                    delete_btn = ctk.CTkButton(
                        cell_frame,
                        text="🗑",
                        width=34,
                        height=34,
                        fg_color="transparent",
                        hover_color="#D5C28E",
                        text_color="black",
                        font=("Arial", 18),
                        command=lambda r=row: self.delete_row(r)
                    )

                delete_btn.pack(
                    side="left",
                    padx=2,
                    pady=5
                )

            else:

                entry = ctk.CTkEntry(
                    cell_frame,
                    fg_color="#E9DCB0",
                    border_width=0,
                    text_color="black",
                    font=("Arial", 18)
                )

                entry.pack(
                    fill="both",
                    expand=True,
                    padx=5,
                    pady=5
                )

                self.row_entries[row].append(entry)

        self.current_row += 1

    # ==========================================
    # УВЕДОМЛЕНИЯ
    # ==========================================

    def custom_dialog(self, title, text, confirm_text, command):

        dialog = ctk.CTkToplevel(self)

        dialog.geometry("250x185")
        dialog.resizable(False, False)
        dialog.title(title)

        dialog.grab_set()

        # HEADER

        header = ctk.CTkFrame(
            dialog,
            height=40,
            fg_color="#C9A646",
            corner_radius=0
        )

        header.pack(fill="x")

        header_label = ctk.CTkLabel(
            header,
            text=title,
            font=("Arial", 16),
            text_color="black"
        )

        header_label.pack(expand=True)

        # TEXT

        text_label = ctk.CTkLabel(
            dialog,
            text=text,
            font=("Arial", 14),
            text_color="#444444",
            wraplength=200
        )

        text_label.pack(expand=True)

        # BUTTONS

        buttons = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        buttons.pack(fill="x")

        confirm_btn = ctk.CTkButton(
            buttons,
            text=confirm_text,
            width=125,
            height=45,
            corner_radius=0,
            fg_color="#D8CCA3",
            hover_color="#C8B57E",
            text_color="#555555",
            command=lambda: [command(), dialog.destroy()]
        )

        confirm_btn.pack(side="left")

        cancel_btn = ctk.CTkButton(
            buttons,
            text="Отмена",
            width=125,
            height=45,
            corner_radius=0,
            fg_color="#D8CCA3",
            hover_color="#C8B57E",
            text_color="#777777",
            command=dialog.destroy
        )

        cancel_btn.pack(side="right")

    # ==========================================
    # СОЗДАТЬ
    # ==========================================

    def show_create_dialog(self):

        self.custom_dialog(
            "Создать",
            "Сохранить изменения",
            "Сохранить",
            self.create_row
        )

    # ==========================================
    # РЕДАКТИРОВАТЬ
    # ==========================================

    def edit_row(self, row):

        self.custom_dialog(
            "Редактировать",
            "Сохранить изменения",
            "Сохранить",
            lambda: None
        )

    # ==========================================
    # УДАЛИТЬ
    # ==========================================

    def delete_row(self, row):

        def remove():

            widgets = self.table_frame.grid_slaves(row=row)

            for widget in widgets:
                widget.destroy()

            if row in self.row_entries:
                del self.row_entries[row]

        self.custom_dialog(
            "Удалить",
            "Удалить информацию",
            "Удалить",
            remove
        )

    # ==========================================
    # ВЫХОД
    # ==========================================

    def show_exit_dialog(self):

        self.custom_dialog(
            "Выход",
            "Вы точно хотите\nвыйти?",
            "Выход",
            self.master.destroy
        )

    # ==========================================
    # ИНФОРМАЦИЯ
    # ==========================================

    def show_info(self, row):

        info_window = ctk.CTkToplevel(self)

        info_window.geometry("467x610")
        info_window.title("Информация")
        info_window.configure(fg_color="#D4B45F")

        info_window.resizable(False, False)

        header = ctk.CTkFrame(
            info_window,
            width=467,
            height=108,
            fg_color="#C9A646",
            corner_radius=0
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            header,
            text="ⓘ",
            font=("Arial", 30),
            text_color="black"
        )

        icon_label.place(x=18, y=18)

        title_entry = ctk.CTkEntry(
            header,
            width=280,
            height=50,
            fg_color="#C9A646",
            border_width=0,
            text_color="black",
            font=("Arial", 22)
        )

        title_entry.place(x=70, y=20)

        close_btn = ctk.CTkButton(
            header,
            text="✕",
            width=25,
            height=25,
            fg_color="transparent",
            hover_color="#B89435",
            text_color="black",
            font=("Arial", 24),
            command=info_window.destroy
        )

        close_btn.place(x=420, y=10)


# ==========================================
# ЗАПУСК
# ==========================================

if __name__ == "__main__":

    app = App()
    app.mainloop()