import Shape from './shape'
import RegularityEvaluator from './regularity_evaluator'

export default function ({canvasProxy, ruleset}) {
  let regularityEvaluator = new RegularityEvaluator(ruleset)
  let startingPoint = canvasProxy.getCenter()
  let growingShape = new Shape({canvasProxy, startingPoint})
  while (!growingShape.isOnCanvasEdge()) {
    let minScore = Infinity
    let minScorePoint
    for (let point of growingShape.neighbours) {
      let score = regularityEvaluator.computeFor(shape, point)
      if (score < minScore) {
        minScore = score
        minScorePoint = point
      }
    }
    console.log('Adding point to Shape: minScore=', minScore, 'minScorePoint=', minScorePoint)
    growingShape.addPoint(minScorePoint)
  }
}
