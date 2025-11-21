# MCP Configuration Template

This directory contains the template configuration file for integrating NVIDIA NIM with Cursor IDE.

## File: `cursor_mcp_config.json`

This is a **template** file showing the structure needed for Cursor's MCP configuration.

### Important Notes:

1. **API Key Options:**
   - **Option 1 (Environment Variable):** Use `${NIM_API_KEY}` to read from your system environment variables
   - **Option 2 (Hardcoded):** Replace `${NIM_API_KEY}` with your actual API key directly in the file
   
   **Recommendation:** For local development, hardcoding the key in your actual `mcp.json` file is simpler and works reliably. For sharing/configuring multiple machines, use environment variables.

2. **Path Configuration:**
   - Replace `C:\\path\\to\\USDcodeNIM_MCP` with your actual repository path
   - Use forward slashes (`/`) or escaped backslashes (`\\`) for Windows paths
   - Example: `E:\\SynologyDrive\\9999_LocalRepo\\USDcodeNIM_MCP\\scripts\\nim_mcp_server.py`

3. **Model Name:**
   - The model name is set to: `nvidia/usdcode-llama-3.1-70b-instruct`
   - This is the correct model identifier for NVIDIA's USD code model

## Where to Place This Configuration

Copy the contents of this template into your Cursor MCP configuration file:

**Windows:** `C:\Users\<username>\.cursor\mcp.json`

**Note:** If you already have other MCP servers configured, merge this configuration into the existing `mcpServers` object.

## Example: Hardcoded API Key (Recommended for Local Use)

```json
{
  "mcpServers": {
    "nvidia-nim": {
      "command": "python",
      "args": [
        "E:\\SynologyDrive\\9999_LocalRepo\\USDcodeNIM_MCP\\scripts\\nim_mcp_server.py"
      ],
      "env": {
        "NIM_API_KEY": "nvapi-your-actual-key-here",
        "NIM_ENDPOINT": "https://integrate.api.nvidia.com/v1/chat/completions",
        "NIM_MODEL": "nvidia/usdcode-llama-3.1-70b-instruct"
      }
    }
  }
}
```

## Example: Using Environment Variable

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
        "NIM_MODEL": "nvidia/usdcode-llama-3.1-70b-instruct"
      }
    }
  }
}
```

**Note:** When using `${NIM_API_KEY}`, make sure the environment variable is set in the same context where Cursor runs (may require system-level environment variable configuration).

---

**Last Updated:** 2025-11-21

