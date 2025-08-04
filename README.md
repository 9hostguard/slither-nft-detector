# slither-nft-detector
Nft transfers toolkit; erc721-erc1155- transfer checker; unsafe NFT-transfer detector

# 🛡️ Slither NFT Transfer Detector

![Slither Audit](https://github.com/9hostguard/slither-nft-detector/actions/workflows/slither.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This custom Slither detector identifies unsafe ERC721 and ERC1155 transfers that lack callback validation. It helps auditors catch critical vulnerabilities in NFT protocols, staking vaults, and marketplaces.

---

## 🚨 What It Detects

- ERC721 `transferFrom` without:
  - `require` checks
  - `onERC721Received` validation
  - `isContract` recipient check

- ERC1155 `safeTransferFrom` and `safeBatchTransferFrom` without:
  - `onERC1155Received` / `onERC1155BatchReceived` validation
  - `isContract` recipient check

---

## 🧪 Usage

```bash
slither src/UnsafeERC1155Transfer.sol \
  --detect unchecked-nft-transfer \
  --custom-detectors slither-custom-detectors
```