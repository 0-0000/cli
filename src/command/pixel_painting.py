"""
Create a block Pixel Painting in the Miniworld map.
"""



from typing import List, Tuple, Union


import PIL.Image


from base import to_hex_rgb
from base import BaseMiniScript



# Pixel painting project class.
class PixelPainting(BaseMiniScript):
    """Generate Pixel Painting script by image file.
    """
    _path:Union[str, None] = None
    _image = None
    """Image file in `PIL` lib."""
    _pixmap = None
    _width:Union[int, None] = None
    _height:Union[int, None] = None
    _position: Union[Tuple[int, int, int], None]  = None
    """Coordinates of the lower left corner of the image."""
    def open(self, filename:str) -> None:
        """Generate `Miniworld Lua Script` by self args.

        Args:
            filename: Image file path.

        Raises:
            OSError: Cannot open image file.
        """
        self._image = PIL.Image.open(filename).convert("RGB") # To RGB image.
        self._width = self._image.width
        self._height = self._image.height
        self._pixmap = self._image.load() # To pixmap.
        self._path = filename
        self._image.close()
        self._position = (0, 0, 0)
        self._init = True
    def _generate_color_map(self) -> List[List[
            Union[Tuple[int, int, int], None]
            # TODO(KaiKai):Transparent is `None`.
        ]]:
        """Generate two-dimensional list that describes colors.

        Notice:
            Start at the bottom left corner of the pixmap,
            working from left to right, and then from bottom to top.

        Returns:
            Generated color map.
            Such as:
        ```
        [[(255, 128, 64), (78, 62, 156), (0, 0, 0)],
         [(64, 128, 255), (255, 255, 255), (245, 62, 108)],
         [(0, 0, 0), (28, 84, 98), (207, 88, 153)]]
        ```

        Raises:
            ValueError("uninitialized"): Instance uninitialized.
        """
        if not self._init:
            raise ValueError("uninitialized")
        result = []
        # Get colors.
        for i in range(self.width)[::-1]:
            result.append([])
            for j in range(self.height):
                result[-1].append(self._pixmap[j, i])
        return result
    def generate_script(self) -> str:
        """Generate the final script, ignore cache.

        Returns:
            Generated script.

        Raises:
            ValueError("uninitialized"): Instance uninitialized.
            OSError: Cannot open template script, please check permission.
        """
        if not self._init:
            raise ValueError("uninitialized")
        result = ""
        # Read template script.
        with open("./assets/template/script/pixel_painting.dev.lua") as f:
            result = f.read()
        # Replace keywords.
        # Keywords looks like `[[$KEYWORD]]`.
        result = (result
            .replace("[[$POSITION_X]]", str(self.position[0]))
            .replace("[[$POSITION_Y]]", str(self.position[1]))
            .replace("[[$POSITION_Z]]", str(self.position[2]))
            .replace("[[$SIZE_WIDTH]]", str(self.width))
            .replace("[[$SIZE_HEIGHT]]", str(self.height))
            .replace("[[$BLOCK_ID]]", str(666))) # Constant.
        color_str = ""
        for i in self._generate_color_map(): # Generate color table.
            color_str += "  {"
            for j in i:
                color_str += to_hex_rgb(j) + ", "
            color_str = color_str[:-2] # Delete last `, `.
            color_str += "},\n" # Next line.
        color_str = "{\n" + color_str # Start table.
        color_str = color_str[:-2] # Delete last `,`.
        color_str += "\n}" # End table.
        result = result.replace("[[$PAITING]]", color_str)
        return result
    @property
    def width(self) -> Union[int, None]:
        return self._width
    @property
    def height(self) -> Union[int, None]:
        return self._height
    @property
    def position(self) -> Union[Tuple[int, int, int], None]:
        return self._position
    @position.setter
    def position(self, position:Tuple[int, int, int]) -> None:
        self._position = position