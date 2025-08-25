import ftplib
from typing import Optional


class MikroTikClient:
    def __init__(
        self,
        host,
        port=2122,
        username="admin",
        password="password",
        timeout=30,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        self.ftp: Optional[ftplib.FTP] = None
        self.connected = False

    def connect(self) -> bool:
        """Установка соединения"""
        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(self.host, self.port, self.timeout)
            self.ftp.login(self.username, self.password)
            self.connected = True
            return True

        except Exception as e:
            print(f"Ошибка подключения к {self.host}:{self.port}, {e}")
            self.connected = False
            return False

    def upload_file(self, local_path: str, remote_filename: str) -> bool:
        """Загрузка файла на устройство"""
        if not self.connected or not self.ftp:
            print("Нет активного соединения")
            return False

        try:
            with open(local_path, "rb") as file:
                self.ftp.storbinary(f"STOR {remote_filename}", file)
            print(f"Файл {remote_filename} успешно загружен на {self.host}")
            return True

        except Exception as e:
            print(f"Ошибка загрузки файла на {self.host}: {e}")
            return False
