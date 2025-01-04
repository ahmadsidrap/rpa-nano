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

    def process_text(self, text):
        """
        Process the input text and extract noun phrases, verbs, and named entities.
        """
        doc = self.nlp(text)
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
        entities = [(entity.text, entity.label_) for entity in doc.ents]
        return noun_phrases, verbs, entities
    
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

        # Find the root verb of the sentence
        command = None
        original_command_word = None
        for token in doc:
            if self.debug_mode or self.debug_test:
                print("text:", token.text, ", pos:", token.pos_, ", dep:", token.dep_, ", head:", token.head.text)
            
            # Check for named entities
            if token.text in self.command_map:
                original_command_word = token.text
                command = self.command_map[token.text]

        # Find the noun chunks in the sentence
        target = None
        token_related_target = []
        data = {}

        # If the command is 'show', find the target noun and related tokens
        if command == 'show':
            for token in doc:
                # Check for nouns related to the root verb
                if token.pos_ == 'NOUN' and token.head.text == original_command_word and token.dep_ != 'ROOT':
                    target = token.lemma_
                    break
                elif token.dep_ == 'ROOT' and token.head.text != token.text:
                    target = token.lemma_
                    break

        elif command == 'up' or command == 'down':
            has_punct = False
            for token in doc:
                # Check for punctuation marks
                if token.pos_ == 'PUNCT':
                    has_punct = True
                    target = token.head.text
                # Check for nouns related to the root verb
                # Response to command: "stop container: x"
                if has_punct and token.head.text == original_command_word:
                    target = token.text
                # Reponse to command: "stop container x"
                elif not has_punct and token.pos_ == 'NOUN' and token.head.text == original_command_word:
                    target = token.text

        elif command == 'copy':
            data["source"] = None

            for token in doc:
                # Source
                if token.dep_ in {'advmod', 'oprd', 'appos', 'npadvmod'} and token.head.text == original_command_word:
                    data["source"] = token.text
                elif data['source'] is None and token.pos_ == 'ADP' and token.dep_ == 'prep' and token.head.text == original_command_word: # Response to /x/x/x/x
                    data["source"] = self.get_connected_token_until_similar(doc, token)

                # Get the path
                elif token.pos_ == 'PUNCT' and token.head.text == original_command_word:
                    data["path"] = token.text
                elif token.pos_ == 'PUNCT' and token.head.text == 'in': # Reponse to /x/x/x/x
                    data["path"] = doc[token.i:].text
                    break

                if token.pos_ == 'NOUN' and token.head.pos_ == "ADP" and token.head.head.text == original_command_word:
                    target = token.text
            
        if command is not None:
            # Find the tokens related to the target noun
            for token in doc:
                if token.head.lemma_ == target:
                    token_related_target.append(token.lemma_)

        if self.debug_mode or self.debug_test:
            print("Command:", command, "Target:", target, "Tokens:", token_related_target, "Data: ", data)

        return command, target, token_related_target, data
    
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
