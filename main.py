import dearpygui.dearpygui as dpg
import langs as l

def google_login():
    print("Google")

def email_login():
    print("Email")

dpg.create_context()
dpg.create_viewport(title="Pyxis")
dpg.setup_dearpygui()

with dpg.window(label=l.t("login_title")): # Why an error
    dpg.add_text("Log in with email")
    dpg.add_input_text(label="Email")
    dpg.add_input_text(label="Password")
    dpg.add_button(label="Log in")
    dpg.add_button(label="I forgot my password")
    dpg.add_button(label="Log in with Google", callback=google_login)
    dpg.add_button(label=l.t("create_account"))

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()