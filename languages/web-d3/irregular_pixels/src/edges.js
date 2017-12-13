/* TODO: Implementation is plain wrong here:
   - we do not check that the edge is contiguous (no holes)
   - we only check the FIRST edge found, whereas there may be another, longer one
 */

function longestTopEdge (shape) {
  let shapeWidth = shape.rightPoint.x - shape.leftPoint.x + 1
  let shapePointsOnEdge = 0
  for (let i = 0; i < shapeWidth; i++) {
    let pos = {x: shape.leftPoint.x + i, y: shape.topPoint.y}
    if (shape.isPointInShape(pos)) {
      shapePointsOnEdge += 1
    }
  }
  return shapePointsOnEdge
}

function longestBottomEdge (shape) {
  let shapeWidth = shape.rightPoint.x - shape.leftPoint.x + 1
  let shapePointsOnEdge = 0
  for (let i = 0; i < shapeWidth; i++) {
    let pos = {x: shape.leftPoint.x + i, y: shape.bottomPoint.y}
    if (shape.isPointInShape(pos)) {
      shapePointsOnEdge += 1
    }
  }
  return shapePointsOnEdge
}

function longestLeftEdge (shape) {
  let shapehHeight = shape.bottomPoint.y - shape.topPoint.y + 1
  let shapePointsOnEdge = 0
  for (let i = 0; i < shapehHeight; i++) {
    let pos = {x: shape.leftPoint.x, y: shape.topPoint.y + i}
    if (shape.isPointInShape(pos)) {
      shapePointsOnEdge += 1
    }
  }
  return shapePointsOnEdge
}

function longestRightEdge (shape) {
  let shapehHeight = shape.bottomPoint.y - shape.topPoint.y + 1
  let shapePointsOnEdge = 0
  for (let i = 0; i < shapehHeight; i++) {
    let pos = {x: shape.rightPoint.x, y: shape.topPoint.y + i}
    if (shape.isPointInShape(pos)) {
      shapePointsOnEdge += 1
    }
  }
  return shapePointsOnEdge
}

export { longestTopEdge, longestBottomEdge, longestLeftEdge, longestRightEdge }
