import os


def get_allowed_origins() -> list[str]:
    raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return origins or ["http://localhost:5173", "http://127.0.0.1:5173"]


def get_vector_db_path() -> str:
    return os.getenv("VECTOR_DB_PATH", "./data/chroma")


def get_upload_dir_path() -> str:
    return os.getenv("UPLOAD_DIR", "./uploads")


def get_conversation_store_path() -> str:
    return os.getenv("CONVERSATION_STORE_PATH", "./data/conversations.json")


def get_auth_users_path() -> str:
    return os.getenv("AUTH_USERS_PATH", "./data/users.json")


def get_auth_sessions_path() -> str:
    return os.getenv("AUTH_SESSIONS_PATH", "./data/sessions.json")
