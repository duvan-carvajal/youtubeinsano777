from flask import Flask, render_template, request, send_file
import os
import uuid
import yt_dlp
import tkinter as tk
from tkinter import filedialog
import platform

app = Flask(__name__)
if platform.system() == "Windows":
    DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
elif platform.system() == "Darwin":  # macOS
    DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
else:  # Linux
    DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Descargas")
    if not os.path.exists(DOWNLOAD_FOLDER):  # fallback
        DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    quality = request.form["quality"]

    file_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.%(ext)s")
    ydl_opts = {"outtmpl": output_template}
    if quality == "best":
     ydl_opts["format"] = "best"
    elif quality == "bestaudio":
     ydl_opts["format"] = "bestaudio"
    
    else:
     print("invalid choice. Defaulting to best quality.")
     ydl_opts["format"] = "best"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=True)
      downloaded_file = ydl.prepare_filename(info)
      print("Archivo descargado:", downloaded_file)
      print("Existe?:", os.path.exists(downloaded_file))

    if os.path.exists(downloaded_file):
        return send_file(
            os.path.abspath(downloaded_file),  # ruta absoluta segura
            as_attachment=True,
            download_name=os.path.basename(downloaded_file)  # fuerza nombre correcto
        )
    return "Error jaja"
   
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=True)



