# Generates random rose mathematical patterns using colours from palettes.
# The palettes are deployed on the Ethereum blockchain (see palettes.io).
# The images are generated as svg files and can be stored on-chain.
# More information can be found on the pattern: https://en.wikipedia.org/wiki/Rose_%28mathematics%29

import math
import random


class RosePattern:
    def __init__(self, name, shape_colours, background_colour="#000000", img_length=1000,
                 point_radius=2, colour_line_length=20, step=0.02, rotation_period=60):
        self.name = name
        self.shape_colours = shape_colours
        self.background_colour = background_colour
        self.img_length = img_length
        self.point_radius = point_radius
        self.colour_line_length = colour_line_length
        self.step = step
        self.rotation_period = rotation_period

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

    def _generate_rotate_animation(self, _clockwise_direction=True):
        rotateAnimation = '<animateTransform attributeType="xml" attributeName="transform" type="rotate" ' 
        if _clockwise_direction:
            rotateAnimation += 'from="0" to="360"'
        else:
            rotateAnimation += 'from="360" to="0"'
        rotateAnimation += ' dur="{}s" additive="sum" repeatCount="indefinite" />"'.format(
            self.rotation_period)
        return rotateAnimation

    def generate(self):
        with open("svg/generated/{}.svg".format(self.name), 'w') as f:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{0}" viewBox="' +
                    '{1} {1} {0} {0}">'.format(self.img_length, -self.img_length/2))

            background = self._generate_background()
            f.write("\n\t"+background)

            f.write("\n\t<g>")
            first_pattern = self._generate_pattern(7, 8)
            for shape in first_pattern:
                f.write("\n\t\t"+shape)
            f.write('\n\t\t'+self._generate_rotate_animation())
            f.write('\n\t</g>')

            f.write("\n\t<g>")
            second_pattern = self._generate_pattern(4, 5)
            for shape in second_pattern:
                f.write("\n\t\t"+shape)
            f.write('\n\t\t'+self._generate_rotate_animation(False))
            f.write('\n\t</g>')

            f.write('\n\tSorry, your browser does not support inline SVG.')
            f.write('\n</svg>')


def main():
    palette_colours = ["#44ffcc", "#bb7722", "#77bbee", "#9988cc", "#ff5566"]

    rose_black_bg = RosePattern(
        name="rose_black_bg", shape_colours=palette_colours)
    rose_black_bg.generate()

    rose_white_bg = RosePattern(
        name="rose_white_bg", shape_colours=palette_colours, background_colour="#ffffff")
    rose_white_bg.generate()

    rose_black_bg_thin = RosePattern(
        name="rose_black_bg_thin", shape_colours=palette_colours, point_radius=1)
    rose_black_bg_thin.generate()

    rose_white_bg_thin = RosePattern(
        name="rose_white_bg_thin", shape_colours=palette_colours, background_colour="#ffffff",
        point_radius=1)
    rose_white_bg_thin.generate()

    rose_black_bg_more_steps = RosePattern(
        name="rose_black_bg_more_steps", shape_colours=palette_colours, step=0.01)
    rose_black_bg_more_steps.generate()

    rose_white_bg_more_steps = RosePattern(
        name="rose_white_bg_more_steps", shape_colours=palette_colours,
        background_colour="#ffffff", step=0.01)
    rose_white_bg_more_steps.generate()

    rose_black_bg_way_more_steps = RosePattern(
        name="rose_black_bg_way_more_steps", shape_colours=palette_colours, step=0.001)
    rose_black_bg_way_more_steps.generate()

    rose_white_bg_way_more_steps = RosePattern(
        name="rose_white_bg_way_more_steps", shape_colours=palette_colours,
        background_colour="#ffffff", step=0.001)
    rose_white_bg_way_more_steps.generate()

    rose_black_bg_optimised = RosePattern(
        name="rose_black_bg_optimised", shape_colours=palette_colours, img_length=500,
        point_radius=1)
    rose_black_bg_optimised.generate()


if __name__ == "__main__":
    main()
