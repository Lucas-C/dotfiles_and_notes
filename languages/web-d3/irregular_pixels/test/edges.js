/* eslint-disable camelcase */
import test from 'ava'
import Shape from '../src/shape'
import { longestTopEdge, longestBottomEdge, longestLeftEdge, longestRightEdge } from '../src/edges'
import { DUAL_FIG_4x4_IN_6x6, RECTANGLE_3x5 } from './utils/figures'

test('Longest top edge of a 4x4 shape', t => {
  t.is(longestTopEdge(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)), 2)
})

test('Longest top edge of a rectangle shape', t => {
  t.is(longestTopEdge(Shape.fromString(RECTANGLE_3x5)), 3)
})

test('Longest bottom edge of 4x4 shape', t => {
  t.is(longestBottomEdge(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)), 2)
})

test('Longest bottom edge of a rectangle shape', t => {
  t.is(longestBottomEdge(Shape.fromString(RECTANGLE_3x5)), 3)
})

test('Longest left edge of 4x4 shape', t => {
  t.is(longestLeftEdge(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)), 2)
})

test('Longest left edge of a rectangle shape', t => {
  t.is(longestLeftEdge(Shape.fromString(RECTANGLE_3x5)), 5)
})

test('Longest right edge of 4x4 shape', t => {
  t.is(longestRightEdge(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)), 2)
})

test('Longest right edge of a rectangle shape', t => {
  t.is(longestRightEdge(Shape.fromString(RECTANGLE_3x5)), 5)
})
