export default class {
  constructor ({canvas, width, height, pixelSize}) {
    this.canvas = canvas
    this.width = width
    this.height = height

    if (canvas) { // May be null if MockCanvasProxy
      if (canvas.width !== width) {
        canvas.width = width
      }
      if (canvas.height !== height) {
        canvas.height = height
      }
      canvas.style.width = (pixelSize * width) + 'px'
      canvas.style.height = (pixelSize * height) + 'px'
      canvas.getContext('2d').clearRect(0, 0, width, height)
      this.imageData = canvas.getContext('2d').getImageData(0, 0, width, height)
    }
  }

  setPixelBlack ({x, y}) {
    let greyLevel = 0
    this.setPixelGrey({x, y, greyLevel})
  }

  setPixelWhite ({x, y}) {
    let greyLevel = 255
    this.setPixelGrey({x, y, greyLevel})
  }

  setPixelGrey ({x, y, greyLevel}) {
    let k = 4 * (x * this.width + y)
    this.imageData.data[k] = greyLevel
    this.imageData.data[k + 1] = greyLevel
    this.imageData.data[k + 2] = greyLevel
    this.imageData.data[k + 3] = 255 // alpha
  }

  isPixelBlack ({x, y}) {
    let k = 4 * (x * this.width + y)
    return this.imageData.data[k] === 0 && this.imageData.data[k + 3] === 255
  }

  getCenter () {
    return {x: Math.trunc(this.width / 2), y: Math.trunc(this.height / 2)}
  }

  render () {
    this.canvas.getContext('2d').putImageData(this.imageData, 0, 0)
  }
}
