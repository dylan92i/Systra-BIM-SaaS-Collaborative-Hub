# utilities.py

import os
from flask import session, current_app

def get_user_folder():
    user_id = session.get('user_id')
    if not user_id:
        return None
    root_folder = os.path.join(current_app.root_path, 'user_files', str(user_id))
    return root_folder

def secure_user_path(path):
    # Sécurise le chemin transmis (évite les '..' path traversal etc)
    path = os.path.normpath(path).replace("\\", "/")
    if path.startswith("../") or ".." in path:
        return ""
    return path
