import threading
import ossapi
import dearpygui.dearpygui as dpg
from auth.credential_manager import CredentialManager
from services.merge import merge_top_scores


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
            user_data={
                "app_user_id": user_id,
                "credential_manager": credential_manager,
                "status_tag": "merge_status_text",
                "table_tag": "results_table",
                "main_input_tag": "main_player_input",
                "merge_input_tag": "merge_player_input",
                "button_tag": "fetch_merge_button",
            },
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
            dpg.add_table_column(label="Rank", default_sort=True)
            dpg.add_table_column(label="User")
            dpg.add_table_column(label="Beatmap")
            dpg.add_table_column(label="PP")
            dpg.add_table_column(label="Accuracy")
            dpg.add_table_column(label="Mods")


def on_merge_clicked(sender, app_data, user_data):
    """Fetch, merge, and render the top plays for two users."""
    status_tag = user_data["status_tag"]
    table_tag = user_data["table_tag"]
    main_input_tag = user_data["main_input_tag"]
    merge_input_tag = user_data["merge_input_tag"]
    button_tag = user_data["button_tag"]
    app_user_id = user_data["app_user_id"]
    credential_manager: CredentialManager = user_data["credential_manager"]

    # Read inputs
    main_id_raw = dpg.get_value(main_input_tag).strip()
    merge_id_raw = dpg.get_value(merge_input_tag).strip()

    # Validate
    if not main_id_raw or not merge_id_raw:
        dpg.set_value(status_tag, "Please enter both user IDs.")
        return
    if not main_id_raw.isdigit() or not merge_id_raw.isdigit():
        dpg.set_value(status_tag, "User IDs must be numeric.")
        return

    main_id = int(main_id_raw)
    merge_id = int(merge_id_raw)

    # Decrypt credentials
    dpg.set_value(status_tag, "Decrypting credentials...")
    creds = credential_manager.decrypt_credentials(app_user_id)
    if not creds:
        dpg.set_value(status_tag, "Failed to decrypt credentials. Check User ID.")
        return

    client_id = creds["client_id"]
    client_secret = creds["client_secret"]

    # Disable UI during work
    _set_loading_state(button_tag, main_input_tag, merge_input_tag, True)
    dpg.set_value(status_tag, "Fetching and merging top plays...")

    def worker():
        try:
            api = ossapi.Ossapi(client_id, client_secret)
            merged = merge_top_scores(api, main_id, merge_id, limit=100)

            # Render results
            _render_results(table_tag, merged)
            dpg.set_value(status_tag, f"Merged {len(merged)} unique beatmaps.")
        except Exception as e:
            dpg.set_value(status_tag, f"Error: {e}")
        finally:
            _set_loading_state(button_tag, main_input_tag, merge_input_tag, False)

    threading.Thread(target=worker, daemon=True).start()


def _set_loading_state(
    button_tag: str, main_input_tag: str, merge_input_tag: str, is_loading: bool
):
    try:
        dpg.configure_item(button_tag, enabled=not is_loading)
        dpg.configure_item(main_input_tag, enabled=not is_loading)
        dpg.configure_item(merge_input_tag, enabled=not is_loading)
    except Exception:
        pass


def _clear_results_table(table_tag: str):
    # Remove existing rows (slot 1 contains rows in DearPyGUI tables)
    try:
        children = dpg.get_item_children(table_tag, 1) or []
        for row_id in children:
            dpg.delete_item(row_id)
    except Exception:
        pass


def _render_results(table_tag: str, rows):
    _clear_results_table(table_tag)
    rank = 1
    for beatmap_id, data in rows:
        score = data["score"]
        user = data["user"]
        pp_val = data.get("pp", getattr(score, "pp", 0.0))
        acc = getattr(score, "accuracy", 0.0)
        mods = getattr(score, "mods", None)
        mods_str = ",".join([m.acronym for m in mods]) if mods is not None else ""

        with dpg.table_row(parent=table_tag):
            dpg.add_text(str(rank))
            dpg.add_text(user.username)
            dpg.add_text(str(beatmap_id))
            dpg.add_text(f"{pp_val:.2f}")
            dpg.add_text(f"{acc * 100:.2f}%")
            dpg.add_text(mods_str)
        rank += 1
