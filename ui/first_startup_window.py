import dearpygui.dearpygui as dpg
from auth import CredentialManager


class FirstStartupWindow:
    """Handles the first-time setup UI for collecting user credentials"""

    def __init__(self, on_complete_callback, credential_manager: CredentialManager):
        self.on_complete_callback = on_complete_callback
        self.credential_manager = credential_manager
        self.user_id_input = None
        self.client_id_input = None
        self.client_secret_input = None
        self.status_text = None

    def create_window(self):
        """Create the first startup configuration window"""
        with dpg.window(
            label="First Time Setup",
            tag="setup_window",
            modal=True,
            width=500,
            height=400,
            no_close=True,
        ):
            dpg.add_text("osu! Profile Merger!")
            dpg.add_separator()
            dpg.add_text("Please enter your osu! API credentials:")
            dpg.add_spacer(height=2)

            # osu! User ID input
            dpg.add_text("osu! User ID:")
            self.user_id_input = dpg.add_input_text(
                hint="Your numeric osu! user ID", width=400
            )
            dpg.add_spacer()

            # Client ID input
            dpg.add_text("Client ID:")
            self.client_id_input = dpg.add_input_text(
                hint="Your osu! API client ID", width=400
            )
            dpg.add_spacer()

            # Client Secret input
            dpg.add_text("Client Secret:")
            self.client_secret_input = dpg.add_input_text(
                hint="Your osu! API client secret", password=True, width=400
            )
            dpg.add_spacer(height=2)

            # Status text
            self.status_text = dpg.add_text("", color=(255, 0, 0))
            dpg.add_spacer()

            # Buttons
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Save Credentials", callback=self._save_credentials, width=150
                )

        # Center the window
        dpg.set_item_pos("setup_window", [150, 100])

    def _save_credentials(self):
        """Save the entered credentials"""
        user_id = dpg.get_value(self.user_id_input).strip()
        client_id = dpg.get_value(self.client_id_input).strip()
        client_secret = dpg.get_value(self.client_secret_input).strip()

        # Validate inputs
        if not user_id or not client_id or not client_secret:
            dpg.set_value(self.status_text, "Please fill in all fields.")
            return

        # Validate user ID is numeric
        if not user_id.isdigit():
            dpg.set_value(self.status_text, "User ID must be numeric.")
            return

        # Encrypt and save credentials
        encrypted_data = self.credential_manager.encrypt_credentials(
            user_id, client_id, client_secret
        )
        self.credential_manager.save_credentials(encrypted_data)

        dpg.set_value(self.status_text, "")
        dpg.delete_item("setup_window")

        # Call the completion callback
        self.on_complete_callback(user_id)
