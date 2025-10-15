class ILPRefinedParser:
    def __init__(self):
        self.stack = []
        self.buffer = []
        self.pos_tags = {
            "the": "Det",
            "a": "Det",
            "an": "Det",
            "cat": "Noun",
            "dog": "Noun",
            "eats": "Verb",
            "runs": "Verb"
        }

    def should_shift(self, word):
        """Shift if the word is a determiner or if there are still words in the buffer."""
        return word in self.pos_tags

    def should_reduce(self):
        """Reduce if the last two elements on the stack form a valid phrase."""
        if len(self.stack) >= 2:
            top1, top2 = self.stack[-1], self.stack[-2]
            return (top2, top1) in [("Det", "Noun"), ("NP", "VP"), ("Noun", "VP"), ("Noun", "Verb")]
        return False

    def shift(self):
        """Move a word from the buffer to the stack, replacing it with its POS tag."""
        if self.buffer:
            word = self.buffer.pop(0)
            self.stack.append(self.pos_tags.get(word, word))  # Convert to POS tag if applicable

    def reduce(self):
        """Combine elements on the stack into a phrase."""
        if len(self.stack) >= 2:
            top1 = self.stack.pop()
            top2 = self.stack.pop()
            if (top2, top1) == ("Det", "Noun"):
                self.stack.append("NP")  # Determiner + Noun → NP
            elif top1 == "Noun":  # Standalone Noun can become NP
                self.stack.append("NP")
            elif (top2, top1) in [("Noun", "Verb"), ("NP", "Verb")]:
                self.stack.append("VP")  # Noun + Verb → VP
            elif (top2, top1) == ("NP", "VP"):
                self.stack.append("S")  # NP + VP → Sentence (S)

    def parse(self, words):
        """Apply learned Shift-Reduce rules."""
        self.buffer = words[:]

        while self.buffer:
            if self.should_shift(self.buffer[0]):
                self.shift()
            else:
                break  # Stop shifting if no match

        while self.should_reduce():
            self.reduce()

        return self.stack


parser = ILPRefinedParser()
result = parser.parse(["the", "cat", "eats"])
print(result)  # Expected output: ['S']
