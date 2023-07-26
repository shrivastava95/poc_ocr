from ironpdf import *
# Instantiate Renderer
renderer = ChromePdfRenderer()
# Create a PDF from a URL or local file path
pdf = renderer.RenderUrlAsPdf("https://www.amazon.com/?tag=hp2-brobookmark-us-20")
# Extract all pages to a folder as image files
pdf.RasterizeToImageFiles("assets/images/*.png",DPI=96)