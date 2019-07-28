class Answer:
    def __init__(self, *digits_list, position=0):
        self.position = position
        self.lines = [self._digits2line(digits) for digits in digits_list]
        self.index = 0
    def iteration(self, digits):
        self.lines.append(self._digits2line(digits))
        self.index += 1
        target_index = self._find_passage_on_line()
        if self.position < target_index:
            self.position += 1
            return '>'
        elif self.position > target_index:
            self.position -= 1
            return '<'
        return ''
    def _digits2line(self, digits):
        line = ''
        char = '#'
        for digit in digits:
            line += char * digit
            char = ' ' if char == '#' else '#'
        return line
    def _find_passage_on_line(self):
        line = self.lines[self.index]
        i = self.position
        steer_right = True  # False means left
        while i >= 0 and i < len(line):
            if line[i] != '#':
                return i
            if steer_right:
                i = 2 * self.position - i + 1
                steer_right = False
            else:
                i = 2 * self.position - i
                steer_right = True
        # Imminent crash:
        return self.position
