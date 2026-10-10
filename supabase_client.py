import os
import webbrowser
from html import escape
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import langs as l
from supabase import create_client, Client
from dotenv import load_dotenv

PORT = 8765
TEMPLATE = Path(__file__).parent / "login_callback.html"

load_dotenv()

# Create Supabase client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Session state
actual_session = None
current_user = None


# Render the page shown in the browser after the OAuth redirect
def render_callback_page(success: bool) -> bytes:
    values = {
        "{{lang}}": str(l.get_system_locale()).replace("_", "-"),
        "{{app}}": l.t("login_browser_title"),
        "{{status}}": "ok" if success else "error",
        "{{title}}": l.t("login_browser_done" if success else "login_browser_fail"),
        "{{hint}}": l.t("login_browser_hint" if success else "login_browser_fail_hint"),
    }
    html = TEMPLATE.read_text(encoding="utf-8")
    for key_, value in values.items():
        html = html.replace(key_, escape(value))
    return html.encode("utf-8")


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
        return False, f"{l.t('login_error')}: {e}"


# Login with Google
def google_login() -> tuple[bool, str]:
    global actual_session, current_user
    try:
        res = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {"redirect_to": f"http://localhost:{PORT}/callback"}
        })

        result = {}

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                q = parse_qs(urlparse(self.path).query)
                result["code"] = q.get("code", [None])[0]
                body = render_callback_page(bool(result["code"]))
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        server = HTTPServer(("localhost", PORT), Handler)
        server.timeout = 120  # maximum wait 2 min
        webbrowser.open(res.url)
        server.handle_request()
        server.server_close()

        code = result.get("code")
        if not code:
            return False, l.t("login_failed")

        resp = supabase.auth.exchange_code_for_session({"auth_code": code})
        if resp.user:
            actual_session = resp.session
            current_user = resp.user
            return True, l.t("login_success")
        return False, l.t("login_failed")
    except Exception as e:
        return False, f"{l.t('login_error')}: {e}"


# Get actual session
def get_session():
    return actual_session


# Logout
def logout():
    global actual_session, current_user
    supabase.auth.sign_out()
    actual_session = None
    current_user = None