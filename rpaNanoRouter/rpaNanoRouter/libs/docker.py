import json
import subprocess

# Define the Docker class
class Docker:
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