# ============================================================================
# FILE: form_submit.py (STREAMLIT CLOUD SAFE)
# ============================================================================

from db import get_personal_data_collection, get_notes_collection
from datetime import datetime, timezone


def _get_collections():
    return (
        get_personal_data_collection(),
        get_notes_collection()
    )


def update_personal_info(existing, update_type, **kwargs):
    personal_data_collection, _ = _get_collections()

    if update_type == "goals":
        existing["goals"] = kwargs.get("goals", [])
        update_field = {"goals": existing["goals"]}
    else:
        existing[update_type] = kwargs
        update_field = {update_type: existing[update_type]}

    personal_data_collection.update_one(
        {"_id": existing["_id"]},
        {"$set": update_field}
    )

    return existing


def add_note(note, profile_id):
    _, notes_collection = _get_collections()

    new_note = {
        "user_id": profile_id,
        "text": note,
        "metadata": {"ingested": datetime.now(timezone.utc)},
    }

    result = notes_collection.insert_one(new_note)
    new_note["_id"] = result.inserted_id
    return new_note


def delete_note(_id):
    _, notes_collection = _get_collections()
    return notes_collection.delete_one({"_id": _id})
