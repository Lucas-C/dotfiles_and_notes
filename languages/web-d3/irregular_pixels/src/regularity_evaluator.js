import ruleset1 from './ruleset1'

export default class {
  constructor (rulesetName) {
    if (rulesetName !== 'ruleset1') {
      throw new Error('Unknown rulset: ' + rulesetName)
    }
    this.ruleset = ruleset1
  }
  computeFor (point) {
    return 0
  }
}
