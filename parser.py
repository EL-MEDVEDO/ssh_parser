from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, ssh_exception
import logging
from db_manager import DatabaseManager

class Parser:

    def __init__(self, db):
        self.hosts = []
        self.connections = []
        self.db = db
        self.setup_logging()
        self.output = None

    #Устанавливаем логирование
    def setup_logging(self):
        logging.basicConfig(filename='command_log.txt', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    #функция, отвечающая за логирование команд
    def log_command(self, command, host):
        logging.info(f'Command executed on {host}: {command}')

    # Эта функция отвечает за подключение SSH-клиента
    def ssh_connect(self):
        for host in self.hosts:
            ssh_client = SSHClient()
            # Установим политику хоста. Мы добавляем новое имя хоста и новый ключ хоста в объект local Host Keys
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            try:
                ssh_client.connect(hostname=host[0], port=host[1], username=host[2], password=host[3], banner_timeout=300)
                # Если мы подключились и нет ошибок, то добавляем наш клиент в список подключенных соединений
                self.connections.append(ssh_client)
                # Логируем подключение
                logging.info(f"Connection established to {host[0]} with username={host[2]} and password={host[3]}")
                print(f"Connection established to {host[0]} with username={host[2]} and password={host[3]}")
            except AuthenticationException:
                # Логируем
                logging.warning(f"Authentication failed for {host[0]} with username={host[2]} and password={host[3]}")
            except ssh_exception.SSHException:
                logging.error(f"Failed to connect to {host[0]} - Rate limiting on server")
            except Exception as err:
                logging.error(f"Failed to connect to {host[0]} - {str(err)}")

    # Функция, отвечающая за закрытие всех соединений
    def do_close(self):
        for conn in self.connections:
            conn.close()
            logging.info(f"Connection closed: {conn}")
        self.connections.clear()
        self.hosts.clear()

    # Функция выполняет команды на удаленном устройстве и возвращает их + логирование
    def execute_command(self, conn, command, host):
        stdin, stdout, stderr = conn.exec_command(command)
        stdin.close()
        output = stdout.read().decode('utf-8').strip()
        self.log_command(command, host)
        return output

    #Функция сбора информации
    def do_run(self):
        for host, conn in zip(self.hosts, self.connections):
            try:
                #Команды
                os_name_cmd = "uname -s"
                os_version_cmd = "uname -r"
                os_arch_cmd = "uname -m"
                os_core_cmd = 'uname -a'
                lsb_release_cmd = 'lsb_release -a'
                system_boot_information_cmd = 'uptime'
                date_cmd = "date"

                #Выполнение команд
                os_name = self.execute_command(conn, os_name_cmd, host[0])
                os_version = self.execute_command(conn, os_version_cmd, host[0])
                os_arch = self.execute_command(conn, os_arch_cmd, host[0])
                os_core = self.execute_command(conn, os_core_cmd, host[0])
                lsb_release = self.execute_command(conn, lsb_release_cmd, host[0])
                system_boot_information = self.execute_command(conn, system_boot_information_cmd, host[0])
                date = self.execute_command(conn, date_cmd, host[0])

                #Занесение информации в DB
                try:
                    self.db.insert_system_info(host[0], host[1], host[2], host[3],
                                                  os_name, os_version, os_arch, os_core,
                                                  lsb_release, system_boot_information, date)
                    logging.info(f"Data inserted into the database for host {host[0]}")
                except Exception as err:
                    logging.error(f'Error in insert into the database on {host}: {str(err)}')
                    print(f'Error in database: {str(err)}')

                #Вывод информации
                self.output = (
                    f"Host: {host[0]}\n"
                    f"Port: {host[1]}\n"
                    f"User: {host[2]}\n"
                    f"Password: {host[3]}\n"
                    f"OS: {os_name}\n"
                    f"Version: {os_version}\n"
                    f"Architecture: {os_arch}\n"
                    f"Core: {os_core}\n"
                    f"Common information: {lsb_release}\n"
                    f"System boot information: {system_boot_information}\n"
                    f"Date: {date}\n"
                    f"{'-' * 50}")
                print(self.output)
            except Exception as err:
                logging.error(f'Error execute command on host {host}: {str(err)}')
                print(f'Error: {str(err)}')
        #Закрытие соединений
        self.do_close()
