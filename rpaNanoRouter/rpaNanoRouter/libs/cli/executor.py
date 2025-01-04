import json
import subprocess
import os

# Define the Executor class
class Executor:

    debug_mode = False

    def __init__(self):
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

    def subprocess_run(self, command):
        """
        Run a subprocess command.
        """
        check = True
        capture_output = True
        text = True
        if self.debug_mode:
            command_str = ' '.join(command)
            print(f"Execute command: {command_str}")
            return f"Execute command: {command_str}"
        else:
            return subprocess.run(command, check=check, capture_output=capture_output, text=text)

    def execute_command(self, cmd_data):
        """
        Execute the specified command on the target container.
        """
        data = []
        if cmd_data["command"] == 'time':
            data = self.command_date()
        else:
            raise ValueError(f"Unknown command.")
        return data
        
    def command_date(self):
        return self.subprocess_run(['date'])
    
    