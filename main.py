import dearpygui.dearpygui as dpg
import langs as l

def google_login():
    print("Google")

def email_login():
    print("Email")

def forgot_password():
    print("Forgot Password")

def register():
    print("Register")

dpg.create_context()

with dpg.window(tag="login", label=l.t("login_title")): # type: ignore
    dpg.add_text(l.t("email_login"))
    dpg.add_input_text(label=l.t("email_label"))
    dpg.add_input_text(label=l.t("password_label"))
    dpg.add_button(label=l.t("login_button"), callback=email_login)
    dpg.add_button(label=l.t("forgot_password_button"), callback=forgot_password)
    dpg.add_button(label=l.t("google_login"), callback=google_login)
    dpg.add_button(label=l.t("register_button"), callback=register)

with dpg.window(tag="main", label=l.t("main_title")): # type: ignore
    dpg.add_text(l.t("main_title"))
    dpg.add_text("tst")

dpg.create_viewport(title="Pyxis")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()