import Shape from './shape'

function mirrorHorizontally (shape) {
  let mirrorAxeYDoubled = shape.topPoint.y + shape.bottomPoint.y
  let mirrorShape = new Shape(shape) // only copies dimensions
  for (const strPoint of shape.points) {
    let [x, y] = Shape.deserialize(strPoint)
    mirrorShape.addPoint({x: x, y: mirrorAxeYDoubled - y})
  }
  return mirrorShape
}

function mirrorVertically (shape) {
  let mirrorAxeXDoubled = shape.leftPoint.x + shape.rightPoint.x
  let mirrorShape = new Shape(shape) // only copies dimensions
  for (const strPoint of shape.points) {
    let [x, y] = Shape.deserialize(strPoint)
    mirrorShape.addPoint({x: mirrorAxeXDoubled - x, y: y})
  }
  return mirrorShape
}

function mirrorTopLeftDiagonal (shape) {
  let center = {x: (shape.leftPoint.x + shape.rightPoint.x) / 2, y: (shape.topPoint.y + shape.bottomPoint.y) / 2}
  let mirrorShape = new Shape(shape) // only copies dimensions
  for (const strPoint of shape.points) {
    let [x, y] = Shape.deserialize(strPoint)
    mirrorShape.addPoint({x: center.x + (y - center.y), y: center.y + (x - center.x)})
  }
  return mirrorShape
}

function mirrorTopRightDiagonal (shape) {
  let center = {x: (shape.leftPoint.x + shape.rightPoint.x) / 2, y: (shape.topPoint.y + shape.bottomPoint.y) / 2}
  let mirrorShape = new Shape(shape) // only copies dimensions
  for (const strPoint of shape.points) {
    let [x, y] = Shape.deserialize(strPoint)
    mirrorShape.addPoint({x: center.x - (y - center.y), y: center.y - (x - center.x)})
  }
  return mirrorShape
}

function rotateQuarter (shape) {
  let center = {x: (shape.leftPoint.x + shape.rightPoint.x) / 2, y: (shape.topPoint.y + shape.bottomPoint.y) / 2}
  let rotatedShape = new Shape(shape) // only copies dimensions
  for (const strPoint of shape.points) {
    let [x, y] = Shape.deserialize(strPoint)
    rotatedShape.addPoint({x: center.x - (y - center.y), y: center.y + (x - center.x)})
  }
  return rotatedShape
}

function rotateQuarterInvert (shape) {
  let center = {x: (shape.leftPoint.x + shape.rightPoint.x) / 2, y: (shape.topPoint.y + shape.bottomPoint.y) / 2}
  let rotatedShape = new Shape(shape) // only copies dimensions
  for (const strPoint of shape.points) {
    let [x, y] = Shape.deserialize(strPoint)
    rotatedShape.addPoint({x: center.x + (y - center.y), y: center.y - (x - center.x)})
  }
  return rotatedShape
}

function centralSymmetry (shape) {
  let center = {x: (shape.leftPoint.x + shape.rightPoint.x) / 2, y: (shape.topPoint.y + shape.bottomPoint.y) / 2}
  let rotatedShape = new Shape(shape) // only copies dimensions
  for (const strPoint of shape.points) {
    let [x, y] = Shape.deserialize(strPoint)
    rotatedShape.addPoint({x: center.x - (x - center.x), y: center.y - (y - center.y)})
  }
  return rotatedShape
}

export { mirrorHorizontally, mirrorVertically, mirrorTopLeftDiagonal, mirrorTopRightDiagonal, rotateQuarter, rotateQuarterInvert, centralSymmetry }
