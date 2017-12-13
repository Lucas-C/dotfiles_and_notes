export default [
  {
    name: 'Axial symetry',
    score: 5,
    match: function {shapePoints, shapeNeighbours}() { return false }
  },
  {
    name: 'Rotation by 90° / 180° / 270°',
    score: 4,
    match: function ({shapePoints, shapeNeighbours}) { return false }
  },
  {
    name: 'Has an uninterrupted face of length > 2',
    score: 3,
    match: function ({shapePoints, shapeNeighbours}) { return false }
  },
  {
    name: 'Has an uninterrupted diagonal of length > 2',
    score: 2,
    match: function ({shapePoints, shapeNeighbours}) { return false }
  },
  {
    name: 'Same as 2 previous rules but allowing for discontinuities',
    score: 1,
    match: function ({shapePoints, shapeNeighbours}) { return false }
  }
]
