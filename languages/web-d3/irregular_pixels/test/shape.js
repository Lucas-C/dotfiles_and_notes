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

test('A point has 4 direct neighbours', t => {
  let canvasProxy = new MockCanvasProxy({width: 3, height: 3})
  let startingPoint = canvasProxy.getCenter()
  let shape = new Shape({canvasProxy, startingPoint})
  t.deepEqual(shape.listDirectNeighbours({x: 1, y: 1}), [
    {x: 2, y: 1},
    {x: 1, y: 2},
    {x: 0, y: 1},
    {x: 1, y: 0}
  ])
})

test('A length-3 vertical Shape in a 3x3 canvas has 6 neighbours', t => {
  let canvasProxy = new MockCanvasProxy({width: 3, height: 3})
  let startingPoint = canvasProxy.getCenter()
  let shape = new Shape({canvasProxy, startingPoint})
  shape.addPoint('1,0')
  shape.addPoint('1,2')
  t.deepEqual(Array.from(shape.neighbours).sort(), [
    '0,0',
    '0,1',
    '0,2',
    '2,0',
    '2,1',
    '2,2'
  ])
  shape.removePoint('1,2')
  shape.removePoint('1,0')
  t.is(shape.neighbours.size, 4)
})
