let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
let data = imageData.data;

for (let i = 0; i < data.length; i += 4) {
  data[i]     = i % 255;     // rouge
  data[i + 1] = i*i % 255;   // vert
  data[i + 2] = i*i*i % 255; // bleu
  data[i + 3] = 255;         // alpha
}

ctx.putImageData(imageData, 0, 0);
