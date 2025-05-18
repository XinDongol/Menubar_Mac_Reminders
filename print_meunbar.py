import rumps
import subprocess
import logging
import os
import sys

# Set up logging to a file in the user's Library/Logs directory
log_file = os.path.expanduser('~/Library/Logs/ReminderMenuBar.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG, # Use logging.INFO for less verbose logs in production
    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
)

class ReminderMenuBarApp(rumps.App):
    def __init__(self):
        logging.info("Application initializing")
        super(ReminderMenuBarApp, self).__init__(
            "ReminderApp", # Internal name for rumps, not the display name
            title="📝 Loading..."
        )
        # Define menu structure
        self.menu = [
            'Refresh',
            rumps.separator,
            'Quit'
        ]
        # Perform initial update
        self.update_reminder_display()
        
        # Set up auto-refresh timer (every 1 second)
        self.timer = rumps.Timer(self.timed_update, 1)
        self.timer.start()
        
        logging.info("Application initialized successfully")
    
    @rumps.clicked('Refresh')
    def on_refresh_clicked(self, _):
        logging.info("'Refresh' menu item clicked")
        self.update_reminder_display()
    
    # rumps handles the 'Quit' button automatically if it's in the menu.
    # You can add a @rumps.clicked('Quit') method if you need custom quit logic.

    def get_first_reminder(self):
        logging.debug("Fetching first reminder from Apple Reminders")
        apple_script = '''
        tell application "Reminders"
            set allIncompleteReminders to {}
            try
                repeat with aList in lists
                    set allIncompleteReminders to allIncompleteReminders & (reminders in aList whose completed is false)
                end repeat
                
                if count of allIncompleteReminders is greater than 0 then
                    -- Attempt to sort by creation date if possible, or just take the first one found
                    -- Sorting can be complex across all reminder types and versions.
                    -- For simplicity, we'll take the first one as encountered.
                    set firstReminder to item 1 of allIncompleteReminders
                    return name of firstReminder
                else
                    return "No incomplete reminders"
                end if
            on error errMsg number errNum
                return "Error: " & errMsg
            end try
        end tell
        '''
        try:
            process = subprocess.run(
                ['osascript', '-e', apple_script], 
                capture_output=True, 
                text=True,
                check=False # Do not raise an exception for non-zero exit codes
            )
            if process.returncode != 0:
                error_message = process.stderr.strip()
                logging.error(f"AppleScript execution failed with code {process.returncode}: {error_message}")
                return f"Error: Script failed ({process.returncode})"
            
            reminder_text = process.stdout.strip()
            if not reminder_text:
                logging.info("AppleScript returned empty output, assuming no reminders.")
                return "No incomplete reminders" # Or a more specific "Error: Empty Script Output"

            logging.info(f"Successfully fetched reminder: {reminder_text}")
            return reminder_text
            
        except FileNotFoundError:
            logging.error("osascript command not found. This app requires macOS.")
            return "Error: osascript missing"
        except Exception as e:
            logging.error(f"An unexpected error occurred in get_first_reminder: {str(e)}", exc_info=True)
            return "Error: Python exception"
    
    def timed_update(self, _):
        self.update_reminder_display()
    
    def update_reminder_display(self):
        logging.debug("Updating menu bar display")
        reminder_text = self.get_first_reminder()
        
        if reminder_text == "No incomplete reminders":
            self.title = "📝 No reminders"
        elif reminder_text.startswith("Error:"):
            # Display a generic error or part of the error message for brevity
            self.title = "⚠️ Error" 
            logging.warning(f"Displaying error state in menu bar due to: {reminder_text}")
        else:
            # Truncate if too long for menu bar
            max_len = 30 
            display_text = (reminder_text[:max_len] + '...') if len(reminder_text) > max_len else reminder_text
            self.title = f"📝 {display_text}"
        logging.info(f"Menu bar title updated to: {self.title}")

if __name__ == "__main__":
    logging.info("ReminderMenuBarApp starting up")
    # It's good practice to wrap the app run in a try-except for critical errors.
    try:
        app = ReminderMenuBarApp()
        app.run()
    except Exception as e:
        # This will catch errors during app.run() itself, which can be rare with rumps
        # but good for catching unexpected issues.
        logging.critical(f"A critical error occurred: {str(e)}", exc_info=True)
        # Optionally, try to show a native alert if GUI is available
        # rumps.alert("Critical Error", f"The application encountered a critical error and will now close: {str(e)}")
        sys.exit(1)
    logging.info("ReminderMenuBarApp shut down")