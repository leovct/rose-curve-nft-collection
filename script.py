# Generates random rose mathematical patterns using colours from palettes.
# The palettes are deployed on the Ethereum blockchain (see palettes.io).
# The images are generated as svg files and can be stored on-chain.
# More information can be found on the pattern: https://en.wikipedia.org/wiki/Rose_%28mathematics%29

import math
import random


class RosePattern:
    def __init__(self, _name, _img_length, _background_colour, _shape_colours, _point_radius,
                 _colour_line_length, _step):
        self.name = _name
        self.img_length = _img_length
        self.background_colour = _background_colour
        self.shape_colours = _shape_colours
        self.point_radius = _point_radius
        self.colour_line_length = _colour_line_length
        self.step = _step

    def _generate_background(self):
        return '<rect x="{0}" y="{0}" width="{1}" height="{1}" fill="{2}"></rect>'.format(
            -self.img_length, 2*self.img_length, self.background_colour)

    def _generate_pattern(self, _n, _d):
        # A rose is the set of points in polar coordinates specified by the polar equation:
        # r = a*cos(k*theta) with k = n/d
        a = self.img_length/2-20
        k = _n/_d

        # The colour of the points is randomly choosen and changes every x generated points (see the
        # _colour_line_length parameter)
        last_palette_colour_index = len(self.shape_colours)-1
        number_points_with_same_colour = 0
        point_colour = self.shape_colours[random.randint(
            0, last_palette_colour_index)]

        points = []
        theta = 0.
        while theta < 2*math.pi*_d:
            # Compute the polar coordinates of the point
            r = a * math.cos(k * theta)

            # Compute the cartesian coordinates of the point
            x = r * math.cos(theta)
            y = r * math.sin(theta)

            # Create the point using the svg format
            point = '<circle cx="{}" cy="{}" r="{}" fill="{}"></circle>'.format(
                x, y, self.point_radius, point_colour)
            points.append(point)

            # Increment theta
            theta += self.step

            # Check if the colour of the point needs to be changed
            number_points_with_same_colour += 1
            if number_points_with_same_colour >= self.colour_line_length:
                number_points_with_same_colour = 0
                point_colour = self.shape_colours[random.randint(
                    0, last_palette_colour_index)]
        # return all the points forming the rose pattern shape
        return points

    def generate(self):
        with open("generated/{}.svg".format(self.name), 'w') as f:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{0}" viewBox="{1} {1} {0} {0}">'.format(
                self.img_length, -self.img_length/2))

            background = self._generate_background()
            f.write("\n\t"+background)

            first_pattern = self._generate_pattern(7, 2)
            for shape in first_pattern:
                f.write("\n\t"+shape)

            second_pattern = self._generate_pattern(7, 8)
            for shape in second_pattern:
                f.write("\n\t"+shape)

            f.write('\n</svg>')


def main():
    palette_colours = ["#44ffcc", "#bb7722", "#77bbee", "#9988cc", "#ff5566"]

    rose_black_bg = RosePattern("rose_black_bg", 1000, "#000000", palette_colours, 2, 20, 0.02)
    rose_black_bg.generate()

    rose_white_bg = RosePattern("rose_white_bg", 1000, "#ffffff", palette_colours, 2, 20, 0.02)
    rose_white_bg.generate()

    rose_black_bg_thin = RosePattern("rose_black_bg_thin", 1000, "#000000", palette_colours, 1, 20, 0.02)
    rose_black_bg_thin.generate()

    rose_white_bg_thin = RosePattern("rose_white_bg_thin", 1000, "#ffffff", palette_colours, 1, 20, 0.02)
    rose_white_bg_thin.generate()

    rose_black_bg_more_steps = RosePattern("rose_black_bg_more_steps", 1000, "#000000", palette_colours, 2, 20, 0.01)
    rose_black_bg_more_steps.generate()

    rose_white_bg_more_steps = RosePattern("rose_white_bg_more_steps", 1000, "#ffffff", palette_colours, 2, 20, 0.01)
    rose_white_bg_more_steps.generate()

    rose_black_bg_way_more_steps = RosePattern("rose_black_bg_way_more_steps", 1000, "#000000", palette_colours, 2, 20, 0.001)
    rose_black_bg_way_more_steps.generate()

    rose_white_bg_way_more_steps = RosePattern("rose_white_bg_way_more_steps", 1000, "#ffffff", palette_colours, 2, 20, 0.001)
    rose_white_bg_way_more_steps.generate()

    rose_black_bg_optimised = RosePattern("rose_black_bg_optimised", 500, "#000000", palette_colours, 1, 20, 0.01)
    rose_black_bg_optimised.generate()


if __name__ == "__main__":
    main()
