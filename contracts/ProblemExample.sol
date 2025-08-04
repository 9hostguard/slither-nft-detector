// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InsecureNFT {
    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        // Missing bytes data param
    }
}