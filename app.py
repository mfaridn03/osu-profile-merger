import dearpygui.dearpygui as dpg
from auth import CredentialManager
from ui import FirstStartupWindow, create_main_window, UserIdPromptWindow


class OsuProfileMergerApp:
    """Main application class for osu! Profile Merger"""

    def __init__(self):
        self.credential_manager = CredentialManager()

    def initialize_gui(self):
        """Initialize the DearPyGUI context and viewport"""
        dpg.create_context()
        dpg.create_viewport(title="osu! Profile Merger", width=800, height=600)

    def setup_main_flow(self):
        """Setup the main application flow based on configuration state"""
        if not self.credential_manager.credentials_exist():
            self._show_first_startup()
        else:
            self._show_user_id_prompt()

    def _show_first_startup(self):
        """Show first startup configuration window"""

        def on_setup_complete():
            self._show_main_window()

        startup_window = FirstStartupWindow(self.credential_manager, on_setup_complete)
        startup_window.create_window()

    def _show_user_id_prompt(self):
        """Show user ID prompt for returning users"""

        def on_prompt_complete():
            self._show_main_window()

        user_id_prompt = UserIdPromptWindow(on_prompt_complete, self.credential_manager)
        user_id_prompt.create_window()

    def _show_main_window(self):
        """Show the main application window"""
        create_main_window()
        dpg.set_primary_window("primary_window", True)

    def run(self):
        """Run the application"""
        self.initialize_gui()
        self.setup_main_flow()

        # Start the GUI loop
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()

        # Cleanup
        dpg.destroy_context()


def main():
    """Main entry point"""
    app = OsuProfileMergerApp()
    app.run()


if __name__ == "__main__":
    main()
