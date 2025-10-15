class Parser:
    def __init__(self):
        self.stack = []
        self.buffer = []

    # move word from buffer to stack
    def shift(self, word):
        self.stack.append(word)

    # combine elements of current stack to a phrase
    def reduce(self):
        if len(self.stack) >= 2:
            phrase = (self.stack.pop(), self.stack.pop())  # Example of forming a phrase
            self.stack.append(phrase)

    # parse algorithm (no control rules)
    def parse(self, words):
        self.buffer = words
        while self.buffer:
            self.shift(self.buffer.pop(0))  # always shift (!TOO GENERAL!)

        while len(self.stack) > 1:
            self.reduce()  # always reduce (!TOO GENERAL!)

        return self.stack

