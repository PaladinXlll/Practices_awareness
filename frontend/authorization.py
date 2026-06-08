import threading
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_functions import authorize_user


# ==========================================
# НАСТРОЙКА
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

ctk.set_widget_scaling(1)
ctk.set_window_scaling(1)


# ==========================================
# ГРАДИЕНТ
# ==========================================

def create_gradient_image(
    width,
    height,
    radius=0,
    color1="#C9AE6D",
    color2="#A8731F"
):

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

        for y in range(height):

            draw_pixel = True

            if radius > 0:

                # Левый верхний угол
                if x < radius and y < radius:
                    dist = math.sqrt((radius - x) ** 2 + (radius - y) ** 2)
                    if dist > radius:
                        draw_pixel = False

                # Правый верхний угол
                if x >= width - radius and y < radius:
                    dist = math.sqrt((x - (width - radius)) ** 2 + (radius - y) ** 2)
                    if dist > radius:
                        draw_pixel = False

                # Левый нижний угол
                if x < radius and y >= height - radius:
                    dist = math.sqrt((radius - x) ** 2 + (height - radius - y) ** 2)
                    if dist > radius:
                        draw_pixel = False

                # Правый нижний угол
                if x >= width - radius and y >= height - radius:
                    dist = math.sqrt((x - (width - radius)) ** 2 + (height - radius - y) ** 2)
                    if dist > radius:
                        draw_pixel = False

            if draw_pixel:
                draw.point((x, y), fill=(r, g, b, 255))

    return ImageTk.PhotoImage(image)


# ==========================================
# ГЛАВНОЕ ОКНО
# ==========================================

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Practices Awareness")
        self.geometry("1280x910")
        self.configure(fg_color="#E9DCB0")

        # ==========================================
        # HEADER
        # ==========================================

        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="#986722",
            height=80,
            corner_radius=0
        )

        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        # ==========================================
        # ЛОГОТИП
        # ==========================================

        self.logo_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color="transparent"
        )

        self.logo_frame.pack(side="left", padx=20)

        self.logo1 = ctk.CTkLabel(
            self.logo_frame,
            text="PRACTICES",
            text_color="white",
            font=("Bayon", 30, "bold")
        )

        self.logo1.pack(anchor="w")

        self.logo2 = ctk.CTkLabel(
            self.logo_frame,
            text="AWARENESS",
            text_color="white",
            font=("Bayon", 30, "bold")
        )

        self.logo2.pack(anchor="w", padx=(90, 0))

        # ==========================================
        # ЛОГОТИП
        # ==========================================

        try:

            logo_path = "frontend/assets/logo.png"

            if os.path.exists(logo_path):

                image = Image.open(logo_path)
                image = image.resize((120, 120))

                self.logo_img = ImageTk.PhotoImage(image)

                self.logo_label = tk.Label(
                    self.header_frame,
                    image=self.logo_img,
                    bg="#986722",
                    bd=0
                )

                self.logo_label.pack(side="right", padx=20)

        except Exception as e:
            print(e)

        # ==========================================
        # КОНТЕЙНЕР
        # ==========================================

        self.container = ctk.CTkFrame(
            self,
            fg_color="#E9DCB0",
            corner_radius=0
        )

        self.container.pack(fill="both", expand=True)

        self.show_login()

    def show_login(self):

        for widget in self.container.winfo_children():
            widget.destroy()

        LoginFrame(
            self.container,
            self.show_dashboard
        ).pack(fill="both", expand=True)

    def show_dashboard(self):

        for widget in self.container.winfo_children():
            widget.destroy()

        DashboardFrame(
            self.container
        ).pack(fill="both", expand=True)


# ==========================================
# LOGIN
# ==========================================

class LoginFrame(ctk.CTkFrame):

    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color="#E9DCB0")

        self.on_login_success = on_login_success

        card_width = 510
        card_height = 518

        # ==========================================
        # КАРТОЧКА
        # ==========================================

        self.card = ctk.CTkFrame(
            self,
            width=card_width,
            height=card_height,
            fg_color="#F2F2F2",
            corner_radius=0
        )

        self.card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.card.pack_propagate(False)
        self.card.grid_propagate(False)

        # ==========================================
        # HEADER ГРАДИЕНТ
        # ==========================================

        header_height = 110

        self.header_canvas = tk.Canvas(
            self.card,
            height=header_height,
            highlightthickness=0,
            bd=0,
            bg="#F2F2F2"
        )

        self.header_canvas.place(
            x=0,
            y=0,
            relwidth=1,
            height=header_height
        )

        def draw_header(event=None):
            real_width = self.card.winfo_width()

            if real_width <= 1:
                return

            self.header_image = create_gradient_image(
                real_width,
                header_height,
                radius=0
            )

            self.header_canvas.delete("all")

            self.header_canvas.create_image(
                0,
                0,
                anchor="nw",
                image=self.header_image
            )

            self.header_canvas.create_text(
                real_width // 2,
                header_height // 2,
                text="Авторизация",
                fill="white",
                font=("Advent Pro", 50)
            )

        self.card.bind("<Configure>", draw_header)

        # ==========================================
        # ЛОГИН
        # ==========================================

        self.entry_log = ctk.CTkEntry(
            self.card,
            width=408,
            height=73,
            placeholder_text="Логин",
            font=("Advent Pro", 28),
            corner_radius=30,
            border_width=2,
            border_color="#555555",
            fg_color="#F2F2F2",
            text_color="black"
        )

        self.entry_log.place(
            relx=0.5,
            y=180,
            anchor="center"
        )

        # ==========================================
        # ПАРОЛЬ
        # ==========================================

        self.entry_pass = ctk.CTkEntry(
            self.card,
            width=408,
            height=73,
            placeholder_text="Пароль",
            font=("Advent Pro", 28),
            corner_radius=30,
            border_width=2,
            border_color="#555555",
            fg_color="#F2F2F2",
            text_color="black",
            show="*"
        )

        self.entry_pass.place(
            relx=0.5,
            y=290,
            anchor="center"
        )

        # ==========================================
        # ОШИБКА
        # ==========================================

        self.error_label = ctk.CTkLabel(
            self.card,
            text="",
            text_color="red",
            font=("Advent Pro", 18),
            fg_color="transparent"
        )

        self.error_label.place(
            relx=0.5,
            y=360,
            anchor="center"
        )

        # ==========================================
        # КНОПКА
        # ==========================================

        btn_width = 470
        btn_height = 80

        self.btn_image = create_gradient_image(
            btn_width,
            btn_height,
            radius=30
        )

        self.btn_canvas = tk.Canvas(
            self.card,
            width=btn_width,
            height=btn_height,
            highlightthickness=0,
            bd=0,
            bg="#F2F2F2"
        )

        self.btn_canvas.place(
            relx=0.5,
            y=440,
            anchor="center"
        )

        self.btn_canvas.create_image(
            0,
            0,
            anchor="nw",
            image=self.btn_image
        )

        # ==========================================
        # ТЕКСТ КНОПКИ БЕЗ ФОНА
        # ==========================================

        self.btn_canvas.create_text(
            btn_width // 2,
            btn_height // 2,
            text="Вход",
            fill="white",
            font=("Advent Pro", 36)
        )

        self.btn_canvas.bind(
            "<Button-1>",
            lambda e: self.check_credentials()
        )

        self.btn_canvas.configure(cursor="hand2")

    # ==========================================
    # ПРОВЕРКА
    # ==========================================

    def check_credentials(self):

        login = self.entry_log.get()
        password = self.entry_pass.get()

        self.error_label.configure(
            text="Проверка..."
        )

        def auth_task():

            user = authorize_user(login, password)

            self.after(
                0,
                lambda: self.handle_auth_result(user)
            )
        threading.Thread(
            target=auth_task,
            daemon=True
        ).start()

    def handle_auth_result(self, user):

        if user:

            self.on_login_success()

        else:

            self.error_label.configure(
                text="Неверный логин или пароль"
            )

# ==========================================
# DASHBOARD
# ==========================================

class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#DCCB98")

        label = ctk.CTkLabel(
            self,
            text="Добро пожаловать!",
            font=("Advent Pro", 40, "bold"),
            text_color="#986722"
        )

        label.pack(expand=True)


# ==========================================
# ЗАПУСК
# ==========================================

if __name__ == "__main__":

    app = App()
    app.mainloop()
