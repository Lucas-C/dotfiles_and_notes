import CanvasShape from './canvas_shape'
import RegularityEvaluator from './regularity_evaluator'

export default function ({canvasProxy, ruleset}) {
  let regularityEvaluator = new RegularityEvaluator(ruleset)
  let growingShape = new CanvasShape(canvasProxy)
  growingShape.addPoint(canvasProxy.getCenter())
  let statsPointsPerScore = {}
  while (!growingShape.isOnCanvasEdge()) {
    let minScore = Infinity
    let minScorePoint
    for (const point of growingShape.neighbours) {
      let score = regularityEvaluator.computeFor({growingShape, point})
      if (score < minScore) {
        minScore = score
        minScorePoint = point
      }
    }
    growingShape.addStrPoint(minScorePoint)
    statsPointsPerScore[minScore] = (statsPointsPerScore[minScore] || 0) + 1
  }
  console.log('Points picked per score level:', statsPointsPerScore)
}
