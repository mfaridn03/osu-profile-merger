import dearpygui.dearpygui as dpg
from auth.credential_manager import CredentialManager


class UserIdPromptWindow:
    """Handles the user ID prompt for returning users"""

    def __init__(
        self,
        on_complete_callback,
        credential_manager: CredentialManager,
    ):
        self.on_complete_callback = on_complete_callback
        self.credential_manager = credential_manager
        self.user_id_input = None
        self.submit_button = None
        self.status_text = None

    def create_window(self):
        """Create the user ID prompt window"""
        with dpg.window(
            tag="user_id_prompt_window",
            modal=True,
            width=400,
            height=270,
            no_close=True,
        ):
            dpg.add_text("Welcome back!")
            dpg.add_separator()
            dpg.add_text(
                "Enter your osu! user ID to continue. It must be the same as the one you entered for the first time.",
                wrap=350,
            )
            dpg.add_spacer(height=2)
            self.user_id_input = dpg.add_input_text(
                hint="osu! user ID",
                width=350,
                on_enter=True,
                callback=self._on_submit,
            )
            dpg.add_spacer(height=2)

            # Status text for feedback
            self.status_text = dpg.add_text("", color=(255, 0, 0), wrap=350)
            dpg.add_spacer()

            # Buttons
            with dpg.group(horizontal=True):
                self.submit_button = dpg.add_button(
                    label="Submit", callback=self._on_submit, width=100
                )

        # Center the window
        dpg.set_item_pos("user_id_prompt_window", [200, 175])

    def _on_submit(self):
        """Handle submit button click - currently does nothing as requested"""
        user_id = dpg.get_value(self.user_id_input).strip()

        # Validate user ID
        if not user_id:
            dpg.set_value(self.status_text, "Please enter your User ID.")
            return

        if not user_id.isdigit():
            dpg.set_value(self.status_text, "User ID must be numeric.")
            return

        # Attempt to decrypt config file using entered user ID
        try:
            decrypted_data = self.credential_manager.decrypt_credentials(user_id)
        except Exception as e:
            dpg.set_value(self.status_text, f"Error decrypting credentials: {str(e)}")
            return

        if not decrypted_data:
            dpg.set_value(
                self.status_text,
                "Invalid User ID. To reset, delete the config.json file located in the data folder.",
            )
            return

        # Clear any error messages
        dpg.set_value(self.status_text, "")

    def get_user_id(self):
        """Get the entered user ID"""
        if self.user_id_input:
            return dpg.get_value(self.user_id_input).strip()
        return ""

    def close_window(self):
        """Close the user ID prompt window"""
        if dpg.does_item_exist("user_id_prompt_window"):
            dpg.delete_item("user_id_prompt_window")
