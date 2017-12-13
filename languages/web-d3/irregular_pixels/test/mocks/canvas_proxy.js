import CanvasProxy from '../../src/canvas_proxy'

export default class extends CanvasProxy {
  constructor ({width, height}) {
    let canvas = null
    let pixelSize = 1
    super({canvas, width, height, pixelSize})
    this.imageData = {data: Array(width * height * 4).fill(255)}
  }
}
