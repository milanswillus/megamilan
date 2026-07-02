import json
from config import STATE_FILE

def load_states():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden der State-Datei: {e}")
    return {}

def save_states(states):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(states, f, indent=4)
    except Exception as e:
        print(f"Fehler beim Speichern der State-Datei: {e}")

def get_active_template(chat_id):
    states = load_states()
    user_state = states.get(str(chat_id), {})
    return user_state.get("active_template")

def set_active_template(chat_id, template_key):
    states = load_states()
    chat_id_str = str(chat_id)
    if chat_id_str not in states:
        states[chat_id_str] = {}
    states[chat_id_str]["active_template"] = template_key
    save_states(states)

def clear_active_template(chat_id):
    states = load_states()
    chat_id_str = str(chat_id)
    if chat_id_str in states:
        states[chat_id_str]["active_template"] = None
        save_states(states)
