# ============================================================================
# FILE: form_submit.py
# ============================================================================

from db import personal_data_collection, notes_collection
from datetime import datetime, timezone


def update_personal_info(existing, update_type, **kwargs):
    """Update personal information in the database"""
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
    """Add a new note"""
    new_note = {
        "user_id": profile_id,
        "text": note,
        "metadata": {"injested": datetime.now(timezone.utc)},
    }
    result = notes_collection.insert_one(new_note)
    new_note["_id"] = result.inserted_id
    return new_note


def delete_note(_id):
    """Delete a note by ID"""
    return notes_collection.delete_one({"_id": _id})