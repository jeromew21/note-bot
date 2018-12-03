import numpy as np
import sklearn
from sen_parser import *

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

        quant = get_quantity(sentence)
        func = classify(tokenize(sentence))
        
        if func == -1:
            return "I do not know what you are talking about."
        elif func == 0:
            self.lastCommand = True
            return "What would you like me to note?"
        elif func == 1:
            return self.retrieveNote(quant)
        elif func == 2:
            return self.deleteNote(quant)
        elif func == 3:
            return self.totalNotes()

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
            return "You have no notes."
    
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
