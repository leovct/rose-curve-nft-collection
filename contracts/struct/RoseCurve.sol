// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

struct RoseCurve {
    uint256 size;
    uint256 step;
    uint256 colourLineLength;
    uint256 pointRadius;
    uint256 rotationPeriod;
    string[5] paletteColours;
    string backgroundColour;
}
