
    npm install

Then open `index.html`

## Design notes

I'm using strings to modelize 2 points in order to benefit from `===` comparison and hence the `Set` data structure.

<!--Tasks:
- 1st perfs review seems to point to Set.add as the bottleneck
- implement 1st ruleset
-->