![Slither Analysis](https://img.shields.io/badge/slither-passed-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

slither . --detect unchecked-nft-transfer

## 🎥 Demo

![Detector Demo](demo.gif)

## 🧠 Slither Registry

This detector is compatible with Slither's custom registry.

To use:
```bash
slither . --detect unchecked-nft-transfer
```

---

### ✅ 6. **Optional JSON Output**

📄 Modify `detect_unchecked_nft_transfer.py`:

Add this at the end of `_detect()`:

```python
import json

if self.args.get("json"):
    print(json.dumps([r.json for r in results], indent=2))
```

slither . --detect unchecked-nft-transfer --json

## 🔮 Future Enhancements

- [ ] ERC777 and proxy-based transfer detection
- [ ] Delegatecall tracing
- [ ] MythX integration
- [ ] Severity scoring via Slither hooks

# TODO: Add ERC777 support
# TODO: Detect delegatecall-based transfer proxies
# TODO: Integrate with MythX for deeper analysis