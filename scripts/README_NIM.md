# NVIDIA NIM Integration - Quick Reference

## Files Created

1. **`nim_mcp_server.py`** - MCP server wrapper for Cursor integration
2. **`nim_direct_client.py`** - Simple direct client for standalone use
3. **`validate_with_nim.py`** - Validation script for USD Python files
4. **`requirements_nim.txt`** - Python dependencies

## Quick Setup

```bash
# 1. Install dependencies
pip install -r scripts/requirements_nim.txt

# 2. Set API key
set NIM_API_KEY=your_key_here  # Windows
export NIM_API_KEY=your_key_here  # Linux/Mac

# 3. Test validation
python scripts/validate_with_nim.py scripts/validate_asset.py
```

## Usage Examples

### Validate USD Code
```bash
python scripts/validate_with_nim.py path/to/script.py
python scripts/validate_with_nim.py path/to/script.py --context "Asset validation script"
```

### Generate USD Code
```bash
python scripts/nim_direct_client.py "Create a USD stage with a cube"
```

### Use in Python Scripts
```python
from scripts.nim_direct_client import NIMDirectClient
import asyncio

async def main():
    client = NIMDirectClient()
    
    # Generate code
    code = await client.generate_code("Create a USD stage")
    print(code)
    
    # Validate code
    result = await client.validate_code(code)
    print(result)
    
    await client.close()

asyncio.run(main())
```

## Cursor MCP Configuration

Add to your Cursor MCP config (location varies by Cursor version):

```json
{
  "mcpServers": {
    "nvidia-nim": {
      "command": "python",
      "args": ["<full_path_to>/scripts/nim_mcp_server.py"],
      "env": {
        "NIM_API_KEY": "${NIM_API_KEY}"
      }
    }
  }
}
```

**Note:** Update the path in `args` to match your actual project location.

## Get API Key

Visit: https://build.nvidia.com/nvidia/usdcode

## Full Documentation

See `docs/NVIDIA_NIM_Integration_Guide.md` for complete setup instructions.

