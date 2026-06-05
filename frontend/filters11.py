import sys
import os
import calendar
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QScrollArea, QFrame, QPushButton, QComboBox, QGridLayout
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPainter, QPen, QColor

# ==============================================================================
# КОНФИГУРАЦИЯ ИНТЕРФЕЙСА
# ==============================================================================
FONT_FAMILY = "Advent Pro" 
FONT_SIZE_BASE = 14
FONT_SIZE_LARGE = 18       

COLOR_MAIN_BG = "#d1b36a"
COLOR_BORDER = "#bda058"
COLOR_TEXT_DARK = "#000000"
COLOR_PRESSED_BG = "#A68A48"
COLOR_ACCENT_LINE = "#8c531d"
COLOR_COMBO_BG = "#e6d3ab"
COLOR_WEEKEND = "#a63a26"

# Цвета для блоков и эффектов
COLOR_SUBMENU_BG = "#e9dcb0"     # Бежевый фон для плашки («Преподаватели», «Зимний/Летний»)
COLOR_SUBMENU_HOVER = "#c8c8c8"  # Чистый серый цвет при наведении (hover)

# ------------------------------------------------------------------------------
# Ленивая загрузка иконки
# ------------------------------------------------------------------------------
_MARKER_ICON_CACHE = None

def get_marker_icon():
    global _MARKER_ICON_CACHE
    if _MARKER_ICON_CACHE is None:
        if QApplication.instance() is None:
            return None
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "toshka.png")
        if os.path.exists(icon_path):
            _MARKER_ICON_CACHE = QIcon(icon_path)
        else:
            print(f"⚠️ Иконка не найдена: {icon_path}")
            _MARKER_ICON_CACHE = None
    return _MARKER_ICON_CACHE


# ==============================================================================
# РУЧНАЯ ОТРИСОВКА ТОЛСТОЙ ЛИНИИ-КАПСУЛЫ (ШИРИНА 12px)
# ==============================================================================
class CapsuleLine(QWidget):
    """Класс для создания идеально гладких толстых закругленных линий"""
    def __init__(self, width=12, color=COLOR_ACCENT_LINE, parent=None):
        super().__init__(parent)
        self.line_width = width
        self.line_color = QColor(color)
        self.setFixedWidth(self.line_width)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pen = QPen(self.line_color)
        pen.setWidth(self.line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        offset = self.line_width / 2
        painter.drawLine(
            int(offset), int(offset), 
            int(offset), int(self.height() - offset)
        )


# ==============================================================================
# БАЗОВЫЕ КОМПОНЕНТЫ
# ==============================================================================

class FilterCategoryButton(QPushButton):
    """Кнопка главной категории – всегда с иконкой"""
    def __init__(self, text, is_open=False, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedHeight(40) 
        self.base_text = text
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        icon = get_marker_icon()
        if icon is not None:
            self.setIcon(icon)
            self.setIconSize(QSize(12, 12))

        self.setChecked(is_open)
        self.update_state(is_open)

        self.setStyleSheet(f"""
        QPushButton {{
            background-color: transparent;
            border: 0px;
            outline: none;
            color: {COLOR_TEXT_DARK};
            font-family: "{FONT_FAMILY}";
            font-size: {FONT_SIZE_LARGE}px;
            font-weight: bold;
            text-align: left;
            padding-left: 5px;
        }}
        QPushButton:hover {{
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 5px;
        }}
        QPushButton:pressed {{
            background-color: {COLOR_PRESSED_BG};
        }}
        QPushButton:checked {{
            background-color: transparent;
        }}
        """)
        self.toggled.connect(self.update_state)

    def update_state(self, checked):
        arrow = "  ▲" if checked else "  ▼"
        self.setText(f"   {self.base_text}{arrow}")


class StaticListElement(QWidget):
    def __init__(self, text, has_arrow=False, sub_items=None, show_icon=False, parent=None):
        super().__init__(parent)
        self.text = text
        self.has_arrow = has_arrow
        self.is_sub_open = False
        self.show_icon = show_icon

        self.main_vbox = QVBoxLayout(self)
        self.main_vbox.setContentsMargins(0, 0, 0, 0)
        self.main_vbox.setSpacing(2)

        self.row_btn = QPushButton()
        self.row_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        if self.show_icon:
            icon = get_marker_icon()
            if icon is not None:
                self.row_btn.setIcon(icon)
                self.row_btn.setIconSize(QSize(12, 12))

        self.row_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: transparent;
            color: {COLOR_TEXT_DARK};
            font-family: "{FONT_FAMILY}";
            font-size: {FONT_SIZE_BASE}px;
            border: 0px;
            border-radius: 5px;
            text-align: left;
            padding: 8px 10px;
        }}
        QPushButton:hover {{
            background-color: {COLOR_SUBMENU_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {COLOR_PRESSED_BG};
        }}
        """)

        display_text = text
        if has_arrow:
            display_text = f"{text}   ▼"
        if self.show_icon:
            self.row_btn.setText(f"   {display_text}")
        else:
            self.row_btn.setText(display_text)

        self.main_vbox.addWidget(self.row_btn)

        self.sub_menu_widget = None
        if has_arrow and sub_items:
            self.sub_menu_widget = ExpandedSubMenu(sub_items, has_item_arrows=False, is_nested=True, show_icon_for_items=False, has_bg=True)
            self.sub_menu_widget.setVisible(False)
            self.main_vbox.addWidget(self.sub_menu_widget)
            self.row_btn.clicked.connect(self.toggle_sub_menu)

    def toggle_sub_menu(self):
        if self.sub_menu_widget:
            self.is_sub_open = not self.is_sub_open
            self.sub_menu_widget.setVisible(self.is_sub_open)
            arrow = "   ▲" if self.is_sub_open else "   ▼"
            if self.show_icon:
                self.row_btn.setText(f"   {self.text}{arrow}")
            else:
                self.row_btn.setText(f"{self.text}{arrow}")


class ExpandedSubMenu(QWidget):
    def __init__(self, items, has_item_arrows=False, is_nested=False, show_icon_for_items=False, has_bg=False, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet("background-color: transparent;")
        
        layout = QHBoxLayout(self)
        left_margin = 20 if is_nested else 12
        layout.setContentsMargins(left_margin, 2, 6, 4)
        layout.setSpacing(12) 

        line = CapsuleLine(width=12, color=COLOR_ACCENT_LINE)
        layout.addWidget(line)

        list_container = QFrame()
        if has_bg:
            list_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLOR_SUBMENU_BG};
                    border-radius: 8px;
                }}
            """)
        else:
            list_container.setStyleSheet("background-color: transparent;")
            
        list_container_layout = QVBoxLayout(list_container)
        
        padding_inside = 6 if has_bg else 0
        list_container_layout.setContentsMargins(padding_inside, padding_inside, padding_inside, padding_inside)
        list_container_layout.setSpacing(3)

        for item in items:
            list_container_layout.addWidget(StaticListElement(
                item,
                has_arrow=has_item_arrows,
                sub_items=["Зимний семестр", "Летний семестр"] if has_item_arrows else None,
                show_icon=show_icon_for_items
            ))

        layout.addWidget(list_container)


# ==============================================================================
# КАЛЕНДАРЬ (ДАТА)
# ==============================================================================

class NoScrollComboBox(QComboBox):
    def wheelEvent(self, e):
        e.ignore()


class CalendarSubMenu(QWidget):
    dateSelected = pyqtSignal(int, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.selected_date = datetime.now()
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 2, 6, 4)
        main_layout.setSpacing(12) 

        line = CapsuleLine(width=12, color=COLOR_ACCENT_LINE)
        main_layout.addWidget(line)

        cal_container = QWidget()
        cal_container.setStyleSheet("background: transparent;")
        cal_layout = QVBoxLayout(cal_container)

        self.month_box = NoScrollComboBox()
        self.month_box.addItems(["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                                 "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"])
        self.month_box.setCurrentIndex(self.current_month - 1)
        self.month_box.setCursor(Qt.CursorShape.PointingHandCursor)
        self.month_box.setStyleSheet(f"""
        QComboBox {{
            background-color: {COLOR_COMBO_BG};
            border: 0px;
            border-radius: 4px;
            padding: 4px;
            color: {COLOR_TEXT_DARK};
            font-family: "{FONT_FAMILY}";
            font-size: {FONT_SIZE_BASE}px;
            font-weight: bold;
        }}
        QComboBox::drop-down {{ border: 0px; }}
        QComboBox QAbstractItemView {{
            background-color: {COLOR_COMBO_BG};
            border: 1px solid {COLOR_BORDER};
            color: {COLOR_TEXT_DARK};
            selection-background-color: {COLOR_SUBMENU_HOVER};
            selection-color: {COLOR_TEXT_DARK};
        }}
        """)
        self.month_box.currentIndexChanged.connect(self.on_month_changed)
        cal_layout.addWidget(self.month_box)

        self.grid_widget = QWidget()
        self.grid = QGridLayout(self.grid_widget)
        self.grid.setSpacing(2)
        cal_layout.addWidget(self.grid_widget)

        main_layout.addWidget(cal_container)
        self.update_calendar_grid()

    def on_month_changed(self):
        self.current_month = self.month_box.currentIndex() + 1
        self.update_calendar_grid()

    def update_calendar_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for col, day in enumerate(["пн", "вт", "ср", "чт", "пт", "сб", "вс"]):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"color: {COLOR_WEEKEND if col>=5 else COLOR_TEXT_DARK}; font-family: '{FONT_FAMILY}'; font-size: 12px; font-weight: bold;")
            self.grid.addWidget(lbl, 0, col)

        cal_obj = calendar.Calendar(firstweekday=0)
        month_weeks = cal_obj.monthdayscalendar(self.current_year, self.current_month)

        for row, week in enumerate(month_weeks, 1):
            for col, day in enumerate(week):
                if day == 0:
                    continue
                btn = QPushButton(str(day))
                btn.setFixedSize(28, 24)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {COLOR_TEXT_DARK};
                    font-family: "{FONT_FAMILY}";
                    border: 0px;
                    border-radius: 4px;
                }}
                QPushButton:hover {{ background: {COLOR_SUBMENU_HOVER}; }}
                QPushButton:pressed {{ background: {COLOR_PRESSED_BG}; }}
                """)
                btn.clicked.connect(lambda checked, y=self.current_year, m=self.current_month, d=day: self.dateSelected.emit(y, m, d))
                self.grid.addWidget(btn, row, col)


# ==============================================================================
# ОСНОВНОЙ ВИДЖЕТ ФИЛЬТРА
# ==============================================================================

class CalendarGoldFilterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(280)
        self.setObjectName("Main")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.setStyleSheet(f"""
        QWidget#Main {{
            background-color: {COLOR_MAIN_BG};
            border: 1px solid {COLOR_BORDER};
            border-radius: 10px;
        }}
        QScrollArea {{
            background: transparent;
            border: 0px;
        }}
        QScrollBar:vertical {{
            background: transparent;
            width: 14px; 
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {COLOR_ACCENT_LINE};
            border-radius: 7px;
            min-height: 20px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        # Шапка
        header = QHBoxLayout()
        title = QLabel("≡  Фильтр")
        title.setStyleSheet(f"color: {COLOR_TEXT_DARK}; font-family: '{FONT_FAMILY}'; font-size: {FONT_SIZE_LARGE}px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        for icon in ["✓", "✕"]:
            btn = QPushButton(icon)
            btn.setFixedWidth(25)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"QPushButton {{ background: transparent; color: {COLOR_TEXT_DARK}; font-family: '{FONT_FAMILY}'; font-weight: bold; font-size: {FONT_SIZE_LARGE}px; }} QPushButton:hover {{ color: white; }}")
            header.addWidget(btn)
        layout.addLayout(header)

        # Прокручиваемая область
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # ОТКЛЮЧАЕМ СКРОЛЛБАРЫ СПРАВА И СНИЗУ:
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self.clayout = QVBoxLayout(content)
        self.clayout.setSpacing(8)
        self.clayout.setContentsMargins(0, 0, 0, 0)

        # Секции
        self.add_sec("Мероприятия", ["Конференция", "День открытых дверей", "Семинар"], open=False, has_arrows=False, has_bg=False)
        
        # Преподаватели
        self.add_sec("Преподаватели", 
                     ["Агашина Анастасия Евгеньевна", "Денисова Анна Алексеевна", "Томилова Анна Владимировна", "Малишева Платон Отарович", "Никитин Владислав Сергеевич"], 
                     open=False, has_arrows=False, has_bg=True)

        # Календарь
        self.cal_btn = FilterCategoryButton("Дата")
        self.cal_view = CalendarSubMenu()
        self.cal_view.setVisible(False)
        self.cal_btn.toggled.connect(self.cal_view.setVisible)
        self.cal_view.dateSelected.connect(self.on_date_selected)
        self.clayout.addWidget(self.cal_btn)
        self.clayout.addWidget(self.cal_view)

        # Учебный год — Добавлен элемент "2026/2027"
        self.add_sec("Учебный год", ["2024/2025", "2025/2026", "2026/2027"], open=True, has_arrows=True, has_bg=False)
        
        self.add_sec("Контроль", ["Наумушкина Н.С.", "Кучина А.А.", "Сметанина К.В."], open=False, has_arrows=False, has_bg=False)

        self.clayout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def add_sec(self, title, items, open=False, has_arrows=False, has_bg=False):
        btn = FilterCategoryButton(title, is_open=open)
        menu = ExpandedSubMenu(items, has_item_arrows=has_arrows, show_icon_for_items=False, has_bg=has_bg)
        menu.setVisible(open)
        btn.toggled.connect(menu.setVisible)
        self.clayout.addWidget(btn)
        self.clayout.addWidget(menu)

    def on_date_selected(self, year, month, day):
        print(f"Выбрана дата: {day:02d}.{month:02d}.{year}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    font = QFont("Advent Pro", 12)
    app.setFont(font)
    
    app.setStyle("Fusion")
    w = CalendarGoldFilterWidget()
    w.show()
    w.resize(300, 600)
    sys.exit(app.exec())