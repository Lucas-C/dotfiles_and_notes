import ruleset1 from './ruleset1'

export default class {
  constructor (rulesetName) {
    if (rulesetName !== 'ruleset1') {
      throw new Error('Unknown rulset: ' + rulesetName)
    }
    this.ruleset = ruleset1
  }

  computeFor (shape, point) {
    let score = 0
    shape.addPoint(point)
    for (let rule of this.ruleset) {
        if (rule.match(shape)) {
            score = rule.score
            break
        }
    }
    shape.removePoint(point)
    return score
  }
}
