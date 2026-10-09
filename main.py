import dearpygui.dearpygui as dpg
import langs as l
import supabase_client as sc
import dearpygui.demo as demo
import json
import os

language = "en"

try:
    with open("config.json", "r") as f:
        config = json.load(f)
        language = config.get("locale")

except FileNotFoundError:
    with open("config.json", "w") as f:
        language = l.get_system_locale()
        json.dump({"locale": l.get_system_locale()}, f)

l.change_locale(language)

def google_login():
    sc.google_login()

def email_login():
    sc.login()

def forgot_password():
    print("Forgot Password")

def register():
    print("Register")

def print_me():
    print("Print")

def language_updated(sender, app_data):
    print(l.change_locale(app_data))


dpg.create_context()

with dpg.window(tag="login", label=l.t("login_title")): # type: ignore
    dpg.add_text(l.t("email_login"))
    dpg.add_input_text(hint=l.t("email_label"), tag="input_email")
    dpg.add_input_text(password=True, hint=l.t("password_label"), tag="input_password")
    dpg.add_button(label=l.t("login_button"), callback=email_login)
    dpg.add_button(label=l.t("forgot_password_button"), callback=forgot_password)
    dpg.add_button(label=l.t("google_login"), callback=google_login)
    dpg.add_button(label=l.t("register_button"), callback=register)

with dpg.window(tag="main", label=l.t("main_title"), no_close=True): # type: ignore
    with dpg.menu_bar():
        with dpg.menu(label=l.t("settings")):
            dpg.add_text(l.t("language_selector"))
            dpg.add_combo(l.languages, default_value=(l.get_system_locale()), callback=language_updated)

        dpg.add_menu_item(label="Help", callback=print_me)

    dpg.add_text(l.t("main_title"))

demo.show_demo()

dpg.create_viewport(title="Pyxis")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()