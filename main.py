import dearpygui.dearpygui as dpg
import langs as l
import supabase_client as sc
import dearpygui.demo as demo
import json
import threading
import os
import sys
import requests
import importlib
import pkgutil
import apps

# Load local apps
def load_local_apps():
    found = []
    for m in pkgutil.iter_modules(apps.__path__):
        try:
            mod = importlib.import_module(f"apps.{m.name}")
            if hasattr(mod, "launch") and hasattr(mod, "app"):
                found.append(mod)
        except Exception as e:
            print(f"Error loading app {m.name}:", e)
    return found

# Run an app
def run_app(sender, app_data, user_data):
    try:
        user_data()  # launch() from the app
    except Exception as e:
        popup(f"Error: {e}", False)

# Icon selection
if sys.platform == "win32":
    small_icon = large_icon = "icons/icon.ico"
else:
    small_icon = "icons/icon_small.png"
    large_icon = "icons/icon_large.png"

# Variables
language = "en"
session_active = False
restart_requested = False
url = "https://raw.githubusercontent.com/maxmax567/Pyxis/main/apps.json"

# Window groups, maybe separate file??
window_groups = {"account": ["account", "login", "register_window"], "all": ["account", "login", "register_window"]}

# Load config
try:
    with open("config.json", "r") as f:
        config = json.load(f)
        if config.get("locale") in l.languages:
            language = config.get("locale")
        else:
            language = l.get_system_locale()
            with open("config.json", "w") as s:
                l.change_locale(l.get_system_locale())
                json.dump({"locale": l.get_system_locale()}, s)

except (FileNotFoundError, json.JSONDecodeError):
    with open("config.json", "w") as s:
        language = l.get_system_locale()
        json.dump({"locale": l.get_system_locale()}, s)

# Load Supabase apps list
def fetch_remote_apps():
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Error loading apps:", e)
        return []

# Change language to the loaded in the configuration
l.change_locale(language)

# Log in with Google
def google_login():
    def worker():
        global session_active
        ok, message = sc.google_login()
        print("google_login ->", ok, message)  # comprueba que llega aquí
        session_active = ok
        close("account")  # cierra account y login
        update_accounts()
        popup("login_browser_done" if ok else message, translate=ok)
    threading.Thread(target=worker, daemon=True).start()

def popup(msg: str, translate: bool = True) -> None:
    close("all")
    text = l.t(msg) if translate else msg
    dpg.set_value("popup_msg", text)

    def _show():
        vw = dpg.get_viewport_client_width()
        vh = dpg.get_viewport_client_height()
        dpg.configure_item(
            "popup",
            show=True,
            pos=[max(vw // 2 - 150, 0), max(vh // 2 - 50, 0)],
        )
        dpg.focus_item("popup")

    dpg.set_frame_callback(dpg.get_frame_count() + 3, _show)

def close_popup():
    dpg.configure_item("popup", show=False)

# Log in with email/password
def email_login():
    sc.login()

# Forgot password
def forgot_password():
    print("Forgot Password")

# Register
def register():
    popup("Not working :(", False)

# Open register
def open_register():
    close("account")

    def _show():
        vw = dpg.get_viewport_client_width()
        vh = dpg.get_viewport_client_height()
        dpg.configure_item(
            "register_window",
            show=True,
            pos=[max(vw // 2 - 150, 0), max(vh // 2 - 85, 0)],
        )
        dpg.focus_item("register_window")

    dpg.set_frame_callback(dpg.get_frame_count() + 3, _show)

# Restart
def restart():
    global restart_requested
    restart_requested = True
    dpg.stop_dearpygui()

def show_lang_popup():
    vw = dpg.get_viewport_client_width()
    vh = dpg.get_viewport_client_height()
    dpg.configure_item(
        "lang_popup",
        show=True,
        pos=[max(vw // 2 - 200, 0), max(vh // 2 - 60, 0)],
    )
    dpg.focus_item("lang_popup")

# Close restart window
def close_lang_popup():
    dpg.configure_item("lang_popup", show=False)

# Language changed
def language_updated(sender, app_data):
    try:
        data = json.dumps({"locale": app_data})
        l.change_locale(app_data)
        with open("config.json", "w") as s:
            s.write(data)
    except Exception as e:
        print("Error en language_updated:", e)
        return

    dpg.set_frame_callback(dpg.get_frame_count() + 3, show_lang_popup)

# Open settings
def open_settings():
    dpg.configure_item("settings", show=True)
    dpg.focus_item("settings")

# Open account
def open_account():
    close("account")
    dpg.configure_item("account", show=True)
    dpg.focus_item("account")

def open_login():
    close("account")
    vw = dpg.get_viewport_client_width()
    vh = dpg.get_viewport_client_height()
    dpg.configure_item(
        "login",
        show=True,
        pos=[max(vw // 2 - 150, 0), max(vh // 2 - 100, 0)],
    )
    dpg.focus_item("login")

def close(window_group: str):
    global window_groups
    if window_group in window_groups:
        for i in window_groups[window_group]:
            dpg.configure_item(i, show=False)
    else:
        print("Not a group")

# Update accounts UI
def update_accounts():
    dpg.configure_item("login_btn", enabled=not session_active)
    dpg.configure_item("close_session", enabled=session_active)
    dpg.configure_item("register_btn", enabled=not session_active)

# Close session
def logout():
    global session_active
    session_active = False
    update_accounts()
    sc.logout()

dpg.create_context()

# Create theme
with dpg.theme() as global_theme: # type: ignore
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4.0)

    with dpg.theme_component(dpg.mvButton, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (85, 85, 85, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (85, 85, 85, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (85, 85, 85, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (150, 150, 150, 255))

    with dpg.theme_component(dpg.mvInputText, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (85, 85, 85, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (150, 150, 150, 255))

# Load fonts
with dpg.font_registry():
    default_font = dpg.add_font("./fonts/Rubik-Regular.ttf", size=40)

dpg.bind_font(default_font)

# Change font size
def change_font_size(sender, app_data):
    dpg.set_global_font_scale(app_data)

# Restart to apply changes window, it was for the language change, but better if it is generic
with dpg.window(tag="lang_popup", modal=True, show=False, no_close=True, no_resize=True, width=400, label=l.t("lang_popup_title")):  # type: ignore
    dpg.add_text(l.t("lang_popup_desc"))
    dpg.add_text(l.t("lang_popup_alert"))
    dpg.add_separator()
    with dpg.group(horizontal=True):  # type: ignore
        dpg.add_button(label=l.t("restart"), callback=restart)
        dpg.add_button(label=l.t("cancel"), callback=close_lang_popup)

# Generic popup
with dpg.window(tag="popup", label=l.t("system_msg"), show=False, modal=True, no_resize=True, width=300, height=200):
    dpg.add_text("", tag="popup_msg", wrap=280)
    dpg.add_separator()
    dpg.add_button(label=l.t("ok"), callback=close_popup)

# Settings window
with dpg.window(tag="settings", label=l.t("settings"), show=False, width=300, height=300, pos=[300, 0]):  # type: ignore
    dpg.add_text(l.t("language_selector"))
    dpg.add_combo(l.languages, default_value=language, callback=language_updated, tag="language_value")
    dpg.add_text(l.t("font_scale"))
    dpg.add_slider_float(
        label="",
        default_value=0.5,
        min_value=0.3,
        max_value=1,
        callback=change_font_size
    )

# Account window
with dpg.window(label=l.t("account"), tag="account", show=False, width=300, height=200, pos=[300, 0]):  # type: ignore
    dpg.add_button(label=l.t("login_button"), enabled=not session_active, callback=open_login, tag="login_btn")
    dpg.add_button(label=l.t("close_session"), enabled=session_active, tag="close_session", callback=logout)
    dpg.add_button(label=l.t("register_button"), callback=open_register, tag="register_btn", enabled=not session_active)

# Login window
with dpg.window(tag="login", label=l.t("login_title"), show=False, no_move=True, no_resize=True, no_collapse=True, modal=True):  # type: ignore
    dpg.add_text(l.t("email_login"))
    dpg.add_input_text(hint=l.t("email_label"), tag="input_email")
    dpg.add_input_text(password=True, hint=l.t("password_label"), tag="input_password")
    dpg.add_button(label=l.t("login_button"), callback=email_login)
    dpg.add_button(label=l.t("forgot_password_button"), callback=forgot_password)
    dpg.add_button(label=l.t("google_login"), callback=google_login)
    dpg.add_button(label=l.t("register_button"), callback=open_register)
    dpg.add_button(label=l.t("back"), callback=open_account)

# Register window
with dpg.window(tag="register_window", label=l.t("register_button"), show=False, no_move=True, no_resize=True, no_collapse=True, modal=True, width=300, height=300):
    dpg.add_input_text(hint=l.t("email_label"), tag="input_email_reg")
    dpg.add_input_text(password=True, hint=l.t("password_label"), tag="input_password_reg")
    dpg.add_input_text(password=True, hint=l.t("password_label_confirm"), tag="input_password_reg_confirm")
    dpg.add_button(label=l.t("register_button"), callback=register)
    dpg.add_button(label=l.t("back"), callback=open_account)

# Pyxis menu
with dpg.window(tag="main", label=l.t("main_title"), no_close=True, width=300, height=400):  # type: ignore
    with dpg.menu_bar():  # type: ignore
        dpg.add_menu_item(label=l.t("settings"), callback=open_settings)
        dpg.add_menu_item(label=l.t("account"), callback=open_account)
    with dpg.collapsing_header(label=l.t("official_apps")):
        for mod in load_local_apps():
            dpg.add_button(label=l.t(mod.app), width=-1, callback=run_app, user_data=mod.launch)

#demo.show_demo()

dpg.bind_theme(global_theme)
dpg.create_viewport(title="Pyxis", small_icon=small_icon, large_icon=large_icon)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_global_font_scale(0.5)
dpg.start_dearpygui()
dpg.destroy_context()

if restart_requested:
    os.execv(sys.executable, [sys.executable] + sys.argv)