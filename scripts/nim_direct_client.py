#!/usr/bin/env python3
"""
Direct NVIDIA NIM Client (OpenAI-compatible)

This is a simpler alternative to the MCP server - a direct client that can be
used in scripts or integrated with tools that support OpenAI-compatible APIs.

Since NVIDIA NIM uses an OpenAI-compatible API, you can also configure Cursor
to use NIM directly as a custom AI provider if Cursor supports OpenAI-compatible endpoints.

Usage:
    python scripts/nim_direct_client.py "Generate a USD stage with a cube"
    
Environment Variables:
    NIM_API_KEY: Your NVIDIA NIM API key (required)
    NIM_ENDPOINT: Optional, defaults to USD code model endpoint
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    import httpx
except ImportError:
    print("Error: httpx not installed. Install with: pip install httpx", file=sys.stderr)
    sys.exit(1)


class NIMDirectClient:
    """
    Direct client for NVIDIA NIM API.
    
    This can be used as a drop-in replacement for OpenAI's client in many cases,
    since NIM uses an OpenAI-compatible API.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize NIM client.
        
        Args:
            api_key: NVIDIA NIM API key (or from NIM_API_KEY env var)
            endpoint: API endpoint URL
            model: Model name (defaults to "nvidia/usdcode-llama-3.1-70b-instruct")
        """
        self.api_key = api_key or os.getenv("NIM_API_KEY")
        if not self.api_key:
            raise ValueError(
                "NIM_API_KEY not provided. Set it as environment variable.\n"
                "Get your API key from: https://build.nvidia.com/nvidia/usdcode"
            )
        
        # Default endpoint for USD code model
        default_endpoint = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.endpoint = endpoint or os.getenv("NIM_ENDPOINT", default_endpoint)
        
        # Hardcoded fallback to ensure correct model is used if env var is missing or wrong
        default_model = "nvidia/usdcode-llama-3.1-70b-instruct"
        env_model = os.getenv("NIM_MODEL")
        
        # If env_model is "usdcode" (old default), override it with the correct one
        if env_model == "usdcode":
            self.model = default_model
        else:
            self.model = model or env_model or default_model
        
        self.client = httpx.AsyncClient(
            timeout=60.0,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send chat completion request.
        
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
            "top_p": 1,
            "expert_type": "auto",  # Merged directly into payload
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
            
            # Provide specific guidance for common errors
            if e.response.status_code == 404:
                error_msg += (
                    f"\n\n404 Not Found - The endpoint URL may be incorrect.\n"
                    f"Current endpoint: {self.endpoint}\n"
                    f"Current model: {self.model}\n\n"
                    f"Troubleshooting:\n"
                    f"1. Verify your API key is correct at: https://build.nvidia.com/nvidia/usdcode\n"
                    f"2. Check NVIDIA NIM documentation for the correct endpoint format\n"
                    f"3. Try setting NIM_ENDPOINT environment variable with the correct endpoint"
                )
            elif e.response.status_code == 401:
                error_msg += (
                    f"\n\n401 Unauthorized - API key may be invalid or expired.\n"
                    f"Verify your API key at: https://build.nvidia.com/nvidia/usdcode"
                )
            elif e.response.status_code == 403:
                error_msg += (
                    f"\n\n403 Forbidden - API key may not have access to this model.\n"
                    f"Check your API key permissions at: https://build.nvidia.com/nvidia/usdcode"
                )
            
            try:
                error_detail = e.response.json()
                error_msg += f"\n\nAPI Response: {json.dumps(error_detail)}"
            except:
                error_msg += f"\n\nAPI Response: {e.response.text}"
            
            raise RuntimeError(error_msg)
    
    async def generate_code(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate USD code from a prompt."""
        system_msg = """You are a USD (Universal Scene Description) code generation expert.
Generate clean, well-commented USD Python code following best practices."""
        
        user_msg = prompt
        if context:
            user_msg = f"Context: {context}\n\n{prompt}"
        
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
        
        response = await self.chat(messages, temperature=0.7)
        
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        
        raise RuntimeError("Failed to generate code")
    
    async def validate_code(self, code: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Validate USD code."""
        prompt = f"""Review this USD code and provide validation feedback:

```python
{code}
```

{f"Context: {context}" if context else ""}

Provide: errors, warnings, suggestions, and overall assessment.
Format as JSON with keys: valid, errors, warnings, suggestions, assessment."""
        
        messages = [
            {"role": "system", "content": "You are a USD code validation expert. Respond with valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.chat(messages, temperature=0.3)
        
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            try:
                return json.loads(content)
            except json.JSONDecodeError:
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
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


async def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python nim_direct_client.py <prompt>")
        print("Example: python nim_direct_client.py 'Generate a USD stage with a cube'")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    
    client = NIMDirectClient()
    try:
        code = await client.generate_code(prompt)
        print(code)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())

