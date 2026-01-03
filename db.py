# ============================================================================
# FILE: db.py (FIXED & STREAMLIT-CLOUD SAFE)
# ============================================================================

from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

ENDPOINT = os.getenv("ASTRA_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")


@st.cache_resource
def get_db():
    """Create and cache AstraDB client"""
    client = DataAPIClient(TOKEN)
    return client.get_database_by_api_endpoint(ENDPOINT)


def get_collection(name: str):
    """Lazy-load a collection (safe for cold starts)"""
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
