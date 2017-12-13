import Shape from './shape'

export default class extends Shape {
  constructor ({canvasProxy, startingPoint}) {
    super({planeWidth: canvasProxy.width, planeHeight: canvasProxy.height, startingPoint: null})
    this.canvasProxy = canvasProxy
    this.addPoint(startingPoint) // To ensure setPixelBlack is called
  }

  isPointInShape (point) {
    return this.canvasProxy.isPixelBlack(point)
  }

  addPoint (point) {
    super.addPoint(point)
    let [x, y] = Shape.pointStr2Tuple(point)
    this.canvasProxy.setPixelBlack({x, y})
  }

  removePoint (point) {
    super.removePoint(point)
    let [x, y] = Shape.pointStr2Tuple(point)
    this.canvasProxy.setPixelWhite({x, y})
  }

  isOnCanvasEdge () { // Complexity: O(2*(width+height))
    for (let i = 0; i < this.planeWidth; i += 1) {
      if (this.canvasProxy.isPixelBlack({x: i, y: 0}) || this.canvasProxy.isPixelBlack({x: i, y: this.planeHeight - 1})) {
        return true
      }
    }
    for (let j = 0; j < this.planeHeight; j += 1) {
      if (this.canvasProxy.isPixelBlack({x: 0, y: j}) || this.canvasProxy.isPixelBlack({x: this.planeWidth - 1, y: j})) {
        return true
      }
    }
    return false
  }
}
