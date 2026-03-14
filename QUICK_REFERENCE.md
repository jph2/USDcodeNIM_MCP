---
arys_schema_version: '1.2'
id: e4096d0f-2174-4392-9d34-818e67545544
title: NVIDIA NIM MCP - Quick Reference Guide
type: TECHNICAL
status: active
trust_level: 2
created: '2026-02-17T09:42:16Z'
last_modified: '2026-02-17T09:42:16Z'
---

**Version**: 1.0.0 | **Date**: 16.02.2026 | **Time**: 12:00 | **GlobalID**: 20260216_1200_USDcodeNIM_MCP_batch

**Tag block:**
#troubleshooting #reference #usd_core #vscode #v_model #creative #cursor #mcp_protocol #opencode #framework_integration #openusd #references #analysis #conversion #workflow_automation #ai_coding_agents #best_practices #deterministic_workflows

# NVIDIA NIM MCP - Quick Reference Guide

## 🚀 Quick Start

### 1. Get API Key
Visit: [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)

Navigate to the NVIDIA NIM platform and search for "USD code" or "usdcode" in the model catalog. Once you find the USD code model, sign in or create an account to access your API key. The API key will be displayed on the model's page after authentication.

### 2. Configure Cursor
Open Cursor and click the **cog wheel icon** in the upper right corner to access settings. Select **Cursor Settings**, then navigate to **Tools & MCP**. Click **Add a new MCP server** and paste the following JSON configuration into the file:

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

**Important:** Make sure to update the path to match your repository location and replace `your_api_key_here` with your actual API key. The configuration file is located at `C:\Users\<username>\.cursor\mcp.json` - if you already have other MCP servers configured, simply add the `nvidia-nim` entry to the existing `mcpServers` object.

### 3. Restart Cursor
Close and reopen Cursor completely.

### 4. Verify Connection
Settings → Tools & MCP → Check `nvidia-nim` is **green** ✅

---

## 💬 Using in Cursor Chat

### Generate USD Code
```
Generate a USD Python script that creates a red cube
```

### Validate USD Code
```
Validate this USD script using NVIDIA NIM
```
*(With a USD file open)*

### Ask USD Questions
```
What's the best way to create a USD stage?
```

### Fix USD Code
```
Fix this USD code: [paste code]
```

---

## 🧪 Terminal Testing

### Test Server
```powershell
# With environment variable
$env:NIM_API_KEY = "your_key"
python scripts/nim_mcp_server.py test

# Or pass key directly
python scripts/nim_mcp_server.py test "your_api_key_here"
```

### Generate Code
```powershell
python scripts/nim_direct_client.py "Create a USD stage with a sphere"
```

### Validate File
```powershell
python scripts/validate_with_nim.py path/to/script.py
python scripts/validate_with_nim.py path/to/script.py --context "Asset validation"
```

---

## 📋 Common Commands

| Task | Command |
|------|---------|
| Test MCP Server | `python scripts/nim_mcp_server.py test` |
| Generate Code | `python scripts/nim_direct_client.py "your prompt"` |
| Validate File | `python scripts/validate_with_nim.py file.py` |
| Check API Key | `echo $env:NIM_API_KEY` (PowerShell) |
| Install Dependencies | `pip install httpx` |

---

## 🔧 Troubleshooting

### MCP Server Red/Not Connected
- ✅ Check API key in `mcp.json`
- ✅ Verify Python path is correct
- ✅ Ensure `httpx` is installed
- ✅ Restart Cursor completely

### 403 Forbidden Error
- ✅ Check NVIDIA Build account credits
- ✅ Verify API key has model access
- ✅ Generate new API key if needed

### 404 Not Found Error
- ✅ Model name should be: `nvidia/usdcode-llama-3.1-70b-instruct`
- ✅ Endpoint should be: `https://integrate.api.nvidia.com/v1/chat/completions`

### Terminal Test Fails
- ✅ Set environment variable: `$env:NIM_API_KEY = "your_key"`
- ✅ Or pass key as argument: `python scripts/nim_mcp_server.py test "your_key"`

---

## 📁 File Locations

| File | Purpose |
|------|---------|
| `scripts/nim_mcp_server.py` | MCP server for Cursor |
| `scripts/nim_direct_client.py` | Standalone client |
| `scripts/validate_with_nim.py` | Validation script |
| `config/cursor_mcp_config.json` | Config template |
| `C:\Users\<user>\.cursor\mcp.json` | Your Cursor MCP config |

---

## 🎯 Example Prompts for Cursor

### Code Generation
- "Generate USD code to create a stage with a cube"
- "Write a USD script that exports geometry to USD file"
- "Create USD code for a material with texture"

### Code Validation
- "Validate this USD code using NVIDIA NIM"
- "Check if this follows USD best practices"
- "Review this USD script for errors"

### Learning
- "Explain USD layer composition"
- "What's the difference between Usd.Stage.CreateNew and CreateInMemory?"
- "How do I add materials to USD prims?"

### Debugging
- "Fix this USD code: [paste code]"
- "Why is this USD script failing?"
- "Optimize this USD code"

---

## ⚙️ Configuration

### Environment Variables
- `NIM_API_KEY` - Your NVIDIA NIM API key (required)
- `NIM_ENDPOINT` - API endpoint (default: `https://integrate.api.nvidia.com/v1/chat/completions`)
- `NIM_MODEL` - Model name (default: `nvidia/usdcode-llama-3.1-70b-instruct`)

### Model Information
- **Model Name:** `nvidia/usdcode-llama-3.1-70b-instruct`
- **Endpoint:** `https://integrate.api.nvidia.com/v1/chat/completions`
- **API Format:** OpenAI-compatible

---

## 📚 Resources

- **NVIDIA NIM:** [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)
- **NVIDIA Docs:** [docs.nvidia.com/nim/](https://docs.nvidia.com/nim/)
- **MCP Protocol:** [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **USD Docs:** [openusd.org](https://openusd.org/)

---

## ✅ Status Check

- [ ] API key obtained from NVIDIA Build
- [ ] API key added to `mcp.json`
- [ ] Model name set to `nvidia/usdcode-llama-3.1-70b-instruct`
- [ ] Cursor restarted
- [ ] MCP server shows green in Settings
- [ ] Terminal test works: `python scripts/nim_mcp_server.py test`
- [ ] Can generate code in Cursor chat
- [ ] Can validate code in Cursor chat

---

**Last Updated:** 2025-11-21  
**Version:** 1.0.0  
**Status:** ✅ Fully Operational

