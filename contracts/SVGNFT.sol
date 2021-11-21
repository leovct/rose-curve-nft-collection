// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "./lib/URI.sol";

/**
 * @title A contract to create a collection of NFTs that output SVG code in their URI
 * @author leovct
 * @dev Compliant with OpenZeppelin's implementation of the ERC721 spec draft
 */
contract SVGNFT is ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    event MintedSVGNFT(uint256 indexed tokenId, string tokenURI);

    constructor() ERC721("Scalable Vector Graphics NFT", "SVGNFT") {}

    /**
     * @notice Mint a SVG NFT
     * @param _svg the svg code of the NFT
     */
    function mint(string memory _svg) public {
        uint256 tokenId = _tokenIdCounter.current();
        _safeMint(msg.sender, tokenId);
        _tokenIdCounter.increment();

        string memory svgURI = URI._svgToImageURI(_svg);
        string memory tokenURI = URI._formatTokenURI("Scalable Vector Graphics NFT",
            "A simple collection of circles and rectangles.", tokenId, svgURI);
        _setTokenURI(tokenId, tokenURI);

        emit MintedSVGNFT(tokenId, tokenURI);
    }
}
