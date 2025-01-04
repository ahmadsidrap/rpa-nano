import json
import subprocess
import os

# Define the Executor class
class Executor:

    def execute_command(self, command, target, token_related_target, cmd_data):
        """
        Execute the specified command on the target container.
        """
        data = []
        if command == 'show':
            if target == 'container' or target == 'containers':
                if 'active' in token_related_target:
                    data = self.get_active()
                elif 'inactive' in token_related_target:
                    data = self.get_inactive()
                else:
                    data = self.get_containers()

            elif target == 'volume' or target == 'volumes':
                data = self.get_volumes()

            elif target == 'image' or target == 'images':
                data = self.get_images()
            else:
                raise ValueError(f"Unknown target: {target}")

        elif command == 'down':
            data = self.stop_container(target)

        elif command == 'up':
            data = self.start_container(target)

        elif command == 'copy':
            source = cmd_data["source"]
            path = cmd_data["path"]
            data = self.copy_data(target, source, path)

        else:
            raise ValueError(f"Unknown command: {command}")

        return data
    
    def copy_data(self, target, source, path):
        """
        Copy data from the source container to the target container.
        """
        images = self.get_active(True)

        # Get the source and destination containers
        containerDst = images[f"rpa-{target}"]
        idDst = containerDst["ID"]
        pathSrc = f"./shared/{source}"
        pathDst = f"{idDst}:/{path}"
        subprocess.run(["docker", "cp", pathSrc, pathDst], check=True, capture_output=True, text=True)
        
        return f"File copied from {source} to {target} successfully."
    
    def get_images(self):
        """
        Get the list of Docker images.
        """
        result = subprocess.run(["docker", "image", "ls", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
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
        result = subprocess.run(["docker", "volume", "ls", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
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
        subprocess.run(["docker-compose", "-f", filename, "up", "-d"], check=True)

        return f"Container {name} started successfully."
    
    def stop_container(self, name):
        """
        Stop the specified container.
        """
        # Container path
        container_path = os.getenv('CONTAINER_PATH')
        filename = f"./{container_path}/{name}/docker-compose.yaml"
        subprocess.run(["docker-compose", "-f", filename, "down"], check=True)

        return f"Container {name} started successfully"

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
    
    def get_inactive(self, useKey=False):
        """
        Get the list of inactive (stopped) containers.
        """
        result = subprocess.run(["docker", "ps", "-a", "--filter", "status=exited", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
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