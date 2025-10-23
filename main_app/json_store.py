import json, os, threading, uuid

import os, json, threading, uuid

DATA_PATH = os.path.join("/tmp", "career_data.json")  # ✅ Vercel-safe writable path
_lock = threading.Lock()


def _init():
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump({"users": [], "casts": []}, f, indent=2)

def _read():
    _init()
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _write(data):import json, os, threading, uuid

DATA_PATH = os.path.join(os.path.dirname(__file__), "career_data.json")
_lock = threading.Lock()

def _init():
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump({"users": [], "casts": []}, f, indent=2)

def _read():
    _init()
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _write(data):
    with _lock:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def create_user(email, first_name, last_name, password):
    data = _read()
    user_id = str(uuid.uuid4())
    data["users"].append({
        "id": user_id,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "casts": []
    })
    _write(data)
    return user_id

def get_user(email, password=None):
    data = _read()
    for u in data["users"]:
        if u["email"] == email and (password is None or u["password"] == password):
            return u
    return None

def add_cast(user_id, job_title, job_description):
    data = _read()
    cast_id = str(uuid.uuid4())
    data["casts"].append({
        "id": cast_id,
        "user_id": user_id,
        "job_title": job_title,
        "job_description": job_description,
        "resume_url": "",
        "video_url": "",
        "teleprompter_text": ""
    })
    _write(data)
    return cast_id

def update_cast(cast_id, updates):
    data = _read()
    for c in data["casts"]:
        if c["id"] == cast_id:
            c.update(updates)
            break
    _write(data)

def get_cast(cast_id):
    data = _read()
    for c in data["casts"]:
        if c["id"] == cast_id:
            return c
    return None

def get_user_casts(user_id):
    data = _read()
    return [c for c in data["casts"] if c["user_id"] == user_id]

    with _lock:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def create_user(email, first_name, last_name, password_hash):
    data = _read()
    user_id = str(uuid.uuid4())
    data["users"].append({
        "id": user_id,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password_hash,
        "casts": []
    })
    _write(data)
    return user_id

def get_user_by_email(email):
    data = _read()
    for u in data["users"]:
        if u["email"] == email:
            return u
    return None

def add_cast(user_id, job_title, job_description):
    data = _read()
    cast_id = str(uuid.uuid4())
    new_cast = {
        "id": cast_id,
        "user_id": user_id,
        "job_title": job_title,
        "job_description": job_description,
        "resume_url": "",
        "video_url": "",
        "teleprompter_text": ""
    }
    data["casts"].append(new_cast)
    _write(data)
    return cast_id

def update_cast(cast_id, updates):
    data = _read()
    for c in data["casts"]:
        if c["id"] == cast_id:
            c.update(updates)
            break
    _write(data)

def get_user_casts(user_id):
    data = _read()
    return [c for c in data["casts"] if c["user_id"] == user_id]

def get_cast(cast_id):
    data = _read()
    for c in data["casts"]:
        if c["id"] == cast_id:
            return c
    return None
