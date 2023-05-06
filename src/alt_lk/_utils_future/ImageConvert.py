from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from utils import Log

log = Log('ImageConvert')


class ImageConvert:
    def __init__(self, path):
        self.path = path

    def to_png(self):
        assert self.path.endswith('.svg')
        drawing = svg2rlg(self.path)
        png_path = self.path[:-3] + 'png'
        renderPM.drawToFile(drawing, png_path, fmt="PNG", dpi=600)
        log.info(f'Saved {png_path}')
        return png_path
