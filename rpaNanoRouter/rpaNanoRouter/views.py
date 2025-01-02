import json
import subprocess
import os
from rest_framework.views import APIView
from rest_framework.response import Response

# Start the container
class RpaUp(APIView):
    
    def get(self, request):
        # Read path parameters
        app_name = request.query_params.get("app_name", None)
        filename = f"./containers/{app_name}/docker-compose.yaml"
        subprocess.run(["docker-compose", "-f", filename, "up", "-d"], check=True)
        return Response({"message": "Success"})

# Shut down the container
class RpaDown(APIView):
    def get(self, request):
        app_name = request.query_params.get("app_name", None)
        filename = f"./containers/{app_name}/docker-compose.yaml"
        subprocess.run(["docker-compose", "-f", filename, "down"], check=True)
        return Response({"message": "Success"})

# Get active containers
class RpaActive(APIView):
    def get(self, request):
        result = subprocess.run(["docker", "ps", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
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
        return Response({"message": "Success", "data": data})

# Get images
class RpaImage(APIView):
    def get(self, request):
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
        return Response({"message": "Success", "data": data})

# Get volumes
class RpaVolume(APIView):
    def get(self, request):
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
        return Response({"message": "Success", "data": data})