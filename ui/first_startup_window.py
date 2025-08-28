import dearpygui.dearpygui as dpg
from auth import CredentialManager


class FirstStartupWindow:
    """Handles the first-time setup UI for collecting user credentials"""

    def __init__(self, credential_manager: CredentialManager, on_complete_callback):
        self.credential_manager = credential_manager
        self.on_complete_callback = on_complete_callback
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
            dpg.add_spacing(count=2)

            # osu! User ID input
            dpg.add_text("osu! User ID:")
            self.user_id_input = dpg.add_input_text(
                hint="Your numeric osu! user ID", width=400
            )
            dpg.add_spacing()

            # Client ID input
            dpg.add_text("Client ID:")
            self.client_id_input = dpg.add_input_text(
                hint="Your osu! API client ID", width=400
            )
            dpg.add_spacing()

            # Client Secret input
            dpg.add_text("Client Secret:")
            self.client_secret_input = dpg.add_input_text(
                hint="Your osu! API client secret", password=True, width=400
            )
            dpg.add_spacing(count=2)

            # Status text
            self.status_text = dpg.add_text("", color=(255, 0, 0))
            dpg.add_spacing()

            # Buttons
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Save Credentials", callback=self._save_credentials, width=150
                )
                dpg.group(xoffset=20)
                dpg.add_button(label="Help", callback=self._show_help, width=100)

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

        try:
            # Encrypt and save credentials
            encrypted_data = self.credential_manager.encrypt_credentials(
                user_id, client_id, client_secret
            )
            self.credential_manager.save_credentials(encrypted_data)

            dpg.set_value(self.status_text, "")
            dpg.delete_item("setup_window")

            # Call the completion callback
            self.on_complete_callback()

        except Exception as e:
            dpg.set_value(self.status_text, f"Error saving credentials: {str(e)}")

    def _show_help(self):
        """Show help information"""
        if dpg.does_item_exist("help_window"):
            dpg.delete_item("help_window")

        with dpg.window(
            label="Help", tag="help_window", modal=True, width=600, height=300
        ):
            dpg.add_text("How to get your osu! API credentials:")
            dpg.add_separator()
            dpg.add_text("1. Go to https://osu.ppy.sh/home/account/edit#oauth")
            dpg.add_text("2. Create a new OAuth application")
            dpg.add_text("3. Copy the Client ID and Client Secret")
            dpg.add_text("4. Your User ID can be found in your profile URL")
            dpg.add_spacing(count=2)
            dpg.add_text(
                "Note: Credentials are encrypted and stored locally.", color=(0, 255, 0)
            )
            dpg.add_spacing()
            dpg.add_button(
                label="Close", callback=lambda: dpg.delete_item("help_window")
            )
