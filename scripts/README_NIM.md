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

1. Visit [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)
2. Sign in with your NVIDIA account
3. Generate an API key
4. Copy the API key
5. Set it as an environment variable using the instructions above

**Do NOT paste the API key into any Python script files!**

## Using in Cursor

Once configured, use NVIDIA NIM directly in Cursor's chat:

**Generate USD Code:**
- "Generate a USD Python script that creates a red cube"
- "Create USD code for a material with texture"

**Validate USD Code:**
- "Validate this USD script using NVIDIA NIM" (with file open)
- "Check if this follows USD best practices"

**Ask Questions:**
- "What's the best way to create a USD stage?"
- "Explain USD layer composition"

## Full Documentation

- **Complete Guide:** `docs/NVIDIA_NIM_Integration_Guide.md`
- **Quick Reference:** `QUICK_REFERENCE.md` (in repository root)

