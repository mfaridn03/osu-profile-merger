import dearpygui.dearpygui as dpg


def main():
    dpg.create_context()

    dpg.create_viewport(title="Title", width=800, height=600)

    with dpg.window(label="Window", tag="primary_window"):
        dpg.add_text("Hello, World!")

    dpg.set_primary_window("primary_window", True)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.start_dearpygui()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
