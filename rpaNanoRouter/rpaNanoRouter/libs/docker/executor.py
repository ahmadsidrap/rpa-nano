import json
import subprocess
import os

# Define the Executor class
class Executor:

    debug_mode = False

    def __init__(self):
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

    def subprocess_run(self, command, check=True, capture_output=True, text=True):
        """
        Run a subprocess command.
        """
        if self.debug_mode:
            command_str = ' '.join(command)
            print(f"Execute command: {command_str}")
            return f"Execute command: {command_str}"
        else:
            return subprocess.run(command, check=check, capture_output=capture_output, text=text)

    def execute_command(self, command, target, token_related_target, cmd_data):
        """
        Execute the specified command on the target container.
        """
        data = []
        if command == 'show':
            if target == 'container':
                if any(keyword in token_related_target for keyword in ['active', 'run']):
                    data = self.get_active()
                elif any(keyword in token_related_target for keyword in ['inactive', 'exit']):
                    data = self.get_inactive()
                else:
                    data = self.get_containers()

            elif target == 'volume':
                data = self.get_volumes()

            elif target == 'image':
                data = self.get_images()
            else:
                raise ValueError(f"Unknown target.")

        elif command == 'down':
            data = self.stop_container(target)

        elif command == 'up':
            data = self.start_container(target)

        elif command == 'copy':
            source = cmd_data["source"]
            path = cmd_data["path"]
            data = self.copy_data(target, source, path)

        else:
            raise ValueError(f"Unknown command.")

        return data
    
    def copy_data(self, target, source, path):
        """
        Copy data from the source container to the target container.
        """
        if not self.debug_mode:
            images = self.get_active(True)

            # Get the source and destination containers
            containerDst = images[f"rpa-{target}"]
            idDst = containerDst["ID"]
            pathSrc = f"./shared/{source}"
            pathDst = f"{idDst}:{path}"
        else:
            pathSrc = f"./shared/{source}"
            pathDst = f"{target}:{path}"

        result = self.subprocess_run(["docker", "cp", pathSrc, pathDst], check=True, capture_output=True, text=True)
        if self.debug_mode:
            return result
        
        return f"File copied from {source} to {target} successfully."
    
    def get_images(self):
        """
        Get the list of Docker images.
        """
        result = self.subprocess_run(["docker", "image", "ls", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
        if self.debug_mode and not hasattr(result, 'stdout'):
            return result
        data = [
            {
                "Repository": image["Repository"],
                "Tag": image["Tag"],
                "ID": image["ID"],
                "CreatedSince": image["CreatedSince"],
                "Size": image["Size"]
            }
            for image in (json.loads(line) for line in result.stdout.splitlines())
        ]
        return data
    
    def get_volumes(self):
        """
        Get the list of Docker volumes.
        """
        result = self.subprocess_run(["docker", "volume", "ls", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
        if self.debug_mode and not hasattr(result, 'stdout'):
            return result
        data = [
            {
                "Driver": volume["Driver"],
                "Labels": volume["Labels"],
                "Mountpoint": volume["Mountpoint"],
                "Name": volume["Name"],
                "Scope": volume["Scope"]
            }
            for volume in (json.loads(line) for line in result.stdout.splitlines())
        ]
        return data
    
    def start_container(self, name):
        """
        Start the specified container.
        """
        # Container path
        container_path = os.getenv('CONTAINER_PATH')
        filename = f"./{container_path}/{name}/docker-compose.yaml"
        result = self.subprocess_run(["docker-compose", "-f", filename, "up", "-d"], check=True)
        if self.debug_mode:
            return result

        return f"Container {name} started successfully."
    
    def stop_container(self, name):
        """
        Stop the specified container.
        """
        # Container path
        container_path = os.getenv('CONTAINER_PATH')
        filename = f"./{container_path}/{name}/docker-compose.yaml"
        result = self.subprocess_run(["docker-compose", "-f", filename, "down"], check=True)
        if self.debug_mode:
            return result

        return f"Container {name} started successfully"

    # Get all containers
    def get_containers(self, useKey=False):
        result = self.subprocess_run(["docker", "ps", "-a", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
        if self.debug_mode and not hasattr(result, 'stdout'):
            return result
        if not useKey:
            data = [
                {
                    "ID": container["ID"],
                    "Names": container["Names"],
                    "Networks": container["Networks"],
                    "Image": container["Image"],
                    "CreatedAt": container["CreatedAt"],
                    "Status": container["Status"],
                    "Ports": container["Ports"],
                    "State": container["State"]
                }
                for container in (json.loads(line) for line in result.stdout.splitlines())
            ]
        else:
            data = {
                container["Names"]: {
                    "ID": container["ID"],
                    "Networks": container["Networks"],
                    "Image": container["Image"],
                    "CreatedAt": container["CreatedAt"],
                    "Status": container["Status"],
                    "Ports": container["Ports"],
                    "State": container["State"]
                }
                for container in (json.loads(line) for line in result.stdout.splitlines())
            }
        return data

    # Get active containers
    def get_active(self, useKey=False):
        result = self.subprocess_run(["docker", "ps", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
        if self.debug_mode and not hasattr(result, 'stdout'):
            return result
        if not useKey:
            data = [
                {
                    "ID": container["ID"],
                    "Names": container["Names"],
                    "Networks": container["Networks"],
                    "Image": container["Image"],
                    "CreatedAt": container["CreatedAt"],
                    "Status": container["Status"],
                    "Ports": container["Ports"],
                    "State": container["State"]
                }
                for container in (json.loads(line) for line in result.stdout.splitlines())
            ]
        else:
            data = {
                container["Names"]: {
                    "ID": container["ID"],
                    "Networks": container["Networks"],
                    "Image": container["Image"],
                    "CreatedAt": container["CreatedAt"],
                    "Status": container["Status"],
                    "Ports": container["Ports"],
                    "State": container["State"]
                }
                for container in (json.loads(line) for line in result.stdout.splitlines())
            }
        return data
    
    def get_inactive(self, useKey=False):
        """
        Get the list of inactive (stopped) containers.
        """
        result = self.subprocess_run(["docker", "ps", "-a", "--filter", "status=exited", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
        if self.debug_mode and not hasattr(result, 'stdout'):
            return result
        if not useKey:
            data = [
                {
                    "ID": container["ID"],
                    "Names": container["Names"],
                    "Networks": container["Networks"],
                    "Image": container["Image"],
                    "CreatedAt": container["CreatedAt"],
                    "Status": container["Status"],
                    "Ports": container["Ports"],
                    "State": container["State"]
                }
                for container in (json.loads(line) for line in result.stdout.splitlines())
            ]
        else:
            data = {
                container["Names"]: {
                    "ID": container["ID"],
                    "Networks": container["Networks"],
                    "Image": container["Image"],
                    "CreatedAt": container["CreatedAt"],
                    "Status": container["Status"],
                    "Ports": container["Ports"],
                    "State": container["State"]
                }
                for container in (json.loads(line) for line in result.stdout.splitlines())
            }
        return data