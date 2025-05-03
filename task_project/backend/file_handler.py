# backend/file_handler.py

import os
from flask import current_app

def save_uploaded_file(file):
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    return file_path
