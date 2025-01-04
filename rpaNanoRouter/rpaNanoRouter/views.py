import json
import subprocess
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .libs.docker import Docker
from .libs.nlp import Nlp

# Start the container
class RpaUp(APIView):
    
    def get(self, request):
        # Container path
        container_path = os.getenv('CONTAINER_PATH')
        # Read path parameters
        app_name = request.query_params.get("app_name", None)
        filename = f"./{container_path}/{app_name}/docker-compose.yaml"
        try:
            subprocess.run(["docker-compose", "-f", filename, "up", "-d"], check=True)
        except subprocess.CalledProcessError as e:
            return Response({"message": "Error", "error": str(e.stderr)}, status=500)
        return Response({"message": "Success"})

# Shut down the container
class RpaDown(APIView):
    def get(self, request):
        # Container path
        container_path = os.getenv('CONTAINER_PATH')
        # Read app_name parameter
        app_name = request.query_params.get("app_name", None)
        filename = f"./{container_path}/{app_name}/docker-compose.yaml"
        try:
            subprocess.run(["docker-compose", "-f", filename, "down"], check=True)
        except subprocess.CalledProcessError as e:
            return Response({"message": "Error", "error": str(e.stderr)}, status=500)
        return Response({"message": "Success"})

# Get all containers
class RpaContainer(APIView):
    def get(self, request):
        data = []
        try:
            data = Docker().get_containers()
        except subprocess.CalledProcessError as e:
            return Response({"message": "Error", "error": str(e.stderr)}, status=500)
        return Response({"message": "Success", "data": data})

# Get active containers
class RpaActive(APIView):
    def get(self, request):
        data = []
        try:
            data = Docker().get_active()
        except subprocess.CalledProcessError as e:
            return Response({"message": "Error", "error": str(e.stderr)}, status=500)
        return Response({"message": "Success", "data": data})

# Get images
class RpaImage(APIView):
    def get(self, request):
        data = []
        try:
            data = Docker().get_images()
        except subprocess.CalledProcessError as e:
            return Response({"message": "Error", "error": str(e.stderr)}, status=500)
        return Response({"message": "Success", "data": data})

# Get volumes
class RpaVolume(APIView):
    def get(self, request):
        data = []
        try:
            data = Docker().get_volumes()
        except subprocess.CalledProcessError as e:
            return Response({"message": "Error", "error": str(e.stderr)}, status=500)
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
    
class RpaNlp(APIView):
    def get(self, request):
        """
        Process the input text using spaCy.
        """
        # Load NLP library
        nlp = Nlp()
        
        # Get the text from the request
        message = request.query_params.get("msg", None)
        # Process the text
        command, target, token_related_target = nlp.process_command(message)
        print("Command:", command, "Target:", target, "Tokens:", token_related_target)

        docker = Docker()

        data = []
        try:
            data = docker.execute_command(command, target, token_related_target)
        except subprocess.CalledProcessError as e:
            return Response({"message": "Error", "error": str(e.stderr)}, status=500)
        return Response({"message": "Success", "data": data})