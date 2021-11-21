// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "base64-sol/base64.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title Provide useful functions to manipulate URIs to create NFTs
 * @author leovct
 */
library URI {
    using Strings for uint256;

    /**
     * @notice Create an image URI with SVG code embedded
     * @param _svg the svg code to embed in the URI
     */
    function _svgToImageURI(string memory _svg) internal pure returns (string memory) {
        string memory baseURL = "data:image/svg+xml;base64,";
        string memory svgBase64Encoded = Base64.encode(bytes(string(abi.encodePacked(_svg))));
        return string(abi.encodePacked(baseURL, svgBase64Encoded));
    }

    /**
     * @notice Format the token URI of the NFT
     * @param _imageURI the URI of the NFT
     */
    function _formatTokenURI(uint256 _tokenId, string memory _imageURI) internal pure returns (string memory) {
        string memory baseURL = "data:application/json;base64,";
        string memory tokenJsonBase64Encoded = Base64.encode(bytes(abi.encodePacked("{",
            '"name": "Scalable Vector Graphics NFT #', _tokenId.toString(), '", ',
            '"description": "A simple collection of circles.", ',
            '"image": "', _imageURI, '"',
        "}")));
        return string(abi.encodePacked(baseURL, tokenJsonBase64Encoded));
    }
}
