import os

from flask import Flask, flash, redirect, render_template, url_for
from werkzeug.utils import secure_filename

from .forms import UploadForm
from .mikrotik_client import MikroTikClient


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    @app.route("/", methods=["GET", "POST"])
    def index():
        form = UploadForm()

        if form.validate_on_submit():
            ip_address = form.ip_address.data
            firmware_file = form.firmware_file.data

            try:
                filename = secure_filename(firmware_file.filename)
                temp_path = os.path.join("/tmp", filename)
                firmware_file.save(temp_path)

                client = MikroTikClient(
                    host=ip_address, port=2122, username="admin", password="password"
                )
                if client.connect():
                    success = client.upload_file(temp_path, filename)
                    if success:
                        flash("Файл успешно загружен на устройство!", "success")
                    else:
                        flash("Ошибка при загрузке файла на устройство", "error")
                else:
                    flash(f"Ошибка при коннекте с {ip_address}", "error")

                if os.path.exists(temp_path):
                    os.remove(temp_path)

            except Exception as e:
                flash(f"Оошибка: {str(e)}", "error")

            return redirect(url_for("index"))

        return render_template("index.html", form=form)

    return app
