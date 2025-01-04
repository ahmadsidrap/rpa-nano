import spacy

class Nlp:

    def __init__(self):
        # Load the spaCy English language model
        self.nlp = spacy.load("en_core_web_sm")

    def process_text(self, text):
        """
        Process the input text and extract noun phrases, verbs, and named entities.
        """
        doc = self.nlp(text)
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
        entities = [(entity.text, entity.label_) for entity in doc.ents]
        return noun_phrases, verbs, entities

    def process_command(self, text):
        """
        Process the input text and extract the command, target, and related tokens
        """
        # Parse the text using spaCy
        doc = self.nlp(text.lower())

        # Find the root verb of the sentence
        command = None
        for token in doc:
            print("Analyze tokens:", token.text, token.pos_, token.dep_, token.head.text)
            # Check for named entities
            if token.text == 'show' and token.dep_ == 'ROOT':
                command = token.text

        # Find the noun chunks in the sentence
        target = None
        token_related_target = []
        if command == 'show':
            for token in doc:
                # Check for nouns related to the root verb
                if token.pos_ == 'NOUN' and token.head.text == command:
                    target = token.text
                    break
            
            # Find the tokens related to the target noun
            for token in doc:
                if token.head.text == target:
                    token_related_target.append(token.text)

        return command, target, token_related_target
