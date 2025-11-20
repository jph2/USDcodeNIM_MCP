#!/usr/bin/env python3
"""
NVIDIA NIM MCP Server Wrapper

This script provides an MCP (Model Context Protocol) server interface
for NVIDIA NIM API, specifically configured for USD code generation and validation.

The NVIDIA NIM API is OpenAI-compatible, making it easy to integrate with
existing tools and workflows.

Usage:
    This server is typically run by Cursor's MCP system. To test manually:
    python scripts/nim_mcp_server.py

Environment Variables:
    NIM_API_KEY: Your NVIDIA NIM API key from build.nvidia.com
    NIM_ENDPOINT: Optional, defaults to USD code model endpoint
    NIM_MODEL: Optional model name, defaults to "usdcode"
"""

import os
import sys
import json
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import httpx
except ImportError:
    print("Error: httpx not installed. Install with: pip install httpx", file=sys.stderr)
    sys.exit(1)


class NIMClient:
    """Client for NVIDIA NIM API (OpenAI-compatible)."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        model: str = "usdcode"
    ):
        """
        Initialize NIM client.
        
        Args:
            api_key: NVIDIA NIM API key (or from NIM_API_KEY env var)
            endpoint: API endpoint URL (defaults to USD code model)
            model: Model name (defaults to "usdcode")
        """
        self.api_key = api_key or os.getenv("NIM_API_KEY")
        if not self.api_key:
            raise ValueError(
                "NIM_API_KEY not provided. Set it as environment variable or pass as argument.\n"
                "Get your API key from: https://build.nvidia.com/nvidia/usdcode"
            )
        
        # Default endpoint for USD code model
        default_endpoint = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.endpoint = endpoint or os.getenv("NIM_ENDPOINT", default_endpoint)
        self.model = model or os.getenv("NIM_MODEL", "usdcode")
        self.client = httpx.AsyncClient(
            timeout=60.0,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send chat completion request to NIM API.
        
        Args:
            messages: List of message dicts with "role" and "content"
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream responses
            
        Returns:
            Response dict with completion data
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        if stream:
            payload["stream"] = True
        
        try:
            response = await self.client.post(self.endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_msg = f"NIM API error: {e.response.status_code}"
            try:
                error_detail = e.response.json()
                error_msg += f" - {error_detail}"
            except:
                error_msg += f" - {e.response.text}"
            raise RuntimeError(error_msg)
    
    async def validate_usd_code(
        self,
        code: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate USD code using NIM model.
        
        Args:
            code: USD Python code or USDA/USDC code to validate
            context: Optional context about what the code should do
            
        Returns:
            Validation result with suggestions and errors
        """
        prompt = f"""You are a USD (Universal Scene Description) code expert. 
Review the following USD code and provide validation feedback.

Code to validate:
```python
{code}
```

{f"Context: {context}" if context else ""}

Please provide:
1. Syntax errors (if any)
2. USD API usage issues
3. Best practice violations
4. Suggestions for improvement
5. Overall assessment (valid/invalid with explanation)

Format your response as JSON with keys: valid, errors, warnings, suggestions, assessment.
"""
        
        messages = [
            {
                "role": "system",
                "content": "You are a USD code validation expert. Always respond with valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = await self.chat_completion(messages, temperature=0.3)
        
        # Extract content from response
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            try:
                # Try to parse as JSON
                return json.loads(content)
            except json.JSONDecodeError:
                # If not JSON, wrap in a structured format
                return {
                    "valid": True,
                    "errors": [],
                    "warnings": [],
                    "suggestions": [],
                    "assessment": content
                }
        
        return {
            "valid": False,
            "errors": ["Failed to get validation response"],
            "warnings": [],
            "suggestions": [],
            "assessment": "Unable to validate code"
        }
    
    async def generate_usd_code(
        self,
        prompt: str,
        context: Optional[str] = None
    ) -> str:
        """
        Generate USD code using NIM model.
        
        Args:
            prompt: Description of what code to generate
            context: Optional context about the project or requirements
            
        Returns:
            Generated code as string
        """
        system_prompt = """You are a USD (Universal Scene Description) code generation expert.
Generate clean, well-commented USD Python code following best practices:
- Use proper pxr imports
- Include error handling
- Add helpful comments for USD concepts
- Follow PEP 8 style guidelines
- Use pathlib for file operations
"""
        
        user_prompt = prompt
        if context:
            user_prompt = f"Context: {context}\n\n{prompt}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = await self.chat_completion(messages, temperature=0.7)
        
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        
        raise RuntimeError("Failed to generate code")
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


async def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle MCP protocol request.
    
    This is a simplified MCP handler. For full MCP protocol support,
    you would need to implement the complete MCP specification.
    """
    method = request.get("method")
    params = request.get("params", {})
    
    client = NIMClient()
    
    try:
        if method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "validate_usd_code":
                code = arguments.get("code", "")
                context = arguments.get("context")
                result = await client.validate_usd_code(code, context)
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": result
                }
            
            elif tool_name == "generate_usd_code":
                prompt = arguments.get("prompt", "")
                context = arguments.get("context")
                code = await client.generate_usd_code(prompt, context)
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"code": code}
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -32601, "message": f"Unknown method: {method}"}
            }
    
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {"code": -32603, "message": str(e)}
        }
    
    finally:
        await client.close()


async def main():
    """Main entry point for MCP server."""
    # Read from stdin (MCP protocol uses stdio)
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await handle_mcp_request(request)
            print(json.dumps(response), flush=True)
        
        except json.JSONDecodeError:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            }
            print(json.dumps(error_response), flush=True)
        
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    # Test mode: validate a sample code snippet
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        async def test():
            client = NIMClient()
            test_code = """
from pxr import Usd, UsdGeom

stage = Usd.Stage.CreateNew("test.usd")
xform = UsdGeom.Xform.Define(stage, "/World")
stage.GetRootLayer().Save()
"""
            result = await client.validate_usd_code(test_code)
            print(json.dumps(result, indent=2))
            await client.close()
        
        asyncio.run(test())
    else:
        # Run as MCP server
        asyncio.run(main())

