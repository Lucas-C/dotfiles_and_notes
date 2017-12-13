import test from 'ava'
import Shape from '../src/shape'
import MockCanvasProxy from './mocks/canvas_proxy'

test('A new Shape at the center of a 3x3 canvas is not on its edge', t => {
  let canvasProxy = new MockCanvasProxy({width: 3, height: 3})
  let startingPoint = canvasProxy.getCenter()
  let shape = new Shape({canvasProxy, startingPoint})
  t.false(shape.isOnCanvasEdge())
})

test('A new Shape in a 2x2 canvas is on its edge', t => {
  let canvasProxy = new MockCanvasProxy({width: 2, height: 2})
  let startingPoint = canvasProxy.getCenter()
  let shape = new Shape({canvasProxy, startingPoint})
  t.true(shape.isOnCanvasEdge())
})

test('A new Shape in a 3x3 canvas has 4 neighbours', t => {
  let canvasProxy = new MockCanvasProxy({width: 3, height: 3})
  let startingPoint = canvasProxy.getCenter()
  let shape = new Shape({canvasProxy, startingPoint})
  t.deepEqual(shape.neighbours, [
    {x: 2, y: 1},
    {x: 1, y: 2},
    {x: 0, y: 1},
    {x: 1, y: 0}
  ])
})

let arrayOfPointsSorter = function (a, b) {
  if (a.x !== b.x) return a.x > b.x ? 1 : -1
  if (a.y !== b.y) return a.y > b.y ? 1 : -1
  return 0
}

test('A length-3 vertical Shape in a 3x3 canvas has 6 neighbours', t => {
  let canvasProxy = new MockCanvasProxy({width: 3, height: 3})
  let startingPoint = canvasProxy.getCenter()
  let shape = new Shape({canvasProxy, startingPoint})
  shape.addPoint({x: 1, y: 0})
  shape.addPoint({x: 1, y: 2})
  t.deepEqual(shape.neighbours.sort(arrayOfPointsSorter), [
    {x: 0, y: 0},
    {x: 0, y: 1},
    {x: 0, y: 2},
    {x: 2, y: 0},
    {x: 2, y: 1},
    {x: 2, y: 2}
  ].sort(arrayOfPointsSorter))
})
