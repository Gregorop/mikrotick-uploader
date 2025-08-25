import ftplib
from typing import Optional
import logging

logger = logging.getLogger(__name__)


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
        logger.debug(
            f"Попытка подключения к {self.host}:{self.port}, timeout: {self.timeout}"
        )
        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(self.host, self.port, self.timeout)
            self.ftp.login(self.username, self.password)
            self.connected = True
            return True

        except Exception as e:
            logger.error(
                f"Ошибка подключения к {self.host}:{self.port}: {str(e)}", exc_info=True
            )
            self.connected = False
            return False

    def upload_file(self, local_path: str, remote_filename: str) -> bool:
        """Загрузка файла на устройство"""
        if not self.connected or not self.ftp:
            logger.error("Нет активного соединения")
            return False

        try:
            with open(local_path, "rb") as file:
                self.ftp.storbinary(f"STOR {remote_filename}", file)
            logger.debug(f"Файл {remote_filename} успешно загружен на {self.host}")
            return True

        except Exception as e:
            logger.error(f"Ошибка загрузки файла на {self.host}: {e}")
            return False
