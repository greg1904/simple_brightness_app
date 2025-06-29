from util.DisplayCapability import DisplayCapability

class DisplayCapabilities:
    INITIAL_VAL = "NIL"

    def __init__(self):
        self.dictionary = {}
    
    def add_capability(self, capability : DisplayCapability, code : str):
        self.dictionary.update({capability.value : { "code" : code, "minValue" : self.INITIAL_VAL, "maxValue" : self.INITIAL_VAL, "currentValue" : self.INITIAL_VAL, "actualValue" : self.INITIAL_VAL }})
