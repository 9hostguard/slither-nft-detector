// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Incomplete ERC721 contract - missing 4-argument safeTransferFrom
contract InsecureNFT {
    mapping(uint256 => address) private _owners;
    mapping(address => mapping(address => bool)) private _operatorApprovals;
    mapping(uint256 => address) private _tokenApprovals;

    function ownerOf(uint256 tokenId) public view returns (address) {
        return _owners[tokenId];
    }

    function approve(address to, uint256 tokenId) public {
        _tokenApprovals[tokenId] = to;
    }

    function getApproved(uint256 tokenId) public view returns (address) {
        return _tokenApprovals[tokenId];
    }

    function isApprovedForAll(address owner, address operator) public view returns (bool) {
        return _operatorApprovals[owner][operator];
    }

    // This implementation is INCOMPLETE - it only has the 3-argument version
    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        // Missing bytes data param - this should trigger our detector
        require(_isApprovedOrOwner(msg.sender, tokenId), "Not approved");
        _transfer(from, to, tokenId);
    }

    function _isApprovedOrOwner(address spender, uint256 tokenId) internal view returns (bool) {
        address owner = ownerOf(tokenId);
        return (spender == owner || getApproved(tokenId) == spender || isApprovedForAll(owner, spender));
    }

    function _transfer(address from, address to, uint256 tokenId) internal {
        _owners[tokenId] = to;
    }
}

// Complete ERC721 contract - has both versions
contract SecureNFT {
    mapping(uint256 => address) private _owners;
    mapping(address => mapping(address => bool)) private _operatorApprovals;
    mapping(uint256 => address) private _tokenApprovals;

    function ownerOf(uint256 tokenId) public view returns (address) {
        return _owners[tokenId];
    }

    function approve(address to, uint256 tokenId) public {
        _tokenApprovals[tokenId] = to;
    }

    function getApproved(uint256 tokenId) public view returns (address) {
        return _tokenApprovals[tokenId];
    }

    function isApprovedForAll(address owner, address operator) public view returns (bool) {
        return _operatorApprovals[owner][operator];
    }

    // 3-argument version
    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        safeTransferFrom(from, to, tokenId, "");
    }

    // 4-argument version - this makes it compliant
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory data) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Not approved");
        _safeTransfer(from, to, tokenId, data);
    }

    function _isApprovedOrOwner(address spender, uint256 tokenId) internal view returns (bool) {
        address owner = ownerOf(tokenId);
        return (spender == owner || getApproved(tokenId) == spender || isApprovedForAll(owner, spender));
    }

    function _safeTransfer(address from, address to, uint256 tokenId, bytes memory data) internal {
        _transfer(from, to, tokenId);
        _checkOnERC721Received(from, to, tokenId, data);
    }

    function _transfer(address from, address to, uint256 tokenId) internal {
        _owners[tokenId] = to;
    }

    function _checkOnERC721Received(address from, address to, uint256 tokenId, bytes memory data) internal {
        // Implementation would check if recipient can handle ERC721 tokens
    }
}