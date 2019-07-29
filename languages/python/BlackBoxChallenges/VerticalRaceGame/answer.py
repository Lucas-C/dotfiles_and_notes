from collections import defaultdict


class Answer:
    def __init__(self, *digits_list, position=0):
        self.position = position
        self.lines = [_digits2line(digits) for digits in digits_list]
        self.index = 1

    def iteration(self, digits):
        self.lines.append(_digits2line(digits))
        self.index += 1
        _, target_index = self._find_best_move_on_line(self.index, [self.position])
        if target_index is None:
            return ''
        if self.position < target_index:
            self.position += 1
            return '>'
        elif self.position > target_index:
            self.position -= 1
            return '<'
        return ''

    def _find_best_move_on_line(self, line_index, positions):
        # positions = prev line
        # passages  = next line
        # moves     = link between them: passage -> position
        line = self.lines[line_index]
        moves = _moves_from(line, positions)
        passages = list(moves.keys())
        if not passages:
            return (None, positions[0])  # end line or imminent crash
        picked_passage = passages[0]
        if len(passages) > 1:
            # Recursing to consider next lines:
            if line_index + 1 < len(self.lines):
                picked_passage, _ = self._find_best_move_on_line(line_index + 1, passages)
                if picked_passage is None:
                    return (None, None)
            else:
                # Last line in sight and still cannot choose ? Pick the most central position:
                picked_passage = _most_central(passages, middle_pos=len(line)/2)
        return (_most_central(moves[picked_passage], middle_pos=len(line)/2), picked_passage)

def _digits2line(digits):
    line = ''
    char = '#'
    for digit in digits:
        line += char * digit
        char = ' ' if char == '#' else '#'
    return line

def _moves_from(line, positions):
    moves = defaultdict(list)
    for pos in positions:
        for next_pos in (pos - 1, pos, pos + 1):
            if next_pos >= 0 and next_pos < len(line) and line[next_pos] == ' ':
                moves[next_pos].append(pos)
    return moves

def _most_central(indices, middle_pos):
    return sorted(indices, key=lambda i: abs(i - middle_pos))[0]
