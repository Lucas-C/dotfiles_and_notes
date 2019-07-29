import random, string


class Answer:
    def __init__(self, *args, **kwargs):
        pass
    def iteration(self, *args, **kwargs):
        return random.choice(string.printable)
