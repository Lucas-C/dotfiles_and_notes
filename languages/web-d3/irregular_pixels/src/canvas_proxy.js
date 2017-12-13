export default class {
  constructor ({canvas, width, height, pixelSize}) {
    this.canvas = canvas
    this.width = width
    this.height = height
    this.pixelSize = pixelSize

    if (canvas) { // May be null if MockCanvasProxy
      if (canvas.width !== width) {
        canvas.width = width
      }
      if (canvas.height !== height) {
        canvas.height = height
      }
      canvas.getContext('2d').clearRect(0, 0, width, height)
      this.imageData = canvas.getContext('2d').getImageData(0, 0, width, height)
    }
  }

  getWidth () {
    return this.width / this.pixelSize
  }

  getHeight () {
    return this.height / this.pixelSize
  }

  setPixelBlack ({x, y}) {
    let greyLevel= 0
    setPixelGrey({x, y, greyLevel})
  }

  setPixelWhite ({x, y}) {
    let greyLevel= 255
    setPixelGrey({x, y, greyLevel})
  }

  setPixelGrey ({x, y, greyLevel}) {
    [x, y] = [x * this.pixelSize, y * this.pixelSize]
    for (let i = 0; i < this.pixelSize; i += 1) {
      for (let j = 0; j < this.pixelSize; j += 1) {
        let k = 4 * ((x + i) * this.width + y + j)
        this.imageData.data[k] = greyLevel
        this.imageData.data[k + 1] = greyLevel
        this.imageData.data[k + 2] = greyLevel
        this.imageData.data[k + 3] = 255 // alpha
      }
    }
  }

  isPixelBlack ({x, y}) {
    [x, y] = [x * this.pixelSize, y * this.pixelSize]
    return this.imageData.data[4 * (x * this.width + y)] === 0 && this.imageData.data[4 * (x * this.width + y) + 3] === 255
  }

  getCenter () {
    return {x: Math.trunc(this.getWidth() / 2), y: Math.trunc(this.getHeight() / 2)}
  }

  render () {
    this.canvas.getContext('2d').putImageData(this.imageData, 0, 0)
  }
}
