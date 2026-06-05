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
COLOR_SUBMENU_BG = "#e9dcb0"
COLOR_SUBMENU_HOVER = "#c8c8c8"

_MARKER_ICON_CACHE = None

def get_marker_icon():
    global _MARKER_ICON_CACHE
    if _MARKER_ICON_CACHE is None and QApplication.instance():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "toshka.png")
        if os.path.exists(icon_path):
            _MARKER_ICON_CACHE = QIcon(icon_path)
    return _MARKER_ICON_CACHE

class CapsuleLine(QWidget):
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
        painter.drawLine(int(offset), int(offset),
                        int(offset), int(self.height() - offset))

class NoScrollComboBox(QComboBox):
    def wheelEvent(self, e):
        e.ignore()

class FilterCategoryButton(QPushButton):
    def __init__(self, text, is_open=False, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedHeight(40)
        self.base_text = text
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        icon = get_marker_icon()
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(12, 12))

        self.setChecked(is_open)
        self._update_style()
        self._on_toggled(is_open)
        self.toggled.connect(self._on_toggled)

    def _update_style(self):
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
        """)

    def _on_toggled(self, checked):
        arrow = "  ▲" if checked else "  ▼"
        self.setText(f"   {self.base_text}{arrow}")

class StaticListElement(QWidget):
    def __init__(self, text, has_arrow=False, sub_items=None,
                 show_icon=False, parent=None):
        super().__init__(parent)
        self.text = text
        self.has_arrow = has_arrow
        self.is_sub_open = False
        self.show_icon = show_icon

        self.main_vbox = QVBoxLayout(self)
        self.main_vbox.setContentsMargins(0, 0, 0, 0)
        self.main_vbox.setSpacing(2)

        self.row_btn = self._create_button()
        self.main_vbox.addWidget(self.row_btn)

        if has_arrow and sub_items:
            self._create_submenu(sub_items)

    def _create_button(self):
        btn = QPushButton()
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        if self.show_icon:
            icon = get_marker_icon()
            if icon:
                btn.setIcon(icon)
                btn.setIconSize(QSize(12, 12))

        btn.setStyleSheet(f"""
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
            QPushButton:hover {{ background-color: {COLOR_SUBMENU_HOVER}; }}
            QPushButton:pressed {{ background-color: {COLOR_PRESSED_BG}; }}
        """)

        display_text = f"{self.text}   ▼" if self.has_arrow else self.text
        btn.setText(f"   {display_text}" if self.show_icon else display_text)
        return btn

    def _create_submenu(self, sub_items):
        self.sub_menu_widget = ExpandedSubMenu(
            sub_items, has_item_arrows=False, is_nested=True,
            show_icon_for_items=True, has_bg=True
        )
        self.sub_menu_widget.setVisible(False)
        self.main_vbox.addWidget(self.sub_menu_widget)
        self.row_btn.clicked.connect(self._toggle_submenu)

    def _toggle_submenu(self):
        if self.sub_menu_widget:
            self.is_sub_open = not self.is_sub_open
            self.sub_menu_widget.setVisible(self.is_sub_open)
            arrow = "   ▲" if self.is_sub_open else "   ▼"
            prefix = "   " if self.show_icon else ""
            self.row_btn.setText(f"{prefix}{self.text}{arrow}")

class ExpandedSubMenu(QWidget):
    def __init__(self, items, has_item_arrows=False, is_nested=False,
                 show_icon_for_items=False, has_bg=False, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

        layout = QHBoxLayout(self)
        left_margin = 20 if is_nested else 12
        layout.setContentsMargins(left_margin, 2, 6, 4)
        layout.setSpacing(12)

        layout.addWidget(CapsuleLine(width=12, color=COLOR_ACCENT_LINE))

        list_container = self._create_list_container(has_bg)
        list_layout = QVBoxLayout(list_container)
        padding = 6 if has_bg else 0
        list_layout.setContentsMargins(padding, padding, padding, padding)
        list_layout.setSpacing(3)

        for item in items:
            sub_items_list = ["Зимний семестр", "Летний семестр"] if has_item_arrows else None
            list_layout.addWidget(StaticListElement(
                item, has_arrow=has_item_arrows,
                sub_items=sub_items_list,
                show_icon=show_icon_for_items
            ))

        layout.addWidget(list_container)

    def _create_list_container(self, has_bg):
        container = QFrame()
        if has_bg:
            container.setStyleSheet(
                f"QFrame {{ background-color: {COLOR_SUBMENU_BG}; "
                f"border-radius: 8px; }}"
            )
        else:
            container.setStyleSheet("background-color: transparent;")
        return container

class CalendarSubMenu(QWidget):
    dateSelected = pyqtSignal(int, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 2, 6, 4)
        main_layout.setSpacing(12)

        main_layout.addWidget(CapsuleLine(width=12, color=COLOR_ACCENT_LINE))

        cal_container = QWidget()
        cal_layout = QVBoxLayout(cal_container)

        self.month_box = self._create_month_selector()
        cal_layout.addWidget(self.month_box)

        self.grid_widget = QWidget()
        self.grid = QGridLayout(self.grid_widget)
        self.grid.setSpacing(2)
        cal_layout.addWidget(self.grid_widget)

        main_layout.addWidget(cal_container)

        self.day_buttons = []
        self._init_calendar_grid()
        self._update_calendar_grid()

    def _create_month_selector(self):
        months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                  "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

        combo = NoScrollComboBox()
        combo.addItems(months)
        combo.setCurrentIndex(self.current_month - 1)
        combo.setCursor(Qt.CursorShape.PointingHandCursor)
        combo.setStyleSheet(f"""
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
        combo.currentIndexChanged.connect(self._on_month_changed)
        return combo

    def _init_calendar_grid(self):
        days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]

        for col, day in enumerate(days):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            color = COLOR_WEEKEND if col >= 5 else COLOR_TEXT_DARK
            lbl.setStyleSheet(
                f"color: {color}; font-family: '{FONT_FAMILY}'; "
                f"font-size: 12px; font-weight: bold;"
            )
            self.grid.addWidget(lbl, 0, col)

        btn_style = f"""
            QPushButton {{
                background: transparent;
                color: {COLOR_TEXT_DARK};
                font-family: "{FONT_FAMILY}";
                border: 0px;
                border-radius: 4px;
            }}
            QPushButton:hover {{ background: {COLOR_SUBMENU_HOVER}; }}
            QPushButton:pressed {{ background: {COLOR_PRESSED_BG}; }}
        """

        for row in range(1, 7):
            for col in range(7):
                btn = QPushButton()
                btn.setFixedSize(28, 24)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet(btn_style)
                btn.clicked.connect(self._on_day_clicked)
                self.grid.addWidget(btn, row, col)
                self.day_buttons.append(btn)

    def _on_month_changed(self):
        self.current_month = self.month_box.currentIndex() + 1
        self._update_calendar_grid()

    def _update_calendar_grid(self):
        cal_obj = calendar.Calendar(firstweekday=0)
        month_weeks = cal_obj.monthdayscalendar(self.current_year, self.current_month)

        flat_days = []
        for week in month_weeks:
            flat_days.extend(week)
        flat_days.extend([0] * (len(self.day_buttons) - len(flat_days)))

        for btn, day in zip(self.day_buttons, flat_days):
            if day == 0:
                btn.setVisible(False)
            else:
                btn.setText(str(day))
                btn.setProperty("day_val", day)
                btn.setVisible(True)

    def _on_day_clicked(self):
        btn = self.sender()
        if btn and btn.property("day_val"):
            self.dateSelected.emit(
                self.current_year, self.current_month, btn.property("day_val")
            )

class CalendarGoldFilterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(280)
        self.setMaximumWidth(350)
        self.setObjectName("Main")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._apply_styles()
        self._setup_ui()

    def _apply_styles(self):
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
            QScrollBar:vertical, QScrollBar:horizontal {{
                background: transparent;
                width: 0px;
                height: 0px;
                margin: 0px;
                border: none;
            }}
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
                background: transparent;
                min-height: 0px;
                min-width: 0px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                height: 0px;
                width: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
        """)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        layout.addLayout(self._create_header())
        layout.addWidget(self._create_scroll_area())

    def _create_header(self):
        header = QHBoxLayout()
        title = QLabel("≡  Фильтр")
        title.setStyleSheet(
            f"color: {COLOR_TEXT_DARK}; font-family: '{FONT_FAMILY}'; "
            f"font-size: {FONT_SIZE_LARGE}px; font-weight: bold;"
        )
        header.addWidget(title)
        header.addStretch()

        btn_style = (
            f"QPushButton {{ background: transparent; color: {COLOR_TEXT_DARK}; "
            f"font-family: '{FONT_FAMILY}'; font-weight: bold; "
            f"font-size: {FONT_SIZE_LARGE}px; }} "
            f"QPushButton:hover {{ color: white; }}"
        )

        for icon in ["✓", "✕"]:
            btn = QPushButton(icon)
            btn.setFixedWidth(25)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(btn_style)
            header.addWidget(btn)

        return header

    def _create_scroll_area(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self.clayout = QVBoxLayout(content)
        self.clayout.setSpacing(8)
        self.clayout.setContentsMargins(0, 0, 0, 0)

        self._add_sections()
        self._add_calendar()

        self.clayout.addStretch()
        scroll.setWidget(content)
        return scroll

    def _add_sections(self):
        events = [
            "Конференция", "День открытых дверей", "Методический семинар",
            "Педагогическое чтение", "Фестиваль", "Мастер-класс",
            "Чтение", "Профессиональные пробы", "Чемпионат"
        ]
        self.add_sec("Мероприятия", events, open=False, has_arrows=False, has_bg=False)

        teachers = [
            "Агашина Анастасия Евгеньевна", "Денисова Анна Алексеевна",
            "Томилова Анна Владимировна", "Малишева Платон Отарович",
            "Никитин Владислав Сергеевич"
        ]
        self.add_sec("Преподаватели", teachers, open=False,
                    has_arrows=False, has_bg=True)

        self.add_sec("Учебный год", ["2024/2025", "2025/2026", "2026/2027"],
                    open=False, has_arrows=True, has_bg=False)

    def _add_calendar(self):
        self.cal_btn = FilterCategoryButton("Дата")
        self.cal_view = CalendarSubMenu()
        self.cal_view.setVisible(False)
        self.cal_btn.toggled.connect(self.cal_view.setVisible)
        self.cal_view.dateSelected.connect(self.on_date_selected)
        self.clayout.addWidget(self.cal_btn)
        self.clayout.addWidget(self.cal_view)

        self.add_sec("Контроль", ["Наумушкина Н.С.", "Кучина А.А.", "Сметанина К.В."],
                    open=False, has_arrows=False, has_bg=False)

    def add_sec(self, title, items, open=False, has_arrows=False, has_bg=False):
        btn = FilterCategoryButton(title, is_open=open)
        menu = ExpandedSubMenu(items, has_item_arrows=has_arrows,
                              show_icon_for_items=False, has_bg=has_bg)
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