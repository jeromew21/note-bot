import numpy as np
import sklearn
from sen_parser import *
import random

class Conversation:

    def __init__(self):
        '''
        The init function: Here, you should load any
        PyTorch models / word vectors / etc. that you
        have previously trained.
        '''
        self.notes = []
        self.lastCommand = False

    def respond(self, sentence):
        '''
        This is the only method you are required to support
        for the Conversation class. This method should accept
        some input from the user, and return the output
        from the chatbot.
        '''
        if self.lastCommand:
            self.lastCommand = False
            self.takeNote(sentence)
            return "Note taken."

        tokens = tokenize(sentence)

        quant = get_quantity(sentence)
        func = classify(tokens)
        sass = ""
        if "please" in sentence.split(" "):
            sass = " " + random.choice(("Thank you for saying please. So rare these days.", "", "You're very, very welcome."))
        else:
            sass = " " + random.choice(("Also, what happened to common courtesy?", "", "Also, what's the magic word?"))
        
        if func == -1:
            return "I do not know what you are talking about. " + random.choice(("Please speaka English.", "Are you deaf?", "Are you four years old?"))
        elif func == 0:
            self.lastCommand = True
            return "What would you like me to note?" + sass
        elif func == 1:
            return self.retrieveNote(quant) + sass
        elif func == 2:
            return self.deleteNote(quant) + sass
        elif func == 3:
            return self.totalNotes() + sass

        return sentence

    def takeNote(self, sentence):
        self.notes.append(sentence)  

    def retrieveNote(self, q):
        if self.notes:
            if q == -1 or q is None:
                return "Your last note was: " + self.notes[-1]
            if q <= 0 or q > len(self.notes):
                return "I do not have that many notes!"
            return "Your {0} note was: ".format(q-1) + self.notes[q-1]
        else:
            return "You have no notes. " + random.choice(("", "It's empty, just like your mind."))
    
    def deleteNote(self, q):
        if self.notes:
            if q == -1 or q is None:
                return "Deleted " + self.notes.pop()
            if q <= 0 or q > len(self.notes):
                return "I do not have that many notes!"
            return "Deleted " + self.notes.pop(q-1)
        else:
            return "You have no notes to delete."

    def totalNotes(self):
        return "You have " + str(len(self.notes)) + " notes."
