from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Contract


class MissingERC721SafeTransferDetector(AbstractDetector):
    ARGUMENT = "missing-erc721-safetransfer"
    HELP = "Detects ERC721 contracts that implement safeTransferFrom(address,address,uint256) but miss the required 4-argument version with bytes data"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    def _detect(self):
        results = []

        for contract in self.slither.contracts:
            if not contract.is_interface:
                has_three_arg_safe_transfer = False
                has_four_arg_safe_transfer = False
                three_arg_function = None

                # Check all functions in the contract
                for function in contract.functions:
                    if function.name == "safeTransferFrom":
                        # Check for 3-argument version: safeTransferFrom(address,address,uint256)
                        if len(function.parameters) == 3:
                            param_types = [str(param.type) for param in function.parameters]
                            if (param_types == ["address", "address", "uint256"]):
                                has_three_arg_safe_transfer = True
                                three_arg_function = function
                        
                        # Check for 4-argument version: safeTransferFrom(address,address,uint256,bytes)
                        elif len(function.parameters) == 4:
                            param_types = [str(param.type) for param in function.parameters]
                            if (param_types == ["address", "address", "uint256", "bytes"]):
                                has_four_arg_safe_transfer = True

                # If contract has 3-arg but missing 4-arg safeTransferFrom
                if has_three_arg_safe_transfer and not has_four_arg_safe_transfer:
                    info = [
                        "ERC721 contract ",
                        contract,
                        " implements safeTransferFrom(address,address,uint256) in ",
                        three_arg_function,
                        " but is missing the required 4-argument version safeTransferFrom(address,address,uint256,bytes)\n"
                    ]
                    results.append(self.generate_result(info))

        return results