import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from .libs.docker.executor import Executor as Docker
from .libs.docker.nlp import Nlp
    
class RpaNlp(APIView):
    def post(self, request):
        """
        Process the input text using spaCy.
        """
        # Load NLP library
        nlp = Nlp()
        
        # Get the text from the request
        message = request.data.get("message", None)
        # Process the text
        command, target, token_related_target, cmd_data = nlp.process_command(message)
        print("Command:", command, "Target:", target, "Tokens:", token_related_target, "Data: ", cmd_data)

        docker = Docker()

        data = []
        try:
            data = docker.execute_command(command, target, token_related_target, cmd_data)
        except subprocess.CalledProcessError as e:
            return Response({"message": "Error", "error": str(e.stderr)}, status=500)
        return Response({"message": "Success", "data": data})