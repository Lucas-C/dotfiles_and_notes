import CanvasShape from './canvas_shape'
import RegularityEvaluator from './regularity_evaluator'

export default function ({canvasProxy, ruleset}) {
  let regularityEvaluator = new RegularityEvaluator(ruleset)
  let startingPoint = canvasProxy.getCenter()
  let growingShape = new CanvasShape({canvasProxy, startingPoint})
  let statsPointsPerScore = {}
  while (!growingShape.isOnCanvasEdge()) {
    let minScore = Infinity
    let minScorePoint
    for (let point of growingShape.neighbours) {
      let score = regularityEvaluator.computeFor({growingShape, point})
      if (score < minScore) {
        minScore = score
        minScorePoint = point
      }
    }
    growingShape.addPoint(minScorePoint)
    statsPointsPerScore[minScore] += 1
  }
  console.log('Points picked per score level:', statsPointsPerScore)
}
