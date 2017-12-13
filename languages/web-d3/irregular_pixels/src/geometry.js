import Shape from './shape'

function mirrorHorizontally (shape) {
  let mirrorAxeYDoubled = (shape.topPoint.y + shape.bottomPoint.y)
  let mirrorShape = new Shape(shape) // only copies dimensions
  for (const strPoint of shape.points) {
    let [x, y] = Shape.deserialize(strPoint)
    mirrorShape.addPoint({x: x, y: mirrorAxeYDoubled - y})
  }
  return mirrorShape
}

function mirrorVertically (shape) {
  let mirrorAxeXDoubled = (shape.leftPoint.x + shape.rightPoint.x)
  let mirrorShape = new Shape(shape) // only copies dimensions
  for (const strPoint of shape.points) {
    let [x, y] = Shape.deserialize(strPoint)
    mirrorShape.addPoint({x: mirrorAxeXDoubled - x, y: y})
  }
  return mirrorShape
}

export { mirrorHorizontally, mirrorVertically }
