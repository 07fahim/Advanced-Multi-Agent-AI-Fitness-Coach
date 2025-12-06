# ============================================================================
# FILE: main.py
# ============================================================================

import streamlit as st
from profiles import (
    create_profile, get_notes, get_profile, 
    get_profile_by_name, create_profile_by_name, get_all_user_names,
    delete_profile_by_name
)
from form_submit import update_personal_info, add_note, delete_note
from langchain_agents import MacroAgent, AskAISystem

# Initialize agents (cached for performance)
@st.cache_resource
def get_agents():
    """Initialize and cache AI agents"""
    return MacroAgent(), AskAISystem()

macro_agent, ask_ai_system = get_agents()

# Page config
st.set_page_config(
    page_title="AI Fitness Coach",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header with professional styling
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.title("🏋️ Fitness Coach")
    st.markdown("### *Your Personal Trainer & Nutritionist in One*")
    st.divider()


def personal_data_form():
    """Form for collecting personal user data"""
    with st.form("personal_data"):
        st.header("👤 Personal Information")
        st.caption("Tell us about yourself to get personalized recommendations")
        profile = st.session_state.profile

        # Get values - use None/empty for placeholders
        name_value = profile["general"].get("name", "") or ""
        age_value = profile["general"].get("age")
        weight_value = profile["general"].get("weight")
        height_value = profile["general"].get("height")
        gender_value = profile["general"].get("gender", "")
        activity_value = profile["general"].get("activity_level", "")

        name = st.text_input("Name", value=name_value, placeholder="Enter your name")
        
        # Use min_value as default for empty fields to avoid validation errors
        age = st.number_input(
            "Age (years)", 
            min_value=1, 
            max_value=120, 
            step=1, 
            value=int(age_value) if age_value is not None and age_value > 0 else 1,
            help="Enter your age in years"
        )
        age = age if age > 0 else None
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input(
                "Weight (kg)", 
                min_value=0.0, 
                max_value=300.0, 
                step=0.1, 
                value=float(weight_value) if weight_value is not None and weight_value > 0 else 0.0,
                help="Enter your weight in kilograms"
            )
            weight = weight if weight > 0 else None
        with col2:
            height = st.number_input(
                "Height (cm)", 
                min_value=0.0, 
                max_value=250.0, 
                step=0.1, 
                value=float(height_value) if height_value is not None and height_value > 0 else 0.0,
                help="Enter your height in centimeters"
            )
            height = height if height > 0 else None
        
        genders = ["", "Male", "Female", "Other"]
        try:
            gender_index = genders.index(gender_value) if gender_value else 0
        except ValueError:
            gender_index = 0
        gender = st.radio(
            "Gender", 
            genders[1:],  # Skip empty option in display
            index=gender_index - 1 if gender_index > 0 else 0,
            horizontal=True
        )
        gender = gender if gender else None
        
        activities = ["", "Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"]
        try:
            activity_index = activities.index(activity_value) if activity_value else 0
        except ValueError:
            activity_index = 0
        activity_level = st.selectbox(
            "Activity Level", 
            activities[1:],  # Skip empty option in display
            index=activity_index - 1 if activity_index > 0 else None,
            placeholder="Select activity level"
        )
        activity_level = activity_level if activity_level else None

        personal_data_submit = st.form_submit_button("💾 Save Personal Information", type="primary")
        
        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner("Saving..."):
                    st.session_state.profile = update_personal_info(
                        profile, 
                        "general", 
                        name=name, 
                        weight=weight, 
                        height=height,
                        gender=gender, 
                        age=age, 
                        activity_level=activity_level
                    )
                    st.success("✅ Information saved!")
            else:
                st.warning("⚠️ Please fill in all fields!")


def goals_form():
    """Form for selecting fitness goals"""
    profile = st.session_state.profile
    
    with st.form("goals_form"):
        st.header("🎯 Fitness Goals")
        st.caption("Select your primary fitness objectives")
        
        goals = st.multiselect(
            "Select your fitness goals",
            ["Muscle Gain", "Fat Loss", "Stay Active"],
            default=profile.get("goals", ["Muscle Gain"])
        )

        goals_submit = st.form_submit_button("💾 Save Goals", type="primary")
        
        if goals_submit:
            if goals:
                with st.spinner("Saving..."):
                    st.session_state.profile = update_personal_info(
                        profile, 
                        "goals", 
                        goals=goals
                    )
                    st.success("✅ Goals updated!")
            else:
                st.warning("⚠️ Please select at least one goal!")


def macros():
    """Macro calculator with AI generation"""
    profile = st.session_state.profile
    
    nutrition = st.container(border=True)
    nutrition.header("🥗 Nutrition & Macros")
    nutrition.caption("Track your daily macronutrients and calories")
    
    if nutrition.button("🤖 Generate Macros with AI", type="primary", use_container_width=True):
        with st.spinner("🧠 AI is calculating your personalized macros..."):
            try:
                result = macro_agent.generate_macros(
                    profile.get("general"), 
                    profile.get("goals")
                )
                profile["nutrition"] = result
                st.session_state.profile = profile
                nutrition.success("✅ AI has generated your personalized macros!")
                st.balloons()  # Celebration animation
            except Exception as e:
                nutrition.error(f"❌ Error: {str(e)}")

    with nutrition.form("nutrition_form", border=False):
        col1, col2, col3, col4 = st.columns(4)
        
        # Get values - use None for placeholders
        calories_value = profile["nutrition"].get("calories")
        protein_value = profile["nutrition"].get("protein")
        fat_value = profile["nutrition"].get("fat")
        carbs_value = profile["nutrition"].get("carbs")
        
        with col1:
            calories = st.number_input(
                "Calories", 
                min_value=0, 
                step=1,
                value=int(calories_value) if calories_value is not None else 0,
                help="Daily calorie target"
            )
            calories = calories if calories > 0 else None
        with col2:
            protein = st.number_input(
                "Protein (g)", 
                min_value=0, 
                step=1,
                value=int(protein_value) if protein_value is not None else 0,
                help="Daily protein in grams"
            )
            protein = protein if protein > 0 else None
        with col3:
            fat = st.number_input(
                "Fat (g)", 
                min_value=0, 
                step=1,
                value=int(fat_value) if fat_value is not None else 0,
                help="Daily fat in grams"
            )
            fat = fat if fat > 0 else None
        with col4:
            carbs = st.number_input(
                "Carbs (g)", 
                min_value=0, 
                step=1,
                value=int(carbs_value) if carbs_value is not None else 0,
                help="Daily carbs in grams"
            )
            carbs = carbs if carbs > 0 else None

        if st.form_submit_button("💾 Save Macros", type="primary"):
            with st.spinner("Saving..."):
                st.session_state.profile = update_personal_info(
                    profile, 
                    "nutrition", 
                    protein=protein, 
                    calories=calories,
                    fat=fat, 
                    carbs=carbs
                )
                st.success("✅ Macros saved!")


def notes():
    """Notes management with vector search"""
    st.header("📋 Fitness Journal & Notes")
    st.caption("📝 Document your progress, workouts, and insights - AI uses these for personalized advice!")
    
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5, 1])
        with cols[0]:
            st.text(note.get("text"))
        with cols[1]:
            if st.button("🗑️", key=f"del_{i}"):
                delete_note(note.get("_id"))
                st.session_state.notes.pop(i)
                st.rerun()
    
    st.markdown("---")
    new_note = st.text_area(
        "➕ Add a new note:", 
        placeholder="E.g., 'Completed 5km run today, felt great!' or 'Noticed I have more energy after eating more protein'",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        add_note_button = st.button("➕ Add Note", type="primary", use_container_width=True)
    with col2:
        pass  # Empty column for spacing
    
    if add_note_button:
        if new_note:
            with st.spinner("💾 Adding note..."):
                note = add_note(new_note, st.session_state.profile_id)
                st.session_state.notes.append(note)
                st.success("✅ Note added successfully!")
                st.rerun()
        else:
            st.warning("⚠️ Please enter a note before adding!")


def ask_ai_func():
    """AI chat interface with multi-agent routing and chat history"""
    st.header("🤖 AI Fitness Coach Chat")
    st.caption("💡 Ask anything about fitness, nutrition, or workouts - Your AI coach uses your profile and notes for personalized advice!")
    
    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation History")
        with st.container():
            for i, (role, message) in enumerate(st.session_state.chat_history):
                if role == "human":
                    with st.chat_message("user"):
                        st.write(message)
                else:  # ai
                    with st.chat_message("assistant"):
                        st.write(message)
        st.divider()
    
    user_question = st.text_area(
        "Your question:",
        placeholder="Example: Can you create a leg day workout routine for me?",
        key="user_question_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        ask_button = st.button("🤖 Ask AI Coach", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    if ask_button:
        if user_question:
            with st.spinner("🧠 AI is thinking..."):
                try:
                    # Convert chat history to LangChain format
                    langchain_history = []
                    for role, message in st.session_state.chat_history:
                        langchain_history.append((role, message))
                    
                    # Get AI response
                    result = ask_ai_system.ask(
                        user_question,
                        st.session_state.profile,
                        st.session_state.profile_id,
                        chat_history=langchain_history
                    )
                    
                    # Add to chat history
                    st.session_state.chat_history.append(("human", user_question))
                    st.session_state.chat_history.append(("ai", result))
                    
                    # Rerun to display updated chat history
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question!")


def user_selection():
    """User selection screen - name-based"""
    st.title("👤 Welcome to AI Fitness Coach")
    st.markdown("### Get Started")
    st.info("💡 Enter your name to continue. If you're new, a profile will be created for you automatically.")
    
    # Get existing users
    existing_users = get_all_user_names()
    
    if existing_users:
        st.markdown("### 👥 Existing Users")
        st.caption("Select your name if you've used the app before")
        
        # Profile selection section
        selected_existing = st.selectbox(
            "Choose your profile:",
            [""] + existing_users,
            key="existing_user_select",
            help="Select your name from the list",
            label_visibility="visible"
        )
        
        if selected_existing:
            profile = get_profile_by_name(selected_existing)
            if profile:
                st.session_state.user_name = selected_existing
                st.session_state.profile = profile
                st.session_state.profile_id = profile["_id"]
                st.session_state.notes = get_notes(profile["_id"])
                st.session_state.chat_history = []
                st.rerun()
        
        # Delete profile section - separate and clearly marked
        st.markdown("---")
        st.markdown("#### 🗑️ Delete Profile")
        st.caption("⚠️ Permanently delete a profile and all associated data")
        
        delete_profile_name = st.selectbox(
            "Select profile to delete:",
            [""] + existing_users,
            key="delete_profile_select",
            help="Choose a profile to permanently delete",
            label_visibility="visible"
        )
        
        if delete_profile_name:
            st.warning(f"⚠️ **Warning:** You are about to delete profile: **{delete_profile_name}**")
            st.caption("This will permanently delete the profile and all associated notes. This action cannot be undone.")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🗑️ Confirm Delete", type="primary", use_container_width=True, key="confirm_delete_user_select"):
                    if delete_profile_by_name(delete_profile_name):
                        st.success(f"✅ Profile '{delete_profile_name}' and all associated data have been deleted.")
                        st.info("🔄 Refreshing user list...")
                        # Clear the delete selection by rerunning (widget will reset)
                        if "delete_profile_select" in st.session_state:
                            del st.session_state.delete_profile_select
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete profile. Please try again.")
            with col2:
                if st.button("❌ Cancel", use_container_width=True, key="cancel_delete_user_select"):
                    # Clear the delete selection by rerunning (widget will reset)
                    if "delete_profile_select" in st.session_state:
                        del st.session_state.delete_profile_select
                    st.rerun()
    
    st.divider()
    st.markdown("### ✨ New User")
    st.caption("Enter your name to create a new profile")
    
    with st.form("user_selection_form"):
        user_name = st.text_input(
            "👤 Your Name:",
            placeholder="e.g., John, Sarah, Alex...",
            key="new_user_name",
            help="This will be used to personalize your experience"
        )
        submit = st.form_submit_button("🚀 Get Started", type="primary", use_container_width=True)
        
        if submit:
            if user_name and user_name.strip():
                # Check if user already exists
                existing_profile = get_profile_by_name(user_name.strip())
                
                if existing_profile:
                    # Load existing profile
                    st.session_state.user_name = user_name.strip()
                    st.session_state.profile = existing_profile
                    st.session_state.profile_id = existing_profile["_id"]
                    st.session_state.notes = get_notes(existing_profile["_id"])
                    st.session_state.chat_history = []
                    st.rerun()
                else:
                    # Create new profile
                    profile_id, new_profile = create_profile_by_name(user_name.strip())
                    if profile_id and new_profile:
                        st.session_state.user_name = user_name.strip()
                        st.session_state.profile = new_profile
                        st.session_state.profile_id = profile_id
                        st.session_state.notes = []
                        st.session_state.chat_history = []
                        st.success(f"✅ Welcome, {user_name.strip()}! Your profile has been created.")
                        st.rerun()
                    else:
                        st.error("❌ Could not create profile. Please try again.")
            else:
                st.warning("⚠️ Please enter your name!")


def forms():
    """Main app coordinator"""
    # Check if user is selected
    if "user_name" not in st.session_state or "profile" not in st.session_state:
        user_selection()
        return
    
    # Refresh notes if needed
    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)
    
    # Display current user in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 👤 Current User")
    st.sidebar.markdown(f"**{st.session_state.user_name}**")
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🔄 Switch User", use_container_width=True):
        # Clear session state to show user selection again
        for key in ["user_name", "profile", "profile_id", "notes", "chat_history"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚠️ Danger Zone")
    st.sidebar.caption("Permanently delete your profile")
    
    if not st.session_state.get("show_delete_confirm", False):
        if st.sidebar.button("🗑️ Delete My Profile", use_container_width=True, type="secondary"):
            st.session_state.show_delete_confirm = True
            st.rerun()
    else:
        st.sidebar.warning(f"⚠️ Delete **{st.session_state.user_name}**?")
        st.sidebar.caption("This action cannot be undone!")
        
        if st.sidebar.button("✅ Yes, Delete", use_container_width=True, type="primary", key="sidebar_confirm_delete"):
            if delete_profile_by_name(st.session_state.user_name):
                st.sidebar.success("✅ Profile deleted!")
                # Clear session state
                for key in ["user_name", "profile", "profile_id", "notes", "chat_history", "show_delete_confirm"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
            else:
                st.sidebar.error("❌ Failed to delete profile.")
        
        if st.sidebar.button("❌ Cancel", use_container_width=True, key="sidebar_cancel_delete"):
            st.session_state.show_delete_confirm = False
            st.rerun()
    
    # Render forms directly without tabs
    personal_data_form()
    st.divider()
    goals_form()
    st.divider()
    macros()
    st.divider()
    notes()
    st.divider()
    ask_ai_func()


if __name__ == "__main__":
    forms()