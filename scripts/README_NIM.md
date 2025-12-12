# NVIDIA NIM Scripts - Reference Guide

> **Note:** For complete setup instructions, see the [README.md](../README.md) and [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) in the repository root. This guide focuses specifically on the scripts in this directory.

## Files in This Directory

1. **`nim_mcp_server.py`** - MCP server wrapper for Cursor integration
2. **`nim_direct_client.py`** - Simple direct client for standalone use
3. **`validate_with_nim.py`** - Validation script for USD Python files
4. **`requirements_nim.txt`** - Python dependencies

## Quick Setup

```bash
# 1. Install dependencies
pip install -r scripts/requirements_nim.txt

# 2. Set API key (IMPORTANT: Do NOT paste API key into scripts - use environment variable)
# See detailed instructions below

# 3. Test validation
python scripts/validate_with_nim.py scripts/validate_asset.py
```

## Setting the API Key (Environment Variable)

**IMPORTANT:** The API key should be set as an environment variable, NOT pasted into the Python scripts. All scripts automatically read from the `NIM_API_KEY` environment variable.

### Windows PowerShell (Recommended)

**For current session:**
```powershell
$env:NIM_API_KEY = "your_api_key_here"
```

**For persistent (survives restarts):**
```powershell
[System.Environment]::SetEnvironmentVariable("NIM_API_KEY", "your_api_key_here", "User")
```
*Note: Requires restarting PowerShell/terminal after setting*

**Verify it's set:**
```powershell
echo $env:NIM_API_KEY
```

### Windows Command Prompt (CMD)

**For current session:**
```cmd
set NIM_API_KEY=your_api_key_here
```

**For persistent (survives restarts):**
```cmd
setx NIM_API_KEY "your_api_key_here"
```
*Note: Requires opening a new CMD window after using setx*

**Verify it's set:**
```cmd
echo %NIM_API_KEY%
```

### Linux/Mac

**For current session:**
```bash
export NIM_API_KEY=your_api_key_here
```

**For persistent (add to ~/.bashrc or ~/.zshrc):**
```bash
echo 'export NIM_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Verify it's set:**
```bash
echo $NIM_API_KEY
```

### Why Environment Variables?

- ✅ **Security**: API keys are not stored in code files
- ✅ **Flexibility**: Change keys without editing code
- ✅ **Best Practice**: Avoid committing secrets to version control
- ✅ **MCP Compatible**: Cursor's MCP system reads environment variables automatically

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

For Cursor MCP setup instructions, see the [README.md](../README.md) Quick Start section. The `nim_mcp_server.py` script is used by Cursor's MCP system.

**Configuration file location:** `C:\Users\<username>\.cursor\mcp.json`

## Get API Key

For detailed API key setup instructions, see the [README.md](../README.md) Quick Start section.

**Quick steps:**
1. Visit [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)
2. Navigate to the NVIDIA NIM platform and search for "USD code" or "usdcode" in the model catalog
3. Sign in or create an account to access your API key
4. Set it as an environment variable using the instructions above

**Do NOT paste the API key into any Python script files!**

## Using in Cursor

For usage examples and prompts, see the [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) or [README.md](../README.md) Usage section.

## Full Documentation

- **Main Guide:** [README.md](../README.md) - Start here for setup
- **Quick Reference:** [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) - Condensed reference
- **Complete Guide:** [docs/NVIDIA_NIM_Integration_Guide.md](../docs/NVIDIA_NIM_Integration_Guide.md) - Detailed troubleshooting and advanced topics

