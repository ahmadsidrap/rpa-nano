import json
import subprocess
import os

# Define the Docker class
class Docker:

    def execute_command(self, command, target, token_related_target):
        """
        Execute the specified command on the target container.
        """
        data = []
        if (command == 'show' and (target == 'container' or target == 'containers')):
            if 'active' in token_related_target:
                data = self.get_active()
            else:
                data = self.get_containers()

        elif command == 'down':
            data = self.stop_container(target)

        elif command == 'up':
            data = self.start_container(target)
        return data
    
    def start_container(self, name):
        """
        Start the specified container.
        """
        # Container path
        container_path = os.getenv('CONTAINER_PATH')
        filename = f"./{container_path}/{name}/docker-compose.yaml"
        subprocess.run(["docker-compose", "-f", filename, "up", "-d"], check=True)
        return True
    
    def stop_container(self, name):
        """
        Stop the specified container.
        """
        # Container path
        container_path = os.getenv('CONTAINER_PATH')
        filename = f"./{container_path}/{name}/docker-compose.yaml"
        subprocess.run(["docker-compose", "-f", filename, "down"], check=True)
        return True

    # Get all containers
    def get_containers(self, useKey=False):
        result = subprocess.run(["docker", "ps", "-a", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
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
        result = subprocess.run(["docker", "ps", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
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