from colorsys import hsv_to_rgb, rgb_to_hsv

class RGBLight:
    @property
    def color(self):
        '''Get current color as RGB values

        Returns:
            Tuple of RGB values in range of 0-255
        '''
        raise NotImplementedError('This method should be overridden')

    @color.setter
    def color(self, rgb):
        '''Set color as RGB values

        Args:
            rgb: Tuple of RGB values in range of 0-255
        '''
        raise NotImplementedError('This method should be overridden')

    @property
    def hsv_color(self):
        '''Get current color as HSV values

        Returns:
            Tuple of HSV values in range of 0-1
        '''
        return rgb_to_hsv(*(i / 255.0 for i in self.color))

    @hsv_color.setter
    def hsv_color(self, hsv):
        '''Set color as HSV values

        Args:
            hsv: Tuple of HSV values in range of 0-1
        '''
        self.color = tuple(i * 255.0 for i in hsv_to_rgb(*hsv))
