import dearpygui.dearpygui as dpg
import langs as l

app = "tasks"
input_tag = f"{app}_input"
list_tag = f"{app}_list"

# Estado: lista de dicts {id, text, done}
tasks = []
task_counter = 0


def refresh_list():
    if not dpg.does_item_exist(list_tag):
        return
    dpg.delete_item(list_tag, children_only=True)
    for task in tasks:
        with dpg.group(horizontal=True, parent=list_tag):
            dpg.add_checkbox(
                default_value=task["done"],
                callback=lambda s, a, u: toggle_task(u, a),
                user_data=task["id"],
            )
            dpg.add_text(task["text"], color=(150, 150, 150, 255) if task["done"] else (255, 255, 255, 255))
            dpg.add_button(
                label="✕",
                small=True,
                callback=lambda s, a, u: delete_task(u),
                user_data=task["id"],
            )


def add_task(sender, app_data):
    global task_counter
    text = dpg.get_value(input_tag).strip()
    if not text:
        return
    task_counter += 1
    tasks.append({"id": task_counter, "text": text, "done": False})
    dpg.set_value(input_tag, "")
    refresh_list()


def toggle_task(task_id, checked):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = checked
            break
    refresh_list()


def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    refresh_list()


def clear_completed(sender, app_data):
    global tasks
    tasks = [t for t in tasks if not t["done"]]
    refresh_list()


def launch():
    if dpg.does_item_exist(app):
        dpg.configure_item(app, show=True)
        dpg.focus_item(app)
        return

    win_w, win_h = 450, 500
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
    ):
        with dpg.group(horizontal=True):
            dpg.add_input_text(tag=input_tag, hint=l.t("new_task"), width=-100)
            dpg.add_button(label="+", width=80, callback=add_task)

        dpg.add_separator()
        dpg.add_child_window(tag=list_tag, height=-50, border=True)
        dpg.add_button(label=l.t("clear_completed"), callback=clear_completed)

    refresh_list()