import ShapeWithNeigbours from './shape_with_neighbours'

export default class extends ShapeWithNeigbours {
  constructor (canvasProxy) {
    super({planeWidth: canvasProxy.width, planeHeight: canvasProxy.height})
    this.canvasProxy = canvasProxy
  }

  cloneCanvasShape () {
    let shape = super.clone()
    shape.canvasProxy = this.canvasProxy
    return shape
  }

  isPointInShape (point) { // Override because faster: O(1)
    return this.canvasProxy.isPixelBlack(point)
  }

  addPoint (point) {
    super.addPoint(point)
    this.canvasProxy.setPixelBlack(point)
  }

  removeStrPoint (strPoint) {
    super.removeStrPoint(strPoint)
    let [x, y] = ShapeWithNeigbours.deserialize(strPoint)
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
