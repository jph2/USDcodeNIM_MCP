# NVIDIA NIM Integration Guide for Cursor

This guide explains how to integrate NVIDIA's NIM (NVIDIA Intelligent Model) USD code model into Cursor for enhanced USD development workflows.

## Overview

NVIDIA NIM provides specialized AI models for USD code generation and validation. This integration allows you to:

- **Generate USD code** using the specialized USD code model
- **Validate USD Python scripts** automatically
- **Get USD-specific suggestions** and best practices
- **Double-check generated code** for errors and improvements

## Quick Start

**Fastest way to get started:**

1. Get your API key from [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)
2. Set environment variable: `set NIM_API_KEY=your_key` (Windows) or `export NIM_API_KEY=your_key` (Linux/Mac)
3. Install dependencies: `pip install -r scripts/requirements_nim.txt`
4. Test validation: `python scripts/validate_with_nim.py scripts/validate_asset.py`

For full Cursor integration, continue with the setup steps below.

## Prerequisites

1. **NVIDIA NIM API Key**: Get your API key from [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)
2. **Python 3.10+** with `httpx` installed: `pip install httpx`
3. **Cursor IDE** with MCP support

## Setup Steps

### 1. Get Your NVIDIA NIM API Key

1. Visit [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)
2. Sign in with your NVIDIA account
3. Generate an API key
4. Copy the API key (you'll need it in the next step)

### 2. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:NIM_API_KEY = "your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set NIM_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export NIM_API_KEY=your_api_key_here
```

**Persistent Setup (Windows):**
Add to System Environment Variables or use `setx`:
```cmd
setx NIM_API_KEY "your_api_key_here"
```

### 3. Install Dependencies

```bash
pip install httpx
```

### 4. Configure Cursor MCP

Cursor stores MCP configuration in a specific location. The configuration file is provided at:
- `config/cursor_mcp_config.json`

**To use it:**

1. **Find your Cursor MCP config location:**
   - Windows: `%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
   - Or check Cursor Settings → Features → Model Context Protocol

2. **Add the NVIDIA NIM server configuration:**
   ```json
   {
     "mcpServers": {
       "nvidia-nim": {
         "command": "python",
         "args": [
           "E:\\SynologyDrive\\9999_LocalRepo\\USDcodeNIM_MCP\\scripts\\nim_mcp_server.py"
         ],
         "env": {
           "NIM_API_KEY": "${NIM_API_KEY}",
           "NIM_ENDPOINT": "https://integrate.api.nvidia.com/v1/chat/completions",
           "NIM_MODEL": "usdcode"
         }
       }
     }
   }
   ```

   **Important:** Update the path in `args` to match your actual project location.

3. **Restart Cursor** to load the new MCP server

### 5. Verify Installation

Test the MCP server manually:
```bash
python scripts/nim_mcp_server.py test
```

This should validate a sample USD code snippet and print results.

## Usage

### Option 1: Direct Client (Simplest)

Use the direct client for quick code generation or validation:

```bash
# Generate USD code
python scripts/nim_direct_client.py "Create a USD stage with a cube mesh"

# Or use programmatically in your scripts
from scripts.nim_direct_client import NIMDirectClient
import asyncio

async def example():
    client = NIMDirectClient()
    code = await client.generate_code("Create a USD stage")
    print(code)
    await client.close()

asyncio.run(example())
```

### Option 2: MCP Server Integration (Full Cursor Integration)

Once configured, you can use NIM through Cursor's AI features:

1. **Code Generation**: Ask Cursor to generate USD code, and it can use NIM for USD-specific suggestions
2. **Code Validation**: Use the validation script to check your USD Python files

### Standalone Validation Script

Validate any USD Python file using the standalone script:

```bash
# Basic validation
python scripts/validate_with_nim.py scripts/validate_asset.py

# With context
python scripts/validate_with_nim.py scripts/validate_asset.py --context "This script validates USD assets"
```

The script will:
- Read your USD Python file
- Send it to NVIDIA NIM for validation
- Report errors, warnings, and suggestions
- Provide an overall assessment

### Example Output

```
Reading file: scripts/validate_asset.py
Validating with NVIDIA NIM...

======================================================================
NIM VALIDATION RESULTS
======================================================================
✓ Status: VALID

Warnings (2):
  1. Consider adding type hints for better code clarity
  2. Some error messages could be more descriptive

Suggestions (1):
  1. Add docstring examples for common usage patterns

Assessment:
  The code follows USD best practices and uses proper pxr imports.
  Error handling is comprehensive. Minor improvements suggested above.
======================================================================
```

## MCP Server Features

The NIM MCP server provides these tools:

### `validate_usd_code`
Validates USD Python code and returns structured feedback.

**Parameters:**
- `code` (string): The USD code to validate
- `context` (string, optional): Context about what the code should do

**Returns:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": ["warning message"],
  "suggestions": ["suggestion"],
  "assessment": "Overall assessment"
}
```

### `generate_usd_code`
Generates USD code based on a prompt.

**Parameters:**
- `prompt` (string): Description of code to generate
- `context` (string, optional): Additional context

**Returns:**
```json
{
  "code": "generated code here"
}
```

## Troubleshooting

### "NIM_API_KEY not provided" Error

- Ensure the environment variable is set: `echo $NIM_API_KEY` (Linux/Mac) or `echo %NIM_API_KEY%` (Windows)
- Restart Cursor after setting the environment variable
- Check that the MCP config uses `${NIM_API_KEY}` syntax

### "httpx not installed" Error

```bash
pip install httpx
```

### MCP Server Not Connecting

1. Verify the Python path in the MCP config is correct
2. Test the server manually: `python scripts/nim_mcp_server.py test`
3. Check Cursor's MCP logs (usually in Developer Tools → Console)
4. Ensure Python is in your PATH

### API Rate Limits

NVIDIA NIM may have rate limits. If you encounter rate limit errors:
- Add delays between requests
- Use the validation script sparingly
- Consider caching validation results

## Advanced Configuration

### Custom Endpoint

If you're using a custom NIM endpoint:

```json
{
  "env": {
    "NIM_ENDPOINT": "https://your-custom-endpoint.com/v1/chat/completions"
  }
}
```

### Different Model

To use a different NIM model:

```json
{
  "env": {
    "NIM_MODEL": "your-model-name"
  }
}
```

## Integration with CI/CD

You can integrate NIM validation into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Validate USD Code with NIM
  env:
    NIM_API_KEY: ${{ secrets.NIM_API_KEY }}
  run: |
    python scripts/validate_with_nim.py scripts/validate_asset.py
```

## Security Notes

- **Never commit API keys** to version control
- Use environment variables or secret management systems
- The MCP config uses `${NIM_API_KEY}` to reference environment variables
- Consider using Cursor's built-in secret management if available

## Resources

- [NVIDIA NIM USD Code Model](https://build.nvidia.com/nvidia/usdcode)
- [NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [USD Python API Documentation](https://openusd.org/release/api/index.html)

## Support

For issues with:
- **NIM API**: Check [NVIDIA's documentation](https://docs.nvidia.com/nim/)
- **MCP Integration**: Check Cursor's MCP documentation
- **USD Code**: Refer to project guides in `docs/guides_Guardrails/`

---

**Last Updated**: 2025-11-21
**Version**: 1.0.0

