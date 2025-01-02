import json
import subprocess
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .libs.docker import Docker

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
        docker = Docker()
        data = docker.get_active()
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
    
# Copy data
class RpaCopy(APIView):
    def get(self, request):
        # Get active containers
        docker = Docker()
        data = docker.get_active(True)

        # Get the source and destination containers
        container = request.query_params.get("container", None)
        source = request.query_params.get("src", None)
        destination = request.query_params.get("dst", None)
        containerDst = data[f"rpa-{container}"]
        idDst = containerDst["ID"]
        pathSrc = f"./shared/{source}"
        pathDst = f"{idDst}:/{destination}"

        try:
            # Copy the data
            subprocess.run(["docker", "cp", pathSrc, pathDst], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            return Response({"message": "Error", "error": str(e.stderr)}, status=500)

        data = {
            "destination": containerDst["ID"],
        }
        return Response({"message": "Success", "data": data})