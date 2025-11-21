# USDcodeNIM_MCP

NVIDIA NIM (NVIDIA Intelligent Model) integration for Cursor IDE, specifically configured for USD (Universal Scene Description) code generation and validation.

## Overview

This repository provides tools and configurations to integrate NVIDIA's specialized USD code model into Cursor IDE through the Model Context Protocol (MCP). It enables:

- **USD Code Generation** using NVIDIA's specialized USD code model
- **Automated Code Validation** with structured feedback
- **USD-Specific Suggestions** and best practices
- **Double-Checking** generated code for errors and improvements

## Quick Start

1. **Get your API key** from [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)

2. **Set environment variable:**
   ```powershell
   $env:NIM_API_KEY = "your_api_key_here"  # Windows PowerShell
   ```
   ```cmd
   set NIM_API_KEY=your_api_key_here  # Windows CMD
   ```
   ```bash
   export NIM_API_KEY=your_api_key_here  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r scripts/requirements_nim.txt
   ```

4. **Test the integration:**
   ```bash
   python scripts/nim_mcp_server.py test
   ```

## Repository Structure

```
USDcodeNIM_MCP/
├── scripts/
│   ├── nim_mcp_server.py      # MCP server wrapper for Cursor integration
│   ├── nim_direct_client.py    # Direct client for standalone use
│   ├── validate_with_nim.py   # Validation script for USD Python files
│   ├── requirements_nim.txt    # Python dependencies
│   └── README_NIM.md          # Quick reference guide
├── config/
│   └── cursor_mcp_config.json  # Cursor MCP configuration template
├── docs/
│   └── NVIDIA_NIM_Integration_Guide.md  # Complete setup documentation
└── README.md                  # This file
```

## Features

### 1. MCP Server Integration
Full Cursor IDE integration through Model Context Protocol, providing USD code generation and validation tools.

### 2. Direct Client
Standalone Python client for use in scripts, CI/CD pipelines, or other tools.

### 3. Code Validation
Automated validation of USD Python code with structured feedback (errors, warnings, suggestions).

### 4. Code Generation
Generate USD code from natural language prompts using NVIDIA's specialized model.

## Usage

### Using in Cursor (Recommended) ✨

Once configured, use NVIDIA NIM directly in Cursor's chat:

**Generate USD Code:**
```
Generate a USD Python script that creates a red cube mesh
```

**Validate USD Code:**
```
Validate this USD script using NVIDIA NIM
```
*(With a USD file open)*

**Ask USD Questions:**
```
What's the best way to create a USD stage?
```

### Standalone Validation
```bash
python scripts/validate_with_nim.py path/to/usd_script.py
python scripts/validate_with_nim.py path/to/usd_script.py --context "Asset validation script"
```

### Code Generation
```bash
python scripts/nim_direct_client.py "Create a USD stage with a cube mesh"
```

### Programmatic Use
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

To integrate with Cursor IDE:

1. **Get your API key** from [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)
2. **Edit your MCP config:** `C:\Users\<username>\.cursor\mcp.json`
3. **Add the NVIDIA NIM server** configuration from `config/cursor_mcp_config.json`
4. **Update the path** in the config to match your repository location
5. **Set your API key** in the `env.NIM_API_KEY` field
6. **Set model name:** `nvidia/usdcode-llama-3.1-70b-instruct`
7. **Restart Cursor** completely

**Quick Setup:**
```json
{
  "mcpServers": {
    "nvidia-nim": {
      "command": "python",
      "args": ["C:\\path\\to\\USDcodeNIM_MCP\\scripts\\nim_mcp_server.py"],
      "env": {
        "NIM_API_KEY": "your_api_key_here",
        "NIM_MODEL": "nvidia/usdcode-llama-3.1-70b-instruct"
      }
    }
  }
}
```

See `docs/NVIDIA_NIM_Integration_Guide.md` for detailed setup instructions.
See `QUICK_REFERENCE.md` for a quick reference guide.

## Requirements

- Python 3.10+
- `httpx` library (install via `pip install -r scripts/requirements_nim.txt`)
- NVIDIA NIM API key from [build.nvidia.com](https://build.nvidia.com/nvidia/usdcode)
- Cursor IDE (for MCP integration)

## Documentation

- **Quick Reference**: `QUICK_REFERENCE.md` (start here!)
- **Scripts Guide**: `scripts/README_NIM.md`
- **Complete Guide**: `docs/NVIDIA_NIM_Integration_Guide.md`
- **Configuration**: `config/cursor_mcp_config.json`

## Resources

- [NVIDIA NIM USD Code Model](https://build.nvidia.com/nvidia/usdcode)
- [NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [USD Python API Documentation](https://openusd.org/release/api/index.html)

## License

This project is provided as-is for integration with NVIDIA NIM services.

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-21

