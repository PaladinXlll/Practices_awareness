import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os

# ==========================================
# НАСТРОЙКА ТЕМЫ
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
        self.minsize(1000, 700)

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

            image_path = "C:/Users/vostr/OneDrive/Desktop/Subtract1.png"

            if os.path.exists(image_path):

                image = Image.open(image_path)
                image = image.resize((100, 50))

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
        # КНОПКА НАЗАД
        # ==========================================

        back_image = Image.open(
            "C:/Users/vostr/OneDrive/Desktop/выход.png"
        )

        self.back_icon = ctk.CTkImage(
            light_image=back_image,
            dark_image=back_image,
            size=(32, 32)
        )

        back_btn = ctk.CTkButton(
            top_bar,
            image=self.back_icon,
            text="",
            width=40,
            fg_color="transparent",
            hover_color="#C8B57E"
        )

        back_btn.pack(
            side="left",
            padx=(10, 5),
            pady=5
        )

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
        # КНОПКА ДОБАВИТЬ
        # ==========================================

        add_image = Image.open(
            "C:/Users/vostr/OneDrive/Desktop/добавить.png"
        )

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

        add_btn.pack(
            side="right",
            padx=15
        )

        # ==========================================
        # ПРОКРУЧИВАЕМАЯ ТАБЛИЦА
        # ==========================================

        table_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#E6D7A8",
            corner_radius=15
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.table_frame = table_frame
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

        widths = [180, 220, 220, 150, 150, 220, 220, 120]

        # ==========================================
        # ЗАГОЛОВКИ
        # ==========================================

        for i, col in enumerate(columns):

            header = ctk.CTkLabel(
                table_frame,
                text=col,
                font=("Arial", 18, "bold"),
                text_color="#2B2B2B",
                fg_color="#D9C998",
                corner_radius=0,
                height=45
            )

            header.grid(
                row=0,
                column=i,
                sticky="nsew",
                ipadx=10,
                ipady=10
            )

            table_frame.grid_columnconfigure(
                i,
                weight=1,
                minsize=widths[i]
            )

        # ==========================================
        # СТАРТОВЫЕ СТРОКИ
        # ==========================================

        for _ in range(10):
            self.create_row()

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
                border_color="#7A6A45"
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
                    font=("Arial", 18),
                    state="disabled"
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
                # КНОПКА РЕДАКТИРОВАНИЯ
                # ==========================================

                edit_image = Image.open(
                    "C:/Users/vostr/OneDrive/Desktop/редактор.png"
                )

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
                    command=lambda r=row: self.show_edit_dialog(r)
                )

                edit_btn.pack(
                    side="left",
                    padx=(5, 2),
                    pady=5
                )

                # ==========================================
                # КНОПКА УДАЛЕНИЯ
                # ==========================================

                delete_image = Image.open(
                    "C:/Users/vostr/OneDrive/Desktop/icons8-удалить-24 1.png"
                )

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
                    command=lambda r=row: self.show_delete_dialog(r)
                )

                delete_btn.pack(
                    side="left",
                    padx=2,
                    pady=5
                )

            # ==========================================
            # ОСТАЛЬНЫЕ КОЛОНКИ
            # ==========================================

            else:

                entry = ctk.CTkEntry(
                    cell_frame,
                    fg_color="#E9DCB0",
                    border_width=0,
                    text_color="black",
                    font=("Arial", 18),
                    state="disabled"
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
    # СОЗДАТЬ НОВУЮ СТРОКУ
    # ==========================================

    def create_new_row(self, dialog):

        self.create_row()
        dialog.destroy()

    # ==========================================
    # ОКНО СОЗДАНИЯ
    # ==========================================

    def show_create_dialog(self):

        dialog = ctk.CTkToplevel(self)

        dialog.geometry("250x186")
        dialog.resizable(False, False)
        dialog.title("Создать")

        dialog.configure(fg_color="#DDD0A4")

        header = ctk.CTkFrame(
            dialog,
            height=38,
            fg_color="#C7A545",
            corner_radius=0
        )

        header.pack(fill="x")

        title = ctk.CTkLabel(
            header,
            text="Создать",
            font=("Arial", 24),
            text_color="#333333"
        )

        title.place(relx=0.5, rely=0.5, anchor="center")

        text_label = ctk.CTkLabel(
            dialog,
            text="Сохранить изменения",
            font=("Arial", 20),
            text_color="#444444"
        )

        text_label.pack(pady=35)

        bottom = ctk.CTkFrame(
            dialog,
            height=45,
            fg_color="#D6C79A",
            corner_radius=0
        )

        bottom.pack(side="bottom", fill="x")

        save_btn = ctk.CTkButton(
            bottom,
            text="Сохранить",
            width=125,
            height=45,
            fg_color="#D6C79A",
            hover_color="#C7B887",
            text_color="#555555",
            corner_radius=0,
            command=lambda: self.create_new_row(dialog)
        )

        save_btn.pack(side="left")

        separator = tk.Frame(
            bottom,
            width=1,
            bg="#8F845D"
        )

        separator.pack(side="left", fill="y")

        cancel_btn = ctk.CTkButton(
            bottom,
            text="Отмена",
            width=125,
            height=45,
            fg_color="#D6C79A",
            hover_color="#C7B887",
            text_color="#777777",
            corner_radius=0,
            command=dialog.destroy
        )

        cancel_btn.pack(side="left")

    # ==========================================
    # ОКНО РЕДАКТИРОВАНИЯ
    # ==========================================

    def show_edit_dialog(self, row):

        dialog = ctk.CTkToplevel(self)

        dialog.geometry("250x186")
        dialog.resizable(False, False)
        dialog.title("Редактирование")

        dialog.configure(fg_color="#DDD0A4")

        header = ctk.CTkFrame(
            dialog,
            height=38,
            fg_color="#C7A545",
            corner_radius=0
        )

        header.pack(fill="x")

        title = ctk.CTkLabel(
            header,
            text="Редактировать",
            font=("Arial", 24),
            text_color="#333333"
        )

        title.place(relx=0.5, rely=0.5, anchor="center")

        text_label = ctk.CTkLabel(
            dialog,
            text="Сохранить изменения",
            font=("Arial", 20),
            text_color="#444444"
        )

        text_label.pack(pady=40)

        bottom = ctk.CTkFrame(
            dialog,
            height=45,
            fg_color="#D6C79A",
            corner_radius=0
        )

        bottom.pack(side="bottom", fill="x")

        save_btn = ctk.CTkButton(
            bottom,
            text="Сохранить",
            width=125,
            height=45,
            fg_color="#D6C79A",
            hover_color="#C7B887",
            text_color="#555555",
            corner_radius=0,
            command=lambda: self.enable_row_editing(row, dialog)
        )

        save_btn.pack(side="left")

        separator = tk.Frame(
            bottom,
            width=1,
            bg="#8F845D"
        )

        separator.pack(side="left", fill="y")

        cancel_btn = ctk.CTkButton(
            bottom,
            text="Отмена",
            width=125,
            height=45,
            fg_color="#D6C79A",
            hover_color="#C7B887",
            text_color="#777777",
            corner_radius=0,
            command=dialog.destroy
        )

        cancel_btn.pack(side="left")

    # ==========================================
    # ВКЛЮЧИТЬ РЕДАКТИРОВАНИЕ
    # ==========================================

    def enable_row_editing(self, row, dialog):

        for entry in self.row_entries[row]:
            entry.configure(state="normal")

        dialog.destroy()

    # ==========================================
    # ОКНО УДАЛЕНИЯ
    # ==========================================

    def show_delete_dialog(self, row):

        dialog = ctk.CTkToplevel(self)

        dialog.geometry("250x186")
        dialog.resizable(False, False)
        dialog.title("Удаление")

        dialog.configure(fg_color="#DDD0A4")

        # HEADER

        header = ctk.CTkFrame(
            dialog,
            height=38,
            fg_color="#C7A545",
            corner_radius=0
        )

        header.pack(fill="x")

        title = ctk.CTkLabel(
            header,
            text="Удалить",
            font=("Arial", 24),
            text_color="#333333"
        )

        title.place(relx=0.5, rely=0.5, anchor="center")

      

        # ТЕКСТ

        text_label = ctk.CTkLabel(
            dialog,
            text="Удалить информацию",
            font=("Arial", 20),
            text_color="#444444"
        )

        text_label.pack(pady=(0, 60))

        # НИЖНЯЯ ПАНЕЛЬ

        bottom = ctk.CTkFrame(
            dialog,
            height=45,
            fg_color="#D6C79A",
            corner_radius=0
        )

        bottom.pack(side="bottom", fill="x")

        # УДАЛИТЬ

        delete_btn = ctk.CTkButton(
            bottom,
            text="Удалить",
            width=125,
            height=45,
            fg_color="#D6C79A",
            hover_color="#C7B887",
            text_color="#555555",
            corner_radius=0,
            command=lambda: self.delete_row(row, dialog)
        )

        delete_btn.pack(side="left")

        # РАЗДЕЛИТЕЛЬ

        separator = tk.Frame(
            bottom,
            width=1,
            bg="#8F845D"
        )

        separator.pack(side="left", fill="y")

        # ОТМЕНА

        cancel_btn = ctk.CTkButton(
            bottom,
            text="Отмена",
            width=125,
            height=45,
            fg_color="#D6C79A",
            hover_color="#C7B887",
            text_color="#777777",
            corner_radius=0,
            command=dialog.destroy
        )

        cancel_btn.pack(side="left")

    # ==========================================
    # УДАЛЕНИЕ СТРОКИ
    # ==========================================

    def delete_row(self, row, dialog):

        widgets = self.table_frame.grid_slaves(row=row)

        for widget in widgets:
            widget.destroy()

        if row in self.row_entries:
            del self.row_entries[row]

        dialog.destroy()

    # ==========================================
    # ОКНО ИНФОРМАЦИИ
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

        line = tk.Frame(
            info_window,
            bg="#9E7B27",
            height=1
        )

        line.pack(fill="x")

        content = ctk.CTkFrame(
            info_window,
            fg_color="#D4B45F",
            corner_radius=0
        )

        content.pack(fill="both", expand=True)

        desc_title = ctk.CTkLabel(
            content,
            text="Описание:",
            font=("Arial", 22),
            text_color="black"
        )

        desc_title.pack(anchor="w", padx=20, pady=(22, 10))

        desc_textbox = ctk.CTkTextbox(
            content,
            width=400,
            height=200,
            fg_color="#D4B45F",
            text_color="black",
            border_width=0,
            font=("Arial", 16)
        )

        desc_textbox.pack(
            padx=20,
            fill="x"
        )

        separator = tk.Frame(
            content,
            bg="#9E7B27",
            height=1
        )

        separator.pack(fill="x", padx=20, pady=28)

        teacher_title = ctk.CTkLabel(
            content,
            text="Преподаватели:",
            font=("Arial", 22),
            text_color="black"
        )

        teacher_title.pack(anchor="w", padx=20, pady=(0, 15))

        teachers_textbox = ctk.CTkTextbox(
            content,
            width=400,
            height=120,
            fg_color="#D4B45F",
            text_color="black",
            border_width=0,
            font=("Arial", 16)
        )

        teachers_textbox.pack(
            padx=20,
            pady=(0, 20),
            fill="x"
        )


# ==========================================
# ЗАПУСК
# ==========================================

if __name__ == "__main__":

    app = App()
    app.mainloop()