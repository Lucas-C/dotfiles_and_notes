export default [
  {
    name: 'Axial symetry',
    score: 5,
    match: function (shape) { return false } // TODO
  },
  {
    name: 'Rotation by 90° / 180° / 270°',
    score: 4,
    match: function (shape) { return false } // TODO
  },
  {
    name: 'Has an uninterrupted face of length > 2',
    score: 3,
    match: function (shape) { return false } // TODO
  },
  {
    name: 'Has an uninterrupted diagonal of length > 2',
    score: 2,
    match: function (shape) { return false } // TODO
  },
  {
    name: 'Same as 2 previous rules but allowing for discontinuities',
    score: 1,
    match: function (shape) { return false } // TODO
  }
]
