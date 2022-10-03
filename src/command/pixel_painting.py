"""
Create a block Pixel Painting in the Miniworld map.
"""



from typing import List, Tuple, Union


import PIL.Image



# Pixel painting project class.
class PixelPainting:
    _path:Union[str, None] = None
    _image = None
    _pixmap = None
    _width:Union[int, None] = None
    _height:Union[int, None] = None
    # Coordinates of the lower left corner of the image.
    _position: Union[Tuple[int, int, int], None]  = None
    # Lua script.
    _script:Union[str, None] = None
    def open(self, filename:str) -> None:
        # Open file.
        self._image = PIL.Image.open(filename)
        # Get attr.
        self._width = self._image.width
        self._height = self._image.height
        # Get image pixmap.
        self._pixmap = self._image.load()
        self._path = filename
        # Close file.
        self._image.close()
    def _to_hex_rgb(self, color:Tuple[int, int, int]):
        """
        Convert color tuple to RGB hex code.
        """
        return hex(color[0] * 0x10000 + color[1] * 0x100 + color[2])
    def generate_color_map(self) -> List[List[
            Union[Tuple[int, int, int], None] # Transparent is `None`.
        ]]:
        """
        Notice:
            Start at the bottom left corner of the pixmap,
              working from left to right, and then from bottom to top.
        """
        result = []
        # Get colors.
        for i in range(self.width)[::-1]:
            result.append([])
            for j in range(self.height):
                result[-1].append(self._pixmap[j, i])
        return result
    def generate_script(self) -> str:
        result = ""
        # Read template script.
        with open("./assets/template/script/pixel_painting.dev.lua") as file:
            result = file.read()
        # Replace keywords.
        # Keywords looks like `[[$BLOCK_ID]]`.
        result = result.replace("[[$POSITION_X]]", str(self.position[0]))
        result = result.replace("[[$POSITION_Y]]", str(self.position[1]))
        result = result.replace("[[$POSITION_Z]]", str(self.position[2]))
        result = result.replace("[[$SIZE_WIDTH]]", str(self.width))
        result = result.replace("[[$SIZE_HEIGHT]]", str(self.height))
        # Replace pixmap data.
        result = result.replace("[[$BLOCK_ID]]", str(666)) # Constant.
        color_map = self.generate_color_map()
        color_str = ""
        for i in color_map: # Generate color table.
            color_str += "  {"
            for j in i:
                color_str += self._to_hex_rgb(j) + ", "
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
    @property
    def script(self) -> str:
        if self._script is None:
            result = self.generate_script()
            self._script = result
            return result
        else:
            return self._script