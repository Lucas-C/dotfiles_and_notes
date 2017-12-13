import CanvasProxy from './canvas_proxy'
import generateShape from './shape_generator'

window.render = function ({canvas, width, height, pixelSize, ruleset}) {
  let canvasProxy = new CanvasProxy({canvas, width, height, pixelSize})

  generateShape({canvasProxy, ruleset})

  canvasProxy.render()
}
