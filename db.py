# ============================================================================
# FILE: db.py (PRODUCTION SAFE)
# ============================================================================

from astrapy import DataAPIClient
from dotenv import load_dotenv
import os

load_dotenv()

ENDPOINT = os.getenv("ASTRA_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")

_client = None
_db = None


def get_db():
    global _client, _db

    if _db is None:
        if not ENDPOINT or not TOKEN:
            raise RuntimeError("Astra DB credentials are missing")

        _client = DataAPIClient(TOKEN)
        _db = _client.get_database_by_api_endpoint(ENDPOINT)

    return _db


def get_collection(name: str):
    db = get_db()
    try:
        return db.get_collection(name)
    except Exception:
        db.create_collection(name)
        return db.get_collection(name)


def get_personal_data_collection():
    return get_collection("personal_data")


def get_notes_collection():
    return get_collection("notes")
