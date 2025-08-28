import dearpygui.dearpygui as dpg
from auth.credential_manager import CredentialManager


def create_main_window(user_id: str, credential_manager: CredentialManager):
    """Create the main application window"""
    with dpg.window(label="osu! Profile Merger", tag="primary_window"):
        dpg.add_text("Configuration")
        dpg.add_separator()

        # Main player input
        dpg.add_text("Main Player:")
        dpg.add_input_text(
            tag="main_player_input",
            hint="Main player user ID",
            width=300,
        )

        dpg.add_spacer(height=10)

        # Merge player input
        dpg.add_text("Player to Merge:")
        dpg.add_input_text(
            tag="merge_player_input",
            hint="Second player user ID",
            width=300,
        )

        dpg.add_spacer(height=10)

        # Action button and status
        dpg.add_button(
            label="Fetch & Merge Tops",
            tag="fetch_merge_button",
            callback=on_merge_clicked,
            width=200,
        )
        dpg.add_spacer(height=4)
        dpg.add_text("", tag="merge_status_text", wrap=700)

        dpg.add_spacer(height=10)
        dpg.add_separator()
        dpg.add_text("Merged Top Plays")

        # Results table
        with dpg.table(
            tag="results_table",
            resizable=True,
            row_background=True,
            borders_outerH=True,
            borders_outerV=True,
            borders_innerH=True,
            borders_innerV=True,
            header_row=True,
            policy=dpg.mvTable_SizingStretchProp,
            scrollY=True,
            height=350,
        ):
            dpg.add_table_column(label="Rank")
            dpg.add_table_column(label="User")
            dpg.add_table_column(label="Beatmap")
            dpg.add_table_column(label="PP")
            dpg.add_table_column(label="Accuracy")
            dpg.add_table_column(label="Mods")


def on_merge_clicked(sender, app_data, user_data):
    """Placeholder callback for merge action; real logic will be wired later."""
    dpg.set_value(
        "merge_status_text", "Fetching and merging top plays... (not implemented yet)"
    )
