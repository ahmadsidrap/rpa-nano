import spacy
import os

class Nlp:

    # Command dictionary to map the root verb to the command tokens
    command_dictionary = {
        "show": ["show", "display", "list", "get", "obtain", "view", "fetch"],
        "up": ["start", "run", "begin", "launch"],
        "down": ["shut", "stop"],
        "copy": ["copy", "transfer"],
    }

    # Inverted dictionary to map the command tokens to the root verb
    command_map = {}

    def __init__(self, debug_test=False):
        # Load the environment variables
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        self.debug_test = debug_test

        # Load the spaCy English language model
        self.nlp = spacy.load("en_core_web_sm")

        # Indexing command dictionary
        self.command_map = self.command_dictionary_index()
    
    def command_dictionary_index(self):
        """
        Create an inverted dictionary to map the command tokens to the root verb
        """
        inverted_dict = {}
        for key, values in self.command_dictionary.items():
            for value in values:
                inverted_dict[value] = key
        return inverted_dict

    def process_command(self, text):
        """
        Process the input text and extract the command, target, and related tokens
        """
        # Parse the text using spaCy
        doc = self.nlp(text.lower())
        data = {
            'command': None,
            'related_tokens': [],
            'source': None,
            'target': None,
        }

        # Check for specific phrases
        for token in doc:
            print("text:", token.text, ", pos:", token.pos_, ", dep:", token.dep_, ", head:", token.head.text)

        # Check for what type of question
        command = self.parse_what(doc)
        if command:
            data["command"] = command
            return data
        
        # Check for who type of question
        command = self.parse_who(doc)
        if command:
            data['command'] = 'show'
            data['target'] = 'container'
            data['related_tokens'] = ['active']
            return data
        
        return data
    
    def parse_who(self, doc):
        """
        Parse the "who" question type
        """
        # Define the pattern for matching questions
        pattern = [{"POS": "PRON"}, {"POS": "AUX"}, {"POS": "PRON"}]
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add("WhoQuery", [pattern])

        # Apply the matcher to the doc
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            print("Matched span:", span.text)
        return False
    
    def parse_what(self, doc):
        """
        Parse the "what" question type
        """
        # Define the pattern for matching questions
        pattern = [{"POS": "DET"}, {"POS": "NOUN"}, {"POS": "AUX", "OP": "?"}, {"POS": "ADV"}]
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add("TimeQuery", [pattern])

        # Apply the matcher to the doc
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            print("Matched span:", span.text)
            for token in span:
                if token.pos_ == "NOUN":
                    print("Noun found:", token.text)
                    return token.text
        return False
    
    def get_connected_token_until_similar(self, doc, token):
        """
        Get connected tokens
        """
        str = ''
        for next_token in doc[token.i+1:]:
            str += next_token.text
            if next_token.head.text == token.text:
                break
        return str
