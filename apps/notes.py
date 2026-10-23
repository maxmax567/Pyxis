import dearpygui.dearpygui as dpg
import langs as l
import os

app = "notes"
editor_tag = f"{app}_editor"
_open_dialog = f"{app}_open_dialog"
_save_dialog = f"{app}_save_dialog"

current_file = None  # ruta del documento en edición


# ---------------- utilidades ----------------
def get_content():
    return dpg.get_value(editor_tag)


def set_content(text):
    dpg.set_value(editor_tag, text)


def update_title(filename=None):
    title = l.t(app)
    if filename:
        title += f" - {filename}"
    if dpg.does_item_exist(app):
        dpg.configure_item(app, label=title)


def _collect_paths(app_data):
    """Normaliza la selección del file_dialog en una lista de rutas.

    En DearPyGui, app_data['selections'] es un dict indexado por el tag de
    la extensión, p.ej. {'.txt': ['/ruta/a.txt']}, por eso selections[0]
    lanza KeyError. Aquí aplanamos ese dict en una lista simple.
    """
    paths = []
    selections = app_data.get('selections') or {}
    for _tag, value in selections.items():
        if isinstance(value, (list, tuple)):
            paths.extend(value)
        elif value:
            paths.append(value)
    if not paths:
        fallback = app_data.get('file_path_name')
        if fallback:
            paths.append(fallback)
    return [p for p in paths if p]


def save_to_file(file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(get_content())
        return True
    except Exception as e:
        print(f"[notes] error al guardar: {e}")
        return False


# ---------------- callbacks de menú ----------------
def new_callback(sender, app_data):
    global current_file
    set_content("")
    current_file = None
    update_title()


def open_callback(sender, app_data):
    if not dpg.does_item_exist(_open_dialog):
        with dpg.file_dialog(directory_selector=False, callback=open_file_selected,
                             tag=_open_dialog, width=500, height=400, modal=True):
            dpg.add_file_extension(".txt")
            dpg.add_file_extension(".*")
    dpg.show_item(_open_dialog)


def save_callback(sender, app_data):
    if current_file:
        save_to_file(current_file)
    else:
        save_as_callback(sender, app_data)


def save_as_callback(sender, app_data):
    if not dpg.does_item_exist(_save_dialog):
        with dpg.file_dialog(directory_selector=False, callback=save_file_selected,
                             tag=_save_dialog, width=500, height=400, modal=True):
            dpg.add_file_extension(".txt")
            dpg.add_file_extension(".*")
    dpg.show_item(_save_dialog)


# ---------------- callbacks de diálogos ----------------
def open_file_selected(sender, app_data):
    global current_file
    paths = _collect_paths(app_data)
    dpg.hide_item(_open_dialog)
    if not paths:
        return

    file_path = paths[0]
    if os.path.isdir(file_path):
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[notes] error al abrir: {e}")
        return

    set_content(content)
    current_file = file_path
    update_title(os.path.basename(file_path))


def save_file_selected(sender, app_data):
    global current_file
    paths = _collect_paths(app_data)
    dpg.hide_item(_save_dialog)
    if not paths:
        return

    file_path = paths[0]
    if os.path.isdir(file_path):          # solo eligió carpeta, sin nombre
        file_path = os.path.join(file_path, "sin_titulo.txt")
    if not file_path.lower().endswith('.txt'):
        file_path += '.txt'

    if save_to_file(file_path):
        current_file = file_path
        update_title(os.path.basename(file_path))


# ---------------- launch ----------------
def launch():
    if dpg.does_item_exist(app):
        dpg.configure_item(app, show=True)
        dpg.focus_item(app)
        return

    # Tamaño "adecuado" para un editor de notas
    win_w, win_h = 700, 500

    # Centrar respecto al viewport (la ventana principal de la app)
    vp_w = dpg.get_viewport_width()
    vp_h = dpg.get_viewport_height()
    pos_x = max(0, (vp_w - win_w) // 2)
    pos_y = max(0, (vp_h - win_h) // 2)

    with dpg.window(
        tag=app,
        label=l.t(app),
        width=win_w,
        height=win_h,
        pos=[pos_x, pos_y],
        no_collapse=True,        # opcional: evita que se colapse a la barra de título
    ):  # type: ignore
        with dpg.menu_bar():  # type: ignore
            with dpg.menu(label=l.t("file")):
                dpg.add_menu_item(label=l.t("new"), callback=new_callback)
                dpg.add_menu_item(label=l.t("open"), callback=open_callback)
                dpg.add_menu_item(label=l.t("save"), callback=save_callback)
                dpg.add_menu_item(label=l.t("save_as"), callback=save_as_callback)

        dpg.add_input_text(tag=editor_tag, multiline=True, height=-1, width=-1, label="")

    update_title()