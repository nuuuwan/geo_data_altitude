from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from utils import Log

log = Log('ImageConvert')
DPI = 100


class ImageConvert:
    def __init__(self, path):
        self.path = path

    def svg_to_png(self):
        if not self.path.endswith('.svg'):
            raise ValueError(f'Expected .svg file, got {self.path}')
        drawing = svg2rlg(self.path)
        png_path = self.path[:-3] + 'png'
        renderPM.drawToFile(drawing, png_path, fmt="PNG", dpi=DPI)
        log.info(f'Saved {png_path}')
        return png_path
