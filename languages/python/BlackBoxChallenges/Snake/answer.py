class Answer:
    def __init__(self, size):
        self.size = size
        self.last_head = None
    def iteration(self, *snake, coin=None):
        dir = ''
        head = snake[0]
        if self.last_head:
            direction = head[0] - self.last_head[0], head[1] - self.last_head[1]
            x, y = head[0] + 2*direction[0], head[1] + 2*direction[1]
            if x < 0 or x >= self.size or y < 0 or y >= self.size:
                dir = '>'
        self.last_head = head            
        return dir
