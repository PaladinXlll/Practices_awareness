import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("light")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("500x300")

        btn = ctk.CTkButton(
            self,
            text="Открыть",
            command=self.show_info
        )

        btn.pack(pady=100)

    def show_info(self):

        WINDOW_W = 467
        WINDOW_H = 610
        HEADER_H = 108

        info_window = ctk.CTkToplevel(self)

        info_window.geometry(
            f"{WINDOW_W}x{WINDOW_H}"
        )

        info_window.title("Информация")

        info_window.configure(
            fg_color="#D4B45F"
        )

        info_window.resizable(
            False,
            False
        )

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

        left = (221, 194, 108)
        right = (186, 144, 48)

        for x in range(real_width):

            k = x / max(real_width - 1, 1)

            r = int(left[0] + (right[0] - left[0]) * k)
            g = int(left[1] + (right[1] - left[1]) * k)
            b = int(left[2] + (right[2] - left[2]) * k)

            color = f"#{r:02x}{g:02x}{b:02x}"

            header.create_line(
                x,
                0,
                x,
                HEADER_H,
                fill=color
            )

        # иконка
        header.create_text(
            34,
            32,
            text="ⓘ",
            font=("Advent Pro", 24),
            fill="black"
        )

        # header текст
        header.create_text(
            72,
            18,
            anchor="nw",
            text="Новые технологии -\nновая педагогика",
            font=("Advent Pro", 22),
            fill="black"
        )

        close_btn = header.create_text(
            real_width - 28,
            24,
            text="✕",
            font=("Advent Pro", 24),
            fill="black"
        )

        header.tag_bind(
            close_btn,
            "<Button-1>",
            lambda e: info_window.destroy()
        )

        # линия под градиентом
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

        # Описание

        description_title = ctk.CTkLabel(
            body,
            text="Описание:",
            text_color="black",
            font=("Advent Pro", 22)
        )

        description_title.pack(
            anchor="w"
        )

        description_space = ctk.CTkLabel(
            body,
            text="",
            height=120
        )

        description_space.pack(
            anchor="w",
            pady=(10, 30)
        )

        # линия над преподавателями

        # ---------- ЛИНИЯ НАД ПРЕПОДАВАТЕЛЯМИ ----------

        line2 = tk.Frame(info_window, height=2, width=465, bg="#A37C26")

        line2.place( x=20, y=416)

        # ---------- ПРЕПОДАВАТЕЛИ ----------

        teachers_title = ctk.CTkLabel(info_window, text="Преподаватели:", text_color="black", fg_color="transparent", font=("Advent Pro", 22))

        teachers_title.place(x=20, y=428)

        # текст преподаватели

        teachers_title = ctk.CTkLabel(info_window, text="Преподаватели:", text_color="black", fg_color="transparent", font=("Advent Pro", 22))

        teachers_title.place(x=20, y=428)

        teachers_space = ctk.CTkLabel(
            body,
            text="",
            height=120
        )

        teachers_space.pack(
            anchor="w"
        )


app = App()
app.mainloop()