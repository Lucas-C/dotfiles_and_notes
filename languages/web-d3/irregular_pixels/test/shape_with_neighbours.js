import test from 'ava'
import ShapeWithNeigbours from '../src/shape_with_neighbours'

test('A point has 4 direct neighbours', t => {
  let shape = new ShapeWithNeigbours({planeWidth: 3, planeHeight: 3})
  shape.addStrPoint('1,1')
  t.deepEqual(shape.listDirectNeighbours({x: 1, y: 1}), [
    {x: 2, y: 1},
    {x: 1, y: 2},
    {x: 0, y: 1},
    {x: 1, y: 0}
  ])
})

test('A length-3 vertical Shape in a 3x3 canvas has 6 neighbours', t => {
  let shape = new ShapeWithNeigbours({planeWidth: 3, planeHeight: 3})
  shape.addStrPoint('1,1')
  shape.addStrPoint('1,0')
  shape.addStrPoint('1,2')
  t.deepEqual(Array.from(shape.neighbours).sort(), [
    '0,0',
    '0,1',
    '0,2',
    '2,0',
    '2,1',
    '2,2'
  ])
  shape.removeStrPoint('1,2')
  shape.removeStrPoint('1,0')
  t.is(shape.neighbours.size, 4)
})
