Note: Sadly, I cannot find the original challenge on codingame.com :(
All I remember is that it was a blackbox puzzle where all you had was text inputs/outputs, and a final "Game Over" message.
And I loved it ;)

**Ideas / next steps / WIP**:

- make hero able to beat AI: `python AnswerRunner.py level0.txt ia_exploring_and_chasing.py`
- strengthen `AutonomousRunner.py` unit tests so that `zipapp.sh` "black box mode" never crashes unexpectedly
- make `hero_ghostcloseby.py` functions aware of walls so that the hero does not fear ghosts behind them
- build other levels
- guess CodingGame scoring


# Runner usage

    ./AutonomousRunner.py

# Black box enigma

    ./zipapp.sh

# Conventions

- INIT: Y X Z
- Per-round: a b c d & coords


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
