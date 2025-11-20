#!/usr/bin/env python3
"""
USD Code Validation using NVIDIA NIM

This script validates USD Python code using NVIDIA's NIM USD code model.
It can be used standalone or integrated into CI/CD pipelines.

Usage:
    python scripts/validate_with_nim.py path/to/script.py
    python scripts/validate_with_nim.py path/to/script.py --context "This script creates a USD stage"
    
Environment Variables:
    NIM_API_KEY: Your NVIDIA NIM API key (required)
    NIM_ENDPOINT: Optional custom endpoint
    NIM_MODEL: Optional model name (defaults to "usdcode")
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
import asyncio

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.nim_mcp_server import NIMClient


async def validate_file(file_path: Path, context: Optional[str] = None) -> bool:
    """
    Validate a USD Python file using NIM.
    
    Args:
        file_path: Path to Python file to validate
        context: Optional context about what the file does
        
    Returns:
        True if validation passed, False otherwise
    """
    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return False
    
    print(f"Reading file: {file_path}")
    code = file_path.read_text(encoding="utf-8")
    
    print("Validating with NVIDIA NIM...")
    client = NIMClient()
    
    try:
        result = await client.validate_usd_code(code, context)
        
        print("\n" + "="*70)
        print("NIM VALIDATION RESULTS")
        print("="*70)
        
        valid = result.get("valid", False)
        errors = result.get("errors", [])
        warnings = result.get("warnings", [])
        suggestions = result.get("suggestions", [])
        assessment = result.get("assessment", "No assessment provided")
        
        if valid:
            print("✓ Status: VALID")
        else:
            print("✗ Status: INVALID")
        
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
        
        if warnings:
            print(f"\nWarnings ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                print(f"  {i}. {warning}")
        
        if suggestions:
            print(f"\nSuggestions ({len(suggestions)}):")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        
        print(f"\nAssessment:")
        print(f"  {assessment}")
        print("="*70 + "\n")
        
        return valid and len(errors) == 0
    
    except Exception as e:
        print(f"ERROR: Validation failed: {e}", file=sys.stderr)
        return False
    
    finally:
        await client.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate USD Python code using NVIDIA NIM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/validate_with_nim.py scripts/validate_asset.py
  python scripts/validate_with_nim.py scripts/validate_asset.py --context "Asset validation script"
        """
    )
    
    parser.add_argument(
        "file",
        type=Path,
        help="Path to USD Python file to validate"
    )
    
    parser.add_argument(
        "--context",
        type=str,
        help="Optional context about what the code does"
    )
    
    args = parser.parse_args()
    
    # Check for API key
    import os
    if not os.getenv("NIM_API_KEY"):
        print(
            "ERROR: NIM_API_KEY environment variable not set.\n"
            "Get your API key from: https://build.nvidia.com/nvidia/usdcode\n"
            "Set it with: set NIM_API_KEY=your_key_here (Windows) or export NIM_API_KEY=your_key_here (Linux/Mac)",
            file=sys.stderr
        )
        sys.exit(1)
    
    success = asyncio.run(validate_file(args.file, args.context))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

