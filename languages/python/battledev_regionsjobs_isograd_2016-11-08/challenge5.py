import math, sys

def local_print(msg): print(msg, file=sys.stderr)

circles = []

class Disc:
    def __init__(self, X, Y, R, H):
        self.X, self.Y, self.R, self.H = X, Y, R, H
        self.parent = None
        self.children = []
        self.total_height = None

    def add(self, disc):
        for child in self.children:
            if child.add(disc):
                return True
        if self.disc_contains(disc):
            disc.parent = self
            self.children.append(disc)
            local_print('disc {} added as child of {}'.format(disc, self))
            return True
        elif disc.disc_contains(self):
            prev_parent = self.parent
            self.parent = disc
            disc.parent = prev_parent
            disc.children.append(self)

            if prev_parent:
                prev_parent.children.remove(self)
                local_print('disc {} added as child of {}'.format(self, disc))
                return True
            else:
                global roots
                roots.remove(self)
                local_print('disc {} added as child of {} which becomes a root'.format(self, disc))
        return False

    def disc_contains(self, disc):
        if self.R < disc.R:
            return False
        d = math.sqrt( (self.X - disc.X)**2 + (self.Y - disc.Y)**2 )
        return d + disc.R < self.R

    def get_top_disc(self, parent_total_height=0, parent_H=0):
        self.total_height = parent_total_height + int(math.fabs(self.H - parent_H))
        if not self.children:
            return self
        top_disc = None
        for child in self.children:
            local_top_disc = child.get_top_disc(self.total_height, self.H)
            if top_disc is None or local_top_disc.total_height > top_disc.total_height:
                top_disc = local_top_disc
        return top_disc

    def __repr__(self):
        return 'Disc: X={} Y={} R={} H={}'.format(self.X, self.Y, self.R, self.H)

N = int(input())
roots = []

for _ in range(N):
    X, Y, R, H = list(map(int, input().split(' ')))
    disc = Disc(X, Y, R, H)
    added = False
    for root_disc in roots:
        if root_disc.add(disc):
            added = True
            break
    if not added:
        local_print('New root: {}'.format(disc))
        roots.append(disc)

top_discs = list(sorted(disc_root.get_top_disc().total_height for disc_root in roots))
local_print('\n'.join(str(d) for d in roots))
local_print(top_discs)
print('{}%'.format(top_discs[-1] + top_discs[-2]))
