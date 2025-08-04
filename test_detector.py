#!/usr/bin/env python3
"""
Test script for the missing ERC721 safeTransferFrom detector.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'detectors'))

from slither import Slither
from missing_erc721_safetransfer import MissingERC721SafeTransferDetector

def test_detector():
    """Test the missing ERC721 safeTransferFrom detector."""
    
    # Initialize Slither with our test contract
    contract_path = "contracts/TestERC721.sol"
    
    if not os.path.exists(contract_path):
        print(f"Error: Contract file {contract_path} not found")
        return False
    
    try:
        # Initialize Slither
        slither = Slither(contract_path)
        
        # Create detector instance with proper arguments
        import logging
        logger = logging.getLogger(__name__)
        compilation_unit = slither.compilation_units[0]  # Get first compilation unit
        detector = MissingERC721SafeTransferDetector(compilation_unit, slither, logger)
        
        # Run the detector
        results = detector._detect()
        
        print(f"Detector found {len(results)} issues:")
        
        for i, result in enumerate(results, 1):
            print(f"\n--- Issue {i} ---")
            print("Description:", result.data['description'])
            
            # Extract contract names mentioned in the issue
            contracts_mentioned = []
            for element in result.elements:
                if element['type'] == 'contract':
                    contracts_mentioned.append(element['name'])
            print("Contracts mentioned:", contracts_mentioned)
        
        # Check if InsecureNFT was detected
        detected_insecure_nft = any("InsecureNFT" in str(result.data) for result in results)
        # Check if SecureNFT was wrongly detected
        detected_secure_nft = any("SecureNFT" in str(result.data) for result in results)
        
        if detected_insecure_nft and not detected_secure_nft:
            print("\n✅ SUCCESS: Correctly detected InsecureNFT and ignored SecureNFT!")
            return True
        elif detected_insecure_nft and detected_secure_nft:
            print("\n⚠️  PARTIAL SUCCESS: Detected InsecureNFT but also wrongly flagged SecureNFT!")
            return False
        elif not detected_insecure_nft:
            print(f"\n❌ FAILED: Expected to detect InsecureNFT, but found issues: {[str(r.data) for r in results]}")
            return False
        else:
            print("\n❌ FAILED: Unexpected state!")
            return False
            
    except Exception as e:
        print(f"Error running detector: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_detector()
    sys.exit(0 if success else 1)