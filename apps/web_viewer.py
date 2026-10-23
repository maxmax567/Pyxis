import dearpygui.dearpygui as dpg
import langs as l
import webbrowser
import subprocess
import sys

app = "web_viewer"
url_tag = f"{app}_url"
status_tag = f"{app}_status"


def _get_url():
    url = dpg.get_value(url_tag).strip()
    if not url:
        return None
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        dpg.set_value(url_tag, url)
    return url


def open_in_browser(sender, app_data):
    url = _get_url()
    if not url:
        return
    try:
        webbrowser.open(url)
        dpg.set_value(status_tag, l.t("opened_in_browser"))
    except Exception as e:
        dpg.set_value(status_tag, f"{l.t('error')}: {e}")


def view_page(sender, app_data):
    """Abre la página en una ventana independiente tipo iframe."""
    url = _get_url()
    if not url:
        return

    # Escapamos comillas simples por si la URL las tuviera
    safe_url = url.replace("'", "\\'")

    # Script que se ejecutará en un proceso totalmente independiente
    script = f"""
import webview
try:
    window = webview.create_window('{safe_url}', url='{safe_url}', width=900, height=600, resizable=True)
    webview.start()
except Exception as e:
    print(f"Error en visor web: {{e}}")
"""

    try:
        # Lanzamos el proceso usando el mismo Python de tu entorno virtual
        subprocess.Popen(
            [sys.executable, '-c', script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        dpg.set_value(status_tag, l.t("loaded"))
    except Exception as e:
        dpg.set_value(status_tag, f"{l.t('error')}: {e}")


def launch():
    if dpg.does_item_exist(app):
        dpg.configure_item(app, show=True)
        dpg.focus_item(app)
        return

    win_w, win_h = 800, 600
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
            dpg.add_input_text(tag=url_tag, hint="https://...", width=-220)
            dpg.add_button(label=l.t("open_browser"), callback=open_in_browser)
            dpg.add_button(label=l.t("view_page"), callback=view_page)

        dpg.add_separator()
        dpg.add_text(
            tag=status_tag,
            default_value=l.t("ready"),
            wrap=win_w - 20,
        )