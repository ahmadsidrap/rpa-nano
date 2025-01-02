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
        subprocess.run(["docker", "ps"], check=True)
        result = subprocess.run(["docker", "ps", "--format", "{{json .}}"], check=True, capture_output=True, text=True)
        data = [json.loads(line) for line in result.stdout.splitlines()]
        return Response({"message": "Success", "data": data})