from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import ipaddress


class IPAddressValidator:
    def __init__(self):
        self.message = "Введите корректный IP адрес"

    def __call__(self, form, field):
        try:
            ipaddress.ip_address(field.data)
        except ValueError:
            raise ValidationError(self.message)


class FileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size
        self.message = f"Размер файла не должен превышать {max_size} байт"

    def __call__(self, form, field):
        if field.data:
            file_data = field.data
            field.data.seek(0)
            file_size = len(file_data.read())
            field.data.seek(0)

            if file_size > self.max_size:
                raise ValidationError(self.message)


class UploadForm(FlaskForm):
    ip_address = StringField(
        "IP адрес куда заливать?",
        validators=[
            DataRequired(message="IP адрес обязателен"),
            IPAddressValidator(),
        ],
    )

    firmware_file = FileField(
        "Файл прошивки",
        validators=[
            FileRequired(message="Выберите файл прошивки"),
            FileAllowed(["bin", "npk"], "Разрешены только файлы .bin и .npk"),
            FileSizeValidator(max_size=50 * 1024 * 1024),
        ],
    )

    submit = SubmitField("Загрузить")
