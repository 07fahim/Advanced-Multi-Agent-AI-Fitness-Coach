# ============================================================================
# FILE: profiles.py (STREAMLIT CLOUD SAFE)
# ============================================================================

from db import get_personal_data_collection, get_notes_collection


def _get_collections():
    return (
        get_personal_data_collection(),
        get_notes_collection()
    )


def get_values(_id):
    return {
        "_id": _id,
        "general": {
            "name": "",
            "age": None,
            "weight": None,
            "height": None,
            "activity_level": "",
            "gender": ""
        },
        "goals": [],
        "nutrition": {
            "calories": None,
            "protein": None,
            "fat": None,
            "carbs": None,
        },
    }


def create_profile(_id):
    personal_data_collection, _ = _get_collections()
    profile_values = get_values(_id)
    result = personal_data_collection.insert_one(profile_values)
    return result.inserted_id, profile_values


def get_profile(_id):
    personal_data_collection, _ = _get_collections()
    return personal_data_collection.find_one({"_id": _id})


def get_profile_by_name(name):
    if not name or not name.strip():
        return None
    personal_data_collection, _ = _get_collections()
    return personal_data_collection.find_one(
        {"general.name": name.strip()}
    )


def create_profile_by_name(name):
    if not name or not name.strip():
        return None, None

    personal_data_collection, _ = _get_collections()

    all_profiles = list(personal_data_collection.find({}))
    next_id = max([p.get("_id", 0) for p in all_profiles] + [0]) + 1

    profile_values = get_values(next_id)
    profile_values["general"]["name"] = name.strip()

    result = personal_data_collection.insert_one(profile_values)
    return result.inserted_id, profile_values


def get_all_user_names():
    personal_data_collection, _ = _get_collections()
    profiles = list(personal_data_collection.find({}))

    names = []
    for profile in profiles:
        name = profile.get("general", {}).get("name", "").strip()
        if name:
            names.append(name)

    return sorted(set(names))


def get_notes(_id):
    _, notes_collection = _get_collections()
    return list(notes_collection.find({"user_id": _id}))


def delete_profile(profile_id):
    personal_data_collection, notes_collection = _get_collections()
    try:
        notes_collection.delete_many({"user_id": profile_id})
        result = personal_data_collection.delete_one({"_id": profile_id})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Error deleting profile: {e}")
        return False


def delete_profile_by_name(name):
    if not name or not name.strip():
        return False

    profile = get_profile_by_name(name.strip())
    if profile:
        return delete_profile(profile["_id"])
    return False
