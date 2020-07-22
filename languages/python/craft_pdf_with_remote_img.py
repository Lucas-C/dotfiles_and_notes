#!/usr/bin/env python3

# GOAL: build a PDF that would trigger an HTTP request to a given URL,
# and if possible even display a remotely hosted image.

# MOTIVATION: to generate "interactive" PDFs with dynamic images.
# With an embedded form sending requests to a remote server, the image could even change based on user input!

# Resources:
# - https://stackoverflow.com/a/36592092/636849
# - https://brendanzagaeski.appspot.com/0004.html
# - https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/PDF32000_2008.pdf
# - Python pdfrw lib: very helpful to auto-generate the final xref table

# Input images sources:
# - https://brendanzagaeski.appspot.com/0004.html
# - https://github.com/Hopding/pdf-lib/raw/master/assets/pdfs/examples/embed_png_and_jpeg_images.pdf
#   qpdf --qdf --object-streams=disable embed_png_and_jpeg_images.pdf embed_png_and_jpeg_images-qpdf.pdf

from pdfrw import PdfArray, PdfDict, PdfName, PdfReader, PdfWriter

pdf = PdfReader('minimal.pdf')
pdf_kid = pdf.Root.Pages.Kids[0]

img = PdfReader('embed_png_and_jpeg_images-qpdf.pdf')
img_kid = img.Root.Pages.Kids[0]

pdf_kid.Contents = img_kid.Contents[0]
pdf_kid.Contents.stream = pdf_kid.Contents.stream[:105]  # unnecessary clean-up: getting rid of traces of Image-7370
pdf_kid.MediaBox = img_kid.MediaBox

alt_img = PdfDict(
    Type=PdfName.XObject,
    SubType=PdfName.Image,
    BitsPerComponent=8,
    ColorSpace=PdfName.DeviceRGB,
    Height=800,
    Width=600,
    Length=0,
    F=PdfDict(
        FS=PdfName.URL,
        F='https://chezsoi.org/lucas/ThePatch.jpg'),
    FFilter=PdfName.DCTDecode)
alt_img.indirect = true

alternates = PdfArray([PdfDict(
    DefaultForPrinting = True,
    Image = alt_img)])
alternates.indirect = true

img_name = PdfName('Image-9960')
img = img_kid.Resources.XObject[img_name]
img.Alternates = alternates
pdf_kid.Resources.XObject = PdfDict()
pdf_kid.Resources.XObject[img_name] = img

out = PdfWriter()
out.addpage(pdf.pages[0])
out.write('out.pdf')

# CONCLUSION: neither Adobe nor Sumatra readers visit the link...
# It may be that readers do not follow this "Alternates" images spec anymore, that HTTPS is not supported, or that I made a mistake in the resulting PDF.
# Anyway, I'm giving up.
# However Canary Tokens use a similar technic that works well (with Adobe not Sumatra): https://github.com/sumatrapdfreader/sumatrapdf/issues/1696
