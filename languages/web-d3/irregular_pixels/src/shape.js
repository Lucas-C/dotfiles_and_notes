class Shape {
  constructor ({planeWidth, planeHeight, startingPoint}) {
    this.planeWidth = planeWidth
    this.planeHeight = planeHeight
    this.points = new Set()
    this.neighbours = new Set()
    if (startingPoint) {
      this.addPoint(startingPoint)
    }
  }

  static pointStr2Tuple (pointStr) {
    let [x, y] = pointStr.split(',')
    return [+x, +y]
  }

  isPointInShape (point) {
    return this.points.has(point.x + ',' + point.y)
  }

  addPoint (point) {
    this.points.add(point)
    let [x, y] = Shape.pointStr2Tuple(point)

    this.neighbours.delete(point) // If it wasn't in there beforehand, noop

    for (let neighbour of this.listDirectNeighbours({x, y})) {
      if (!this.isPointInShape(neighbour)) {
        let neighbourStr = neighbour.x + ',' + neighbour.y
        this.neighbours.add(neighbourStr)
      }
    }
  }

  cloneShape (point) {
    let shape = new Shape({planeWidth: this.planeWidth, planeHeight: this.planeHeight, startingPoint: this.startingPoint})
    shape.points = new Set(this.points)
    shape.neighbours = new Set(this.neighbours)
    return shape
  }

  listDirectNeighbours ({x, y}) {
    let directNeighbours = []
    if (x + 1 < this.planeWidth) directNeighbours.push({x: x + 1, y: y})
    if (y + 1 < this.planeHeight) directNeighbours.push({x: x, y: y + 1})
    if (x > 0) directNeighbours.push({x: x - 1, y: y})
    if (y > 0) directNeighbours.push({x: x, y: y - 1})
    return directNeighbours
  }

  removePoint (point) {
    this.points.delete(point) // If it wasn't in there beforehand, noop
    let [x, y] = Shape.pointStr2Tuple(point)

    for (let neighbour of this.listDirectNeighbours({x, y})) {
      let isStillANeighbour = false
      for (let neighbourNeighbour of this.listDirectNeighbours(neighbour)) {
        if (this.isPointInShape(neighbourNeighbour)) {
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
}
export default Shape
