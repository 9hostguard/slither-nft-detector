// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC1155 {
    function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes calldata data) external;
}

contract UnsafeERC1155Transfer {
    IERC1155 public token;

    constructor(address _token) {
        token = IERC1155(_token);
    }

    function transferWithoutCheck(address from, address to, uint256 id, uint256 amount) external {
        token.safeTransferFrom(from, to, id, amount, "");
    }
}