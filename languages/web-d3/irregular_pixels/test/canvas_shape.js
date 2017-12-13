import test from 'ava'
import CanvasShape from '../src/canvas_shape'
import MockCanvasProxy from './utils/mock_canvas_proxy'

test('A new Shape at the center of a 3x3 canvas is not on its edge', t => {
  let canvasProxy = new MockCanvasProxy({width: 3, height: 3})
  let shape = new CanvasShape(canvasProxy)
  shape.addPoint(canvasProxy.getCenter())
  t.false(shape.isOnCanvasEdge())
})

test('A new Shape in a 2x2 canvas is on its edge', t => {
  let canvasProxy = new MockCanvasProxy({width: 2, height: 2})
  let shape = new CanvasShape(canvasProxy)
  shape.addPoint(canvasProxy.getCenter())
  t.true(shape.isOnCanvasEdge())
})
