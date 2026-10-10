import dearpygui.dearpygui as dpg
import langs as l
import supabase_client as sc
import dearpygui.demo as demo
import json
import threading
import os
import sys

# Icon selection
if sys.platform == "win32":
    small_icon = large_icon = "icons/icon.ico"
else:
    small_icon = "icons/icon_small.png"
    large_icon = "icons/icon_large.png"

language = "en"

session_active = True

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

l.change_locale(language)

def google_login():
    def worker():
        sc.google_login()
    threading.Thread(target=worker, daemon=True).start()

def email_login():
    sc.login()

def forgot_password():
    print("Forgot Password")

# Register
def register():
    print("Register")

# Restart requested?
restart_requested = False

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

dpg.create_context()

with dpg.theme() as global_theme:  # type: ignore
    with dpg.theme_component(dpg.mvAll):  # type: ignore
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4.0)

# Restart to apply changes window, it was for the language change, but better if it is generic
with dpg.window(tag="lang_popup", modal=True, show=False, no_close=True, no_resize=True, width=400, label=l.t("lang_popup_title")):  # type: ignore
    dpg.add_text(l.t("lang_popup_desc"))
    dpg.add_text(l.t("lang_popup_alert"))
    dpg.add_separator()
    with dpg.group(horizontal=True):  # type: ignore
        dpg.add_button(label=l.t("restart"), callback=restart)
        dpg.add_button(label=l.t("cancel"), callback=close_lang_popup)


# Settings window
with dpg.window(tag="settings", label=l.t("settings"), show=False, width=300, height=100, pos=[80, 80]):  # type: ignore
    dpg.add_text(l.t("language_selector"))
    dpg.add_combo(l.languages, default_value=language,
                  callback=language_updated, tag="language_value")

# Account window
with dpg.window(label=l.t("account"), tag="account", show=True, width=300, height=200, pos=[100, 100]):  # type: ignore
    dpg.add_button(label=l.t("login_button"), enabled=False)
    dpg.add_button(label=l.t("close_session"), enabled=True)

# Login window
with dpg.window(tag="login", label=l.t("login_title"), show=False):  # type: ignore
    dpg.add_text(l.t("email_login"))
    dpg.add_input_text(hint=l.t("email_label"), tag="input_email")
    dpg.add_input_text(password=True, hint=l.t("password_label"), tag="input_password")
    dpg.add_button(label=l.t("login_button"), callback=email_login)
    dpg.add_button(label=l.t("forgot_password_button"), callback=forgot_password)
    dpg.add_button(label=l.t("google_login"), callback=google_login)
    dpg.add_button(label=l.t("register_button"), callback=register)

# Pyxis menu
with dpg.window(tag="main", label=l.t("main_title"), no_close=True, width=220, height=400):  # type: ignore
    with dpg.menu_bar():  # type: ignore
        dpg.add_menu_item(label=l.t("settings"), callback=open_settings)
        dpg.add_menu_item(label=l.t("account"), callback=open_account)


    dpg.add_text(l.t("main_title"))

# demo.show_demo()

dpg.bind_theme(global_theme)
dpg.create_viewport(title="Pyxis", small_icon=small_icon, large_icon=large_icon)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

if restart_requested:
    os.execv(sys.executable, [sys.executable] + sys.argv)