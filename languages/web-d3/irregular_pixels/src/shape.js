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

    for (let neighbour of listDirectNeighbours(point)) {
      if (!this.canvasProxy.isPixelBlack(neighbour) && indexOfPointInArray(this.neighbours, neighbour) < 0) {
        this.neighbours.push(neighbour)
      }
    }
  }

  listDirectNeighbours (point) {
    let directNeighbours = []
    if (point.x + 1 < this.canvasProxy.getWidth()) directNeighbours.push({x: point.x + 1, y: point.y})
    if (point.y + 1 < this.canvasProxy.getHeight()) directNeighbours.push({x: point.x, y: point.y + 1})
    if (point.x > 0) directNeighbours.push({x: point.x - 1, y: point.y})
    if (point.y > 0) directNeighbours.push({x: point.x, y: point.y - 1})
    return directNeighbours
  }

  removePoint (point) {
    let pointIndex = indexOfPointInArray(this.points, point)
    if (pointIndex < 0) {
      throw new Error('Trying to remove a point not included in shape')
    }
    this.points.splice(pointIndex, 1)
    this.canvasProxy.setPixelWhite(point)

    for (let neighbour of listDirectNeighbours(point)) {
      let isStillANeighbour = false
      for (let neighbourNeighbour of listDirectNeighbours(neighbour)) {
        if (this.canvasProxy.isPixelBlack(neighbourNeighbour) {
            isStillANeighbour = true
        }
      }
      if (!isStillANeighbour) {
        let neighbourIndex = indexOfPointInArray(this.neighbours, neighbour)
        this.neighbours.splice(neighbourIndex, 1)
      }
    }
    this.neighbours.push(point) // We assume this method is called for a point on an edge of the shape
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
