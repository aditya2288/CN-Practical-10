from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
import os
import socket

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cn-practical-10-demo-key")
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB of file data
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE + 64 * 1024  # Allow multipart form overhead.


def human_size(size):
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


@app.route("/")
def index():
    files = []
    for path in sorted(UPLOAD_FOLDER.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if path.is_file() and path.name != ".gitkeep":
            stat = path.stat()
            files.append(
                {
                    "name": path.name,
                    "size": human_size(stat.st_size),
                    "uploaded": datetime.fromtimestamp(stat.st_mtime).strftime("%d %b %Y, %I:%M %p"),
                }
            )
    return render_template("index.html", files=files)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file was selected.", "error")
        return redirect(url_for("index"))

    file = request.files["file"]

    if not file or file.filename == "":
        flash("Please choose a file before uploading.", "error")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    if not filename:
        flash("Invalid filename.", "error")
        return redirect(url_for("index"))

    file.stream.seek(0, os.SEEK_END)
    if file.stream.tell() > MAX_FILE_SIZE:
        abort(413)
    file.stream.seek(0)

    destination = UPLOAD_FOLDER / filename
    file.save(destination)

    flash(f"{filename} uploaded successfully.", "success")
    return redirect(url_for("index"))


@app.route("/download/<path:filename>")
def download_file(filename):
    safe_name = secure_filename(filename)
    if not safe_name or safe_name != filename:
        abort(400)

    path = UPLOAD_FOLDER / safe_name
    if not path.exists() or not path.is_file():
        abort(404)

    return send_from_directory(app.config["UPLOAD_FOLDER"], safe_name, as_attachment=True)


@app.route("/delete/<path:filename>", methods=["POST"])
def delete_file(filename):
    safe_name = secure_filename(filename)
    if not safe_name or safe_name != filename:
        abort(400)

    path = UPLOAD_FOLDER / safe_name
    if not path.exists() or not path.is_file():
        flash("File not found.", "error")
        return redirect(url_for("index"))

    path.unlink()
    flash(f"{safe_name} deleted.", "success")
    return redirect(url_for("index"))


@app.errorhandler(413)
def file_too_large(_):
    flash("File is too large. Maximum upload size is 20 MB.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    local_ip = get_local_ip()
    print("\n" + "=" * 58)
    print(" Cloud-Based File Sharing System")
    print("=" * 58)
    print(" Local URL   : http://127.0.0.1:5000")
    print(f" Network URL : http://{local_ip}:5000")
    print(" Protocol    : HTTP over TCP/IP")
    print("=" * 58 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
