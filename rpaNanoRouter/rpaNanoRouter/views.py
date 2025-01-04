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

        status = 200
        data = []
        try:
            data = docker.execute_command(command, target, token_related_target, cmd_data)
        except Exception as e:
            status = 500
            if hasattr(e, 'stderr') and e.stderr:
                data = [{"Error": str(e.stderr)}]
            else:
                data = [{"Error": str(e)}]
        return Response({"data": data}, status=status)