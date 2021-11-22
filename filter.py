import argparse

import numpy as np
from PIL import Image
from pathlib import Path


class PixelArtGenerator:

    def __init__(self, gradations=6, pixel_step=10):
        self.step = pixel_step
        self.gradation = 255 / gradations

    def get_pixel_color(self, img_array, i, j):
        """
        Calculate brightness of segment for pixelArt
        :param img_array: numpy image array
        :param i: pixel x coordinate
        :param j: pixel y coordinate
        :return: median brightness of image segment
        >>> t = PixelArtGenerator(pixel_step=2)
        >>> t.get_pixel_color(np.ones((4, 4)), 0, 0)
        1.0

        >>> t = PixelArtGenerator(pixel_step=2)
        >>> t.get_pixel_color(np.array([[124, 76, 24], [54, 54, 160], [89, 35, 35]]), 0, 0)
        77

        >>> t = PixelArtGenerator(pixel_step=1)
        >>> t.get_pixel_color(np.array([[124, 76, 24], [54, 54, 160], [89, 35, 35]]), 0, 0)
        124
        """
        return np.sum(img_array[i: i + self.step, j: j + self.step]) // (self.step ** 2)

    def set_pixel_color(self, img_array, i, j, s):
        """
        Change pixels color on image segment.
        :param img_array: numpy image array
        :param i: x start coordinate
        :param j: y start coordinate
        :param s: size of segment in pixels
        :return: numpy array with changed brightness of pixels
        >>> t = PixelArtGenerator(pixel_step=2)
        >>> t.set_pixel_color(np.ones((4, 4)), 0, 0, 255)
        array([[85., 85.,  1.,  1.],
               [85., 85.,  1.,  1.],
               [ 1.,  1.,  1.,  1.],
               [ 1.,  1.,  1.,  1.]])

        >>> t = PixelArtGenerator()
        >>> t.set_pixel_color(np.ones((4, 4)), 2, 2, 255)
        array([[ 1.,  1.,  1.,  1.],
               [ 1.,  1.,  1.,  1.],
               [ 1.,  1., 85., 85.],
               [ 1.,  1., 85., 85.]])

        >>> t = PixelArtGenerator(gradations=1, pixel_step=3)
        >>> t.set_pixel_color(np.ones((6, 6)), 2, 2, 0)
        array([[1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1.],
               [1., 1., 0., 0., 0., 1.],
               [1., 1., 0., 0., 0., 1.],
               [1., 1., 0., 0., 0., 1.],
               [1., 1., 1., 1., 1., 1.]])
        """
        img_array[i: i + self.step, j: j + self.step] = int(s // self.gradation) * self.gradation / 3
        return img_array 

    def generate(self, image):
        """
        Creates PixelArt from image
        :param image: image file
        :return: image file
        """
        img_array = np.array(image)
        h, w = len(img_array), len(img_array[1])
        for i in range(0, h, self.step):
            for j in range(0, w, self.step):
                color = self.get_pixel_color(img_array, i, j)
                img_array = self.set_pixel_color(img_array, i, j, color)
        return Image.fromarray(img_array)


def create_argparse():
    """
    Creates CLI argument parser
    :return: argument parser
    """
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("-o", "--output", help="Output file name", required=True, type=Path)
    cli_parser.add_argument("-i", "--input", help="Input file name", required=True, type=Path)
    cli_parser.add_argument("-g", "--gradation", help="Gradations step", default=6, type=int)
    cli_parser.add_argument("-s", "--size", help="Pixel size", default=10, type=int)
    return cli_parser


if __name__ == "__main__":
    parser = create_argparse()
    args = parser.parse_args()
    img = Image.open(args.input)
    generator = PixelArtGenerator(args.gradation, args.size)
    generator.generate(img).save(args.output)
