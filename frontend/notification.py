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
    # DIALOG
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
    # СОЗДАТЬ
    # ==========================================

def show_create_dialog(self):
        dialog = ctk.CTkToplevel(self.master)
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.title("Создать")
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
                header.create_text(width // 2, 22, text="Создать", fill="black", 
                                  font=("Advent Pro Expanded Light", 20, "bold"),
                                  anchor="center")

        header.after(100, draw_header)

        text_label = ctk.CTkLabel(
            main_frame,
            text="Сохранить изменения",
            font=("Advent Pro Expanded Light", 20),
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
            text="Сохранить",
            height=45,
            corner_radius=0,
            fg_color="#E0D0A0",
            hover_color="#D4C490",
            text_color="#444444",
            font=("Advent Pro Expanded Light", 20, "bold"),
            border_width=0,
            command=self.create_row
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
            font=("Advent Pro Expanded Light", 20, "bold"),
            border_width=0,
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", fill="both", expand=True)

    # ==========================================
    # РЕДАКТИРОВАТЬ
    # ==========================================

    def edit_row(self, row):
        dialog = ctk.CTkToplevel(self.master)
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.title("Редактировать")
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
                header.create_text(width // 2, 22, text="Редактировать", fill="black", 
                                  font=("Advent Pro Expanded Light", 20, "bold"),
                                  anchor="center")

        header.after(100, draw_header)

        text_label = ctk.CTkLabel(
            main_frame,
            text="Начать редактирование",
            font=("Advent Pro Expanded Light", 20),
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
            text="Начать",
            height=45,
            corner_radius=0,
            fg_color="#E0D0A0",
            hover_color="#D4C490",
            text_color="#444444",
            font=("Advent Pro Expanded Light", 20, "bold"),
            border_width=0,
            command=lambda: None
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
            font=("Advent Pro Expanded Light", 20, "bold"),
            border_width=0,
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", fill="both", expand=True)

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

        dialog = ctk.CTkToplevel(self.master)
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
                                  font=("Advent Pro Expanded Light", 20, "bold"),
                                  anchor="center")

        header.after(100, draw_header)

        text_label = ctk.CTkLabel(
            main_frame,
            text="Удалить информацию",
            font=("Advent Pro Expanded Light", 20),
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
            font=("Advent Pro Expanded Light", 20, "bold"),
            border_width=0,
            command=remove
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
            font=("Advent Pro Expanded Light", 20, "bold"),
            border_width=0,
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", fill="both", expand=True)

    # ==========================================
    # ВЫХОД
    # ==========================================

    def show_exit_dialog(self):
        dialog = ctk.CTkToplevel(self.master)
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
                                  font=("Advent Pro Expanded Light", 20, "bold"),
                                  anchor="center")

        header.after(100, draw_header)

        text_label = ctk.CTkLabel(
            main_frame,
            text="Вы точно хотите\nвыйти?",
            font=("Advent Pro Expanded Light", 20),
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
            font=("Advent Pro Expanded Light", 20, "bold"),
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
            font=("Advent Pro Expanded Light", 20, "bold"),
            border_width=0,
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", fill="both", expand=True)
