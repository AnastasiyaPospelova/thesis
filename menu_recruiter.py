import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QPushButton, QHBoxLayout, QLineEdit, QMessageBox, QMenu, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from server import (get_recruiter_fio_by_id, get_candidate_info_by_id, get_candidates_count, delete_candidate_by_id, 
                    check_answers_exist_theory1, check_answers_exist_theory2, check_answers_exist_theory3, 
                    check_answers_exist_theory4, check_answers_exist_logic, get_candidate_fio_by_id, 
                    get_answers_list_by_candidate_theory1, get_answers_list_by_candidate_theory2, 
                    get_answers_list_by_candidate_theory3, get_answers_list_by_candidate_theory4, 
                    get_answers_list_by_candidate_logic, get_recruiters_info, add_recruiter, 
                    delete_recruiter_by_id, get_answers_listt_theory1, get_answers_listt_theory2, 
                    get_answers_listt_theory3, get_answers_listt_theory4, get_answers_listt_logic, reorder_candidate_ids)
from analis import get_candidate_score
from priorities import get_priorities, set_priorities

# Глобальный стиль для всего приложения
STYLE_SHEET = """
    QWidget {
        font-family: 'Segoe UI';
        font-size: 14px;
    }
    QPushButton {
        background-color: #0078D7;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #106EBE;
    }
    QPushButton:pressed {
        background-color: #005A9E;
    }
    QLineEdit {
        padding: 8px;
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        background-color: white;
    }
    QLineEdit:focus {
        border: 1px solid #0078D7;
    }
    QTableWidget {
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        background-color: white;
        gridline-color: #E0E0E0;
    }
    QHeaderView::section {
        background-color: #0078D7;
        color: white;
        padding: 8px;
        border: none;
        font-size: 14px;
    }
    QTableWidget::item {
        padding: 8px;
    }
    QLabel {
        color: #333333;
    }
"""

class DetailsWindow(QWidget):
    def __init__(self, id_candidate):
        super().__init__()
        success, fio = get_candidate_fio_by_id(id_candidate)
        self.setWindowTitle(f"Кандидат {fio}")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.id_candidate = id_candidate
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Заголовок
        title = QLabel(f"Результаты кандидата: {fio}")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078D7; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Создаем таблицу
        self.tests_table = QTableWidget()
        self.tests_table.setRowCount(5)
        self.tests_table.setColumnCount(3)
        self.tests_table.setHorizontalHeaderLabels(["№", "Статус", "Баллы"])
        self.tests_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Устанавливаем высоту строк
        for i in range(self.tests_table.rowCount()):
            self.tests_table.setRowHeight(i, 60)
        
        # Заполняем первый столбец
        test_names = ["Тест 1", "Тест 2", "Тест 3", "Тест 4", "Тест 5"]  # Добавлен "Тест 5"
        for i in range(5):  # Изменено с 4 на 5
            self.tests_table.setItem(i, 0, QTableWidgetItem(test_names[i]))
        
        # Заполняем второй и третий столбцы
        check_functions = [
            check_answers_exist_theory1,
            check_answers_exist_theory2, 
            check_answers_exist_theory3,
            check_answers_exist_theory4,
            check_answers_exist_logic
        ]
        
        get_answers_functions = [
            get_answers_list_by_candidate_theory1,
            get_answers_list_by_candidate_theory2,
            get_answers_list_by_candidate_theory3,
            get_answers_list_by_candidate_theory4,
            get_answers_list_by_candidate_logic
        ]
        
        for i in range(5):  # Изменено с 4 на 5
            success, _ = check_functions[i](self.id_candidate)
            status = "пройден" if success else "не пройден"
            self.tests_table.setItem(i, 1, QTableWidgetItem(status))
            
            if success:
                # Получаем ответы кандидата
                success, answers = get_answers_functions[i](self.id_candidate)
                correct_count = 0
                
                if success:
                    # Получаем правильные ответы
                    success, correct_answers = get_answers_listt_theory1() if i == 0 else \
                                            get_answers_listt_theory2() if i == 1 else \
                                            get_answers_listt_theory3() if i == 2 else \
                                            get_answers_listt_theory4() if i == 3 else \
                                            get_answers_listt_logic()
                    
                    if success:
                        # Сравниваем ответы кандидата с правильными ответами
                        for user_answer, correct_answer in zip(answers, correct_answers):
                            if user_answer == correct_answer:
                                correct_count += 1
                                
                        self.tests_table.setItem(i, 2, QTableWidgetItem(f"{correct_count}/10"))
                    else:
                        self.tests_table.setItem(i, 2, QTableWidgetItem("Ошибка"))
                else:
                    self.tests_table.setItem(i, 2, QTableWidgetItem("Ошибка"))
            else:
                self.tests_table.setItem(i, 2, QTableWidgetItem("---"))
            
        layout.addWidget(self.tests_table)
        self.setLayout(layout)

class AddRecruiterWindow(QWidget):
    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_window = parent
        self.setWindowTitle("Добавить рекрутера")
        self.setGeometry(100, 100, 500, 400)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.Window)
        self.setStyleSheet(STYLE_SHEET)
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Заголовок
        title = QLabel("Добавление нового сотрудника")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078D7; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Создаем поля ввода
        self.fio_input = QLineEdit()
        self.fio_input.setPlaceholderText("Введите ФИО")
        self.fio_input.setMinimumHeight(40)
        
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Введите возраст")
        self.age_input.setMinimumHeight(40)
        
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Введите город")
        self.city_input.setMinimumHeight(40)
        
        self.access_code_input = QLineEdit()
        self.access_code_input.setPlaceholderText("Введите код доступа")
        self.access_code_input.setMinimumHeight(40)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Введите номер телефона")
        self.phone_input.setMinimumHeight(40)
        
        # Добавляем поля в layout
        layout.addWidget(self.fio_input)
        layout.addWidget(self.age_input)
        layout.addWidget(self.city_input)
        layout.addWidget(self.access_code_input)
        layout.addWidget(self.phone_input)
        
        # Кнопка добавления
        self.add_button = QPushButton("Добавить")
        self.add_button.setMinimumWidth(250)
        self.add_button.setMinimumHeight(50)
        self.add_button.clicked.connect(self.add_recruiter_clicked)
        layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        
        # Центрируем окно относительно родительского окна
        if parent:
            self.move(parent.x() + (parent.width() - self.width()) // 2,
                     parent.y() + (parent.height() - self.height()) // 2)

    def add_recruiter_clicked(self):
        fio = self.fio_input.text().strip()
        age = self.age_input.text().strip()
        city = self.city_input.text().strip()
        access_code = self.access_code_input.text().strip()
        phone_number = self.phone_input.text().strip()
        
        # Проверка на пустые поля
        if not all([fio, age, city, access_code, phone_number]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return
            
        # Проверка возраста
        try:
            age = int(age)
            if age < 18 or age > 100:
                QMessageBox.warning(self, "Ошибка", "Возраст должен быть от 18 до 100 лет!")
                return
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Возраст должен быть числом!")
            return
            
        # Проверка телефона
        if not phone_number.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            QMessageBox.warning(self, "Ошибка", "Номер телефона должен содержать только цифры!")
            return
        
        success, message = add_recruiter(fio, age, city, access_code, phone_number)
        
        if success:
            QMessageBox.information(self, "Успех", "Рекрутер успешно добавлен!")
            self.dataChanged.emit()  # Отправляем сигнал об изменении данных
            self.close()  # Закрываем окно
        else:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при добавлении рекрутера: {message}")

class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аналитика")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Заголовок
        title = QLabel("Аналитика результатов")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078D7; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Получаем количество кандидатов
        success, candidates_count = get_candidates_count()
        print(f"Количество кандидатов: {candidates_count}")
        
        # Создаем таблицу
        self.results_table = QTableWidget()
        self.results_table.setRowCount(candidates_count)
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["№", "ФИО", "Результат"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Устанавливаем высоту строк
        for i in range(self.results_table.rowCount()):
            self.results_table.setRowHeight(i, 60)
        
        # Получаем результаты для каждого кандидата
        results = []
        max_result = 0
        max_index = 0
        
        for i in range(candidates_count):
            print(f"\nОбработка кандидата {i + 1}:")
            success, score = get_candidate_score(i + 1)
            print(f"Успех: {success}, Score: {score}")
            if success:
                results.append(score)
                if score > max_result:
                    max_result = score
                    max_index = i
            else:
                print(f"Ошибка при получении score: {score}")
                results.append(0)
        
        print(f"\nМаксимальный результат: {max_result} у кандидата {max_index + 1}")
        
        # Получаем ФИО рекомендуемого кандидата
        success, recommended_fio = get_candidate_fio_by_id(max_index + 1)
        print(f"ФИО рекомендуемого кандидата: {recommended_fio}")
        
        # Заполняем таблицу
        for i in range(candidates_count):
            # Номер кандидата
            self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            
            # ФИО кандидата
            success, fio = get_candidate_fio_by_id(i + 1)
            if success:
                self.results_table.setItem(i, 1, QTableWidgetItem(fio))
                print(f"Кандидат {i + 1}: {fio}, результат: {results[i]:.2f}")
            
            # Результат
            result_item = QTableWidgetItem(f"{results[i]:.2f}")
            result_item.setTextAlignment(Qt.AlignCenter)
            self.results_table.setItem(i, 2, result_item)
        
        layout.addWidget(self.results_table)
        
        # Добавляем информацию о рекомендуемом кандидате
        if success and recommended_fio:
            recommended_label = QLabel(f"Рекомендуемый кандидат: {recommended_fio}")
            recommended_label.setFont(QFont('Segoe UI', 14, QFont.Bold))
            recommended_label.setStyleSheet("color: #0078D7; margin-top: 20px;")
            recommended_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(recommended_label)

class PrioritySettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройка приоритетов")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # Создаем таблицу приоритетов
        self.priorities_table = QTableWidget()
        self.priorities_table.setRowCount(5)
        self.priorities_table.setColumnCount(5)
        
        # Заполняем таблицу текущими значениями
        current_priorities = get_priorities()
        for i in range(5):
            for j in range(5):
                item = QTableWidgetItem(str(current_priorities[i][j]))
                self.priorities_table.setItem(i, j, item)
        
        # Добавляем таблицу на форму
        layout = QVBoxLayout()
        layout.addWidget(self.priorities_table)
        
        # Добавляем кнопку сохранения
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_priorities)
        layout.addWidget(save_button)
        
        self.setLayout(layout)
    
    def save_priorities(self):
        try:
            new_priorities = []
            for i in range(5):
                row = []
                for j in range(5):
                    value = float(self.priorities_table.item(i, j).text())
                    row.append(value)
                new_priorities.append(row)
            set_priorities(new_priorities)
            QMessageBox.information(self, "Успех", "Приоритеты успешно сохранены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить приоритеты: {str(e)}")

class MenuRecruiterWindow(QWidget):
    def __init__(self, ID_recruiter):
        super().__init__()
        self.ID_recruiter = ID_recruiter
        self.setWindowTitle("Меню рекрутера")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Получаем ФИО рекрутера
        success, fio = get_recruiter_fio_by_id(ID_recruiter)
        
        # Заголовок
        title = QLabel(f"Добро пожаловать, {fio}!")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078D7; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0078D7;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #E0E0E0;
            }
        """)
        
        # Создаем layout для первой вкладки
        tab1_layout = QVBoxLayout()
        
        # Добавляем приветствие
        self.welcome_label = QLabel(f"Здравствуйте, {fio}!")
        font = self.welcome_label.font()
        font.setPointSize(16)
        font.setBold(True)
        self.welcome_label.setFont(font)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        
        tab1_layout.addWidget(self.welcome_label)
        self.tab1 = QWidget()
        self.tab1.setLayout(tab1_layout)
        
        # Создаем layout для второй вкладки
        tab2_layout = QVBoxLayout()
        
        # Получаем количество кандидатов
        success, candidates_count = get_candidates_count()
        
        # Создаем таблицу
        self.candidates_table = QTableWidget()
        self.candidates_table.setRowCount(candidates_count)
        self.candidates_table.setColumnCount(4)
        self.candidates_table.setHorizontalHeaderLabels(["№", "ФИО", "Город", "Телефон"])
        
        # Заполняем таблицу
        for i in range(candidates_count):
            # Номер кандидата
            self.candidates_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            
            # Получаем информацию о кандидате
            success, info = get_candidate_info_by_id(i + 1)
            if success:
                self.candidates_table.setItem(i, 1, QTableWidgetItem(info['fio']))
                self.candidates_table.setItem(i, 2, QTableWidgetItem(info['city']))
                self.candidates_table.setItem(i, 3, QTableWidgetItem(info['number']))
        
        # Настраиваем размеры столбцов
        self.candidates_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.candidates_table.verticalHeader().setVisible(False)
        
        # Включаем контекстное меню
        self.candidates_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.candidates_table.customContextMenuRequested.connect(self.show_context_menu)
        
        tab2_layout.addWidget(self.candidates_table)
        
        self.tab2 = QWidget()
        self.tab2.setLayout(tab2_layout)
        
        # Создаем layout для третьей вкладки
        tab3_layout = QVBoxLayout()
        
        # Создаем таблицу рекрутеров
        self.recruiters_table = QTableWidget()
        self.recruiters_table.setColumnCount(6)
        self.recruiters_table.setHorizontalHeaderLabels(["№", "ФИО", "Телефон", "Возраст", "Город", "Код доступа"])
        
        # Настраиваем размеры столбцов
        self.recruiters_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.recruiters_table.verticalHeader().setVisible(False)
        
        # Включаем контекстное меню для таблицы рекрутеров
        self.recruiters_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.recruiters_table.customContextMenuRequested.connect(self.show_recruiters_context_menu)
        
        tab3_layout.addWidget(self.recruiters_table)
        self.tab3 = QWidget()
        self.tab3.setLayout(tab3_layout)

        # Создаем layout для четвертой вкладки
        tab4_layout = QVBoxLayout()
        
        # Создаем контейнер для центрирования содержимого
        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Создаем верхний layout для лейбла и кнопки "Показать"
        top_layout = QHBoxLayout()
        
        # Создаем лейбл с надписью
        self.analytics_label = QLabel("Подсчёт результатов тестирования кандидатов.")
        top_layout.addWidget(self.analytics_label)
        
        # Создаем кнопку "Показать" и подключаем к ней обработчик
        self.show_button = QPushButton("Показать")
        self.show_button.clicked.connect(self.show_analytics)
        top_layout.addWidget(self.show_button)
        
        # Добавляем верхний layout в центрирующий контейнер
        center_layout.addLayout(top_layout)
        
        # Добавляем центрирующий контейнер в основной layout вкладки
        tab4_layout.addWidget(center_container)
        
        # Добавляем растягивающийся элемент для прижатия кнопки к низу
        tab4_layout.addStretch()
        
        # Добавляем кнопку "Изменить приоритеты" внизу
        self.change_priorities_button = QPushButton("Изменить приоритеты")
        self.change_priorities_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        self.change_priorities_button.clicked.connect(self.show_priority_settings)
        tab4_layout.addWidget(self.change_priorities_button, alignment=Qt.AlignCenter)
        
        self.tab4 = QWidget()
        self.tab4.setLayout(tab4_layout)
        
        # Добавляем вкладки
        self.tabs.addTab(self.tab1, "Главная")
        self.tabs.addTab(self.tab2, "Кандидаты")
        self.tabs.addTab(self.tab3, "Пользователи")
        self.tabs.addTab(self.tab4, "Аналитика")
        
        layout.addWidget(self.tabs)
        
        # Загружаем данные рекрутеров при инициализации
        self.load_recruiters()

    def show_analytics(self):
        self.analytics_window = AnalyticsWindow()
        self.analytics_window.show()

    def show_priority_settings(self):
        self.priority_settings_window = PrioritySettingsWindow()
        self.priority_settings_window.show()

    def show_context_menu(self, pos):
        # Получаем индекс строки под курсором
        row = self.candidates_table.rowAt(pos.y())
        if row >= 0:  # Если курсор находится над строкой
            menu = QMenu(self)
            details_action = menu.addAction("Подробности")
            delete_action = menu.addAction("Удалить")
            action = menu.exec_(self.candidates_table.viewport().mapToGlobal(pos))
            
            if action == details_action:
                # Получаем ID кандидата из первой колонки
                candidate_id = int(self.candidates_table.item(row, 0).text())
                # Открываем окно с подробностями
                self.details_window = DetailsWindow(candidate_id)
                self.details_window.show()
                
            elif action == delete_action:
                # Получаем ID кандидата из первой колонки
                candidate_id = int(self.candidates_table.item(row, 0).text())
                # Здесь можно добавить подтверждение удаления
                reply = QMessageBox.question(self, 'Подтверждение', 
                                          'Вы уверены, что хотите удалить этого кандидата?',
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # Удаляем кандидата из базы данных
                    success, message = delete_candidate_by_id(candidate_id)
                    if success:
                        # Удаляем строку из таблицы
                        self.candidates_table.removeRow(row)
                        QMessageBox.information(self, "Успех", message)
                    else:
                        QMessageBox.warning(self, "Ошибка", message)

    def show_recruiters_context_menu(self, pos):
        menu = QMenu(self)
        add_action = menu.addAction("Добавить")
        delete_action = menu.addAction("Удалить")
        
        action = menu.exec_(self.recruiters_table.viewport().mapToGlobal(pos))
        
        row = self.recruiters_table.rowAt(pos.y())
        
        if action == add_action:
            self.add_recruiter_window = AddRecruiterWindow(self)
            self.add_recruiter_window.dataChanged.connect(self.load_recruiters)
            self.add_recruiter_window.show()
        elif action == delete_action and row >= 0:
            # Получаем ID рекрутера из первой колонки
            recruiter_id = int(self.recruiters_table.item(row, 0).text())
            
            # Получаем ФИО рекрутера для отображения в сообщении
            recruiter_fio = self.recruiters_table.item(row, 1).text()
            
            # Запрашиваем подтверждение удаления
            reply = QMessageBox.question(
                self,
                'Подтверждение удаления',
                f'Вы уверены, что хотите удалить сотрудника {recruiter_fio}?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Удаляем рекрутера из базы данных
                success, message = delete_recruiter_by_id(recruiter_id)
                success, message = reorder_candidate_ids()
                
                if success:
                    # Обновляем таблицу
                    self.load_recruiters()
                    QMessageBox.information(self, "Успех", "Сотрудник успешно удален")
                else:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось удалить сотрудника: {message}")

    def load_recruiters(self):
        success, recruiters_info = get_recruiters_info()
        if success:
            # Очищаем таблицу перед загрузкой новых данных
            self.recruiters_table.clearContents()
            self.recruiters_table.setRowCount(0)
            
            # Устанавливаем количество строк
            self.recruiters_table.setRowCount(len(recruiters_info))
            
            # Заполняем таблицу данными
            for i, recruiter in enumerate(recruiters_info):
                self.recruiters_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.recruiters_table.setItem(i, 1, QTableWidgetItem(str(recruiter['fio'])))
                self.recruiters_table.setItem(i, 2, QTableWidgetItem(str(recruiter['phone_number'])))
                self.recruiters_table.setItem(i, 3, QTableWidgetItem(str(recruiter['age'])))
                self.recruiters_table.setItem(i, 4, QTableWidgetItem(str(recruiter['city'])))
                self.recruiters_table.setItem(i, 5, QTableWidgetItem(str(recruiter['access_code'])))
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные рекрутеров")

    def update_recruiter_info(self, row, fio, age, city, access_code, phone_number):
        success, message = get_recruiters_info(row, fio, age, city, access_code, phone_number)
        if success:
            self.recruiters_table.setItem(row, 1, QTableWidgetItem(fio))
            self.recruiters_table.setItem(row, 2, QTableWidgetItem(phone_number))
            self.recruiters_table.setItem(row, 3, QTableWidgetItem(age))
            self.recruiters_table.setItem(row, 4, QTableWidgetItem(city))
            self.recruiters_table.setItem(row, 5, QTableWidgetItem(access_code))
        else:
            QMessageBox.warning(self, "Ошибка", message)