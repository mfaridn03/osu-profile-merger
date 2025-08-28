import dearpygui.dearpygui as dpg


def create_main_window():
    """Create the main application window"""
    with dpg.window(label="osu! Profile Merger", tag="primary_window"):
        dpg.add_text("Main Window")
        dpg.add_separator()
        dpg.add_text("Ready")
