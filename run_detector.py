#!/usr/bin/env python3
"""
CLI script to run slither with the missing ERC721 safeTransferFrom detector.
Usage: python run_detector.py <contract_file>
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'detectors'))

from slither import Slither
from missing_erc721_safetransfer import MissingERC721SafeTransferDetector
import logging

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_detector.py <contract_file>")
        sys.exit(1)
    
    contract_path = sys.argv[1]
    
    if not os.path.exists(contract_path):
        print(f"Error: Contract file {contract_path} not found")
        sys.exit(1)
    
    try:
        print(f"🔍 Running missing ERC721 safeTransferFrom detector on {contract_path}")
        print("=" * 60)
        
        # Initialize Slither
        slither = Slither(contract_path)
        
        # Create detector instance
        logger = logging.getLogger(__name__)
        compilation_unit = slither.compilation_units[0]
        detector = MissingERC721SafeTransferDetector(compilation_unit, slither, logger)
        
        # Run the detector
        results = detector._detect()
        
        if results:
            print(f"Found {len(results)} issues:\n")
            
            for i, result in enumerate(results, 1):
                print(f"Issue #{i}:")
                print(f"  Description: {result.data['description']}")
                print(f"  Impact: {result.data['impact']}")
                print(f"  Confidence: {result.data['confidence']}")
                print()
                
                # Show affected contracts and functions
                for element in result.elements:
                    if element['type'] == 'contract':
                        filename = element['source_mapping']['filename_short']
                        lines = element['source_mapping']['lines']
                        print(f"  📄 Contract: {element['name']} ({filename}#{lines[0]}-{lines[-1]})")
                    elif element['type'] == 'function':
                        filename = element['source_mapping']['filename_short']
                        lines = element['source_mapping']['lines']
                        print(f"  ⚠️  Function: {element['name']} ({filename}#{lines[0]}-{lines[-1]})")
                print()
        else:
            print("✅ No issues found! All ERC721 contracts appear to have both safeTransferFrom variants.")
        
        return len(results)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return -1

if __name__ == "__main__":
    issues_found = main()
    sys.exit(min(issues_found, 1))  # Exit with 1 if any issues found, 0 if clean