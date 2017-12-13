import Shape from './shape'

class ShapeWithNeigbours extends Shape {
  constructor ({planeWidth, planeHeight}) {
    super({planeWidth, planeHeight})
    this.neighbours = new Set()
  }

  cloneShapeWithNeigbours () {
    let shape = super.clone()
    shape.neighbours = new Set(this.neighbours)
    return shape
  }

  addPoint (point) {
    super.addPoint(point)

    this.neighbours.delete(Shape.serialize(point)) // If it wasn't in there beforehand, noop

    for (const neighbour of this.listDirectNeighbours(point)) {
      if (!this.isPointInShape(neighbour)) {
        this.neighbours.add(Shape.serialize(neighbour))
      }
    }
  }

  listDirectNeighbours ({x, y}) {
    let directNeighbours = []
    if (x + 1 < this.planeWidth) directNeighbours.push({x: x + 1, y: y})
    if (y + 1 < this.planeHeight) directNeighbours.push({x: x, y: y + 1})
    if (x > 0) directNeighbours.push({x: x - 1, y: y})
    if (y > 0) directNeighbours.push({x: x, y: y - 1})
    return directNeighbours
  }

  removeStrPoint (strPoint) {
    super.removeStrPoint(strPoint)
    let [x, y] = Shape.deserialize(strPoint)

    for (const neighbour of this.listDirectNeighbours({x, y})) {
      let isStillANeighbour = false
      for (const neighbourNeighbour of this.listDirectNeighbours(neighbour)) {
        if (this.isPointInShape(neighbourNeighbour)) {
          isStillANeighbour = true
        }
      }
      if (!isStillANeighbour) {
        this.neighbours.delete(Shape.serialize(neighbour))
      }
    }
    this.neighbours.add(strPoint) // We assume this method is called for a point on an edge of the shape
  }
}

export default ShapeWithNeigbours
