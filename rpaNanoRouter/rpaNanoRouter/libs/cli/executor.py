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
            if isinstance(command, str):
                command = command.split()
            commands = ['docker', 'exec', '-ti', self.container_id]
            commands.extend(command)
            result = subprocess.run(commands, check=check, capture_output=capture_output, text=text)
            # result = subprocess.run(command, check=check, capture_output=capture_output, text=text)
            if result.returncode == 0:
                return result.stdout
            else:
                raise ValueError(result.stderr)

    def execute_command(self, cmd_data):
        """
        Execute the specified command on the target container.
        """
        data = []
        if cmd_data["command"] == 'time':
            data = self.command_date()
        elif cmd_data["command"] == 'enter':
            data = self.command_enter_container(cmd_data["target"])
        elif cmd_data["command"] == 'user':
            data = self.command_user()
        elif cmd_data["command"] == 'show':
            if 'current' in cmd_data["related_tokens"]:
                data = self.command_current_directory()
            else:
                data = self.command_current_dirs(cmd_data["target"])
        else:
            raise ValueError(f"Unknown command: {cmd_data['command']}")
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
    
    def command_current_directory(self):
        # Get the current directory
        directory = self.subprocess_run(['pwd']).strip()
        return directory
    
    def command_current_dirs(self, path = None):
        # Get the current directory
        if path is None:
            path = "."
        else:
            path = f"./{path}"
        output = self.subprocess_run(["find", path, "-mindepth", "1", "-maxdepth", "1", "-type", "d", "-print0"]).strip()

        # Process the output into JSON array
        directories = output.strip('\0').split('\0')[:-1]  # Remove trailing empty element
        return directories
    
    def command_enter_container(self, path):
        # Enter the specified container
        output = self.subprocess_run(['/bin/sh', '-c', 'cd', path, '&&', "find", ".", "-mindepth", "1", "-maxdepth", "1", "-type", "d", "-print0"])
        return output
    
    def command_user(self):
        # Get the current user
        user = self.subprocess_run(['whoami']).strip()
        return user
    
    