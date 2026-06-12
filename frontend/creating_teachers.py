import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class CreateTeacherWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Создание преподавателя")
        self.geometry("510x520")
        self.resizable(False, False)

        # Цвет фона окна
        self.configure(fg_color="#DDD1A8")

        # ==========================================
        # HEADER
        # ==========================================

        header = ctk.CTkFrame(
            self,
            height=105,
            fg_color="#9B6A22",
            corner_radius=0
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="Создание преподавателя",
            text_color="white",
            font=("Advent Pro", 28)
        )
        title.place(relx=0.5, rely=0.5, anchor="center")

        close_btn = ctk.CTkButton(
            header,
            text="✕",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#83591E",
            text_color="black",
            font=("Arial", 24),
            corner_radius=0,
            command=self.destroy
        )
        close_btn.place(x=465, y=10)

        # ==========================================
        # ОСНОВНАЯ ЧАСТЬ
        # ==========================================

        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        content.pack(fill="both", expand=True)

        # Имя

        self.name_entry = ctk.CTkEntry(
            content,
            width=410,
            height=74,
            corner_radius=37,
            fg_color="#ECECEC",
            border_color="#B8B8B8",
            text_color="black",
            placeholder_text="Имя",
            placeholder_text_color="#9D9D9D",
            font=("Advent Pro", 24)
        )
        self.name_entry.pack(pady=(22, 0))

        # Фамилия

        self.lastname_entry = ctk.CTkEntry(
            content,
            width=410,
            height=74,
            corner_radius=37,
            fg_color="#ECECEC",
            border_color="#B8B8B8",
            text_color="black",
            placeholder_text="Фамилия",
            placeholder_text_color="#9D9D9D",
            font=("Advent Pro", 24)
        )
        self.lastname_entry.pack(pady=(22, 0))

        # Отчество

        self.middlename_entry = ctk.CTkEntry(
            content,
            width=410,
            height=74,
            corner_radius=37,
            fg_color="#ECECEC",
            border_color="#B8B8B8",
            text_color="black",
            placeholder_text="Отчество",
            placeholder_text_color="#9D9D9D",
            font=("Advent Pro", 24)
        )
        self.middlename_entry.pack(pady=(22, 0))

        # Кнопка сохранить

        save_btn = ctk.CTkButton(
            content,
            text="Сохранить",
            width=410,
            height=72,
            corner_radius=36,
            fg_color="#A77422",
            hover_color="#8A611B",
            text_color="white",
            font=("Advent Pro", 28),
            command=self.save_teacher
        )
        save_btn.pack(pady=(20, 0))

    def save_teacher(self):

        first_name = self.name_entry.get()
        last_name = self.lastname_entry.get()
        middle_name = self.middlename_entry.get()

        print("Имя:", first_name)
        print("Фамилия:", last_name)
        print("Отчество:", middle_name)

        self.destroy()


if __name__ == "__main__":
    app = CreateTeacherWindow()
    app.mainloop()