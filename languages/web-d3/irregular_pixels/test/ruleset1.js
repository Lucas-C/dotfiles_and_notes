/* eslint-disable camelcase */
import test from 'ava'
import Shape from '../src/shape'
import ruleset1 from '../src/ruleset1'
import { DIAMOND_5x5, ONLY_DIAGS } from './utils/figures'

test.skip('A diamond matches 3 rules among 5', t => {
  let shape = Shape.fromString(DIAMOND_5x5)
  t.true(ruleset1[0].match(shape))
  t.true(ruleset1[1].match(shape))
  t.false(ruleset1[2].match(shape))
  t.true(ruleset1[3].match(shape))
  t.false(ruleset1[4].match(shape))
})

test.skip('There is a Shape only matching the long diagonals rule', t => {
  let shape = Shape.fromString(ONLY_DIAGS)
  t.false(ruleset1[0].match(shape))
  t.false(ruleset1[1].match(shape))
  t.false(ruleset1[2].match(shape))
  t.true(ruleset1[3].match(shape))
  t.false(ruleset1[4].match(shape))
})
