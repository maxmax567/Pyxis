import os
import langs as l
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Create Supabase client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Session state
actual_session = None
current_user = None

# Login
def login(email: str, password: str) -> tuple[bool, str]:
    global actual_session, current_user
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.user:
            actual_session = response.session
            current_user = response.user
            return True, l.t("login_success")
        return False, l.t("login_failed")
    except Exception as e:
        return False, str(e)

# Login with Google
def google_login() -> tuple[bool, str]:
    global actual_session, current_user
    try:
        response = supabase.auth.sign_in_with_oauth({
            "provider": 'google'
        })
        if response.user:
            actual_session = response.session
            current_user = response.user
            return True, l.t("login_success")
        return False, l.t("login_failed")
    except Exception as e:
        return False, str(e)

# Get actual session
def get_session():
    return actual_session

# Logout
def logout():
    global actual_session, current_user
    supabase.auth.sign_out()
    actual_session = None
    current_user = None