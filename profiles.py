# ============================================================================
# FILE: profiles.py
# ============================================================================

from db import personal_data_collection, notes_collection


def get_values(_id):
    """Get default profile values (empty for placeholders)"""
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
    """Create a new profile in the database"""
    profile_values = get_values(_id)
    result = personal_data_collection.insert_one(profile_values)
    # Return the profile_values, not result object
    return result.inserted_id, profile_values


def get_profile(_id):
    """Get profile by ID"""
    return personal_data_collection.find_one({"_id": {"$eq": _id}})


def get_profile_by_name(name):
    """Get profile by user name"""
    if not name or not name.strip():
        return None
    return personal_data_collection.find_one({"general.name": {"$eq": name.strip()}})


def create_profile_by_name(name):
    """Create a new profile with the given name"""
    if not name or not name.strip():
        return None, None
    
    # Get all profiles to determine next ID
    all_profiles = list(personal_data_collection.find({}))
    next_id = max([p.get("_id", 0) for p in all_profiles] + [0]) + 1
    
    profile_values = get_values(next_id)
    profile_values["general"]["name"] = name.strip()
    
    result = personal_data_collection.insert_one(profile_values)
    return result.inserted_id, profile_values


def get_all_user_names():
    """Get list of all user names from existing profiles"""
    profiles = list(personal_data_collection.find({}))
    names = []
    for profile in profiles:
        name = profile.get("general", {}).get("name", "").strip()
        if name:
            names.append(name)
    return sorted(set(names))


def get_notes(_id):
    """Get all notes for a user"""
    return list(notes_collection.find({"user_id": {"$eq": _id}}))
