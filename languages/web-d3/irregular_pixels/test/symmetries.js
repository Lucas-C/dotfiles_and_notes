/* eslint-disable camelcase */
import test from 'ava'
import Shape from '../src/shape'
import { mirrorHorizontally, mirrorVertically, mirrorTopLeftDiagonal, mirrorTopRightDiagonal, rotateQuarter, rotateQuarterInvert, centralSymmetry } from '../src/symmetries'
import { DUAL_FIG_4x4_IN_4x4, DUAL_FIG_4x4_IN_6x6 } from './utils/figures'

test('Horizontal mirror of a 4x4 shape in a 4x4 plane', t => {
  t.is(mirrorHorizontally(Shape.fromString(DUAL_FIG_4x4_IN_4x4.A)).toString(), DUAL_FIG_4x4_IN_4x4.B)
  t.is(mirrorHorizontally(Shape.fromString(DUAL_FIG_4x4_IN_4x4.B)).toString(), DUAL_FIG_4x4_IN_4x4.A)
})

test('Horizontal mirror of a 4x4 shape in a 6x6 plane', t => {
  t.is(mirrorHorizontally(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.B)
  t.is(mirrorHorizontally(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.A)
})

test('Vertical mirror of a 4x4 shape in a 6x6 plane', t => {
  t.is(mirrorVertically(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.B)
  t.is(mirrorVertically(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.A)
})

test('Vertical mirror of a 4x4 shape in a 4x4 plane', t => {
  t.is(mirrorVertically(Shape.fromString(DUAL_FIG_4x4_IN_4x4.A)).toString(), DUAL_FIG_4x4_IN_4x4.B)
  t.is(mirrorVertically(Shape.fromString(DUAL_FIG_4x4_IN_4x4.B)).toString(), DUAL_FIG_4x4_IN_4x4.A)
})

test('Top-left diagonal mirror of a 4x4 shape in a 6x6 plane', t => {
  t.is(mirrorTopLeftDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.A)
  t.is(mirrorTopLeftDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.B)
})

test('Top-left diagonal mirror of a 4x4 shape in a 6x6 plane', t => {
  t.is(mirrorTopLeftDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.A)
  t.is(mirrorTopLeftDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.B)
})

test('Top-right diagonal mirror of a 4x4 shape in a 6x6 plane', t => {
  t.is(mirrorTopRightDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.A)
  t.is(mirrorTopRightDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.B)
})

test('Top-right diagonal mirror of a 4x4 shape in a 6x6 plane', t => {
  t.is(mirrorTopRightDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.A)
  t.is(mirrorTopRightDiagonal(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.B)
})

test('90° rotation of a 4x4 shape in a 4x4 plane', t => {
  t.is(rotateQuarter(Shape.fromString(DUAL_FIG_4x4_IN_4x4.A)).toString(), DUAL_FIG_4x4_IN_4x4.B)
  t.is(rotateQuarter(Shape.fromString(DUAL_FIG_4x4_IN_4x4.B)).toString(), DUAL_FIG_4x4_IN_4x4.A)
})

test('90° rotation of a 4x4 shape in a 6x6 plane', t => {
  t.is(rotateQuarter(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.B)
  t.is(rotateQuarter(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.A)
})

test('270° rotation of a 4x4 shape in a 4x4 plane', t => {
  t.is(rotateQuarterInvert(Shape.fromString(DUAL_FIG_4x4_IN_4x4.A)).toString(), DUAL_FIG_4x4_IN_4x4.B)
  t.is(rotateQuarterInvert(Shape.fromString(DUAL_FIG_4x4_IN_4x4.B)).toString(), DUAL_FIG_4x4_IN_4x4.A)
})

test('270° rotation of a 4x4 shape in a 6x6 plane', t => {
  t.is(rotateQuarterInvert(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.B)
  t.is(rotateQuarterInvert(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.A)
})

test('Central symmetry of a 4x4 shape in a 4x4 plane', t => {
  t.is(centralSymmetry(Shape.fromString(DUAL_FIG_4x4_IN_4x4.A)).toString(), DUAL_FIG_4x4_IN_4x4.A)
  t.is(centralSymmetry(Shape.fromString(DUAL_FIG_4x4_IN_4x4.B)).toString(), DUAL_FIG_4x4_IN_4x4.B)
})

test('Central symmetry of a 4x4 shape in a 6x6 plane', t => {
  t.is(centralSymmetry(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.A)
  t.is(centralSymmetry(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.B)
})
