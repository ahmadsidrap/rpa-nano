import subprocess
import os
from rest_framework.views import APIView
from rest_framework.response import Response

class RpaUp(APIView):
    
    def get(self, request):
        # Read path parameters
        app_name = request.query_params.get("app_name", None)
        filename = f"./containers/{app_name}/docker-compose.yaml"
        subprocess.run(["docker-compose", "-f", filename, "up", "-d"], check=True)
        return Response({"message": "Hello, world!"})

class RpaDown(APIView):
    
    def get(self, request):
        app_name = request.query_params.get("app_name", None)
        filename = f"./containers/{app_name}/docker-compose.yaml"
        subprocess.run(["docker-compose", "-f", filename, "down"], check=True)
        return Response({"message": "Hello, world!"})