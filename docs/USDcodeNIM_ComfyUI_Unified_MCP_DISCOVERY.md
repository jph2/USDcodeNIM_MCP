---
arys_schema_version: '1.2'
id: c6d70445-6fc9-43ec-9a36-72c0a0c9dc76
title: USDcodeNIM + ComfyUI Unified MCP Discovery
type: STRATEGIC
status: active
trust_level: 2
created: '2026-02-23T22:34:23Z'
last_modified: '2026-02-23T22:34:23Z'
---

**Version**: 1.0.0 | **Date**: 23.02.2026 | **Time**: 23:20 | **GlobalID**: 20260223_2320_USDcodeNIM_MCP_UnifiedMCP_DISCOVERY_001

**Tag block:**
#mcp_protocol #comfyui #openusd #usd_core #workflow_automation #integration_pattern #deterministic_workflows #quality_assurance #analysis #backlog

# USDcodeNIM + ComfyUI Unified MCP Discovery

## TL;DR

Goal: define a no-copy-paste integration path where NIM code generation/validation and ComfyUI execution are orchestrated by one server workflow.

Current decision direction: prefer a single orchestration MCP that talks directly to NIM API + ComfyUI HTTP API, instead of MCP-server-to-MCP-server chaining.

## Problem Statement

Current workflow still requires manual copy/paste between:
- NIM-generated code (Cursor/MCP responses)
- ComfyUI execution inputs (`USD Dev Sandbox` node)

Desired workflow:
- prompt -> generate -> validate -> inject into workflow -> execute -> collect result
- no manual paste steps

## What We Verified

1. `USDcodeNIM_MCP` already has NIM tools:
   - `generate_usd_code`
   - `validate_usd_code`
2. ComfyUI MCP is active and supports workflow manipulation/execution.
3. ComfyUI MCP package in the active environment resolves to:
   - `comfyui-easy-mcp` (v0.2.2)
   - repo: `IO-AtelierTech/comfyui-mcp`

## Architecture Options

### Option A (recommended): Unified orchestration MCP

Extend `scripts/nim_mcp_server.py` (or create a sibling server) to include:
- NIM operations (existing)
- ComfyUI API client calls (new)

Proposed high-level tools:
- `nim_generate_validate_and_run`
- `comfy_set_sandbox_code`
- `comfy_run_workflow`
- `comfy_get_last_sandbox_result`

Pros:
- deterministic single control plane
- simplest UX for non-programmer operation
- easiest to log and debug end-to-end

Cons:
- higher implementation scope in one server

### Option B: Keep servers separate, add thin bridge script

A local bridge script calls both MCPs in sequence and returns combined output.

Pros:
- minimal changes to existing servers

Cons:
- extra glue layer and weaker long-term maintainability
- less clean product surface

### Option C: MCP-to-MCP direct server chaining

Not preferred. MCP servers are sibling endpoints under host orchestration; direct peer chaining adds complexity and fragility.

## Backlog-Ready Scope (Phase 1)

1. Add ComfyUI HTTP client to `USDcodeNIM_MCP`.
2. Add one end-to-end tool:
   - `nim_generate_validate_and_run(prompt, workflow_id, node_id, dry_run=true)`
3. Add safety controls:
   - explicit execute flag
   - workflow/node whitelist
   - timeout/retry + clear error contract
4. Emit structured run log (JSON) for post-run debugging.

## Non-Functional Requirements

- Keep API keys out of committed files (environment variables only).
- Return deterministic structured outputs (`success`, `error`, `trace_id`, `timing_ms`).
- Preserve "dry-run first" default behavior.

## Acceptance Criteria (for planning phase)

- One prompt can generate + validate + execute in ComfyUI without manual paste.
- Run output includes both NIM validation summary and ComfyUI execution result.
- Failure modes are explicit and actionable for non-programmer users.

---

## Links

1. <a id="link-1"></a>[USDcodeNIM_MCP README](../README.md) - Current NIM MCP capabilities and setup baseline.
2. <a id="link-2"></a>[USD Development Ecosystem Roadmap](../ROADMAP.md) - Backlog and phase planning document where this work item is tracked.
3. <a id="link-3"></a>[NVIDIA NIM Integration Guide](./NVIDIA_NIM_Integration_Guide.md) - Detailed NIM setup, operational behavior, and troubleshooting.
4. <a id="link-4"></a>[ComfyUI MCP Repository](https://github.com/IO-AtelierTech/comfyui-mcp) - Upstream ComfyUI MCP implementation source.
5. <a id="link-5"></a>[NVIDIA USDCode Model](https://build.nvidia.com/nvidia/usdcode) - NIM model entry point used by USDcodeNIM_MCP.

---
## Appendix: Raw Findings (copy-paste here)

**Purpose:** Paste your notes, links, snippets, and findings below. No need to place them in specific sections - paste anywhere in the block. Integrate into the discovery body when ready.

```
- User goal: eliminate manual copy/paste between NIM generation and ComfyUI execution.
- Local ComfyUI MCP metadata does not include repo URL directly.
- Package metadata in active venv resolves ComfyUI MCP package as comfyui-easy-mcp 0.2.2.
- Package Project-URL points to IO-AtelierTech/comfyui-mcp.
- Existing USDcodeNIM_MCP server already has generation+validation; orchestration gap is execution handoff.
```

