import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from server import add_candidate, get_candidate_id_by_access_code, get_recruiter_id_by_access_code
from menu import MenuWindow
from menu_recruiter import MenuRecruiterWindow

# Общие стили для приложения
STYLE_SHEET = """
    QWidget {
        font-family: 'Segoe UI', Arial;
        font-size: 12px;
    }
    QLabel {
        color: #333333;
    }
    QLineEdit {
        padding: 8px;
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        background-color: white;
        min-height: 20px;
    }
    QLineEdit:focus {
        border: 1px solid #0078D7;
    }
    QPushButton {
        padding: 8px 16px;
        background-color: #0078D7;
        color: white;
        border: none;
        border-radius: 4px;
        min-height: 20px;
    }
    QPushButton:hover {
        background-color: #106EBE;
    }
    QPushButton:pressed {
        background-color: #005A9E;
    }
    QFrame {
        background-color: white;
        border-radius: 8px;
    }
"""

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добро пожаловать")
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
        
        # Создаем заголовок "Добро пожаловать"
        self.title_label = QLabel("Добро пожаловать")
        font = QFont('Segoe UI', 24, QFont.Bold)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: #0078D7; margin: 20px;")
        
        # Создаем поле для ввода кода авторизации
        self.auth_code_label = QLabel("Введите код авторизации:")
        self.auth_code_label.setFont(QFont('Segoe UI', 12))
        self.auth_code_input = QLineEdit()
        self.auth_code_input.setPlaceholderText("Введите ваш код доступа")
        self.auth_code_input.setMinimumWidth(300)
        
        # Кнопка авторизации
        self.auth_button = QPushButton("Авторизоваться")
        self.auth_button.setFont(QFont('Segoe UI', 12))
        self.auth_button.setMinimumWidth(200)
        self.auth_button.clicked.connect(self.authorize)
        
        # Кнопка регистрации
        self.register_button = QPushButton("Регистрация")
        self.register_button.setFont(QFont('Segoe UI', 12))
        self.register_button.setFixedWidth(150)
        self.register_button.clicked.connect(self.open_registration)
        
        # Создаем основной вертикальный layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Создаем горизонтальный layout для заголовка и кнопки регистрации
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        header_layout.addWidget(self.register_button, alignment=Qt.AlignRight | Qt.AlignTop)
        layout.addLayout(header_layout)
        
        # Добавляем отступ
        layout.addSpacing(40)
        
        # Создаем контейнер для формы авторизации
        auth_frame = QFrame()
        auth_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        auth_layout = QVBoxLayout(auth_frame)
        auth_layout.setSpacing(15)
        
        # Добавляем поля в контейнер
        auth_layout.addWidget(self.auth_code_label)
        auth_layout.addWidget(self.auth_code_input)
        auth_layout.addWidget(self.auth_button, alignment=Qt.AlignCenter)
        
        layout.addWidget(auth_frame)
        layout.addStretch()
        
        main_frame.setLayout(layout)
        
        # Создаем основной layout для окна
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_frame)
        
    def authorize(self):
        auth_code = self.auth_code_input.text()
        if not auth_code:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите код авторизации")
            return
            
        # Проверяем код доступа кандидата
        success_candidate, result_candidate = get_candidate_id_by_access_code(auth_code)
        if success_candidate:
            QMessageBox.information(self, "Успех", "Авторизация успешна!")
            self.menu_window = MenuWindow(result_candidate)
            self.menu_window.show()
            self.close()
            return
            
        # Проверяем код доступа рекрутера
        success_recruiter, result_recruiter = get_recruiter_id_by_access_code(auth_code)
        if success_recruiter:
            QMessageBox.information(self, "Успех", "Авторизация успешна!")
            self.menu_recruiter_window = MenuRecruiterWindow(result_recruiter)
            self.menu_recruiter_window.show()
            self.close()
            return
            
        QMessageBox.warning(self, "Ошибка", "Неверный код авторизации")
        
    def open_registration(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация нового пользователя")
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
        
        # Создаем заголовок "Регистрация"
        self.title_label = QLabel("Регистрация")
        font = QFont('Segoe UI', 24, QFont.Bold)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: #0078D7; margin: 20px;")
        
        # Создаем контейнер для формы
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        # Создаем поля ввода
        self.create_input_field("ФИО:", "full_name")
        self.create_input_field("Возраст:", "age")
        self.create_input_field("Город:", "city")
        self.create_input_field("Телефон:", "phone")
        self.create_input_field("Код доступа:", "access_code")
        
        # Кнопка регистрации
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setFont(QFont('Segoe UI', 12))
        self.register_button.setMinimumWidth(200)
        self.register_button.clicked.connect(self.register)
        
        # Создаем основной layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Добавляем заголовок
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        
        # Добавляем отступ
        layout.addSpacing(20)
        
        # Создаем layout для формы
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Добавляем все поля ввода
        for label, input_field in self.input_fields.items():
            field_layout = QHBoxLayout()
            field_layout.addWidget(label)
            field_layout.addWidget(input_field)
            form_layout.addLayout(field_layout)
        
        # Добавляем кнопку регистрации
        form_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)
        
        layout.addWidget(form_frame)
        main_frame.setLayout(layout)
        
        # Создаем основной layout для окна
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_frame)
        
    def create_input_field(self, label_text, field_name, is_password=False):
        if not hasattr(self, 'input_fields'):
            self.input_fields = {}
            
        label = QLabel(label_text)
        label.setFont(QFont('Segoe UI', 12))
        input_field = QLineEdit()
        input_field.setMinimumWidth(300)
        if is_password:
            input_field.setEchoMode(QLineEdit.Password)
            
        self.input_fields[label] = input_field
        setattr(self, f"{field_name}_input", input_field)
        
    def show_registration_result(self, success, result):
        if success:
            QMessageBox.information(self, "Успех", f"Регистрация успешно завершена! Ваш код доступа: {result}")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при регистрации: {result}")
            
    def register(self):
        full_name = self.full_name_input.text()
        age = self.age_input.text()
        city = self.city_input.text()
        phone = self.phone_input.text()
        access_code = self.access_code_input.text()
        
        if not all([full_name, age, city, phone, access_code]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
            return
        success, result = add_candidate(full_name, age, city, access_code, phone)
        self.show_registration_result(success, result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())
