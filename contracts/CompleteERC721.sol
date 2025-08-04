// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Complete ERC721 contract - should not trigger the detector
contract CompleteERC721 {
    mapping(uint256 => address) private _owners;

    // 3-argument version
    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        safeTransferFrom(from, to, tokenId, "");
    }

    // 4-argument version - this makes it compliant
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory data) public {
        // Implementation here
    }
}