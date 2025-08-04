from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function
from slither.slithir.operations import LowLevelCall, InternalCall, LibraryCall

class UncheckedNFTTransferDetector(AbstractDetector):
    ARGUMENT = "unchecked-nft-transfer"
    HELP = "Detects unchecked ERC1155 safeTransferFrom calls without require/assert checks"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    def _detect(self):
        results = []

        for contract in self.slither.contracts:
            for function in contract.functions:
                if not function.is_implemented:
                    continue

                for node in function.nodes:
                    for ir in node.irs:
                        # Detect all call types to safeTransferFrom
                        if isinstance(ir, (LowLevelCall, InternalCall, LibraryCall)):
                            func_name = getattr(ir, "function_name", None)
                            if func_name and "safeTransferFrom" in func_name and "1155" in func_name:
                                # Check if the node or its dominators contain require/assert
                                if not node.contains_require_or_assert():
                                    info = [
                                        function,
                                        f"Unchecked ERC1155 transfer in `{function.name}` at {node.source_mapping}"
                                    ]
                                    results.append(self.generate_result(info))

        return results