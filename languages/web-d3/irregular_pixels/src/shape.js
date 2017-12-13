let indexOfPointInArray = function (array, needle) {
  return array.findIndex(point => point.x === needle.x && point.y === needle.y)
}

export default class {
  constructor ({canvasProxy, startingPoint}) {
    this.canvasProxy = canvasProxy
    this.points = []
    this.neighbours = []
    this.addPoint(startingPoint)
  }

  addPoint (point) {
    this.points.push(point)
    this.canvasProxy.setPixelBlack(point)

    let neighbourIndex = indexOfPointInArray(this.neighbours, point)
    if (neighbourIndex >= 0) {
      this.neighbours.splice(neighbourIndex, 1)
    }
    let directNeighbours = []
    if (point.x + 1 < this.canvasProxy.getWidth()) directNeighbours.push({x: point.x + 1, y: point.y})
    if (point.y + 1 < this.canvasProxy.getHeight()) directNeighbours.push({x: point.x, y: point.y + 1})
    if (point.x > 0) directNeighbours.push({x: point.x - 1, y: point.y})
    if (point.y > 0) directNeighbours.push({x: point.x, y: point.y - 1})
    for (let neighbour of directNeighbours) {
      if (indexOfPointInArray(this.points, neighbour) < 0 && indexOfPointInArray(this.neighbours, neighbour) < 0) {
        this.neighbours.push(neighbour)
      }
    }
  }

  isOnCanvasEdge () {
    let [width, height] = [this.canvasProxy.getWidth(), this.canvasProxy.getHeight()]
    for (let i = 0; i < width; i += 1) {
      if (this.canvasProxy.isPixelBlack({x: i, y: 0}) || this.canvasProxy.isPixelBlack({x: i, y: height - 1})) {
        return true
      }
    }
    for (let j = 0; j < height; j += 1) {
      if (this.canvasProxy.isPixelBlack({x: 0, y: j}) || this.canvasProxy.isPixelBlack({x: width - 1, y: j})) {
        return true
      }
    }
    return false
  }
}
