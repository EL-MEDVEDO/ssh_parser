import sqlite3

class DatabaseManager:

    def __init__(self, path="ssh_users.db"):
        self.path = path
        self.create_table_system_info()

    @property
    def connection(self):
        return sqlite3.connect(self.path)

    def execute(self, sql: str, params: tuple = None, fetchone=None, fetchall=False, commit=False):
        """
        Выполняет SQL-запрос и возвращает результат
        """
        if not params:
            params = tuple()

        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)

            if commit:
                connection.commit()

            if fetchone:
                data = cursor.fetchone()
            elif fetchall:
                data = cursor.fetchall()
            else:
                data = None

        return data

    def create_table_system_info(self):
        """
        Создает таблицу SystemInfo в базе данных
        """
        sql = """
        CREATE TABLE IF NOT EXISTS SystemInfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        host VARCHAR(255) NOT NULL,
        port INT NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        os_name VARCHAR(255),
        os_version VARCHAR(255),
        os_architecture VARCHAR(255),
        os_core VARCHAR(255),
        Common_information TEXT,
        system_boot_information TEXT,
        date_info VARCHAR(255)
        );
        """
        self.execute(sql, commit=True)

    def insert_system_info(self, host, port, username, password, os_name, os_version, os_arch, os_core,
                           lsb_release_info, system_boot_info, date_info):
        """
        Вставляет системную информацию в таблицу SystemInfo
        """
        sql = """
        INSERT INTO SystemInfo (host, port, username, password, os_name, os_version, os_architecture, os_core,
                                Common_information, system_boot_information, date_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (host, port, username, password, os_name, os_version, os_arch, os_core,
                  lsb_release_info, system_boot_info, date_info)
        self.execute(sql, params=params, commit=True)

    def select_all(self):
        """
        Возвращает всю информацию из таблицы SystemInfo
        """
        sql = "SELECT * FROM SystemInfo"
        return self.execute(sql, fetchall=True)

    def select_by_ip(self, system_ip):
        """
        Возвращает информацию для одного ssh-пользователя по id
        """
        sql = "SELECT * FROM SystemInfo WHERE host = ?"
        params = (system_ip,)
        return self.execute(sql, params=params, fetchone=True)