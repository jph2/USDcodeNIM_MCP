# NVIDIA NIM Integration Guide for Cursor

This guide explains how to integrate NVIDIA's NIM (NVIDIA Intelligent Model) USD code model into Cursor for enhanced USD development workflows.

> **Quick Start:** See `QUICK_REFERENCE.md` in the repository root for a condensed version of this guide.

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

#### 2.1 Understanding Quotation Marks (For Beginners)

**Important for PowerShell users:** When setting environment variables in PowerShell, the quotation marks (`"`) are part of the command syntax, not part of the stored value.

**Example:**
```powershell
$env:NIM_API_KEY = "nvapi-abc123xyz"
```

**What gets stored:** `nvapi-abc123xyz` (without quotes)  
**What you see when checking:** `nvapi-abc123xyz` (no quotes)

The quotes are just PowerShell syntax to define a string. Your actual API key goes between the quotes, but the quotes themselves are not stored.

**Verify it worked:**
```powershell
echo $env:NIM_API_KEY
# Output: nvapi-abc123xyz (no quotes)
```

**Common mistakes to avoid:**

1. **Don't include extra quotes in your API key.** If NVIDIA gives you `nvapi-abc123`, use:
   - ✅ Correct: `$env:NIM_API_KEY = "nvapi-abc123"`
   - ❌ Wrong: `$env:NIM_API_KEY = ""nvapi-abc123""` (double quotes)

2. **Set the API key in the same terminal session** where you'll run the test. Environment variables are session-specific:
   - ✅ Correct: Set the key, then immediately test in the same terminal
   - ❌ Wrong: Set the key in one terminal, then test in a different terminal

3. **If your API key contains spaces** (rare), make sure the entire value is inside quotes:
   - ✅ Correct: `$env:NIM_API_KEY = "nvapi-key with spaces"`
   - ❌ Wrong: `$env:NIM_API_KEY = nvapi-key with spaces` (PowerShell will split on spaces)

#### 2.2 Setting the Environment Variable

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

**Note:** The quotation marks in `setx` are also just syntax - your API key value is stored without the quotes.

### 3. Install Dependencies

**Important:** If you're using a Python virtual environment (recommended), make sure it's activated before installing dependencies.

**Install httpx:**

```bash
# If using a virtual environment, activate it first:
# Windows PowerShell:
& C:/path/to/your/venv/Scripts/Activate.ps1

# Windows CMD:
C:\path\to\your\venv\Scripts\activate.bat

# Linux/Mac:
source /path/to/your/venv/bin/activate

# Then install httpx:
pip install httpx

# Or install from requirements file:
pip install -r scripts/requirements_nim.txt
```

**Verify installation:**
```bash
python -c "import httpx; print(f'httpx version: {httpx.__version__}')"
```

**Expected output:** `httpx version: 0.27.2` (or similar version number)

### 4. Configure Cursor MCP

Cursor stores MCP configuration in a specific location. The configuration file is provided at:
- `config/cursor_mcp_config.json`

**To use it:**

1. **Open Cursor's MCP Settings:**
   - Go to **Cursor Settings** → **Tools & MCP** (or use `Ctrl+,` and search for "MCP")
   - You should see the "Installed MCP Servers" section similar to the screenshot below:

   ![Cursor MCP Settings](images/cursor_mcp_settings.png)
   
   *Cursor's Tools & MCP settings page showing installed MCP servers*

2. **Add the NVIDIA NIM server:**
   - Click on **"New MCP Server"** or **"Add a Custom MCP Server"** button
   - Alternatively, you can manually edit the MCP configuration file:
   
   **Find your Cursor MCP config location:**
   - Windows: `%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
   - Or: `C:\Users\<username>\.cursor\mcp.json` (newer Cursor versions)
   - Or check Cursor Settings → Tools & MCP → View configuration file

3. **Add the NVIDIA NIM server configuration:**
   ```json
   {
     "mcpServers": {
       "nvidia-nim": {
         "command": "python",
         "args": [
           "C:\\path\\to\\USDcodeNIM_MCP\\scripts\\nim_mcp_server.py"
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

   **Important:** Replace `C:\\path\\to\\USDcodeNIM_MCP` with the actual path to your USDcodeNIM_MCP repository. For example:
   - `C:\\Users\\<username>\\USDcodeNIM_MCP\\scripts\\nim_mcp_server.py`
   - `D:\\Projects\\USDcodeNIM_MCP\\scripts\\nim_mcp_server.py`
   - Or use forward slashes: `C:/path/to/USDcodeNIM_MCP/scripts/nim_mcp_server.py`

3. **Restart Cursor** to load the new MCP server

### 5. Verify Installation

**Where to test:** Run this command in your **terminal/command prompt** (not inside Cursor's editor). You can use:
- **Windows PowerShell** (recommended)
- **Windows Command Prompt (CMD)**
- **Terminal** (Linux/Mac)
- **Cursor's integrated terminal** (View → Terminal or `` Ctrl+` ``)

**Steps to test:**

1. **Open a terminal/command prompt** (see options above)

2. **Navigate to the USDcodeNIM_MCP repository:**
   ```powershell
   # Windows PowerShell or CMD
   cd C:\path\to\USDcodeNIM_MCP
   
   # Linux/Mac
   cd /path/to/USDcodeNIM_MCP
   ```

3. **Run the test command:**
   ```bash
   # Option 1: Use environment variable (recommended)
   python scripts/nim_mcp_server.py test
   
   # Option 2: Pass API key directly as argument (for testing)
   python scripts/nim_mcp_server.py test "your_api_key_here"
   ```

4. **Expected results:**
   - ✅ **If API key is set correctly:** You'll see JSON output with validation results for a sample USD code snippet
   - ❌ **If API key is missing:** You'll see an error message: `NIM_API_KEY not provided...`
   - ❌ **If API key is invalid:** You'll see an API error message (401/403)
   
   **Note:** The test command reads the API key from:
   - Environment variable `NIM_API_KEY` (if set)
   - Command-line argument (if provided as second argument)
   - If neither is provided, it will show an error

**Example successful output:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [...],
  "suggestions": [...],
  "assessment": "..."
}
```

**Troubleshooting:**
- If you get `python: command not found`, try `python3` instead
- Make sure you're in the correct directory (where `scripts/nim_mcp_server.py` exists)
- **Most common issue:** The API key isn't set in the current terminal session. Set it in the same terminal where you're testing:
  ```powershell
  $env:NIM_API_KEY = "your_api_key_here"
  echo $env:NIM_API_KEY  # Verify it's set
  python scripts/nim_mcp_server.py test
  ```
- **If using a virtual environment:** Activate it first, then set the API key in the same session:
  ```powershell
  & C:/path/to/venv/Scripts/Activate.ps1
  $env:NIM_API_KEY = "your_api_key_here"
  python scripts/nim_mcp_server.py test
  ```
- Verify your API key is set: `echo $env:NIM_API_KEY` (PowerShell) or `echo %NIM_API_KEY%` (CMD)
- **If your API key has spaces:** Make sure you used quotes when setting it. Check with `echo $env:NIM_API_KEY` - if you only see part of the key, it was split on spaces. Re-set it with quotes: `$env:NIM_API_KEY = "your full key with spaces"`

## Usage

### Option 1: Using NVIDIA NIM in Cursor (Recommended)

Once the MCP server is connected (green status), you can use NVIDIA NIM directly in Cursor's chat:

#### Generate USD Code

**Example prompts:**
- "Generate a USD Python script that creates a red cube mesh"
- "Create a USD stage with a sphere using NVIDIA NIM"
- "Write USD code to export a mesh to a USD file"
- "Generate USD code for a material with a texture"

**How it works:**
1. Open Cursor's chat (Ctrl+L or Cmd+L)
2. Type your prompt asking for USD code generation
3. Cursor will use the NVIDIA NIM MCP server to generate USD-specific code
4. The generated code will be tailored for USD/Omniverse development

#### Validate USD Code

**Example prompts:**
- "Validate this USD script using NVIDIA NIM" (with a file open)
- "Check if this USD code follows best practices"
- "Review this USD Python file for errors"

**How it works:**
1. Open a USD Python file in Cursor
2. Ask Cursor to validate it using NVIDIA NIM
3. Get structured feedback: errors, warnings, suggestions, and assessment

#### Ask USD Questions

**Example prompts:**
- "What's the best way to create a USD stage?"
- "How do I add materials to USD prims?"
- "Explain USD layer composition"

**How it works:**
- Cursor can use NVIDIA NIM's USD expertise to answer your questions
- Get USD-specific guidance and best practices

### Option 2: Direct Client (Standalone Scripts)

Use the direct client for quick code generation or validation outside of Cursor:

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

### Option 3: Validation Script (CI/CD Integration)

Use the validation script for automated checks:

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
- **Important:** Set the API key in the same terminal session where you're testing

### "404 Not Found" Error (API Endpoint)

If you get a `404 Not Found` error when testing:

1. **Verify your API key format:**
   - Check that your API key is correct at [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)
   - API keys typically start with `nvapi-`

2. **Check the endpoint URL:**
   - The default endpoint is: `https://integrate.api.nvidia.com/v1/chat/completions`
   - NVIDIA may have updated the endpoint format - check their latest documentation
   - Try setting a custom endpoint if needed:
     ```powershell
     $env:NIM_ENDPOINT = "https://integrate.api.nvidia.com/v1/nim/usdcode/chat/completions"
     ```

3. **Verify model name:**
   - Default model is `nvidia/usdcode-llama-3.1-70b-instruct`
   - Check if NVIDIA requires a different model identifier
   - Try setting a custom model:
     ```powershell
     $env:NIM_MODEL = "your-model-name"
     ```

4. **Check NVIDIA NIM documentation:**
   - Visit [NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)
   - Look for the correct endpoint format for your API key type
   - Some API keys may require different endpoint URLs

### "401 Unauthorized" or "403 Forbidden" Error

- Your API key may be invalid or expired
- Check your API key at [build.nvidia.com/nvidia/usdcode](https://build.nvidia.com/nvidia/usdcode)
- Verify the API key has access to the USD code model
- Regenerate the API key if needed

### "httpx not installed" Error

```bash
pip install httpx
```

### MCP Server Not Connecting

1. Verify the Python path in the MCP config is correct
2. Test the server manually: `python scripts/nim_mcp_server.py test`
3. Check Cursor's MCP logs (usually in Developer Tools → Console)
4. Ensure Python is in your PATH
5. Make sure the API key is set in the environment where Cursor runs

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

## Common Use Cases & Examples

### Use Case 1: Generate USD Script from Scratch

**In Cursor Chat:**
```
Generate a USD Python script that:
- Creates a new USD stage
- Adds a cube mesh at /World/Cube
- Applies a red material
- Saves to output.usd
```

**Expected Result:** Complete, working USD Python code with proper imports and error handling.

### Use Case 2: Validate Existing USD Code

**In Cursor Chat:**
```
Validate this USD script using NVIDIA NIM and suggest improvements
```
*(With a USD Python file open)*

**Expected Result:** Structured feedback with:
- Errors (if any)
- Warnings
- Suggestions for improvement
- Overall assessment

### Use Case 3: Fix USD Code Issues

**In Cursor Chat:**
```
This USD code has an error. Fix it using NVIDIA NIM best practices:
[Paste your code]
```

**Expected Result:** Corrected code with explanations of what was wrong.

### Use Case 4: Learn USD Concepts

**In Cursor Chat:**
```
Explain USD layer composition with examples
```

**Expected Result:** Detailed explanation with USD-specific examples and best practices.

### Use Case 5: Batch Validation (CI/CD)

**In Terminal:**
```bash
# Validate all USD scripts in a directory
for file in scripts/*.py; do
    python scripts/validate_with_nim.py "$file"
done
```

**Expected Result:** Validation results for each file, suitable for CI/CD pipelines.

## Troubleshooting

### MCP Server Shows Red/Not Connected

**Symptoms:**
- Server appears red in Cursor Settings → Tools & MCP
- Error: "No server info found" in logs

**Solutions:**
1. **Check API Key:** Verify `NIM_API_KEY` is set correctly in `mcp.json`
2. **Check Python Path:** Ensure Python is in PATH or use full path in config
3. **Check Script Path:** Verify the path to `nim_mcp_server.py` is correct
4. **Check httpx:** Ensure `httpx` is installed: `pip install httpx`
5. **Restart Cursor:** Fully close and restart Cursor after config changes
6. **Check Logs:** View Output → MCP logs for specific error messages

### API Returns 403 Forbidden

**Cause:** API key doesn't have access to the model or credits are exhausted.

**Solutions:**
1. Check your NVIDIA Build account credits
2. Verify API key has access to `nvidia/usdcode-llama-3.1-70b-instruct`
3. Generate a new API key if needed
4. Check NVIDIA Build dashboard for account status

### API Returns 400 Bad Request

**Cause:** Invalid request format or parameters.

**Solutions:**
1. Ensure model name is correct: `nvidia/usdcode-llama-3.1-70b-instruct`
2. Check that `expert_type` parameter is included (should be automatic)
3. Verify endpoint URL is correct

### Terminal Test Works But Cursor Doesn't

**Cause:** Different Python environments or missing environment variables.

**Solutions:**
1. Use absolute Python path in `mcp.json`
2. Ensure `httpx` is installed in the Python environment Cursor uses
3. Hardcode API key in `mcp.json` (as we did) instead of relying on env vars

## Support

For issues with:
- **NIM API**: Check [NVIDIA's documentation](https://docs.nvidia.com/nim/)
- **MCP Integration**: Check Cursor's MCP documentation
- **USD Code**: Refer to project guides in `docs/guides_Guardrails/`

## Final Notes

✅ **Integration Complete:** NVIDIA NIM MCP server is now fully integrated with Cursor.

✅ **Verified Working:** Both terminal testing and Cursor MCP integration are functional.

✅ **Ready for Production:** The integration can be used for:
- USD code generation
- USD code validation
- USD best practices guidance
- Learning USD concepts

**Remember:**
- API key is stored in `mcp.json` for Cursor's use
- Terminal tests require environment variable or command-line argument
- Both methods work independently and can be used as needed

---

**Last Updated**: 2025-11-21
**Version**: 1.0.0
**Status**: ✅ Fully Operational

