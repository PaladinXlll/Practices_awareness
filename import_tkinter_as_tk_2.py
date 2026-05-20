import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math
import os

# Настройка внешнего вида
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def create_gradient_image(
    width,
    height,
    radius=0,
    only_top=False,
    color1="#C4A86A",
    color2="#986722",
    text=""
):
    """Создает изображение с горизонтальным градиентом"""

    if width <= 0:
        width = 510

    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    for x in range(width):

        ratio = x / width

        r1 = int(color1[1:3], 16)
        g1 = int(color1[3:5], 16)
        b1 = int(color1[5:7], 16)

        r2 = int(color2[1:3], 16)
        g2 = int(color2[3:5], 16)
        b2 = int(color2[5:7], 16)

        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)

        for y_coord in range(height):

            draw_pixel = True

            if radius > 0:

                # Верхний левый угол
                if x < radius and y_coord < radius:
                    dist = math.sqrt(
                        (radius - x) ** 2 +
                        (radius - y_coord) ** 2
                    )
                    if dist > radius:
                        draw_pixel = False

                # Верхний правый угол
                if x >= width - radius and y_coord < radius:
                    dist = math.sqrt(
                        (x - (width - radius)) ** 2 +
                        (radius - y_coord) ** 2
                    )
                    if dist > radius:
                        draw_pixel = False

                # Нижний левый угол
                if x < radius and y_coord >= height - radius:
                    dist = math.sqrt(
                        (radius - x) ** 2 +
                        (height - radius - y_coord) ** 2
                    )
                    if dist > radius:
                        draw_pixel = False

                # Нижний правый угол
                if x >= width - radius and y_coord >= height - radius:
                    dist = math.sqrt(
                        (x - (width - radius)) ** 2 +
                        (height - radius - y_coord) ** 2
                    )
                    if dist > radius:
                        draw_pixel = False

            if draw_pixel:
                draw.point((x, y_coord), fill=(r, g, b, 255))

    return ImageTk.PhotoImage(image)


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Practices Awareness")
        self.geometry("1280x910")
        self.minsize(800, 700)
        self.configure(fg_color="#E9DCB0")

        # Верхняя панель
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="#986722",
            height=99,
            corner_radius=0
        )

        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        # Логотип слева
        self.logo_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color="transparent"
        )

        self.logo_frame.pack(side="left", padx=20, pady=10)

        self.logo_line1 = ctk.CTkLabel(
            self.logo_frame,
            text="PRACTICES",
            text_color="white",
            font=("Bayon", 32)
        )

        self.logo_line1.pack(anchor="w")

        self.logo_line2 = ctk.CTkLabel(
            self.logo_frame,
            text="AWARENESS",
            text_color="white",
            font=("Bayon", 32)
        )

        self.logo_line2.pack(anchor="w", padx=(100, 0))

        # Логотип справа
        try:

            logo_path = "C:/Users/vostr/OneDrive/Desktop/Subtract1.png"

            if os.path.exists(logo_path):

                logo_image = Image.open(logo_path)

                logo_image = logo_image.resize(
                    (98, 45),
                    Image.LANCZOS
                )

                self.logo_photo = ImageTk.PhotoImage(logo_image)

                self.logo_label_img = tk.Label(
                    self.header_frame,
                    image=self.logo_photo,
                    bg="#986722",
                    bd=0
                )

                self.logo_label_img.pack(
                    side="right",
                    padx=(0, 20),
                    pady=15
                )

            else:
                raise FileNotFoundError

        except Exception as e:

            print("Ошибка загрузки логотипа:", e)

            self.logo_label_img = tk.Label(
                self.header_frame,
                text="📚",
                font=("Arial", 40),
                fg="white",
                bg="#986722"
            )

            self.logo_label_img.pack(
                side="right",
                padx=(0, 20),
                pady=15
            )

        # Контейнер
        self.container = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0
        )

        self.container.pack(fill="both", expand=True)

        self.show_login()

    def show_login(self):

        self.clear_container()

        self.login_view = LoginFrame(
            self.container,
            self.show_dashboard
        )

        self.login_view.pack(fill="both", expand=True)

    def show_dashboard(self):

        self.clear_container()

        self.dashboard_view = DashboardFrame(self.container)

        self.dashboard_view.pack(fill="both", expand=True)

    def clear_container(self):

        for widget in self.container.winfo_children():
            widget.destroy()


class LoginFrame(ctk.CTkFrame):

    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color="#E9DCB0")

        self.on_login_success = on_login_success

        card_width = 510
        card_height = 518

        # Карточка без скругления
        self.card = ctk.CTkFrame(
            self,
            width=card_width,
            height=card_height,
            fg_color="white",
            corner_radius=0
        )

        self.card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.card.update_idletasks()

        actual_width = self.card.winfo_width()

        if actual_width <= 0:
            actual_width = card_width

        # Верхний градиент
        header_height = 106

        self.header_image = create_gradient_image(
            actual_width,
            header_height,
            radius=0
        )

        self.header_label = tk.Label(
            self.card,
            image=self.header_image,
            bd=0
        )

        self.header_label.image = self.header_image

        self.header_label.place(
            x=0,
            y=0,
            width=actual_width,
            height=header_height
        )

        #Заголовок
        title_label = tk.Label(
            self.header_label,
            text="Авторизация",
            font=("Advent Pro", 50),
            fg="white",
            bg="#B78A3A",
            bd=0
        )
        # self.title_canvas.create_text(
        #             200, 35, # 50% от ширины и высоты для центровки
        #             text="Авторизация",
        #             fill="white",
        #             font=("Arial", 22, "bold")
        #         )
        title_label.place(
            relx=0.5,
            y=55,
            anchor="center"
        )

        # Поле логина
        self.entry_log = ctk.CTkEntry(
            self.card,
            width=410,
            height=74,
            placeholder_text="Логин",
            font=("Advent Pro", 25),
            corner_radius=20,
            border_width=2,
            border_color="#4D4C4A",
            fg_color="white",
            text_color="#333333"
        )

        self.entry_log.place(x=50, y=150)

        self.entry_log.bind(
            "<Return>",
            lambda e: self.entry_pass.focus()
        )

        # Поле пароля
        self.entry_pass = ctk.CTkEntry(
            self.card,
            width=410,
            height=74,
            placeholder_text="Пароль",
            font=("Advent Pro", 25),
            corner_radius=20,
            border_width=2,
            border_color="#4D4C4A",
            fg_color="white",
            text_color="#333333",
            show="*"
        )

        self.entry_pass.place(x=50, y=240)

        self.entry_pass.bind(
            "<Return>",
            lambda e: self.check_credentials()
        )

        # Ошибка
        self.error_label = ctk.CTkLabel(
            self.card,
            text="",
            text_color="#E74C3C",
            font=("Advent Pro", 20)
        )

        self.error_label.place(
            x=255,
            y=330,
            anchor="center"
        )

        # =========================
        # КНОПКА СО СКРУГЛЕНИЕМ
        # =========================

        btn_width = 410
        btn_height = 74

        btn_image = create_gradient_image(
            btn_width,
            btn_height,
            radius=20
        )

        btn_label = tk.Label(
            self.card,
            image=btn_image,
            cursor="hand2",
            bd=0
        )

        btn_label.image = btn_image

        btn_label.place(
            x=115,
            y=500,
            width=410,
            height=74
        )

        # Текст кнопки
        btn_text = tk.Label(
            btn_label,
            text="Вход",
            font=("Advent Pro", 35),
            fg="white",
            bg="#B78A3A",
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        )

        btn_text.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # События
        btn_label.bind(
            "<Button-1>",
            lambda e: self.check_credentials()
        )

        btn_text.bind(
            "<Button-1>",
            lambda e: self.check_credentials()
        )

    def check_credentials(self):

        login = self.entry_log.get()
        password = self.entry_pass.get()

        if login == "q" and password == "1":

            self.on_login_success()

        else:

            self.error_label.configure(
                text="Неверный логин или пароль"
            )

            self.entry_log.configure(
                border_color="#E74C3C"
            )

            self.entry_pass.configure(
                border_color="#E74C3C"
            )

            self.after(2000, self.reset_borders)

    def reset_borders(self):

        self.entry_log.configure(
            border_color="#4D4C4A"
        )

        self.entry_pass.configure(
            border_color="#4D4C4A"
        )

        self.error_label.configure(text="")


class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#DCCB98")

        # =========================
        # Верхняя панель навигации
        # =========================

        top_bar = ctk.CTkFrame(
            self,
            height=55,
            fg_color="#D6C189",
            corner_radius=0
        )
        top_bar.pack(fill="x")

        top_bar.pack_propagate(False)

        back_btn = ctk.CTkButton(
            top_bar,
            text="⟲",
            width=40,
            fg_color="transparent",
            hover_color="#C8B57E",
            text_color="black",
            font=("Arial", 22)
        )
        back_btn.pack(side="left", padx=(10, 5), pady=5)

        home_label = ctk.CTkLabel(
            top_bar,
            text="Главная страница",
            font=("Advent Pro", 28, "bold"),
            text_color="black"
        )
        home_label.pack(side="left", padx=10)

        add_btn = ctk.CTkButton(
            top_bar,
            text="⊕",
            width=40,
            fg_color="transparent",
            hover_color="#C8B57E",
            text_color="black",
            font=("Arial", 24)
        )
        add_btn.pack(side="right", padx=15)

        # =========================
        # Таблица
        # =========================

        table_frame = ctk.CTkFrame(
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

        column_widths = [140, 220, 200, 130, 150, 220, 200, 80]

        # =========================
        # Заголовки
        # =========================

        for i, col in enumerate(columns):

            header = ctk.CTkLabel(
                table_frame,
                text=col,
                font=("Advent Pro", 24, "bold"),
                text_color="#2B2B2B",
                fg_color="#D9C998",
                corner_radius=0
            )

            header.grid(
                row=0,
                column=i,
                sticky="nsew",
                ipadx=10,
                ipady=12
            )

            table_frame.grid_columnconfigure(
                i,
                weight=1,
                minsize=column_widths[i]
            )

        # =========================
        # Строки таблицы
        # =========================

        for row in range(1, 14):

            for col in range(len(columns)):

                cell_frame = ctk.CTkFrame(
                    table_frame,
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

                # Первая колонка
                if col == 0:

                    label = ctk.CTkLabel(
                        cell_frame,
                        text="ⓘ",
                        font=("Arial", 22),
                        text_color="black"
                    )

                    label.pack(
                        side="left",
                        padx=10,
                        pady=8
                    )

                # Последняя колонка
                elif col == len(columns) - 1:

                    edit_btn = ctk.CTkButton(
                        cell_frame,
                        text="✎",
                        width=28,
                        height=28,
                        fg_color="transparent",
                        hover_color="#D5C28E",
                        text_color="black",
                        font=("Arial", 18)
                    )

                    edit_btn.pack(
                        side="left",
                        padx=(8, 4),
                        pady=6
                    )

                    delete_btn = ctk.CTkButton(
                        cell_frame,
                        text="⊗",
                        width=28,
                        height=28,
                        fg_color="transparent",
                        hover_color="#D5C28E",
                        text_color="black",
                        font=("Arial", 18)
                    )

                    delete_btn.pack(
                        side="left",
                        padx=4,
                        pady=6
                    )

                else:

                    entry = ctk.CTkEntry(
                        cell_frame,
                        fg_color="#E9DCB0",
                        border_width=0,
                        text_color="black",
                        font=("Advent Pro", 20)
                    )

                    entry.pack(
                        fill="both",
                        expand=True,
                        padx=5,
                        pady=5
                    )

if __name__ == "__main__":

    app = App()
    app.mainloop()
    