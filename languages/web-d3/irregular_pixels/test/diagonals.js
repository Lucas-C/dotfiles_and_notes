/* eslint-disable camelcase */
import test from 'ava'
import Shape from '../src/shape'
import { longestTopLeftDiagonal, longestTopRightDiagonal, longestBottomLeftDiagonal, longestBottomRightDiagonal } from '../src/diagonals'
import { DUAL_FIG_4x4_IN_6x6, DIAMOND_4x4, DIAMOND_5x5 } from './utils/figures'

test('Longest top-left diagonal of a 4x4 shape', t => {
  t.is(longestTopLeftDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)), 3)
  t.is(longestTopLeftDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)), 1)
})

test('Longest top-left diagonal of a diamond shape', t => {
  t.is(longestTopLeftDiagonal(Shape.fromString(DIAMOND_4x4)), 2)
  t.is(longestTopLeftDiagonal(Shape.fromString(DIAMOND_5x5)), 3)
})

test('Longest top-right diagonal of 4x4 shape', t => {
  t.is(longestTopRightDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)), 1)
  t.is(longestTopRightDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)), 3)
})

test('Longest top-right diagonal of a diamond shape', t => {
  t.is(longestTopRightDiagonal(Shape.fromString(DIAMOND_4x4)), 2)
  t.is(longestTopRightDiagonal(Shape.fromString(DIAMOND_5x5)), 3)
})

test('Longest bottom-left diagonal of 4x4 shape', t => {
  t.is(longestBottomLeftDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)), 1)
  t.is(longestBottomLeftDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)), 3)
})

test('Longest bottom-left diagonal of a diamond shape', t => {
  t.is(longestBottomLeftDiagonal(Shape.fromString(DIAMOND_4x4)), 2)
  t.is(longestBottomLeftDiagonal(Shape.fromString(DIAMOND_5x5)), 3)
})

test('Longest bottom-right diagonal of 4x4 shape', t => {
  t.is(longestBottomRightDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)), 3)
  t.is(longestBottomRightDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)), 1)
})

test('Longest bottom-right diagonal of a diamond shape', t => {
  t.is(longestBottomRightDiagonal(Shape.fromString(DIAMOND_4x4)), 2)
  t.is(longestBottomRightDiagonal(Shape.fromString(DIAMOND_5x5)), 3)
})
