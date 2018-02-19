Note: Sadly, I cannot find the original challenge on codingame.com :(
All I remember is that it was a blackbox puzzle where all you had was text inputs/outputs, and a final "Game Over" message.

TODO:
- make `py.test hero_explorerinstinct.py` pass in order to have proper exploration logic
- guess CodingGame scoring
- take a glance at Cygwin mkfifo code


# Runner usage

    mkfifo fifo0 fifo1; ./Runner.py level0.txt ia_exploring_and_chasing.py > fifo0 < fifo1 & ./Answer.py < fifo0 > fifo1

Alt:

    (coproc ./Runner.py level0.txt ia_exploring_and_chasing.py; eval "exec ./Answer.py <&${COPROC[0]} >&${COPROC[1]}")

Note: this does not seem to run properly under Cygwin.


# Conventions

INIT: Y X Z
Per-round: a b c d & coords


# Deductions

- Per-round input quartets are always either "#" or "_" chars
- The number of rounds depends on my output char
- The last list of value at each round looks like coordinates in X / Y: lets name it `coords`
- `coords` seem to move to another "tile" by one in X or Y each round
- Moves:
  * A => droite (x croissant)
  * B => immobile
  * C => haut (y décroissant)
  * D => bas (y croissant)
  * E => gauche (x décroissant)
- Obstacles: neighbours = [a, b, c, d]
  * a => obstacle above (y - 1)
  * b => obstacle on the right (x + 1)
  * c => obstacle below (y + 1)
  * d => obstacle on the left (x - 1)
- the player character is the last `coords`
