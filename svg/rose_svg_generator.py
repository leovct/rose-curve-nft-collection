"""
The Rose SVG Generator generates random rose mathematical patterns using colours from open palettes.
More information can be found on the pattern the README.md file.
"""

import math
import random


class RosePattern:
    """Define a rose pattern object that can then be generated in the svg format."""
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
        """Generate a svg rect tag that is used as the background shape of the svgs."""
        return f'<rect x="{-self.img_length}" y="{-self.img_length}"' + \
            f' width="{2*self.img_length}" height="{2*self.img_length}"' + \
            f' fill="{self.background_colour}"></rect>'

    def _generate_pattern(self, _n, _d):
        """Generate a list of svg circle points corresponding to the rose pattern shape."""
        # A rose is the set of points in polar coordinates specified by the polar equation:
        # r = a*cos(k*theta) with k = n/d
        parameter_a = self.img_length/2-20
        parameter_k = _n/_d

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
            r_coordinate = parameter_a * math.cos(parameter_k * theta)

            # Compute the cartesian coordinates of the point
            x_coordinate = r_coordinate * math.cos(theta)
            y_coordinate = r_coordinate * math.sin(theta)

            # Create the point using the svg format
            point = f'<circle cx="{x_coordinate}" cy="{y_coordinate}" r="{self.point_radius}"' + \
                f' fill="{point_colour}"></circle>'
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
        """Generate the svg tag for the rotation animation of the svgs."""
        rotate_direction = 'from="0" to="360"'
        if not _clockwise_direction:
            rotate_direction = 'from="360" to="0"'
        return '<animateTransform attributeType="xml" attributeName="transform" type="rotate"' + \
            f' {rotate_direction} dur="{self.rotation_period}s" additive="sum"' + \
                ' repeatCount="indefinite"/>'

    def generate(self):
        """Generate the svg file of the rose pattern under svg/generated/."""
        with open(file=f"svg/generated/{self.name}.svg", mode='w', encoding='utf-8') as file:
            file.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.img_length}"' + \
                f' height="{self.img_length}" viewBox= "{-self.img_length/2} ' + \
                f' {-self.img_length/2} {self.img_length} {self.img_length}">')

            background = self._generate_background()
            file.write("\n\t"+background)

            file.write("\n\t<g>")
            first_pattern = self._generate_pattern(7, 8)
            for shape in first_pattern:
                file.write("\n\t\t"+shape)
            file.write('\n\t\t'+self._generate_rotate_animation())
            file.write('\n\t</g>')

            file.write("\n\t<g>")
            second_pattern = self._generate_pattern(4, 5)
            for shape in second_pattern:
                file.write("\n\t\t"+shape)
            file.write('\n\t\t'+self._generate_rotate_animation(_clockwise_direction=False))
            file.write('\n\t</g>')

            file.write('\n\tSorry, your browser does not support inline SVG.')
            file.write('\n</svg>')


def main():
    """
    Main method of the rose svg generator.
    It generates 8 different svgs (4 with black backgrounds and 4 whith white backgrounds).
    """
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

    rose_black_bg_optimised = RosePattern(
        name="rose_black_bg_optimised", shape_colours=palette_colours, img_length=500,
        point_radius=1)
    rose_black_bg_optimised.generate()

    rose_black_white_optimised = RosePattern(
        name="rose_white_bg_optimised", shape_colours=palette_colours, background_colour="#ffffff",
        img_length=500, point_radius=1)
    rose_black_white_optimised.generate()


if __name__ == "__main__":
    main()
