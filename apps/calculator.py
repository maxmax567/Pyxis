import dearpygui.dearpygui as dpg
import langs as l

app = "calculator"
display_tag = f"{app}_display"

# Estado de la calculadora
current_input = "0"
expression = ""
new_input = True


def update_display(value=None):
    global current_input
    if value is not None:
        current_input = value
    if dpg.does_item_exist(display_tag):
        dpg.set_value(display_tag, current_input)


def press_digit(digit):
    global current_input, new_input
    if new_input:
        current_input = str(digit)
        new_input = False
    else:
        if current_input == "0":
            current_input = str(digit)
        else:
            current_input += str(digit)
    update_display()


def press_decimal():
    global current_input, new_input
    if new_input:
        current_input = "0."
        new_input = False
    elif "." not in current_input:
        current_input += "."
    update_display()


def press_operator(op):
    global current_input, expression, new_input
    if expression and not new_input:
        press_equal()
    expression = current_input + f" {op} "
    new_input = True


def press_equal():
    global current_input, expression, new_input
    if not expression:
        return
    try:
        full_expr = expression + current_input
        result = eval(full_expr)
        if isinstance(result, float):
            result = f"{result:.10g}"
        current_input = str(result)
        expression = ""
        new_input = True
        update_display()
    except Exception as e:
        current_input = "Error"
        expression = ""
        new_input = True
        update_display()


def press_clear():
    global current_input, expression, new_input
    current_input = "0"
    expression = ""
    new_input = True
    update_display()


def press_backspace():
    global current_input, new_input
    if new_input:
        return
    if len(current_input) > 1:
        current_input = current_input[:-1]
    else:
        current_input = "0"
        new_input = True
    update_display()


def press_sign():
    global current_input, new_input
    if current_input.startswith("-"):
        current_input = current_input[1:]
    elif current_input != "0":
        current_input = "-" + current_input
    update_display()


def launch():
    if dpg.does_item_exist(app):
        dpg.configure_item(app, show=True)
        dpg.focus_item(app)
        return

    win_w, win_h = 320, 450
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
        no_resize=True,
    ):
        dpg.add_input_text(tag=display_tag, default_value="0", readonly=True, width=-1)
        dpg.add_separator()

        # Fila 1: C, ±, ⌫, /
        with dpg.group(horizontal=True):
            dpg.add_button(label="C", width=70, height=40, callback=lambda: press_clear())
            dpg.add_button(label="±", width=70, height=40, callback=lambda: press_sign())
            dpg.add_button(label="⌫", width=70, height=40, callback=lambda: press_backspace())
            dpg.add_button(label="/", width=70, height=40, callback=lambda: press_operator("/"))

        # Fila 2: 7, 8, 9, *
        with dpg.group(horizontal=True):
            dpg.add_button(label="7", width=70, height=40, callback=lambda: press_digit(7))
            dpg.add_button(label="8", width=70, height=40, callback=lambda: press_digit(8))
            dpg.add_button(label="9", width=70, height=40, callback=lambda: press_digit(9))
            dpg.add_button(label="*", width=70, height=40, callback=lambda: press_operator("*"))

        # Fila 3: 4, 5, 6, -
        with dpg.group(horizontal=True):
            dpg.add_button(label="4", width=70, height=40, callback=lambda: press_digit(4))
            dpg.add_button(label="5", width=70, height=40, callback=lambda: press_digit(5))
            dpg.add_button(label="6", width=70, height=40, callback=lambda: press_digit(6))
            dpg.add_button(label="-", width=70, height=40, callback=lambda: press_operator("-"))

        # Fila 4: 1, 2, 3, +
        with dpg.group(horizontal=True):
            dpg.add_button(label="1", width=70, height=40, callback=lambda: press_digit(1))
            dpg.add_button(label="2", width=70, height=40, callback=lambda: press_digit(2))
            dpg.add_button(label="3", width=70, height=40, callback=lambda: press_digit(3))
            dpg.add_button(label="+", width=70, height=40, callback=lambda: press_operator("+"))

        # Fila 5: 0, ., =
        with dpg.group(horizontal=True):
            dpg.add_button(label="0", width=150, height=40, callback=lambda: press_digit(0))
            dpg.add_button(label=".", width=70, height=40, callback=lambda: press_decimal())
            dpg.add_button(label="=", width=70, height=40, callback=lambda: press_equal())