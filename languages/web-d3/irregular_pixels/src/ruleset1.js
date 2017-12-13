import { mirrorHorizontally, mirrorVertically, mirrorTopLeftDiagonal, mirrorTopRightDiagonal, rotateQuarter, rotateQuarterInvert, centralSymmetry } from './symmetries'
// import { longestTopEdge, longestBottomEdge, longestLeftEdge, longestRightEdge } from './edges'
// import { longestTopLeftDiagonal, longestTopRightDiagonal, longestBottomLeftDiagonal, longestBottomRightDiagonal } from './diagonals'

export default [
  {
    name: 'Axial symetry',
    score: 0,
    match: function (shape) {
      return mirrorHorizontally(shape).equals(shape) || mirrorVertically(shape).equals(shape) || mirrorTopLeftDiagonal(shape).equals(shape) || mirrorTopRightDiagonal(shape).equals(shape)
    }
  },
  {
    name: 'Rotation by 90° / 180° / 270°',
    score: 1,
    match: function (shape) {
      return rotateQuarter(shape).equals(shape) || rotateQuarterInvert(shape).equals(shape) || centralSymmetry(shape).equals(shape)
    }
  },
  {
    name: 'Has an uninterrupted face of length > 2',
    score: 2,
    match: function (shape) {
      return false // longestTopEdge(shape) > 2 || longestBottomEdge(shape) > 2 || longestLeftEdge(shape) > 2 || longestRightEdge(shape) > 2
    }
  },
  {
    name: 'Has an uninterrupted diagonal of length > 2',
    score: 3,
    match: function (shape) {
      return false // longestTopLeftDiagonal(shape) > 2 || longestTopRightDiagonal(shape) > 2 || longestBottomLeftDiagonal(shape) > 2 || longestBottomRightDiagonal(shape) > 2
    }
  },
  {
    name: 'Same as 2 previous rules but allowing for discontinuities',
    score: 4,
    match: function (shape) { return false } // TODO
  }
]
