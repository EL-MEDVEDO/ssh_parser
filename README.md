# SSH Parser
Эта программа на Python подключается к удаленным хостам по SSH, выполняет команды и собирает системную информацию. Он также регистрирует выполненные команды и вставляет системную информацию в базу данных.

# Особенности

SSH-соединение: Подключается к удаленным хостам по SSH с помощью Paramiko.

Выполнение команд: Выполняет команды на удаленных хостах и регистрирует их.

Системная информация: Собирает такую информацию, как название операционной системы, версия, архитектура и многое другое.

Ведение журнала: Записывает выполненные команды и ошибки в файл.

Взаимодействие с базой данных: Вставляет системную информацию в базу данных.

# Перед запуском программы убедитесь, что у вас установлено следующее:

Python

Библиотека Paramiko (pip install paramiko)

Библиотека PyQt5

# EXE-FIle
Есть exe-file, так что можно использовать без настройки окружения и включения компилятора!



# Использование
Введите IP-адрес хоста, порт, имя пользователя и пароль в соответствующие поля.
Нажмите кнопку "Parse".

Выполняет команды SSH на указанных хостах.
Проверьте журнал:

Нажмите кнопку "Check Log", чтобы просмотреть последние 13 записей журнала.
Очистить журнал:

Нажмите кнопку "Clear Log'", чтобы очистить файл журнала.
Поиск в базе данных:

Нажмите кнопку "Search in DB", чтобы выполнить поиск хоста в базе данных.
Помогите:

Нажмите кнопку "Help", чтобы отобразить информацию о том, как пользоваться приложением.
Примечание:

Если загрузка окна занимает много времени, пожалуйста, подождите; в конце концов оно загрузится.
# База данных
Программа взаимодействует с базой данных для хранения системной информации.


![image](https://github.com/EL-MEDVEDO/ssh_parser/assets/110033694/163d8c01-d50a-456e-a7c9-8d5b4ac04cd2)

![image](https://github.com/EL-MEDVEDO/ssh_parser/assets/110033694/ef3346eb-09d7-4849-b8e2-8f4b46e7ff90)

![image](https://github.com/EL-MEDVEDO/ssh_parser/assets/110033694/841254ba-b09c-4fa7-b583-fcd9e35ee967)




# Author
# EL-MEDVEDO

