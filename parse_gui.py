import sys
import ipaddress
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QDesktopWidget
from PyQt5.QtGui import QFont
from parser import Parser
from db_manager import DatabaseManager

class SSHParserGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Создание виджетов
        self.host_label = QLabel('Host:')
        self.host_input = QLineEdit()
        self.port_label = QLabel('Port:')
        self.port_input = QLineEdit()
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.parse_button = QPushButton('Parse')
        self.check_log_button = QPushButton('Check Log')
        self.clear_log_button = QPushButton('Clear Log')
        self.search_in_db_button = QPushButton('Search in DB')
        self.help_button = QPushButton('Help')
        self.output_text = QTextEdit()


        # Настройка шрифта для текста вывода
        font = QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.output_text.setFont(font)

        # Размещение виджетов с помощью QVBoxLayout и QHBoxLayout
        main_layout = QVBoxLayout()

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.host_label)
        input_layout.addWidget(self.host_input)
        input_layout.addWidget(self.port_label)
        input_layout.addWidget(self.port_input)
        input_layout.addWidget(self.username_label)
        input_layout.addWidget(self.username_input)
        input_layout.addWidget(self.password_label)
        input_layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.parse_button)
        button_layout.addWidget(self.check_log_button)
        button_layout.addWidget(self.clear_log_button)
        button_layout.addWidget(self.help_button)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.search_in_db_button)
        main_layout.addWidget(self.output_text)

        # Назначение размещения виджетов
        self.setLayout(main_layout)

        # Подключение сигналов к слотам
        self.parse_button.clicked.connect(self.parse_button_clicked)
        self.check_log_button.clicked.connect(self.check_log_button_clicked)
        self.clear_log_button.clicked.connect(self.clear_log_button_clicked)
        self.search_in_db_button.clicked.connect(self.search_in_db_button_clicked)
        self.help_button.clicked.connect(self.help_button_clicked)

        # Создание экземпляра парсера как атрибута класса
        db_manager = DatabaseManager()
        self.ssh = Parser(db=db_manager)

        # Установка параметров окна
        screen_size = QDesktopWidget().availableGeometry().size()
        center_point = screen_size / 2
        self.setWindowTitle('SSH Parser GUI')
        self.setGeometry(
            int(center_point.width()/2),
            int(center_point.height()/2),
            1200,
            900
        )

    # Метод добавления хоста для GUI
    def add_host_gui(self, host, port, username, password):
        try:
            ip = ipaddress.IPv4Address(host)
        except ipaddress.AddressValueError:
            self.output_text.setPlainText("Please enter a valid IP address.")
            return False

        if not (1 <= port <= 65535):
            self.output_text.setPlainText("Port number must be between 1 and 65535.")
            return False

        if not (host and port and username and password):
            self.output_text.setPlainText("invali data: not all fields are filled in")
            return False

        try:
            self.ssh.hosts.append((host, port, username, password))
        except Exception as e:
            self.output_text.setPlainText(f"Error adding host: {str(e)}")
            return False

        return True

    def help_button_clicked(self):
        # Отображение окна с информацией по использованию
        help_text = (
            "SSH Parser GUI\n"
            "1. Fill in the Host, Port, Username, and Password fields.\n"
            "2. Click the 'Parse' button to execute the SSH commands.\n"
            "3. Click the 'Check Log' button to view the last 10 log entries.\n"
            "4. Click the 'Clear Log' button to clear the log file.\n"
            "5. Click the 'Search in DB' button to search for a host in the database.\n"
            "6. Click the 'Help' button to display this information.\n"
            "\n*********THE MAIN RULE: if the window loads for a long time, wait, it will definitely load :) Good use!********."
        )
        self.output_text.setPlainText(f"Help:\n{help_text}")



    def parse_button_clicked(self):
        # Получение данных из полей ввода
        host = self.host_input.text()
        try:
            port = int(self.port_input.text())
        except Exception as e:
            self.output_text.setPlainText(f"None in label: {str(e)}")

        username = self.username_input.text()
        password = self.password_input.text()

        # Проверка и добавление хоста
        try:
            if self.add_host_gui(host, port, username, password):
                # Создание экземпляра парсера как атрибута класса

                # Подключение SSH
                self.ssh.ssh_connect()

                # Выполнение метода do_run
                self.ssh.do_run()

                # Вывод результатов в текстовое поле
                if self.ssh.output==None:
                    self.output_text.setPlainText(f"*******ERROOOOORRRR*******\n*******Check log*******")
                else:
                    self.output_text.setPlainText(f"Output:\n{self.ssh.output}")
        except Exception as e:
            self.output_text.setPlainText(f"error - couldn't add a host: {str(e)}")
    def check_log_button_clicked(self):
        try:
            # Чтение последних 10 строк из файла command_log.txt
            with open('command_log.txt', 'r') as log_file:
                lines = log_file.readlines()
                last_10_lines = lines[-13:]

            # Вывод последних 10 строк в текстовое поле
            log_text = "Last 10 log entries:\n" + "".join(last_10_lines)
            self.output_text.setPlainText(log_text)
        except Exception as e:
            self.output_text.setPlainText(f"An error occurred while checking the log: {str(e)}")

    def clear_log_button_clicked(self):
        try:
            # Очистка содержимого файла command_log.txt
            open('command_log.txt', 'w').close()

            # Вывод сообщения об успешной очистке
            self.output_text.setPlainText("Log cleared successfully.")
        except Exception as e:
            self.output_text.setPlainText(f"An error occurred while clearing the log: {str(e)}")


    def search_in_db_button_clicked(self):
        try:
            search_result = self.ssh.db.select_by_ip(self.host_input.text())
            # Разбор кортежа
            host_info = (
                f"Host: {search_result[1]}\n"
                f"Port: {search_result[2]}\n"
                f"User: {search_result[3]}\n"
                f"Password: {search_result[4]}\n"
                f"OS: {search_result[5]}\n"
                f"Version: {search_result[6]}\n"
                f"Architecture: {search_result[7]}\n"
                f"Core: {search_result[8]}\n"
                f"Common information: {search_result[9]}\n"
                f"System boot information: {search_result[10]}\n"
                f"Date: {search_result[11]}\n"
            )

            self.output_text.setPlainText("Search result:\n" + host_info)
        except Exception as e:
            self.output_text.setPlainText(f"An error occurred during the database search: {str(e)}")
