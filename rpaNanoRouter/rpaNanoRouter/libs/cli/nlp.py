import spacy
import os

class Nlp:

    # Inverted dictionary to map the command tokens to the root verb
    command_map = {}

    def __init__(self, debug_test=False):
        # Load the environment variables
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        self.debug_test = debug_test

        # Load the spaCy English language model
        self.nlp = spacy.load("en_core_web_sm")

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
            data["type"] = "what"
            data["command"] = command
            return data
        
        # Check for auxiliary verbs
        command = self.parse_auxiliary(doc)
        if command:
            data["type"] = "auxiliary"
            data["command"] = command
            return data
        
        # Check for command type
        verb, noun, target, related_tokens = self.parse_command(doc)
        if verb is not None:
            data["type"] = "command"
            data["command"] = verb
            data["object"] = noun
            data["target"] = target
            data["related_tokens"] = related_tokens
            return data
        
        # Check for who type of question
        command = self.parse_who(doc)
        if command:
            data["type"] = "who"
            data['command'] = 'show'
            data['target'] = 'container'
            data['related_tokens'] = ['active']
            return data
        
        return data
    
    def parse_command(self, doc):
        """
        Parse the command tokens
        """
        # Define the pattern for matching questions
        pattern1 = [{"POS": "VERB"}, {"POS": "PRON", "OP": "?"}, {"POS": "DET", "OP": "?"}, {"POS": "ADJ", "OP": "?"}, {"POS": "NOUN"}]
        pattern2 = [{"POS": "VERB"}, {"POS": "PRON", "OP": "?"}, {"POS": "DET", "OP": "?"}, {"POS": "ADJ", "OP": "?"}, {"POS": "PROPN"}]
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add("CommandQuery", [pattern1, pattern2])

        # Apply the matcher to the doc
        verb = None
        adjectives = []
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            print("Matched span:", span.text)
            for token in span:
                if token.pos_ == "VERB":
                    print("Verb found:", token.text)
                    verb = token.lemma_
                if token.pos_ == "ADJ":
                    print("Adjective found:", token.text)
                    adjectives.append(token.lemma_)
                if token.pos_ == "NOUN" or token.pos_ == "PROPN":
                    print("Noun found:", token.text)
                    target = ''.join([t.text for t in doc[token.i+1:]])
                    return verb, token.lemma_, target, adjectives

        return None, None, None, None
    
    def parse_auxiliary(self, doc):
        """
        Parse the auxiliary verbs
        """
        # Define the pattern for matching questions
        pattern = [{"POS": "NOUN"}, {"POS": "ADV", "OP": "?"}, {"POS": "AUX"}, {"POS": "PUNCT", "OP": "?"}]
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add("AuxQuery", [pattern])

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
