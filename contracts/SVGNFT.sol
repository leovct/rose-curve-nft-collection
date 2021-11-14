// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "./URI.sol";

//// @title A contract to create a collection of NFTs that output SVG code in their URI
//// @author leovct
//// @dev Compliant with OpenZeppelin's implementation of the ERC721 spec draft
contract SVGNFT is ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    event MintedSVGNFT(uint256 indexed tokenId, string tokenURI);

    constructor() ERC721("Scalable Vector Graphics NFT", "SVGNFT") {}

    //// @notice Mint a SVG NFT
    //// @param _svg the svg code of the NFT
    function mint(string memory _svg) public {
        uint256 id = _tokenIdCounter.current();
        _safeMint(msg.sender, id);
        _tokenIdCounter.increment();
        
        string memory svgURI = URI.svgToImageURI(_svg);
        string memory tokenURI = URI.formatTokenURI(id, svgURI);
        _setTokenURI(id, tokenURI);

        emit MintedSVGNFT(id, tokenURI);
    }
}
