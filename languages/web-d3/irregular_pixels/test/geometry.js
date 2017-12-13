import test from 'ava'
import Shape from '../src/shape'
import { mirrorHorizontally, mirrorVertically } from '../src/geometry'
import { DUAL_FIG_4x4_IN_4x4, DUAL_FIG_4x4_IN_6x6 } from './figures'

test('Horizontal mirror of a 4x4 shape in a 4x4 plane', t => {
  t.is(mirrorHorizontally(Shape.fromString(DUAL_FIG_4x4_IN_4x4.A)).toString(), DUAL_FIG_4x4_IN_4x4.B)
  t.is(mirrorHorizontally(Shape.fromString(DUAL_FIG_4x4_IN_4x4.B)).toString(), DUAL_FIG_4x4_IN_4x4.A)
})

test('Vertical mirror of a 4x4 shape in a 4x4 plane', t => {
  t.is(mirrorVertically(Shape.fromString(DUAL_FIG_4x4_IN_4x4.A)).toString(), DUAL_FIG_4x4_IN_4x4.B)
  t.is(mirrorVertically(Shape.fromString(DUAL_FIG_4x4_IN_4x4.B)).toString(), DUAL_FIG_4x4_IN_4x4.A)
})

test('Horizontal mirror of a 4x4 shape in a 5x5 plane', t => {
  console.log('5x5 plane')
  t.is(mirrorHorizontally(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.B)
  t.is(mirrorHorizontally(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.A)
})

test('Vertical mirror of a 4x4 shape in a 5x5 plane', t => {
  console.log('5x5 plane')
  t.is(mirrorVertically(Shape.fromString(DUAL_FIG_4x4_IN_6x6.A)).toString(), DUAL_FIG_4x4_IN_6x6.B)
  t.is(mirrorVertically(Shape.fromString(DUAL_FIG_4x4_IN_6x6.B)).toString(), DUAL_FIG_4x4_IN_6x6.A)
})
