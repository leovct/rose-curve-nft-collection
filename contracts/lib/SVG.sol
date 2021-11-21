// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title SVG library providing useful functions to manipulate SVGs
 * @author leovct
 */
library SVG {
    using Strings for uint256;

    /**
     * @notice Create a SVG
     * @param _width    the width of the SVG
     * @param _height   the height of the SVG
     * @param _content  the content of the SVG
     */
    function _createSVG(uint256 _width, uint256 _height, string memory _content)
        internal pure returns (string memory) {
        return string(abi.encodePacked(
            '<svg xmlns="http://www.w3.org/2000/svg" width="', _width.toString(),
            '" height="', _height.toString(),
            '" viewBox="-', (_width / 2).toString(), " -", (_height / 2).toString(),
            " ", _width.toString(), " ", _height.toString(),
            '">', _content, "</svg>"
        ));
    }

    /**
     * @notice Create a SVG shape
     * @param _content the content of the shape
     * @return the SVG shape
     */
    function _createShape(string memory _content) internal pure returns (string memory) {
        return string(abi.encodePacked("<g>", _content, "</g>"));
    }

    /**
     * @notice Create a SVG rectangle shape
     * @param _x         the x coordinate of the top-right corner of the rectangle
     * @param _y         the y coordinate of the top-right corner of the rectangle
     * @param _width     the width of the rectangle
     * @param _height    the height of the rectangle
     * @param _colour    the colour of the rectangle
     * @return the SVG rectangle shape
     */
    function _createRect(int256 _x, int256 _y, uint256 _width, uint256 _height, string memory _colour)
        internal pure returns (string memory) {
        return string(abi.encodePacked(
            '<rect x="', _int256toString(_x),
            '" y="', _int256toString(_y),
            '" width="', _width.toString(),
            '" height="', _height.toString(),
            '" fill="', _colour, '"></rect>'
        ));
    }

    /**
     * @notice Create a SVG circle shape
     * @param _x         the x coordinate of the circle center
     * @param _y         the y coordinate of the circle center
     * @param _radius    the radius of the circle
     * @param _colour    the colour of the circle
     * @return the SVG circle shape
     */
    function _createCircle(int256 _x, int256 _y, uint256 _radius, string memory _colour)
        internal pure returns (string memory) {
        return string(abi.encodePacked(
            '<circle cx="', _int256toString(_x),
            '" cy="', _int256toString(_y),
            '" r="', _radius.toString(),
            '" fill=', _colour, '"></circle>'
        ));
    }

    /**
     * @notice Create a SVG rotation animation
     * @param _clockwise_direction  the direction of the rotation
     If it is set to true, the rotation will be clockwise and if not, it will be the opposite
     * @param _period               the period of the rotation animation
     * @return the SVG rotation animation
     */
    function _createRotationAnimation(bool _clockwise_direction, uint256 _period)
        internal pure returns (string memory) {
        string memory rotation_direction = 'from="0" to="360"';
        if (!_clockwise_direction) {
            rotation_direction = 'from="360" to="0"';
        }
        return string(abi.encodePacked(
            '<animateTransform attributeType="xml" attributeName="transform" type="rotate" ', rotation_direction,
            ' dur="', _period.toString(), 's" additive="sum" repeatCount="indefinite"/>'
        ));
    }

    /**
     * @notice Converts a variable of type int256 to a string variable
     * @param _i the variable of type int256
     * @return the variable converted to a string
     */
    function _int256toString(int256 _i) internal pure returns (string memory) {
        return (_i < 0) ? string(abi.encodePacked("-", uint256(_i * (-1)).toString())) : uint256(_i).toString();
    }
}
