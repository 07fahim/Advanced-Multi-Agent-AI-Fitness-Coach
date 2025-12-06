
# ============================================================================
# FILE: db.py
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
    """Connect to AstraDB and return database instance"""
    client = DataAPIClient(TOKEN)
    db = client.get_database_by_api_endpoint(ENDPOINT)
    return db


# Get database instance
db = get_db()

# Collection names
collection_names = ["personal_data", "notes"]

# Create collections if they don't exist
for collection in collection_names:
    try:
        db.create_collection(collection)
    except:
        pass  # Collection already exists

# Get collection references
personal_data_collection = db.get_collection("personal_data")
notes_collection = db.get_collection("notes")