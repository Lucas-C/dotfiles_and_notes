Failed experiment: I wanted to procedurally generate pretty B&W pixelated sprites
by enforcing some rules to **avoid** symmetries.

However a single pixel is often enough to break symmetries,
and hence sprites genereted are quite forgettables.

I guess to go on I would need a broader mathematical definition of the discontinuities
I wanted to generate.

## Run

    npm install

Then open `index.html`

## Design notes

I'm using strings to modelize 2d points in order to benefit from `===` comparison and hence the `Set` data structure.

<!--Tasks:
- finish implementing 1st ruleset
- 1st perfs review seems to point to Set.add as the bottleneck
-->
