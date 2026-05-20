import sys
from PyQt6.QtCore import Qt, QSize, QDate
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHeaderView,
    QAbstractItemView, QStyledItemDelegate, QStyleOptionViewItem, QDateEdit,
    QAbstractSpinBox, QStyle
)
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont, QColor, QPen, QPalette
from PyQt6.QtSvg import QSvgRenderer

# --- ВЕКТОРНАЯ ГРАФИКА (SVG) ТОЧНО ПО МАКЕТАМ ---
SVG_ICONS = {
    "arrow_up": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M6 14l6-6 6 6H6z" fill="#FFFFFF"/></svg>''',
    "back": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" fill="#544321"/></svg>''',
    "doc_gear": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 12h-3v3h-2v-3H8v-2h3V9h2v3h3v2z" fill="#544321"/></svg>''',
    "burger": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z" fill="#544321"/></svg>''',
    "info": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" fill="none" stroke="#544321" stroke-width="2"/>
                <path d="M12 11v5M12 7h.01" stroke="#544321" stroke-width="2" stroke-linecap="round"/></svg>''',
    "edit": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z" fill="#2C2C2C"/></svg>''',
    "delete": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z" fill="#2C2C2C"/></svg>'''
}

def create_svg_icon(svg_name, size=QSize(16, 16)):
    """Рендеринг SVG-кода в чистый QIcon"""
    renderer = QSvgRenderer(SVG_ICONS[svg_name].encode('utf-8'))
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


# --- ИСПРАВЛЕННЫЙ КАСТОМНЫЙ ДЕЛЕГАТ ТАБЛИЦЫ ---
class CustomTableDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.info_icon = create_svg_icon("info", QSize(15, 15))

    def paint(self, painter, option, index):
        painter.save()
        
        # Базовый цвет фона ячейки из макета (#E0C58A)
        bg_color = QColor("#E0C58A")
        if option.state & QStyle.StateFlag.State_Selected:
            bg_color = QColor("#D4B475")  # Тон выделения
            
        painter.fillRect(option.rect, bg_color)

        # Отрисовка внутренней сетки таблицы поверх кастомного фона
        painter.setPen(QPen(QColor("#A17E3F"), 1))
        # Рисуем линии по нижней и правой границе ячейки для идеальной сетки
        painter.drawLine(option.rect.left(), option.rect.bottom(), option.rect.right(), option.rect.bottom())
        painter.drawLine(option.rect.right(), option.rect.top(), option.rect.right(), option.rect.bottom())

        # Получаем текст ячейки
        text = index.data(Qt.ItemDataRole.DisplayRole)
        
        # Колонки с данными
        if index.column() == 0:
            # Отрисовка иконки (i) в первой ячейке "Название"
            icon_size = 15
            y_offset = option.rect.y() + (option.rect.height() - icon_size) // 2
            icon_rect = option.rect
            icon_rect.setRect(option.rect.x() + 8, y_offset, icon_size, icon_size)
            self.info_icon.paint(painter, icon_rect, Qt.AlignmentFlag.AlignCenter)
            
            if text:
                text_rect = option.rect
                text_rect.setLeft(option.rect.x() + 28)
                text_rect.setRight(option.rect.right() - 4)
                painter.setPen(QColor("#2C2C2C"))
                painter.setFont(option.font)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter | Qt.TextFlag.TextWordWrap, str(text))
        else:
            # Текстовые данные остальных колонок с переносом слов (если это не виджеты)
            # Колонку даты (4) и кнопок (7, 8) пропускаем, там рендерятся виджеты
            if text and index.column() not in [4, 7, 8]:
                text_rect = option.rect
                text_rect.adjust(8, 4, -8, -4)
                painter.setPen(QColor("#2C2C2C"))
                painter.setFont(option.font)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter | Qt.TextFlag.TextWordWrap, str(text))

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(100, 52)


# --- СТРУКТУРНЫЕ ВИДЖЕТЫ ИНТЕРФЕЙСА ---

class HeaderView(QWidget):
    """Верхняя коричневая шапка приложения"""
    def __init__(self):
        super().__init__()
        self.setFixedHeight(60)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        title = QLabel("PRACTICES\nAWARENESS")
        title.setStyleSheet("""
            color: #FFFFFF; 
            font-size: 14px; 
            font-weight: bold; 
            line-height: 1.0;
            font-family: 'Arial Black', Gadget, sans-serif;
        """)
        
        btn_arrow = QPushButton()
        btn_arrow.setFixedSize(36, 24)
        btn_arrow.setIcon(create_svg_icon("arrow_up", QSize(20, 20)))
        btn_arrow.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_arrow.setStyleSheet("""
            QPushButton {
                background-color: #BA9957; 
                border-radius: 12px; 
                border: none;
            }
            QPushButton:hover { background-color: #CBB076; }
        """)
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(btn_arrow)
        self.setStyleSheet("background-color: #A17E3F;")


class NavigationBar(QWidget):
    """Полоса навигации 'Главная страница'"""
    def __init__(self):
        super().__init__()
        self.setFixedHeight(35)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        
        btn_back = QPushButton()
        btn_back.setFixedSize(20, 20)
        btn_back.setIcon(create_svg_icon("back", QSize(14, 14)))
        btn_back.setStyleSheet("border: none; background: transparent;")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        
        label = QLabel("Главная страница")
        label.setStyleSheet("color: #2C2C2C; font-size: 13px; font-weight: bold; font-family: 'Segoe UI', Arial;")
        
        btn_doc = QPushButton()
        btn_doc.setFixedSize(22, 22)
        btn_doc.setIcon(create_svg_icon("doc_gear", QSize(16, 16)))
        btn_doc.setStyleSheet("border: none; background: transparent;")
        btn_doc.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout.addWidget(btn_back)
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(btn_doc)
        self.setStyleSheet("background-color: #E6D09F; border-bottom: 1px solid #A17E3F;")


class AwarenessTableWidget(QTableWidget):
    """Информационная таблица CRM"""
    def __init__(self):
        super().__init__(0, 9)
        self.setItemDelegate(CustomTableDelegate(self))
        self.init_ui()
        
    def init_ui(self):
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        
        # Тотальная QSS стилизация таблицы и заголовков
        self.setStyleSheet("""
            QTableWidget {
                background-color: #E6D09F;
                border: none;
                gridline-color: #A17E3F;
                font-family: 'Segoe UI', Arial;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #E6D09F;
                color: #2C2C2C;
                font-weight: bold;
                font-size: 12px;
                border: none;
                border-right: 1px solid #A17E3F;
                border-bottom: 2px solid #A17E3F;
                padding: 6px;
            }
        """)
        
        headers = ["Название", "Место проведения", "Мероприятие", "Уровень", "Дата", "Контроль", "Документы", "", ""]
        self.setHorizontalHeaderLabels(headers)
        
        # ИСПРАВЛЕНО: Безопасная установка иконки после генерации объектов HeaderLabels
        burger_icon = create_svg_icon("burger", QSize(14, 14))
        self.horizontalHeaderItem(0).setIcon(burger_icon)
        
        # Выравнивание и пропорции колонок
        h_header = self.horizontalHeader()
        h_header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        h_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        h_header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        
        # Ширина кнопок действий в конце строки
        self.setColumnWidth(7, 35)
        self.setColumnWidth(8, 35)
        
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(52)
        
        self.cellChanged.connect(self.on_data_changed)

    def append_row_data(self, data):
        row = self.rowCount()
        self.insertRow(row)
        
        self.blockSignals(True)
        for col in range(7):
            val = data.get(f"col_{col}", "")
            item = QTableWidgetItem(val)
            self.setItem(row, col, item)
        self.blockSignals(False)
        
        # Интеграция календаря выбора дат в 4-ю колонку
        if "col_4" in data and data["col_4"]:
            date_container = QWidget()
            date_layout = QHBoxLayout(date_container)
            date_layout.setContentsMargins(4, 0, 4, 0)
            
            date_edit = QDateEdit()
            date_edit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
            date_edit.setCalendarPopup(True)
            date_edit.setDate(QDate.fromString(data["col_4"], "dd.MM.yyyy"))
            date_edit.setStyleSheet("""
                QDateEdit { 
                    background: transparent; 
                    border: none; 
                    color: #2C2C2C; 
                    font-family: 'Segoe UI';
                }
            """)
            date_edit.dateChanged.connect(lambda q_date, r=row: print(f"[Дата изменена] Строка {r+1}: {q_date.toString('dd.MM.yyyy')}"))
            date_layout.addWidget(date_edit)
            self.setCellWidget(row, 4, date_container)

        # Интерактивные кнопки упаковываем в контейнеры Layout для центрирования внутри сетки ячейки
        self.setCellWidget(row, 7, self.make_centered_button("edit", row))
        self.setCellWidget(row, 8, self.make_centered_button("delete", row))

    def make_centered_button(self, act_type, row_idx):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn = QPushButton()
        btn.setFixedSize(22, 22)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #CBB076;
                border: 1px solid #A17E3F;
            }
        """)
        
        if act_type == "edit":
            btn.setIcon(create_svg_icon("edit", QSize(14, 14)))
            btn.clicked.connect(lambda: self.editItem(self.item(row_idx, 0)))
        else:
            btn.setIcon(create_svg_icon("delete", QSize(14, 14)))
            btn.clicked.connect(lambda: self.delete_row_callback(btn))
            
        layout.addWidget(btn)
        return container

    def delete_row_callback(self, btn):
        # Находим строку по позиции контейнера кнопки
        idx = self.indexAt(btn.parentWidget().pos())
        if idx.isValid():
            target_row = idx.row()
            print(f"[Удаление] Строка №{target_row + 1} удалена.")
            self.removeRow(target_row)

    def on_data_changed(self, row, col):
        item = self.item(row, col)
        if item:
            print(f"[CRM Изменение] Строка {row+1}, Колонка {col+1} -> Изменено на '{item.text()}'")


# --- ГЛАВНОЕ ОКНО ---

class MainApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Practices Awareness CRM")
        self.resize(1150, 680)
        
        # Полный сброс палитры для изоляции от Dark Mode Windows
        self.force_light_palette()
        
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #E6D09F;")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.header = HeaderView()
        self.nav = NavigationBar()
        self.table = AwarenessTableWidget()
        
        layout.addWidget(self.header)
        layout.addWidget(self.nav)
        layout.addWidget(self.table)
        
        self.load_initial_dataset()

    def force_light_palette(self):
        palette = QPalette()
        base_color = QColor("#E6D09F")
        text_color = QColor("#2C2C2C")
        
        palette.setColor(QPalette.ColorRole.Window, base_color)
        palette.setColor(QPalette.ColorRole.WindowText, text_color)
        palette.setColor(QPalette.ColorRole.Base, base_color)
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#E0C58A"))
        palette.setColor(QPalette.ColorRole.Text, text_color)
        palette.setColor(QPalette.ColorRole.Button, base_color)
        palette.setColor(QPalette.ColorRole.ButtonText, text_color)
        
        # Фиксация цвета выделения
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#D4B475"))
        palette.setColor(QPalette.ColorRole.HighlightedText, text_color)
        self.setPalette(palette)

    def load_initial_dataset(self):
        # Демонстрационный набор данных
        dataset = [
            {
                "col_0": "Новые технологии — новая педагогика",
                "col_1": "163002, Россия, г. Архангельск, Набережная Северной Двины, 17",
                "col_2": "Конференция", "col_3": "Колледж", "col_4": "01.01.2027",
                "col_5": "Наумушкина Н.С.", "col_6": "№ 057\n01 декабря 2026"
            },
            {
                "col_0": "Выставка научных достижений",
                "col_1": "163002, Архангельск, улица Смольный Буян, дом 1",
                "col_2": "Методический семинар", "col_3": "Региональный", "col_4": "20.05.2026",
                "col_5": "Кузин А.А.", "col_6": "№ 102\n20 апреля 2026"
            },
            {
                "col_0": "Будущее образования: вызовы и стратегии",
                "col_1": "163002, Россия, г. Архангельск, набережная Северной Двины, 17",
                "col_2": "Педагогические чтения", "col_3": "Университетский", "col_4": "12.07.2026",
                "col_5": "Смяглина К.В.", "col_6": "№ 368\n10 июня 2026"
            }
        ]
        
        for data in dataset:
            self.table.append_row_data(data)
            
        # Отрисовка пустых золотых строк (повторяющих сетку шаблона)
        for _ in range(11):
            self.table.append_row_data({})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = MainApplicationWindow()
    window.show()
    sys.exit(app.exec())