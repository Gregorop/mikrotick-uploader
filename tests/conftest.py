from io import BytesIO
from werkzeug.datastructures import FileStorage
import pytest
from app.main import create_app


@pytest.fixture
def app_context():
    """Контекст приложения чтобы формы тестились"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.app_context():
        yield


def create_test_file(size, filename="test.bin"):
    """Тестовый файлик"""
    content = b"x" * size
    return FileStorage(
        stream=BytesIO(content),
        filename=filename,
        content_type="application/octet-stream",
    )
