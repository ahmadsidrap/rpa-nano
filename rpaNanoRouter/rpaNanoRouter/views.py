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
        cmd_data = nlp.process_command(message)

        docker = Docker()
        status = 200
        data = []
        try:
            data = docker.execute_command(cmd_data)
            if isinstance(data, str):
                data = [{"Output": data}]
        except Exception as e:
            status = 500
            if hasattr(e, 'stderr') and e.stderr:
                data = [{"Error": str(e.stderr)}]
            else:
                data = [{"Error": str(e)}]
        return Response({"data": data}, status=status)