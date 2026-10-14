import dearpygui.dearpygui as dpg
import langs as l

app = "notes"

def launch():
    if dpg.does_item_exist(app):
        dpg.configure_item(app, show=True)
        dpg.focus_item(app)
        return

    with dpg.window(tag=app, label=l.t(app)): # type: ignore
        dpg.add_input_text(multiline=True, height=-1, label="")