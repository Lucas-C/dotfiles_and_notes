/* TODO: Implementation is plain wrong here:
   - we do not check that the diagonal is contiguous (no holes)
   - we only check the FIRST diagonal found, whereas there may be another, longer one
 */

function longestTopLeftDiagonal (shape) {
  let diagonalLength = 1
  while (true) {
    let yStartPos = shape.topPoint.y + diagonalLength - 1
    let shapePointsOnDiagonal = 0
    for (let i = 0; i < diagonalLength; i++) {
      let pos = {x: shape.leftPoint.x + i, y: yStartPos - i}
      if (shape.isPointInShape(pos)) {
        shapePointsOnDiagonal += 1
      }
    }
    if (shapePointsOnDiagonal > 0) {
      return shapePointsOnDiagonal
    }
    diagonalLength += 1
  }
}

function longestTopRightDiagonal (shape) {
  let diagonalLength = 1
  while (true) {
    let yStartPos = shape.topPoint.y + diagonalLength - 1
    let shapePointsOnDiagonal = 0
    for (let i = 0; i < diagonalLength; i++) {
      let pos = {x: shape.rightPoint.x - i, y: yStartPos - i}
      if (shape.isPointInShape(pos)) {
        shapePointsOnDiagonal += 1
      }
    }
    if (shapePointsOnDiagonal > 0) {
      return shapePointsOnDiagonal
    }
    diagonalLength += 1
  }
}

function longestBottomLeftDiagonal (shape) {
  let diagonalLength = 1
  while (true) {
    let yStartPos = shape.bottomPoint.y - diagonalLength + 1
    let shapePointsOnDiagonal = 0
    for (let i = 0; i < diagonalLength; i++) {
      let pos = {x: shape.leftPoint.x + i, y: yStartPos + i}
      if (shape.isPointInShape(pos)) {
        shapePointsOnDiagonal += 1
      }
    }
    if (shapePointsOnDiagonal > 0) {
      return shapePointsOnDiagonal
    }
    diagonalLength += 1
  }
}

function longestBottomRightDiagonal (shape) {
  let diagonalLength = 1
  while (true) {
    let yStartPos = shape.bottomPoint.y - diagonalLength + 1
    let shapePointsOnDiagonal = 0
    for (let i = 0; i < diagonalLength; i++) {
      let pos = {x: shape.rightPoint.x - i, y: yStartPos + i}
      if (shape.isPointInShape(pos)) {
        shapePointsOnDiagonal += 1
      }
    }
    if (shapePointsOnDiagonal > 0) {
      return shapePointsOnDiagonal
    }
    diagonalLength += 1
  }
}

export { longestTopLeftDiagonal, longestTopRightDiagonal, longestBottomLeftDiagonal, longestBottomRightDiagonal }
