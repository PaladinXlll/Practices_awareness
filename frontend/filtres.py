import sys
import calendar
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QScrollArea, QFrame, QPushButton, QComboBox, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

# ==============================================================================
# КОНФИГУРАЦИЯ ИНТЕРФЕЙСА (ПАЛИТРА ЦВЕТОВ И НАСТРОЙКИ)
# ==============================================================================
FONT_FAMILY = "Segoe UI"
FONT_SIZE_BASE = 10

COLOR_MAIN_BG = "#d1b36a"       # Основной фон панели фильтра
COLOR_BORDER = "#bda058"        # Цвет границ и рамок
COLOR_TEXT_DARK = "#3d2314"     # Цвет основного текста (темно-коричневый)
COLOR_TEXT_MUTED = "#24140a"    # Цвет активного/выделенного текста
COLOR_HOVER_BG = "#c4ae78"      # Фон элементов при наведении мыши
COLOR_ACCENT_LINE = "#8c531d"   # Цвет вертикального маркера-индикатора слева
COLOR_COMBO_BG = "#e6d3ab"      # Фон выпадающего списка месяцев
COLOR_WEEKEND = "#a63a26"       # Цвет выходных дней в календаре

# ==============================================================================
# БАЗОВЫЕ КОМПОНЕНТЫ (ТОЛЬКО ДЛЯ ЧТЕНИЯ)
# ==============================================================================

class FilterCategoryButton(QPushButton):
    """Кнопка главной категории (с кружочком-маркером)"""
    def __init__(self, text, has_arrow=True, is_open=False, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedHeight(35)
        self.base_text = text
        self.has_arrow = has_arrow
        
        self.setChecked(is_open)
        self.update_arrow(is_open)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {COLOR_TEXT_DARK};
                font-size: 14px;
                font-weight: bold;
                text-align: left;
                padding-left: 5px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_HOVER_BG};
                border-radius: 5px;
            }}
        """)
        self.toggled.connect(self.update_arrow)

    def update_arrow(self, checked):
        if self.has_arrow:
            arrow = "  ⌃" if checked else "  ⌄"
            self.setText(f"●   {self.base_text}{arrow}")
        else:
            self.setText(f"●   {self.base_text}")


class StaticListElement(QWidget):
    """Статический элемент списка (отображение без кнопок CRUD)"""
    def __init__(self, text, has_arrow=False, sub_items=None, parent=None):
        super().__init__(parent)
        self.text = text
        self.has_arrow = has_arrow
        self.is_sub_open = False
        
        self.main_vbox = QVBoxLayout(self)
        self.main_vbox.setContentsMargins(0, 0, 0, 0)
        self.main_vbox.setSpacing(0)
        
        # Строка самого элемента
        self.row_widget = QWidget()
        self.row_layout = QHBoxLayout(self.row_widget)
        self.row_layout.setContentsMargins(15, 4, 5, 4)
        self.row_layout.setSpacing(5)
        
        display_text = f"{text}   ⌄" if has_arrow else text
        self.label = QLabel(display_text)
        self.label.setWordWrap(True)
        self.label.setStyleSheet(f"color: {COLOR_TEXT_DARK}; font-size: 13px; background: transparent;")
        self.row_layout.addWidget(self.label, stretch=1)
        
        self.main_vbox.addWidget(self.row_widget)
        
        # Вложенные элементы подменю (например, для семестров/модулей внутри учебного года)
        self.sub_menu_widget = None
        if has_arrow:
            self.sub_menu_widget = ExpandedSubMenu(sub_items or ["Зимний", "Летний"], is_nested=True)
            self.sub_menu_widget.setVisible(False)
            self.main_vbox.addWidget(self.sub_menu_widget)
            
            self.label.setCursor(Qt.CursorShape.PointingHandCursor)
            # ИСПРАВЛЕНО: восстановлена корректная привязка события
            self.label.mousePressEvent = self.toggle_sub_menu

    def toggle_sub_menu(self, event):
        if self.sub_menu_widget:
            self.is_sub_open = not self.is_sub_open
            self.sub_menu_widget.setVisible(self.is_sub_open)
            arrow = "   ⌃" if self.is_sub_open else "   ⌄"
            self.label.setText(f"{self.text}{arrow}")


# ==============================================================================
# КОМПОНЕНТЫ КАЛЕНДАРЯ И СПИСКОВ
# ==============================================================================

class CalendarSubMenu(QWidget):
    """Интерактивный виджет календаря в соответствии с дизайном"""
    dateSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_year = datetime.now().year
        self.selected_date = datetime.now()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 0, 0, 5)
        main_layout.setSpacing(5)

        self.line_indicator = QFrame()
        self.line_indicator.setFixedWidth(12)
        self.line_indicator.setStyleSheet(f"QFrame {{ background-color: {COLOR_ACCENT_LINE}; border-radius: 6px; }}")
        main_layout.addWidget(self.line_indicator)

        cal_container = QWidget()
        cal_layout = QVBoxLayout(cal_container)
        cal_layout.setContentsMargins(5, 0, 0, 0)
        cal_layout.setSpacing(5)

        # Выпадающий список месяцев
        self.month_box = QComboBox()
        self.months_ru = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        self.month_box.addItems(self.months_ru)
        self.month_box.setCurrentIndex(self.selected_date.month - 1)
        self.month_box.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLOR_COMBO_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 4px;
                padding: 3px 5px;
                color: {COLOR_TEXT_DARK};
                font-weight: bold;
            }}
            QComboBox::drop-down {{ border: none; }}
            QComboBox QAbstractItemView {{
                background-color: {COLOR_COMBO_BG};
                selection-background-color: {COLOR_HOVER_BG};
                selection-color: {COLOR_TEXT_DARK};
                color: {COLOR_TEXT_DARK};
                border: 1px solid {COLOR_BORDER};
            }}
        """)
        self.month_box.currentIndexChanged.connect(self.update_calendar_grid)
        cal_layout.addWidget(self.month_box)

        # Сетка дней
        self.grid_widget = QWidget()
        self.grid = QGridLayout(self.grid_widget)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(4)
        cal_layout.addWidget(self.grid_widget)

        # Кнопка «Текущая дата»
        self.btn_today = QPushButton("Текущая дата")
        self.btn_today.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 1px solid {COLOR_ACCENT_LINE};
                color: {COLOR_TEXT_DARK};
                font-size: 11px;
                font-weight: bold;
                border-radius: 4px;
                padding: 3px;
            }}
            QPushButton:hover {{ background-color: {COLOR_HOVER_BG}; }}
        """)
        self.btn_today.clicked.connect(self.set_to_current_date)
        cal_layout.addWidget(self.btn_today)

        main_layout.addWidget(cal_container, stretch=1)
        self.update_calendar_grid()

    def update_calendar_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        days_headers = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
        for col, day in enumerate(days_headers):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            color = COLOR_WEEKEND if col >= 5 else COLOR_TEXT_DARK
            # ИСПРАВЛЕНО: восстановлена корректная строка стиля
            lbl.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 11px;")
            self.grid.addWidget(lbl, 0, col)

        view_month = self.month_box.currentIndex() + 1
        cal_obj = calendar.Calendar(firstweekday=0)
        month_weeks = cal_obj.monthdayscalendar(self.current_year, view_month)

        prev_month = view_month - 1 if view_month > 1 else 12
        prev_year = self.current_year if view_month > 1 else self.current_year - 1
        next_month = view_month + 1 if view_month < 12 else 1
        # ИСПРАВЛЕНО: логическая ошибка (было self.current_year - 1, стало + 1 при переходе на новый год)
        next_year = self.current_year if view_month < 12 else self.current_year + 1
        prev_month_len = calendar.monthrange(prev_year, prev_month)[1]

        row = 1
        for week in month_weeks:
            for col, day in enumerate(week):
                target_day = day
                target_month = view_month
                target_year = self.current_year
                is_current_month = True

                if day == 0:
                    is_current_month = False
                    if row == 1:
                        target_day = prev_month_len - (week.count(0) - 1) + week[:col].count(0)
                        target_month = prev_month
                        target_year = prev_year
                    else:
                        target_day = col - week.index(0) + 1
                        target_month = next_month
                        target_year = next_year

                btn_day = QPushButton(str(target_day))
                btn_day.setFixedSize(24, 20)
                
                is_weekend = col >= 5
                text_color = COLOR_WEEKEND if is_weekend else COLOR_TEXT_DARK
                opacity = "1.0" if is_current_month else "0.4"

                is_selected = (target_day == self.selected_date.day and 
                               target_month == self.selected_date.month and 
                               target_year == self.selected_date.year)

                border_style = f"border: 1px solid {COLOR_ACCENT_LINE}; font-weight: bold;" if is_selected else "border: none;"

                btn_day.setStyleSheet(f"""
                    QPushButton {{
                        background: transparent;
                        {border_style}
                        color: {text_color};
                        font-size: 12px;
                        opacity: {opacity};
                    }}
                    QPushButton:hover {{
                        background-color: {COLOR_HOVER_BG};
                        border-radius: 3px;
                    }}
                """)
                
                btn_day.setProperty("day", target_day)
                btn_day.setProperty("month", target_month)
                btn_day.setProperty("year", target_year)
                btn_day.clicked.connect(self.handle_day_click)

                self.grid.addWidget(btn_day, row, col)
            row += 1

    def handle_day_click(self):
        sender = self.sender()
        day = sender.property("day")
        month = sender.property("month")
        year = sender.property("year")

        self.selected_date = datetime(year, month, day)
        
        if month != self.month_box.currentIndex() + 1:
            self.current_year = year
            self.month_box.blockSignals(True)
            self.month_box.setCurrentIndex(month - 1)
            self.month_box.blockSignals(False)

        self.update_calendar_grid()
        self.dateSelected.emit(self.selected_date.strftime("%d.%m.%Y"))

    def set_to_current_date(self):
        today = datetime.now()
        self.current_year = today.year
        self.selected_date = today
        
        self.month_box.blockSignals(True)
        self.month_box.setCurrentIndex(today.month - 1)
        self.month_box.blockSignals(False)
        
        self.update_calendar_grid()
        self.dateSelected.emit(self.selected_date.strftime("%d.%m.%Y"))


class ExpandedSubMenu(QWidget):
    """Контейнер для отображения вложенных списков без элементов управления CRUD"""
    # ИСПРАВЛЕНО: восстановлена корректная сигнатура метода __init__
    def __init__(self, items, has_item_arrows=False, is_nested=False, parent=None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        # Если меню вложенное (семестры), делаем чуть больший отступ слева в соответствии с дизайном
        left_margin = 20 if is_nested else 5
        self.main_layout.setContentsMargins(left_margin, 0, 0, 5)
        self.main_layout.setSpacing(5)
        
        self.line_indicator = QFrame()
        self.line_indicator.setFixedWidth(12)
        self.line_indicator.setStyleSheet(f"QFrame {{ background-color: {COLOR_ACCENT_LINE}; border-radius: 6px; }}")
        self.main_layout.addWidget(self.line_indicator)
        
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(2)
        
        for item in items:
            self.add_static_item(item, has_item_arrows)
            
        self.main_layout.addWidget(self.list_container, stretch=1)

    def add_static_item(self, text, has_item_arrows):
        # На дизайне внутренние подпункты имеют маркеры «Зимний» / «Летний»
        if not has_item_arrows and (text == "Зимний" or text == "Летний" or text == "1 полугодие" or text == "2 полугодие"):
            text = f"●  {text}"
            
        item_widget = StaticListElement(text, has_arrow=has_item_arrows)
        self.list_layout.addWidget(item_widget)


# ==============================================================================
# ГЛАВНЫЙ ИНТЕРФЕЙС ПАНЕЛИ ФИЛЬТРАЦИИ
# ==============================================================================

class CalendarGoldFilterWidget(QWidget):
    """Главное окно статического фильтра в точечном соответствии с референсом"""
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setObjectName("MainWidget")
        self.setFixedWidth(260)
        self.setMinimumHeight(700)
        
        self.setStyleSheet(f"""
            QWidget#MainWidget {{
                background-color: {COLOR_MAIN_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(4)
        
        # --- ШАПКА ФИЛЬТРА ---
        header_layout = QHBoxLayout()
        header_title = QLabel("≡  Фильтр")
        header_title.setStyleSheet(f"color: {COLOR_TEXT_DARK}; font-size: 18px; font-weight: bold;")
        
        btn_apply = QPushButton("✓")
        btn_close = QPushButton("✕")
        btn_style = f"""
            QPushButton {{ 
                background: transparent; 
                border: none; 
                color: {COLOR_TEXT_DARK}; 
                font-size: 16px; 
                font-weight: bold; 
                max-width: 22px; 
            }} 
            QPushButton:hover {{ color: {COLOR_TEXT_MUTED}; }}
        """
        btn_apply.setStyleSheet(btn_style)
        btn_close.setStyleSheet(btn_style)
        
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_apply)
        header_layout.addWidget(btn_close)
        main_layout.addLayout(header_layout)
        
        # Скролл-зона
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{ background: transparent; }}
            QScrollBar:vertical {{ border: none; background: transparent; width: 5px; }}
            QScrollBar::handle:vertical {{ background: {COLOR_ACCENT_LINE}; border-radius: 2px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ background: none; }}
        """)
        
        scroll_content = QWidget()
        # ИСПРАВЛЕНО: восстановлена корректная строка стиля
        scroll_content.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(scroll_content)
        self.content_layout.setContentsMargins(0, 5, 0, 5)
        self.content_layout.setSpacing(2)
        
        # Генерация чистой динамической структуры (Read-Only)
        self.create_filter_section("Мероприятия", ["Конференция", "День открытых дверей", "Методический семинар", "Педогогическое чтение", "Фестеваль", "Мастер класс", "Чтение", "Профессиональные пробы", "Чемпионат"], is_open=True)
        self.create_filter_section("Преподаватели", ["Агашина Анастасия Евгеньевна", "Денисова Анна Алексеевна", "Томилова Анна Владимировна"], is_open=False)
        
        # Секция интерактивного календаря
        self.create_calendar_section("Дата", is_open=True)
        
        # Секция учебного года со вложенными подпунктами (в соответствии со схемами на дизайне)
        self.create_filter_section("Учебный год", ["2024/2025", "2025/2026", "2026/2027"], is_open=False, has_item_arrows=True)
        
        self.create_filter_section("Контроль", ["Наумушкина Н.С.", "Кучина А.А.", "Сметанина К.В."], is_open=False)
        
        self.content_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

    def create_filter_section(self, title, items, is_open=False, has_item_arrows=False):
        btn = FilterCategoryButton(title, is_open=is_open)
        menu = ExpandedSubMenu(items, has_item_arrows=has_item_arrows)
        
        menu.setVisible(is_open)
        btn.toggled.connect(menu.setVisible)
        
        self.content_layout.addWidget(btn)
        self.content_layout.addWidget(menu)

    def create_calendar_section(self, title, is_open=False):
        btn = FilterCategoryButton(title, is_open=is_open)
        cal = CalendarSubMenu()
        
        cal.dateSelected.connect(lambda d: print(f"Выбрана дата фильтрации: {d}"))
        
        cal.setVisible(is_open)
        btn.toggled.connect(cal.setVisible)
        
        self.content_layout.addWidget(btn)
        self.content_layout.addWidget(cal)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont(FONT_FAMILY, FONT_SIZE_BASE))
    window = CalendarGoldFilterWidget()
    window.show()
    sys.exit(app.exec())