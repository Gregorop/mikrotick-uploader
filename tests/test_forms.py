import pytest
from wtforms import ValidationError

from app.forms import IPAddressValidator, UploadForm
from .conftest import create_test_file


def test_ip_validator_valid_ip():
    validator = IPAddressValidator()
    field = type("MockField", (), {"data": "192.168.1.1"})()
    form = type("MockForm", (), {})()

    try:
        validator(form, field)
        assert True
    except ValidationError:
        assert False, "Кривая валидация нормальный IP не пропустила"


def test_ip_validator_invalid_ip():
    validator = IPAddressValidator()
    field = type("MockField", (), {"data": "1337.9999.0.2"})()
    form = type("MockForm", (), {})()

    with pytest.raises(ValidationError):
        validator(form, field)


def test_file_size_validation_in_limit(app_context):
    form = UploadForm()
    form.ip_address.data = "192.168.1.1"
    form.firmware_file.data = create_test_file(10 * 1024 * 1024)  # 10MB

    assert form.validate()
    assert not form.firmware_file.errors


def test_file_size_validation_over_limit(app_context):
    form = UploadForm()
    form.ip_address.data = "192.168.1.1"
    form.firmware_file.data = create_test_file(60 * 1024 * 1024)

    assert not form.validate()
    assert "размер файла не должен превышать" in str(form.firmware_file.errors).lower()


def test_file_type_validation(app_context):
    form = UploadForm()
    form.ip_address.data = "192.168.1.1"

    invalid_file = create_test_file(1024, "test.exe")
    form.firmware_file.data = invalid_file

    assert not form.validate()
    assert (
        "разрешены только файлы .bin и .npk" in str(form.firmware_file.errors).lower()
    )

    valid_file = create_test_file(1024, "test.bin")
    form.firmware_file.data = valid_file

    assert form.validate()
