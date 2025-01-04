import datetime
import json
import subprocess
import os

# Define the Executor class
class Executor:

    debug_mode = False

    def __init__(self):
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        self.container_id = os.getenv('CONTAINER_ID', '')

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
            commands = ['docker', 'exec', '-ti', self.container_id]
            commands.extend(command)
            result = subprocess.run(commands, check=check, capture_output=capture_output, text=text)
            # result = subprocess.run(command, check=check, capture_output=capture_output, text=text)
            return result.stdout

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
        # Get the current date and time
        date_string = self.subprocess_run(['date']).strip()
        timezone_string = self.subprocess_run(['date', '+%Z']).strip()
        # Convert to datetime object
        dt_object = datetime.datetime.strptime(date_string, "%a %b %d %H:%M:%S UTC %Y")

        # Format as desired
        formatted_date = dt_object.strftime(f"%Y-%m-%d %H:%M:%S {timezone_string}")
        return formatted_date
    
    