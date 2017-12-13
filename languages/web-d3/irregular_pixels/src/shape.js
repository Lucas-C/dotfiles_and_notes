function pointStr2Tuple (pointStr) {
  let [x, y] = pointStr.split(',')
  return [+x, +y]
}

export default class {
  constructor ({canvasProxy, startingPoint}) {
    this.canvasProxy = canvasProxy
    this.points = new Set()
    this.neighbours = new Set()
    this.addPoint(startingPoint)
  }

  addPoint (point) {
    this.points.add(point)
    let [x, y] = pointStr2Tuple(point)
    this.canvasProxy.setPixelBlack({x, y})

    this.neighbours.delete(point) // If it wasn't in there beforehand, noop

    for (let neighbour of this.listDirectNeighbours({x, y})) {
      if (!this.canvasProxy.isPixelBlack(neighbour)) {
        let neighbourStr = neighbour.x + ',' + neighbour.y
        this.neighbours.add(neighbourStr)
      }
    }
  }

  cloneSetsWithPoint (point) {
    let shapePoints = new Set(this.points)
    shapePoints.add(point)

    let shapeNeighbours = new Set(this.neighbours)
    shapeNeighbours.delete(point) // If it wasn't in there beforehand, noop

    let [x, y] = pointStr2Tuple(point)
    for (let neighbour of this.listDirectNeighbours({x, y})) {
      if (!this.canvasProxy.isPixelBlack(neighbour)) {
        let neighbourStr = neighbour.x + ',' + neighbour.y
        shapeNeighbours.add(neighbourStr)
      }
    }

    return {shapePoints, shapeNeighbours}
  }

  listDirectNeighbours ({x, y}) {
    let directNeighbours = []
    if (x + 1 < this.canvasProxy.width) directNeighbours.push({x: x + 1, y: y})
    if (y + 1 < this.canvasProxy.height) directNeighbours.push({x: x, y: y + 1})
    if (x > 0) directNeighbours.push({x: x - 1, y: y})
    if (y > 0) directNeighbours.push({x: x, y: y - 1})
    return directNeighbours
  }

  removePoint (point) {
    this.points.delete(point) // If it wasn't in there beforehand, noop
    let [x, y] = pointStr2Tuple(point)
    this.canvasProxy.setPixelWhite({x, y})

    for (let neighbour of this.listDirectNeighbours({x, y})) {
      let isStillANeighbour = false
      for (let neighbourNeighbour of this.listDirectNeighbours(neighbour)) {
        if (this.canvasProxy.isPixelBlack(neighbourNeighbour)) {
          isStillANeighbour = true
        }
      }
      if (!isStillANeighbour) {
        let neighbourStr = neighbour.x + ',' + neighbour.y
        this.neighbours.delete(neighbourStr)
      }
    }
    this.neighbours.add(point) // We assume this method is called for a point on an edge of the shape
  }

  isOnCanvasEdge () {
    let [width, height] = [this.canvasProxy.width, this.canvasProxy.height]
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
