import ruleset1 from './ruleset1'

export default class {
  constructor (rulesetName) {
    if (rulesetName !== 'ruleset1') {
      throw new Error('Unknown rulset: ' + rulesetName)
    }
    this.ruleset = ruleset1
  }

  computeFor ({growingShape, point}) {
    let shape = growingShape.cloneShape()
    shape.addStrPoint(point)
    let score = 0
    for (const rule of this.ruleset) {
      if (rule.match(shape)) {
        score = rule.score
        break
      }
    }
    return score
  }
}
