"""
Create a block pixel painting in the Miniworld map.
"""



from typing import Union


import PIL.Image



# Pixel painting project class.
class PixelPainting:
    # Image file.
    _pixmap = None
    def __init__(self, filename:str) -> None:
        image = PIL.Image.open(filename)
        self._pixmap = image.load() # Get image pixmap.
        image.close()
    def generate_script(self) -> str:
        # TODO(KaiKai): Complete this feature.
        script = ""
        for i in self._pixmap:
            for j in i:
                pass