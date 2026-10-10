import dearpygui.dearpygui as dpg
import langs as l
import supabase_client as sc
import dearpygui.demo as demo
import json
import threading
import os
import sys

language = "en"

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

def print_me():
    print("Print")

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

def close_lang_popup():
    dpg.configure_item("lang_popup", show=False)

def language_updated(sender, app_data):
    print("callback llamado:", app_data)  # puedes quitarlo cuando funcione
    try:
        data = json.dumps({"locale": app_data})
        l.change_locale(app_data)
        with open("config.json", "w") as s:
            s.write(data)
    except Exception as e:
        print("Error en language_updated:", e)
        return

    # Esperar unos frames a que el combo/menú se cierren antes de abrir el modal
    dpg.set_frame_callback(dpg.get_frame_count() + 3, show_lang_popup)

def open_settings():
    dpg.configure_item("settings", show=True)
    dpg.focus_item("settings")

dpg.create_context()

with dpg.theme() as global_theme:  # type: ignore
    with dpg.theme_component(dpg.mvAll):  # type: ignore
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4.0)

with dpg.window(tag="lang_popup", modal=True, show=False, no_close=True,
                no_resize=True, width=400, label=l.t("lang_popup_title")):  # type: ignore
    dpg.add_text(l.t("lang_popup_desc"))
    dpg.add_text(l.t("lang_popup_alert"))
    dpg.add_separator()
    with dpg.group(horizontal=True):  # type: ignore
        dpg.add_button(label=l.t("restart"), callback=restart)
        dpg.add_button(label=l.t("cancel"), callback=close_lang_popup)


with dpg.window(tag="settings", label=l.t("settings"), show=False,
                width=300, height=100, pos=[80, 80]):  # type: ignore
    dpg.add_text(l.t("language_selector"))
    dpg.add_combo(l.languages, default_value=language,
                  callback=language_updated, tag="language_value")

with dpg.window(tag="login", label=l.t("login_title"), show=False):  # type: ignore
    dpg.add_text(l.t("email_login"))
    dpg.add_input_text(hint=l.t("email_label"), tag="input_email")
    dpg.add_input_text(password=True, hint=l.t("password_label"), tag="input_password")
    dpg.add_button(label=l.t("login_button"), callback=email_login)
    dpg.add_button(label=l.t("forgot_password_button"), callback=forgot_password)
    dpg.add_button(label=l.t("google_login"), callback=google_login)
    dpg.add_button(label=l.t("register_button"), callback=register)

with dpg.window(tag="main", label=l.t("main_title"), no_close=True):  # type: ignore
    with dpg.menu_bar():  # type: ignore
        dpg.add_menu_item(label=l.t("settings"), callback=open_settings)
        dpg.add_menu_item(label="Help", callback=print_me)
        with dpg.menu(label=l.t("account")):  # type: ignore
            dpg.add_button(label=l.t("login_button"))

    dpg.add_text(l.t("main_title"))

    # Botón de prueba: bórralo cuando confirmes que el popup funciona
    dpg.add_button(label="Test popup", callback=show_lang_popup)

# demo.show_demo()

dpg.bind_theme(global_theme)
dpg.create_viewport(title="Pyxis")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

if restart_requested:
    os.execv(sys.executable, [sys.executable] + sys.argv)