import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTabWidget, 
                             QButtonGroup, QMessageBox, QRadioButton, QTableWidget, QHeaderView, 
                             QHBoxLayout, QTableWidgetItem, QFrame)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from server import (get_candidate_fio_by_id, get_question_by_id_theory1, save_answer, 
                   get_question_by_id_theory2, save_answer_theory2, 
                   get_question_by_id_theory3, save_answer_theory3, 
                   get_question_by_id_theory4, save_answer_theory4,
                   get_answers_list_theory1, get_answers_list_theory2,
                   get_answers_list_theory3, get_answers_list_theory4,
                   get_question_text_by_id_theory1, get_question_text_by_id_theory2,
                   get_question_text_by_id_theory3, get_question_text_by_id_theory4,
                   get_answer_by_id_theory1, get_answer_by_id_theory2,
                   get_answer_by_id_theory3, get_answer_by_id_theory4,
                   check_answers_exist_theory1, check_answers_exist_theory2, 
                   check_answers_exist_theory3, check_answers_exist_theory4,
                   check_answers_exist_logic, get_question_by_id_logic,
                   save_answer_logic, get_answers_list_logic,
                   get_question_text_by_id_logic, get_answer_by_id_logic)

# Общие стили для приложения
STYLE_SHEET = """
    QWidget {
        font-family: 'Segoe UI', Arial;
        font-size: 14px;
    }
    QLabel {
        color: #333333;
    }
    QPushButton {
        padding: 10px 20px;
        background-color: #0078D7;
        color: white;
        border: none;
        border-radius: 4px;
        min-height: 30px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #106EBE;
    }
    QPushButton:pressed {
        background-color: #005A9E;
    }
    QRadioButton {
        padding: 10px;
        spacing: 10px;
        font-size: 14px;
    }
    QRadioButton::indicator {
        width: 20px;
        height: 20px;
    }
    QTableWidget {
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        background-color: white;
        font-size: 14px;
    }
    QTableWidget::item {
        padding: 10px;
    }
    QHeaderView::section {
        background-color: #F0F0F0;
        padding: 10px;
        border: 1px solid #CCCCCC;
        font-weight: bold;
        font-size: 14px;
    }
    QFrame {
        background-color: white;
        border-radius: 8px;
    }
"""

class TestWindow(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Тест 1")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.ID_candidate = ID_candidate
        self.test_number = 1
        
        # Проверяем, проходил ли кандидат тест
        success, message = check_answers_exist_theory1(ID_candidate)
        if success:
            QMessageBox.warning(self, "Предупреждение", "Предупреждение: Вы уже проходили этот тест. Повторное прохождение невозможно.")
            self.close()
            return
            
        # Массив для хранения ответов пользователя
        self.user_answers = []
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(self.main_layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Показываем начальный экран
        self.show_start_screen()
        
    def show_start_screen(self):
        # Очищаем текущий layout
        self.clear_layout()
        
        # Создаем контейнер для содержимого
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        
        title = QLabel("Данный тест состоит из десяти вопросов, к каждому прилагается четыре варианта ответа. Этим тестом мы хотим проверить ваши знания основ языка Python. Нажмите кнопку \"Начать\", когда будете готовы.")
        title.setFont(QFont('Segoe UI', 14))
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setStyleSheet("color: #0078D7;")
        
        start_button = QPushButton("Начать")
        start_button.setFont(QFont('Segoe UI', 12))
        start_button.setMinimumWidth(200)
        start_button.clicked.connect(self.start_test)
        
        content_layout.addWidget(title)
        content_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        
        self.main_layout.addWidget(content_frame)
        
    def clear_layout(self):
        # Удаляем все виджеты из layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
    def start_test(self):
        # Запускаем тест
        self.current_question = 1
        self.show_question(self.current_question)
        
    def show_question(self, question_number):
        success, question_data = get_question_by_id_theory1(question_number)
        
        if success:
            # Очищаем текущий layout
            self.clear_layout()
            
            # Создаем контейнер для вопроса
            question_frame = QFrame()
            question_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 8px;
                    padding: 20px;
                }
            """)
            question_layout = QVBoxLayout(question_frame)
            question_layout.setSpacing(20)
            
            # Создаем и настраиваем label для вопроса
            question_label = QLabel(question_data['question'])
            question_label.setFont(QFont('Segoe UI', 14))
            question_label.setWordWrap(True)
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setStyleSheet("color: #0078D7;")
            
            # Создаем radio buttons для вариантов ответов
            self.answer_group = QButtonGroup()
            answers_frame = QFrame()
            answers_layout = QVBoxLayout(answers_frame)
            answers_layout.setSpacing(10)
            
            for i in range(1, 5):
                radio_button = QRadioButton(question_data[f'answer{i}'])
                radio_button.setFont(QFont('Segoe UI', 12))
                radio_button.setProperty('answer_value', i)
                self.answer_group.addButton(radio_button)
                answers_layout.addWidget(radio_button)
            
            # Кнопка для следующего вопроса
            next_button = QPushButton("Следующий вопрос")
            next_button.setFont(QFont('Segoe UI', 12))
            next_button.setMinimumWidth(200)
            next_button.clicked.connect(self.next_question)
            
            question_layout.addWidget(question_label)
            question_layout.addWidget(answers_frame)
            question_layout.addWidget(next_button, alignment=Qt.AlignCenter)
            
            self.main_layout.addWidget(question_frame)
    
    def next_question(self):
        # Проверяем, выбран ли вариант ответа
        selected_button = self.answer_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Предупреждение", "Необходимо выбрать вариант ответа.")
            return
            
        # Сохраняем выбранный ответ вместе с ID кандидата и ID вопроса
        answer_value = selected_button.property('answer_value')
        self.user_answers.append((self.ID_candidate, self.current_question, answer_value))
        
        self.current_question += 1
        if self.current_question <= 10:
            self.show_question(self.current_question)
        else:
            self.save_and_finish_test()
    
    def save_and_finish_test(self):
        # Сохраняем все ответы в базу данных
        for i in range(len(self.user_answers)):
            id_candidate, id_question, answer = self.user_answers[i]
            success, message = save_answer(id_candidate, id_question, answer)
            if not success:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении ответа {i+1}: {message}")
                return
        
        # Очищаем текущий layout
        self.clear_layout()
        
        # Создаем контейнер для сообщения
        message_frame = QFrame()
        message_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        message_layout = QVBoxLayout(message_frame)
        
        # Показываем сообщение о завершении
        message = QLabel("Поздравляем с прохождением теста!\nВаши ответы записаны.")
        message.setFont(QFont('Segoe UI', 14))
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("color: #0078D7;")
        
        message_layout.addWidget(message)
        self.main_layout.addWidget(message_frame)

class TestWindow2(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Тест 2")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.ID_candidate = ID_candidate
        self.test_number = 2
        
        # Проверяем, проходил ли кандидат тест
        success, message = check_answers_exist_theory2(ID_candidate)
        if success:
            QMessageBox.warning(self, "Предупреждение", "Предупреждение: Вы уже проходили этот тест. Повторное прохождение невозможно.")
            self.close()
            return
            
        # Массив для хранения ответов пользователя
        self.user_answers = []
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(self.main_layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Показываем начальный экран
        self.show_start_screen()
        
    def clear_layout(self):
        # Удаляем все виджеты из layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
    def show_start_screen(self):
        # Очищаем текущий layout
        self.clear_layout()
        
        # Создаем контейнер для содержимого
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        
        title = QLabel("Данный тест состоит из десяти вопросов, к каждому прилагается четыре варианта ответа. Этим тестом мы хотим проверить ваши знания основ языка Python. Нажмите кнопку \"Начать\", когда будете готовы.")
        title.setFont(QFont('Segoe UI', 14))
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setStyleSheet("color: #0078D7;")
        
        start_button = QPushButton("Начать")
        start_button.setFont(QFont('Segoe UI', 14))
        start_button.setMinimumWidth(250)
        start_button.setMinimumHeight(50)
        start_button.clicked.connect(self.start_test)
        
        content_layout.addWidget(title)
        content_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        
        self.main_layout.addWidget(content_frame)
        
    def start_test(self):
        # Запускаем тест
        self.current_question = 1
        self.show_question(self.current_question)
        
    def show_question(self, question_number):
        success, question_data = get_question_by_id_theory2(question_number)
        
        if success:
            # Очищаем текущий layout
            self.clear_layout()
            
            # Создаем контейнер для вопроса
            question_frame = QFrame()
            question_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 8px;
                    padding: 20px;
                }
            """)
            question_layout = QVBoxLayout(question_frame)
            question_layout.setSpacing(20)
            
            # Создаем и настраиваем label для вопроса
            question_label = QLabel(question_data['question'])
            question_label.setFont(QFont('Segoe UI', 14))
            question_label.setWordWrap(True)
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setStyleSheet("color: #0078D7;")
            
            # Создаем radio buttons для вариантов ответов
            self.answer_group = QButtonGroup()
            answers_frame = QFrame()
            answers_layout = QVBoxLayout(answers_frame)
            answers_layout.setSpacing(10)
            
            for i in range(1, 5):
                radio_button = QRadioButton(question_data[f'answer{i}'])
                radio_button.setFont(QFont('Segoe UI', 14))
                radio_button.setProperty('answer_value', i)
                self.answer_group.addButton(radio_button)
                answers_layout.addWidget(radio_button)
            
            # Кнопка для следующего вопроса
            next_button = QPushButton("Следующий вопрос")
            next_button.setFont(QFont('Segoe UI', 14))
            next_button.setMinimumWidth(250)
            next_button.setMinimumHeight(50)
            next_button.clicked.connect(self.next_question)
            
            question_layout.addWidget(question_label)
            question_layout.addWidget(answers_frame)
            question_layout.addWidget(next_button, alignment=Qt.AlignCenter)
            
            self.main_layout.addWidget(question_frame)
    
    def next_question(self):
        # Проверяем, выбран ли вариант ответа
        selected_button = self.answer_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Предупреждение", "Необходимо выбрать вариант ответа.")
            return
            
        # Сохраняем выбранный ответ вместе с ID кандидата и ID вопроса
        answer_value = selected_button.property('answer_value')
        self.user_answers.append((self.ID_candidate, self.current_question, answer_value))
        
        self.current_question += 1
        if self.current_question <= 10:
            self.show_question(self.current_question)
        else:
            self.save_and_finish_test()
    
    def save_and_finish_test(self):
        # Сохраняем все ответы в базу данных
        for i in range(len(self.user_answers)):
            id_candidate, id_question, answer = self.user_answers[i]
            success, message = save_answer_theory2(id_candidate, id_question, answer)
            if not success:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении ответа {i+1}: {message}")
                return
        
        # Очищаем текущий layout
        self.clear_layout()
        
        # Создаем контейнер для сообщения
        message_frame = QFrame()
        message_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        message_layout = QVBoxLayout(message_frame)
        
        # Показываем сообщение о завершении
        message = QLabel("Поздравляем с прохождением теста!\nВаши ответы записаны.")
        message.setFont(QFont('Segoe UI', 14))
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("color: #0078D7;")
        
        message_layout.addWidget(message)
        self.main_layout.addWidget(message_frame)

class TestWindow3(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Тест 3")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.ID_candidate = ID_candidate
        self.test_number = 3
        
        # Проверяем, проходил ли кандидат тест
        success, message = check_answers_exist_theory3(ID_candidate)
        if success:
            QMessageBox.warning(self, "Предупреждение", "Предупреждение: Вы уже проходили этот тест. Повторное прохождение невозможно.")
            self.close()
            return
            
        # Массив для хранения ответов пользователя
        self.user_answers = []
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(self.main_layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Показываем начальный экран
        self.show_start_screen()
        
    def clear_layout(self):
        # Удаляем все виджеты из layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
    def show_start_screen(self):
        # Очищаем текущий layout
        self.clear_layout()
        
        # Создаем контейнер для содержимого
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        
        title = QLabel("Данный тест состоит из десяти вопросов, к каждому прилагается четыре варианта ответа. Этим тестом мы хотим проверить ваши знания основ языка Python. Нажмите кнопку \"Начать\", когда будете готовы.")
        title.setFont(QFont('Segoe UI', 14))
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setStyleSheet("color: #0078D7;")
        
        start_button = QPushButton("Начать")
        start_button.setFont(QFont('Segoe UI', 14))
        start_button.setMinimumWidth(250)
        start_button.setMinimumHeight(50)
        start_button.clicked.connect(self.start_test)
        
        content_layout.addWidget(title)
        content_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        
        self.main_layout.addWidget(content_frame)
        
    def start_test(self):
        # Запускаем тест
        self.current_question = 1
        self.show_question(self.current_question)
        
    def show_question(self, question_number):
        success, question_data = get_question_by_id_theory3(question_number)
        
        if success:
            # Очищаем текущий layout
            self.clear_layout()
            
            # Создаем контейнер для вопроса
            question_frame = QFrame()
            question_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 8px;
                    padding: 20px;
                }
            """)
            question_layout = QVBoxLayout(question_frame)
            question_layout.setSpacing(20)
            
            # Создаем и настраиваем label для вопроса
            question_label = QLabel(question_data['question'])
            question_label.setFont(QFont('Segoe UI', 14))
            question_label.setWordWrap(True)
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setStyleSheet("color: #0078D7;")
            
            # Создаем radio buttons для вариантов ответов
            self.answer_group = QButtonGroup()
            answers_frame = QFrame()
            answers_layout = QVBoxLayout(answers_frame)
            answers_layout.setSpacing(10)
            
            for i in range(1, 5):
                radio_button = QRadioButton(question_data[f'answer{i}'])
                radio_button.setFont(QFont('Segoe UI', 14))
                radio_button.setProperty('answer_value', i)
                self.answer_group.addButton(radio_button)
                answers_layout.addWidget(radio_button)
            
            # Кнопка для следующего вопроса
            next_button = QPushButton("Следующий вопрос")
            next_button.setFont(QFont('Segoe UI', 14))
            next_button.setMinimumWidth(250)
            next_button.setMinimumHeight(50)
            next_button.clicked.connect(self.next_question)
            
            question_layout.addWidget(question_label)
            question_layout.addWidget(answers_frame)
            question_layout.addWidget(next_button, alignment=Qt.AlignCenter)
            
            self.main_layout.addWidget(question_frame)
    
    def next_question(self):
        # Проверяем, выбран ли вариант ответа
        selected_button = self.answer_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Предупреждение", "Необходимо выбрать вариант ответа.")
            return
            
        # Сохраняем выбранный ответ вместе с ID кандидата и ID вопроса
        answer_value = selected_button.property('answer_value')
        self.user_answers.append((self.ID_candidate, self.current_question, answer_value))
        
        self.current_question += 1
        if self.current_question <= 10:
            self.show_question(self.current_question)
        else:
            self.save_and_finish_test()
    
    def save_and_finish_test(self):
        # Сохраняем все ответы в базу данных
        for i in range(len(self.user_answers)):
            id_candidate, id_question, answer = self.user_answers[i]
            success, message = save_answer_theory3(id_candidate, id_question, answer)
            if not success:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении ответа {i+1}: {message}")
                return
        
        # Очищаем текущий layout
        self.clear_layout()
        
        # Создаем контейнер для сообщения
        message_frame = QFrame()
        message_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        message_layout = QVBoxLayout(message_frame)
        
        # Показываем сообщение о завершении
        message = QLabel("Поздравляем с прохождением теста!\nВаши ответы записаны.")
        message.setFont(QFont('Segoe UI', 14))
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("color: #0078D7;")
        
        message_layout.addWidget(message)
        self.main_layout.addWidget(message_frame)

class TestWindow4(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Тест 4")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.ID_candidate = ID_candidate
        self.test_number = 4
        
        # Проверяем, проходил ли кандидат тест
        success, message = check_answers_exist_theory4(ID_candidate)
        if success:
            QMessageBox.warning(self, "Предупреждение", "Предупреждение: Вы уже проходили этот тест. Повторное прохождение невозможно.")
            self.close()
            return
            
        # Массив для хранения ответов пользователя
        self.user_answers = []
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(self.main_layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Показываем начальный экран
        self.show_start_screen()
        
    def clear_layout(self):
        # Удаляем все виджеты из layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
    def show_start_screen(self):
        # Очищаем текущий layout
        self.clear_layout()
        
        # Создаем контейнер для содержимого
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        
        title = QLabel("Данный тест состоит из десяти вопросов, к каждому прилагается четыре варианта ответа. Этим тестом мы хотим проверить ваши знания основ языка Python. Нажмите кнопку \"Начать\", когда будете готовы.")
        title.setFont(QFont('Segoe UI', 14))
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setStyleSheet("color: #0078D7;")
        
        start_button = QPushButton("Начать")
        start_button.setFont(QFont('Segoe UI', 14))
        start_button.setMinimumWidth(250)
        start_button.setMinimumHeight(50)
        start_button.clicked.connect(self.start_test)
        
        content_layout.addWidget(title)
        content_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        
        self.main_layout.addWidget(content_frame)
        
    def start_test(self):
        # Запускаем тест
        self.current_question = 1
        self.show_question(self.current_question)
        
    def show_question(self, question_number):
        success, question_data = get_question_by_id_theory4(question_number)
        
        if success:
            # Очищаем текущий layout
            self.clear_layout()
            
            # Создаем контейнер для вопроса
            question_frame = QFrame()
            question_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 8px;
                    padding: 20px;
                }
            """)
            question_layout = QVBoxLayout(question_frame)
            question_layout.setSpacing(20)
            
            # Создаем и настраиваем label для вопроса
            question_label = QLabel(question_data['question'])
            question_label.setFont(QFont('Segoe UI', 14))
            question_label.setWordWrap(True)
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setStyleSheet("color: #0078D7;")
            
            # Создаем radio buttons для вариантов ответов
            self.answer_group = QButtonGroup()
            answers_frame = QFrame()
            answers_layout = QVBoxLayout(answers_frame)
            answers_layout.setSpacing(10)
            
            for i in range(1, 5):
                radio_button = QRadioButton(question_data[f'answer{i}'])
                radio_button.setFont(QFont('Segoe UI', 14))
                radio_button.setProperty('answer_value', i)
                self.answer_group.addButton(radio_button)
                answers_layout.addWidget(radio_button)
            
            # Кнопка для следующего вопроса
            next_button = QPushButton("Следующий вопрос")
            next_button.setFont(QFont('Segoe UI', 14))
            next_button.setMinimumWidth(250)
            next_button.setMinimumHeight(50)
            next_button.clicked.connect(self.next_question)
            
            question_layout.addWidget(question_label)
            question_layout.addWidget(answers_frame)
            question_layout.addWidget(next_button, alignment=Qt.AlignCenter)
            
            self.main_layout.addWidget(question_frame)
    
    def next_question(self):
        # Проверяем, выбран ли вариант ответа
        selected_button = self.answer_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Предупреждение", "Необходимо выбрать вариант ответа.")
            return
            
        # Сохраняем выбранный ответ вместе с ID кандидата и ID вопроса
        answer_value = selected_button.property('answer_value')
        self.user_answers.append((self.ID_candidate, self.current_question, answer_value))
        
        self.current_question += 1
        if self.current_question <= 10:
            self.show_question(self.current_question)
        else:
            self.save_and_finish_test()
    
    def save_and_finish_test(self):
        # Сохраняем все ответы в базу данных
        for i in range(len(self.user_answers)):
            id_candidate, id_question, answer = self.user_answers[i]
            success, message = save_answer_theory4(id_candidate, id_question, answer)
            if not success:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении ответа {i+1}: {message}")
                return
        
        # Очищаем текущий layout
        self.clear_layout()
        
        # Создаем контейнер для сообщения
        message_frame = QFrame()
        message_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        message_layout = QVBoxLayout(message_frame)
        
        # Показываем сообщение о завершении
        message = QLabel("Поздравляем с прохождением теста!\nВаши ответы записаны.")
        message.setFont(QFont('Segoe UI', 14))
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("color: #0078D7;")
        
        message_layout.addWidget(message)
        self.main_layout.addWidget(message_frame)

class TestWindow5(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Тест 5")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        self.ID_candidate = ID_candidate
        self.test_number = 5
        
        # Проверяем, проходил ли кандидат тест
        success, message = check_answers_exist_logic(ID_candidate)
        if success:
            QMessageBox.warning(self, "Предупреждение", "Предупреждение: Вы уже проходили этот тест. Повторное прохождение невозможно.")
            self.close()
            return
            
        # Массив для хранения ответов пользователя
        self.user_answers = []
        self.current_question = 1
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(self.main_layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Показываем начальный экран
        self.show_start_screen()
        
    def clear_layout(self):
        # Удаляем все виджеты из layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
    def show_start_screen(self):
        # Очищаем текущий layout
        self.clear_layout()
        
        # Создаем контейнер для содержимого
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        
        title = QLabel("Данный тест состоит из десяти вопросов, к каждому прилагается четыре варианта ответа. Этим тестом мы хотим проверить ваши логические способности. Нажмите кнопку \"Начать\", когда будете готовы.")
        title.setFont(QFont('Segoe UI', 14))
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setStyleSheet("color: #0078D7;")
        
        start_button = QPushButton("Начать")
        start_button.setFont(QFont('Segoe UI', 14))
        start_button.setMinimumWidth(250)
        start_button.setMinimumHeight(50)
        start_button.clicked.connect(self.start_test)
        
        content_layout.addWidget(title)
        content_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        
        self.main_layout.addWidget(content_frame)
        
    def start_test(self):
        # Запускаем тест
        self.current_question = 1
        self.show_question(self.current_question)
        
    def show_question(self, question_number):
        success, question_data = get_question_by_id_logic(question_number)
        
        if success:
            # Очищаем текущий layout
            self.clear_layout()
            
            # Создаем контейнер для вопроса
            question_frame = QFrame()
            question_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 8px;
                    padding: 20px;
                }
            """)
            question_layout = QVBoxLayout(question_frame)
            question_layout.setSpacing(20)
            
            # Создаем и настраиваем label для вопроса
            question_label = QLabel(question_data['question'])
            question_label.setFont(QFont('Segoe UI', 14))
            question_label.setWordWrap(True)
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setStyleSheet("color: #0078D7;")
            
            # Создаем radio buttons для вариантов ответов
            self.answer_group = QButtonGroup()
            answers_frame = QFrame()
            answers_layout = QVBoxLayout(answers_frame)
            answers_layout.setSpacing(10)
            
            for i in range(1, 5):
                radio_button = QRadioButton(question_data[f'answer{i}'])
                radio_button.setFont(QFont('Segoe UI', 14))
                radio_button.setProperty('answer_value', i)
                self.answer_group.addButton(radio_button)
                answers_layout.addWidget(radio_button)
            
            # Если это 6-й вопрос, добавляем картинку
            if question_number == 6:
                image_label = QLabel()
                pixmap = QPixmap("image.png")
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    image_label.setPixmap(pixmap)
                    image_label.setAlignment(Qt.AlignCenter)
                    question_layout.addWidget(image_label)
            
            # Кнопка для следующего вопроса
            next_button = QPushButton("Следующий вопрос")
            next_button.setFont(QFont('Segoe UI', 14))
            next_button.setMinimumWidth(250)
            next_button.setMinimumHeight(50)
            next_button.clicked.connect(self.next_question)
            
            question_layout.addWidget(question_label)
            question_layout.addWidget(answers_frame)
            question_layout.addWidget(next_button, alignment=Qt.AlignCenter)
            
            self.main_layout.addWidget(question_frame)
    
    def next_question(self):
        # Проверяем, выбран ли вариант ответа
        selected_button = self.answer_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Предупреждение", "Необходимо выбрать вариант ответа.")
            return
            
        # Сохраняем выбранный ответ вместе с ID кандидата и ID вопроса
        answer_value = selected_button.property('answer_value')
        self.user_answers.append((self.ID_candidate, self.current_question, answer_value))
        
        self.current_question += 1
        if self.current_question <= 10:
            self.show_question(self.current_question)
        else:
            self.save_and_finish_test()
    
    def save_and_finish_test(self):
        # Сохраняем все ответы в базу данных
        for i in range(len(self.user_answers)):
            id_candidate, id_question, answer = self.user_answers[i]
            success, message = save_answer_logic(id_candidate, id_question, answer)
            if not success:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении ответа {i+1}: {message}")
                return
        
        # Очищаем текущий layout
        self.clear_layout()
        
        # Создаем контейнер для сообщения
        message_frame = QFrame()
        message_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        message_layout = QVBoxLayout(message_frame)
        
        # Показываем сообщение о завершении
        message = QLabel("Поздравляем с прохождением теста!\nВаши ответы записаны.")
        message.setFont(QFont('Segoe UI', 14))
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("color: #0078D7;")
        
        message_layout.addWidget(message)
        self.main_layout.addWidget(message_frame)

class ResultsWindow1(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Результаты теста 1")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.ID_candidate = ID_candidate
        
        # Получаем ответы кандидата
        success, answers = get_answers_list_theory1(ID_candidate)
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(main_layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Заголовок
        title = QLabel("Результаты теста 1")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078D7; margin-bottom: 20px;")
        main_layout.addWidget(title)
        
        # Создаем таблицу
        table = QTableWidget()
        table.setColumnCount(2)
        table.setRowCount(10)
        table.setHorizontalHeaderLabels(["Вопрос", "Ответ"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
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
                font-size: 14px;
            }
        """)
        
        # Заполняем таблицу
        for i, (question_id, answer_id) in enumerate(answers):
            # Получаем текст вопроса
            success, question_text = get_question_text_by_id_theory1(question_id)
            if success:
                question_item = QTableWidgetItem(question_text)
                question_item.setFlags(question_item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, 0, question_item)
            
            # Получаем текст ответа
            success, answer_text = get_answer_by_id_theory1(question_id, answer_id)
            if success:
                answer_item = QTableWidgetItem(answer_text)
                answer_item.setFlags(answer_item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, 1, answer_item)
        
        # Устанавливаем высоту строк
        for i in range(table.rowCount()):
            table.setRowHeight(i, 60)
        
        main_layout.addWidget(table)
        
        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.setFont(QFont('Segoe UI', 14))
        close_button.setMinimumWidth(250)
        close_button.setMinimumHeight(50)
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button, alignment=Qt.AlignCenter)

class ResultsWindow2(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Результаты теста 2")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.ID_candidate = ID_candidate
        
        # Получаем ответы кандидата
        success, answers = get_answers_list_theory2(ID_candidate)
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(main_layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Заголовок
        title = QLabel("Результаты теста 2")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078D7; margin-bottom: 20px;")
        main_layout.addWidget(title)
        
        # Создаем таблицу
        table = QTableWidget()
        table.setColumnCount(2)
        table.setRowCount(10)
        table.setHorizontalHeaderLabels(["Вопрос", "Ответ"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
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
                font-size: 14px;
            }
        """)
        
        # Заполняем таблицу
        for i, (question_id, answer_id) in enumerate(answers):
            # Получаем текст вопроса
            success, question_text = get_question_text_by_id_theory2(question_id)
            if success:
                question_item = QTableWidgetItem(question_text)
                question_item.setFlags(question_item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, 0, question_item)
            
            # Получаем текст ответа
            success, answer_text = get_answer_by_id_theory2(question_id, answer_id)
            if success:
                answer_item = QTableWidgetItem(answer_text)
                answer_item.setFlags(answer_item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, 1, answer_item)
        
        # Устанавливаем высоту строк
        for i in range(table.rowCount()):
            table.setRowHeight(i, 60)
        
        main_layout.addWidget(table)
        
        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.setFont(QFont('Segoe UI', 14))
        close_button.setMinimumWidth(250)
        close_button.setMinimumHeight(50)
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button, alignment=Qt.AlignCenter)

class ResultsWindow3(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Результаты теста 3")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.ID_candidate = ID_candidate
        
        # Получаем ответы кандидата
        success, answers = get_answers_list_theory3(ID_candidate)
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(main_layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Заголовок
        title = QLabel("Результаты теста 3")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078D7; margin-bottom: 20px;")
        main_layout.addWidget(title)
        
        # Создаем таблицу
        table = QTableWidget()
        table.setColumnCount(2)
        table.setRowCount(10)
        table.setHorizontalHeaderLabels(["Вопрос", "Ответ"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
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
                font-size: 14px;
            }
        """)
        
        # Заполняем таблицу
        for i, (question_id, answer_id) in enumerate(answers):
            # Получаем текст вопроса
            success, question_text = get_question_text_by_id_theory3(question_id)
            if success:
                question_item = QTableWidgetItem(question_text)
                question_item.setFlags(question_item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, 0, question_item)
            
            # Получаем текст ответа
            success, answer_text = get_answer_by_id_theory3(question_id, answer_id)
            if success:
                answer_item = QTableWidgetItem(answer_text)
                answer_item.setFlags(answer_item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, 1, answer_item)
        
        # Устанавливаем высоту строк
        for i in range(table.rowCount()):
            table.setRowHeight(i, 60)
        
        main_layout.addWidget(table)
        
        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.setFont(QFont('Segoe UI', 14))
        close_button.setMinimumWidth(250)
        close_button.setMinimumHeight(50)
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button, alignment=Qt.AlignCenter)

class ResultsWindow4(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Результаты теста 4")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.ID_candidate = ID_candidate
        
        # Получаем ответы кандидата
        success, answers = get_answers_list_theory4(ID_candidate)
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(main_layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Заголовок
        title = QLabel("Результаты теста 4")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078D7; margin-bottom: 20px;")
        main_layout.addWidget(title)
        
        # Создаем таблицу
        table = QTableWidget()
        table.setColumnCount(2)
        table.setRowCount(10)
        table.setHorizontalHeaderLabels(["Вопрос", "Ответ"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
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
                font-size: 14px;
            }
        """)
        
        # Заполняем таблицу
        for i, (question_id, answer_id) in enumerate(answers):
            # Получаем текст вопроса
            success, question_text = get_question_text_by_id_theory4(question_id)
            if success:
                question_item = QTableWidgetItem(question_text)
                question_item.setFlags(question_item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, 0, question_item)
            
            # Получаем текст ответа
            success, answer_text = get_answer_by_id_theory4(question_id, answer_id)
            if success:
                answer_item = QTableWidgetItem(answer_text)
                answer_item.setFlags(answer_item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, 1, answer_item)
        
        # Устанавливаем высоту строк
        for i in range(table.rowCount()):
            table.setRowHeight(i, 60)
        
        main_layout.addWidget(table)
        
        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.setFont(QFont('Segoe UI', 14))
        close_button.setMinimumWidth(250)
        close_button.setMinimumHeight(50)
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button, alignment=Qt.AlignCenter)

class ResultsWindow5(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Результаты теста 5")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.ID_candidate = ID_candidate
        
        # Получаем ответы кандидата
        success, answers = get_answers_list_logic(ID_candidate)
        
        # Создаем основной контейнер
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        
        # Создаем основной layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_frame.setLayout(main_layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)
        
        # Заголовок
        title = QLabel("Результаты теста 5")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078D7; margin-bottom: 20px;")
        main_layout.addWidget(title)
        
        # Создаем таблицу
        table = QTableWidget()
        table.setColumnCount(2)
        table.setRowCount(10)
        table.setHorizontalHeaderLabels(["Вопрос", "Ответ"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
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
                font-size: 14px;
            }
        """)
        
        # Заполняем таблицу
        for i, (question_id, answer_id) in enumerate(answers):
            # Получаем текст вопроса
            success, question_text = get_question_text_by_id_logic(question_id)
            if success:
                question_item = QTableWidgetItem(question_text)
                question_item.setFlags(question_item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, 0, question_item)
            
            # Получаем текст ответа
            success, answer_text = get_answer_by_id_logic(question_id, answer_id)
            if success:
                answer_item = QTableWidgetItem(answer_text)
                answer_item.setFlags(answer_item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, 1, answer_item)
        
        # Устанавливаем высоту строк
        for i in range(table.rowCount()):
            table.setRowHeight(i, 60)
        
        main_layout.addWidget(table)
        
        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.setFont(QFont('Segoe UI', 14))
        close_button.setMinimumWidth(250)
        close_button.setMinimumHeight(50)
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button, alignment=Qt.AlignCenter)

class MenuWindow(QWidget):
    def __init__(self, ID_candidate):
        super().__init__()
        self.setWindowTitle("Меню")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        # ID кандидата
        self.ID_candidate = ID_candidate
        
        # Получаем ФИО кандидата
        success, fio = get_candidate_fio_by_id(ID_candidate)
        if not success:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при получении данных кандидата: {fio}")
            return
        
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
        
        # Создаем заголовок
        title = QLabel(f"Добро пожаловать, {fio}!")
        title.setFont(QFont('Segoe UI', 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078D7; margin: 20px;")
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #F0F0F0;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            QTabBar::tab:hover {
                background-color: #E0E0E0;
            }
        """)
        
        # Создаем первую вкладку (Главная)
        self.tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(title)
        self.tab1.setLayout(tab1_layout)
        
        # Создаем вторую вкладку (Тесты)
        self.tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout.setSpacing(15)
        
        # Создаем контейнер для кнопок
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setSpacing(15)
        
        # Создаем кнопки
        test1_button = QPushButton("Тест 1")
        test2_button = QPushButton("Тест 2")
        test3_button = QPushButton("Тест 3")
        test4_button = QPushButton("Тест 4")
        test5_button = QPushButton("Тест 5")
        
        # Настраиваем кнопки
        for button in [test1_button, test2_button, test3_button, test4_button, test5_button]:
            button.setFont(QFont('Segoe UI', 14))
            button.setMinimumWidth(250)
            button.setMinimumHeight(50)
        
        # Подключаем обработчики
        test1_button.clicked.connect(self.open_test1)
        test2_button.clicked.connect(self.open_test2)
        test3_button.clicked.connect(self.open_test3)
        test4_button.clicked.connect(self.open_test4)
        test5_button.clicked.connect(self.open_test5)
        
        # Добавляем кнопки в layout
        buttons_layout.addWidget(test1_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(test2_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(test3_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(test4_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(test5_button, alignment=Qt.AlignCenter)
        
        tab2_layout.addWidget(buttons_frame)
        self.tab2.setLayout(tab2_layout)
        
        # Создаем третью вкладку (Ответы)
        self.tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        
        # Создаем контейнер для таблицы
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        
        # Создаем таблицу
        table = QTableWidget()
        table.setRowCount(5)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Доступные тесты", "Ответы"])
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #F0F0F0;
                padding: 10px;
                border: 1px solid #CCCCCC;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        # Устанавливаем минимальную высоту строк
        table.verticalHeader().setDefaultSectionSize(80)
        
        # Растягиваем столбцы по содержимому
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        # Заполняем таблицу
        for i in range(5):
            # Добавляем название теста
            test_label = QLabel(f"Тест {i+1}")
            test_label.setAlignment(Qt.AlignCenter)
            test_label.setFont(QFont('Segoe UI', 16, QFont.Bold))
            test_label.setStyleSheet("color: #0078D7;")
            table.setCellWidget(i, 0, test_label)
            
            # Добавляем кнопку "посмотреть"
            view_button = QPushButton("Посмотреть")
            view_button.setFont(QFont('Segoe UI', 14))
            view_button.setMinimumWidth(180)
            view_button.setMinimumHeight(45)
            
            # Подключаем соответствующий обработчик для каждой кнопки
            if i == 0:
                view_button.clicked.connect(self.show_answers_theory1)
            elif i == 1:
                view_button.clicked.connect(self.show_answers_theory2)
            elif i == 2:
                view_button.clicked.connect(self.show_answers_theory3)
            elif i == 3:
                view_button.clicked.connect(self.show_answers_theory4)
            else:
                view_button.clicked.connect(self.show_answers_theory5)
            
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.addWidget(view_button)
            cell_layout.setAlignment(Qt.AlignCenter)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            table.setCellWidget(i, 1, cell_widget)
        
        # Настраиваем размеры столбцов и строк
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        
        table_layout.addWidget(table)
        tab3_layout.addWidget(table_frame)
        self.tab3.setLayout(tab3_layout)
        
        # Добавляем вкладки
        self.tabs.addTab(self.tab1, "Главная")
        self.tabs.addTab(self.tab2, "Тесты")
        self.tabs.addTab(self.tab3, "Ответы")
        
        # Добавляем все в основной layout
        layout.addWidget(self.tabs)
        main_frame.setLayout(layout)
        
        # Создаем основной layout для окна
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(main_frame)

    def open_test1(self):
        self.test_window = TestWindow(self.ID_candidate)
        self.test_window.show()
    
    def open_test2(self):
        self.test_window = TestWindow2(self.ID_candidate)
        self.test_window.show()

    def open_test3(self):
        self.test_window = TestWindow3(self.ID_candidate)
        self.test_window.show()
    
    def open_test4(self):
        self.test_window = TestWindow4(self.ID_candidate)
        self.test_window.show()
        
    def open_test5(self):
        self.test_window = TestWindow5(self.ID_candidate)
        self.test_window.show()

    def show_answers_theory1(self):
        self.results_window = ResultsWindow1(self.ID_candidate)
        self.results_window.show()

    def show_answers_theory2(self):
        self.results_window = ResultsWindow2(self.ID_candidate)
        self.results_window.show()

    def show_answers_theory3(self):
        self.results_window = ResultsWindow3(self.ID_candidate)
        self.results_window.show()

    def show_answers_theory4(self):
        self.results_window = ResultsWindow4(self.ID_candidate)
        self.results_window.show()

    def show_answers_theory5(self):
        self.results_window = ResultsWindow5(self.ID_candidate)
        self.results_window.show()