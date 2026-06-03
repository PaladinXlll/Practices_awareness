import sys
import os
import calendar
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QScrollArea, QFrame, QPushButton, QComboBox, QGridLayout
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon

# ==============================================================================
# КОНФИГУРАЦИЯ ИНТЕРФЕЙСА
# ==============================================================================
FONT_FAMILY = "Segoe UI"
FONT_SIZE_BASE = 10

COLOR_MAIN_BG = "#d1b36a"
COLOR_BORDER = "#bda058"
COLOR_TEXT_DARK = "#3d2314"
COLOR_HOVER_BG = "#c4ae78"
COLOR_ACCENT_LINE = "#8c531d"
COLOR_COMBO_BG = "#e6d3ab"
COLOR_WEEKEND = "#a63a26"

COLOR_ITEM_BG = "#E9DCB0"
COLOR_ITEM_HOVER = "#DBC88E"

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
# БАЗОВЫЕ КОМПОНЕНТЫ
# ==============================================================================

class FilterCategoryButton(QPushButton):
    """Кнопка главной категории – всегда с иконкой"""

    def __init__(self, text, is_open=False, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedHeight(35)
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
            font-size: 14px;
            font-weight: bold;
            text-align: left;
            padding-left: 5px;
        }}
        QPushButton:hover {{
            background-color: #D8C07A;
            border-radius: 5px;
        }}
        QPushButton:pressed {{
            background-color: #C9AE62;
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
            background-color: {COLOR_ITEM_BG};
            border: 0px;
            border-radius: 3px;
            text-align: left;
            padding: 6px 10px;
        }}
        QPushButton:hover {{
            background-color: #D8C07A;
        }}
        QPushButton:pressed {{
            background-color: #C9AE62;
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
            self.sub_menu_widget = ExpandedSubMenu(sub_items, is_nested=True, show_icon_for_items=True)
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
    def __init__(self, items, has_item_arrows=False, is_nested=False, show_icon_for_items=False, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30 if is_nested else 15, 2, 0, 5)

        line = QFrame()
        line.setFixedWidth(10)
        line.setStyleSheet(f"background-color: {COLOR_ACCENT_LINE}; border-radius: 5px;")
        layout.addWidget(line)

        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(3)

        for item in items:
            list_layout.addWidget(StaticListElement(
                item,
                has_arrow=has_item_arrows,
                sub_items=["Зимний", "Летний"] if has_item_arrows else None,
                show_icon=show_icon_for_items
            ))

        layout.addWidget(list_container)


# ==============================================================================
# КАЛЕНДАРЬ С ВОЗМОЖНОСТЬЮ ВЫБОРА ДАТЫ
# ==============================================================================

class CalendarSubMenu(QWidget):
    """Календарь с выбором даты (сигнал dateSelected)"""
    dateSelected = pyqtSignal(int, int, int)  # год, месяц, день

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.selected_date = datetime.now()
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 2, 0, 5)

        line = QFrame()
        line.setFixedWidth(10)
        line.setStyleSheet(f"background-color: {COLOR_ACCENT_LINE}; border-radius: 5px;")
        main_layout.addWidget(line)

        cal_container = QWidget()
        cal_layout = QVBoxLayout(cal_container)

        self.month_box = QComboBox()
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
            font-weight: bold;
        }}
        QComboBox::drop-down {{ border: 0px; }}
        QComboBox QAbstractItemView {{
            background-color: {COLOR_ITEM_BG};
            border: 1px solid {COLOR_BORDER};
            selection-background-color: #D8C07A;
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
        # Очистка сетки
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Заголовки дней
        for col, day in enumerate(["пн", "вт", "ср", "чт", "пт", "сб", "вс"]):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"color: {COLOR_WEEKEND if col>=5 else COLOR_TEXT_DARK}; font-size: 10px; font-weight: bold;")
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
                btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #3d2314;
                    border: 0px;
                    border-radius: 4px;
                }
                QPushButton:hover { background: #D8C07A; }
                QPushButton:pressed { background: #C9AE62; }
                """)
                # При клике на день – испускаем сигнал с выбранной датой
                btn.clicked.connect(lambda checked, y=self.current_year, m=self.current_month, d=day: self.dateSelected.emit(y, m, d))
                self.grid.addWidget(btn, row, col)


# ==============================================================================
# ОСНОВНОЙ ВИДЖЕТ ФИЛЬТРА (РАСШИРЯЕМЫЙ)
# ==============================================================================

class CalendarGoldFilterWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Убираем фиксированную ширину, делаем минимальную – окно можно расширять
        self.setMinimumWidth(260)
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
            width: 10px;
        }}
        QScrollBar::handle:vertical {{
            background: #A8742A;
            border-radius: 5px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Шапка
        header = QHBoxLayout()
        title = QLabel("≡  Фильтр")
        title.setStyleSheet(f"color: {COLOR_TEXT_DARK}; font-size: 16px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        for icon in ["✓", "✕"]:
            btn = QPushButton(icon)
            btn.setFixedWidth(25)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("QPushButton { background: transparent; color: #3d2314; font-weight: bold; } QPushButton:hover { color: white; }")
            header.addWidget(btn)
        layout.addLayout(header)

        # Прокручиваемая область (содержимое будет подстраиваться под ширину)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        content = QWidget()
        self.clayout = QVBoxLayout(content)
        self.clayout.setSpacing(5)
        self.clayout.setContentsMargins(0, 0, 0, 0)

        # Секции
        self.add_sec("Мероприятия", ["Конференция", "День открытых дверей", "Семинар"], open=False, has_arrows=False)
        self.add_sec("Преподаватели", ["Агашина Анастасия Евгеньевна", "Денисова Анна Алексеевна", "Томилова Анна Владимировна"], open=False, has_arrows=False)

        # Календарь с возможностью выбора даты
        self.cal_btn = FilterCategoryButton("Дата")
        self.cal_view = CalendarSubMenu()
        self.cal_view.setVisible(False)
        self.cal_btn.toggled.connect(self.cal_view.setVisible)
        # Подключаем обработчик выбора даты
        self.cal_view.dateSelected.connect(self.on_date_selected)
        self.clayout.addWidget(self.cal_btn)
        self.clayout.addWidget(self.cal_view)

        self.add_sec("Учебный год", ["2024/2025", "2025/2026"], open=False, has_arrows=True)
        self.add_sec("Контроль", ["Наумушкина Н.С.", "Кучина А.А."], open=False, has_arrows=False)

        self.clayout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def add_sec(self, title, items, open=False, has_arrows=False):
        btn = FilterCategoryButton(title, is_open=open)
        menu = ExpandedSubMenu(items, has_item_arrows=has_arrows, show_icon_for_items=False)
        menu.setVisible(open)
        btn.toggled.connect(menu.setVisible)
        self.clayout.addWidget(btn)
        self.clayout.addWidget(menu)

    def on_date_selected(self, year, month, day):
        """Обработчик выбора даты из календаря"""
        # Здесь можно выполнить нужное действие, например:
        print(f"Выбрана дата: {day:02d}.{month:02d}.{year}")
        # Можно также сохранить дату в переменную, обновить фильтр и т.п.
        # Например, показать всплывающее сообщение:
        # QMessageBox.information(self, "Выбор даты", f"Выбрано: {day}.{month}.{year}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = CalendarGoldFilterWidget()
    w.show()
    # Делаем главное окно (сам виджет) расширяемым – можно задать начальный размер
    w.resize(300, 600)  # пример начального размера
    sys.exit(app.exec())