from app.mikrotik_client import MikroTikClient
import os


def test_successful_connection():
    """Куда надо - коннектится"""
    client = MikroTikClient("test-ftp-server")
    success = client.connect()
    assert success


def test_failed_connection():
    """куда попало не коннектится"""
    client = MikroTikClient("192.1337.1.1")
    success = client.connect()
    assert not success


def test_upload_file_success():
    """Пробуем загрузку рандомфайла по frp"""
    test_file = "test_file.bin"
    with open(test_file, "wb") as f:
        f.write(b"test content")

    client = MikroTikClient("test-ftp-server")
    client.connect()
    success = client.upload_file(test_file, "test.bin")
    os.remove("test_file.bin")
    assert success
    assert "test.bin" in os.listdir("fake_mikrotik")
    os.remove("fake_mikrotik/test.bin")
