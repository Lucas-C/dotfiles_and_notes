function setCharAtPos (str, character, i) {
  return str.substr(0, i) + character + str.substr(i + character.length)
}

class Shape {
  constructor ({planeWidth, planeHeight}) {
    this.planeWidth = planeWidth
    this.planeHeight = planeHeight
    this.points = new Set()
    this.topPoint = null
    this.bottomPoint = null
    this.leftPoint = null
    this.rightPoint = null
  }

  cloneShape () {
    let shape = new Shape(this)
    shape.points = new Set(this.points)
    return shape
  }

  equals (shape) {
    if (shape.points.size !== this.points.size) return false
    for (var strPoint of shape.points) if (!this.points.has(strPoint)) return false
    return true
  }

  toString () {
    let strShape = ('\n' + ' '.repeat(this.planeWidth)).repeat(this.planeHeight).substr(1)
    for (const strPoint of this.points) {
      let [x, y] = Shape.deserialize(strPoint)
      strShape = setCharAtPos(strShape, 'X', y * (this.planeWidth + 1) + x)
    }
    return '\n' + strShape
  }

  static fromString (strShape) {
    if (strShape.charAt(0) === '\n') {
      strShape = strShape.substr(1)
    }
    let lines = strShape.split('\n')
    let planeHeight = lines.length
    let planeWidth = (strShape.length - (planeHeight - 1)) / planeHeight
    let shape = new Shape({planeWidth, planeHeight})
    for (const [y, line] of lines.entries()) {
      for (let x = 0; x < line.length; x++) {
        if (line[x] === 'X') {
          shape.addPoint({x, y})
        }
      }
    }
    return shape
  }

  static serialize (point) {
    return point.x + ',' + point.y
  }

  static deserialize (pointStr) {
    let [x, y] = pointStr.split(',')
    return [+x, +y]
  }

  isPointInShape (point) {
    return this.points.has(Shape.serialize(point))
  }

  addPoint (point) {
    this.points.add(Shape.serialize(point))
    if (this.topPoint === null) {
      this.topPoint = point
      this.bottomPoint = point
      this.leftPoint = point
      this.rightPoint = point
      return
    }
    if (point.y < this.topPoint.y) {
      this.topPoint = point
    } else if (point.y > this.bottomPoint.y) {
      this.bottomPoint = point
    }
    if (point.x < this.leftPoint.x) {
      this.leftPoint = point
    } else if (point.x > this.rightPoint.x) {
      this.rightPoint = point
    }
  }

  addStrPoint (strPoint) {
    let [x, y] = Shape.deserialize(strPoint)
    this.addPoint({x, y})
  }

  removeStrPoint (point) {
    this.points.delete(point) // If it wasn't in there beforehand, noop
  }
}

export default Shape
