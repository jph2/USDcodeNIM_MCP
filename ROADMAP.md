# USD Development Ecosystem - Unified Roadmap

**Date:** 10.12.2025  
**Version:** 1.0.0  
**Status:** Active Development  
**Last Updated:** 10.12.2025

---

## Executive Summary

This roadmap consolidates learnings from MCP server comparisons, tool evaluations, and best practices analysis. It provides a unified development plan for the entire USD development ecosystem, including USDcodeNIM_MCP, ComfyUI nodes, and their integration.

---

## Current State

### What We Have

✅ **USDcodeNIM_MCP** - Python-based MCP server for NVIDIA NIM USD code generation
- 2 tools: `generate_usd_code`, `validate_usd_code`
- Cursor IDE integration
- Comprehensive error handling
- Python ecosystem (good for USD)

✅ **ComfyUI Nodes** - Visual USD workflow builder (29 production-ready nodes)
- Complete USD stage management (4 nodes)
- Primitive operations (4 nodes)
- Transform control (3 nodes)
- Material workflows (5 nodes) - including OpenPBR with 40+ parameters
- Variant management (2 nodes)
- Metadata & properties (2 nodes)
- Utility functions (2 nodes)
- Import & conversion (6 nodes) - Blender, Maya, Max, Rhino, C4D
- Debug & analysis (2 nodes)

### Ecosystem Context

✅ **usd-mcp-server** - Direct USD file manipulation (30+ tools)
✅ **NVIDIA Blog MCP** - RAG-powered documentation search
✅ **Griptape** - AI agent orchestration framework (optional)

---

## Roadmap Overview

### Phase 1: Quick Wins (Immediate - 1-2 weeks)
**Goal:** Improve user experience and configuration

### Phase 2: Enhancements (Short-term - 1-2 months)
**Goal:** Add features and expand compatibility

### Phase 3: Integration (Medium-term - 2-4 months)
**Goal:** Better integration with ecosystem tools

### Phase 4: Advanced Features (Long-term - 4+ months)
**Goal:** Advanced capabilities and optimizations

---

## Phase 1: Quick Wins (Immediate)

### 1.1 Add `.env` File Support ⏱️ 30 minutes

**Priority:** High  
**Effort:** Low  
**Impact:** High

**Description:**
Add automatic `.env` file loading for easier configuration.

**Implementation:**
```python
# Add to nim_mcp_server.py
from dotenv import load_dotenv
load_dotenv()  # Auto-load .env file
```

**Benefits:**
- Easier configuration for users
- Better developer experience
- Matches industry standard

**Dependencies:**
- `pip install python-dotenv`

**Status:** 🔴 Not Started

---

### 1.2 Expose More API Parameters ⏱️ 1 hour

**Priority:** Medium  
**Effort:** Low  
**Impact:** Medium

**Description:**
Expose NVIDIA NIM API parameters (temperature, top_p, max_tokens, expert_type) as tool parameters.

**Implementation:**
```python
# Update tool schemas
{
  "temperature": {"type": "number", "default": 0.7},
  "max_tokens": {"type": "integer", "default": 1024},
  "top_p": {"type": "number", "default": 1},
  "expert_type": {"type": "string", "default": "auto"}
}
```

**Benefits:**
- More control for advanced users
- Better model behavior tuning
- Matches ishandotsh implementation pattern

**Status:** 🔴 Not Started

---

### 1.3 Multi-Client Documentation ⏱️ 30 minutes

**Priority:** Medium  
**Effort:** Low  
**Impact:** Medium

**Description:**
Add configuration examples for Claude Desktop and OpenAI Codex.

**Implementation:**
- Update README.md with multi-client examples
- Add configuration templates

**Benefits:**
- Expand user base
- Support more AI development tools
- Better accessibility

**Status:** 🔴 Not Started

---

### 1.4 Improve Type Hints ⏱️ 1 hour

**Priority:** Low  
**Effort:** Low  
**Impact:** Low-Medium

**Description:**
Add comprehensive type hints using TypedDict for better IDE support.

**Implementation:**
```python
from typing import TypedDict

class GenerateCodeParams(TypedDict):
    prompt: str
    context: Optional[str]
    temperature: float
    max_tokens: Optional[int]
```

**Benefits:**
- Better IDE support
- Type checking with mypy
- Improved code quality

**Status:** 🔴 Not Started

---

## Phase 2: Enhancements (Short-term)

### 2.1 Enhanced Error Messages ⏱️ 2 hours

**Priority:** Medium  
**Effort:** Medium  
**Impact:** High

**Description:**
Improve error messages with more specific guidance and troubleshooting steps.

**Current:** Good error handling  
**Enhancement:** Add retry logic and better error recovery

**Status:** 🟡 In Progress (already good, minor improvements)

---

### 2.2 Code Validation Improvements ⏱️ 4 hours

**Priority:** Medium  
**Effort:** Medium  
**Impact:** Medium

**Description:**
Enhance code validation with:
- Syntax checking
- USD API usage validation
- Best practice suggestions
- Performance warnings

**Status:** 🔴 Not Started

---

### 2.3 Batch Operations ⏱️ 3 hours

**Priority:** Low  
**Effort:** Medium  
**Impact:** Medium

**Description:**
Add support for batch code generation/validation.

**Use Case:**
- Generate multiple USD scripts at once
- Validate multiple files
- Batch processing workflows

**Status:** 🔴 Not Started

---

### 2.4 Streaming Support ⏱️ 4 hours

**Priority:** Low  
**Effort:** Medium  
**Impact:** Low-Medium

**Description:**
Add streaming support for code generation (real-time output).

**Benefits:**
- Better UX for long generations
- Progressive output
- Faster perceived performance

**Status:** 🔴 Not Started

---

## Phase 3: Integration (Medium-term)

### 3.1 usd-mcp-server Integration ⏱️ 8 hours

**Priority:** High  
**Effort:** High  
**Impact:** High

**Description:**
Create integration patterns between USDcodeNIM_MCP and usd-mcp-server.

**Workflow:**
1. USDcodeNIM_MCP generates code
2. USDcodeNIM_MCP validates code
3. usd-mcp-server executes code or uses direct tools

**Benefits:**
- Complete USD development workflow
- Best of both worlds (AI + direct manipulation)
- Seamless integration

**Status:** 🔴 Not Started

**Dependencies:**
- usd-mcp-server installed
- Integration documentation

---

### 3.2 NVIDIA Blog MCP Integration ⏱️ 4 hours

**Priority:** Medium  
**Effort:** Medium  
**Impact:** Medium

**Description:**
Integrate with NVIDIA Blog MCP for documentation-aware code generation.

**Workflow:**
1. NVIDIA Blog MCP searches for best practices
2. USDcodeNIM_MCP generates code based on findings
3. USDcodeNIM_MCP validates against best practices

**Benefits:**
- Grounded code generation
- Best practice compliance
- Official documentation integration

**Status:** 🔴 Not Started

---

### 3.3 ComfyUI Nodes Integration ⏱️ 8 hours

**Priority:** High  
**Effort:** High  
**Impact:** High

**Description:**
Create integration between USDcodeNIM_MCP and ComfyUI nodes.

**Workflow Options:**

**Option A: Code Generation → ComfyUI Execution**
1. USDcodeNIM_MCP generates USD Python code
2. USDcodeNIM_MCP validates code
3. Convert code to ComfyUI workflow (or execute directly)
4. ComfyUI nodes execute/manipulate USD files

**Option B: Natural Language → ComfyUI Workflow**
1. USDcodeNIM_MCP generates ComfyUI workflow from natural language
2. User reviews/modifies workflow visually
3. ComfyUI executes workflow

**Option C: ComfyUI → Code Generation**
1. User builds workflow in ComfyUI
2. Export workflow as USD Python code
3. USDcodeNIM_MCP validates/improves code

**Benefits:**
- Best of both worlds (AI + visual workflows)
- Natural language to visual workflows
- Code validation for ComfyUI outputs
- Seamless integration

**Status:** 🔴 Not Started

**Dependencies:**
- ComfyUI nodes installed
- Integration patterns defined

---

### 3.4 Griptape Integration ⏱️ 6 hours

**Priority:** Low  
**Effort:** Medium  
**Impact:** Low

**Description:**
Create Griptape tools/agents that use USDcodeNIM_MCP.

**Use Case:**
- AI agent workflows
- Autonomous USD development
- Multi-tool orchestration

**Status:** 🔴 Not Started

**Note:** Lower priority - Griptape is for AI automation, not our primary use case

---

## 🚀 NEW: Omniverse MCP Server (The Missing Piece!)

### Vision: Chat Directly with Omniverse

**The Big Idea:** Build an MCP server that provides **direct, real-time control** of a running Omniverse instance - not just file manipulation or code generation, but **live interaction**.

**Status:** 🎯 Proposal Complete - Ready for Implementation

**Project Location:** [`OV_USD_Scripts/tools_Scripts_Extensions/00_Extensions/newExtension/omniverse_mcp_server/`](../../OV_Dev/OV_USD_Scripts/tools_Scripts_Extensions/00_Extensions/newExtension/omniverse_mcp_server/)

**Documentation:**
- **[README.md](../../OV_Dev/OV_USD_Scripts/tools_Scripts_Extensions/00_Extensions/newExtension/omniverse_mcp_server/README.md)** - Project overview (includes MCP server quick reference)
- **[PROPOSAL.md](../../OV_Dev/OV_USD_Scripts/tools_Scripts_Extensions/00_Extensions/newExtension/omniverse_mcp_server/docs/PROPOSAL.md)** - Full architecture and design proposal
- **[Extension README](../../OV_Dev/OV_USD_Scripts/tools_Scripts_Extensions/00_Extensions/newExtension/omniverse_mcp_server/extension/README.md)** - Extension details
- **[MCP Server README](../../OV_Dev/OV_USD_Scripts/tools_Scripts_Extensions/00_Extensions/newExtension/omniverse_mcp_server/mcp_server/README.md)** - Detailed MCP server documentation

**Key Features:**
- ✅ Live scene querying ("What's in the scene?")
- ✅ Real-time prim manipulation ("Move that cube")
- ✅ Viewport control ("Focus on this prim")
- ✅ Material operations ("Add red material")
- ✅ Extension control ("Execute this command")

**Architecture:**
```
AI Assistant → Omniverse MCP Server → Omniverse Kit Extension → Live Omniverse
```

**Priority:** 🔥 **HIGH** - This completes the ecosystem!

---

## ComfyUI Nodes Roadmap

### Current Status: ✅ Production Ready (v1.0.0)

**29 nodes** covering complete USD workflows:
- Stage management, prims, transforms, materials, variants, metadata, utilities, imports, debug

### ComfyUI Nodes Enhancements

#### C.1 AI Texture Generator Node ⏱️ 12 hours

**Priority:** Medium  
**Effort:** High  
**Impact:** Medium

**Description:**
Add node for AI-powered texture generation.

**Features:**
- Generate textures from prompts
- Material-aware texture generation
- Integration with OpenPBR materials

**Status:** 🔴 Not Started

---

#### C.2 Hydra Preview Node ⏱️ 16 hours

**Priority:** Medium  
**Effort:** High  
**Impact:** High

**Description:**
Add real-time USD preview using Hydra renderer.

**Features:**
- Live preview in ComfyUI
- Material visualization
- Scene inspection

**Status:** 🔴 Not Started

---

#### C.3 Animation Timeline Node ⏱️ 12 hours

**Priority:** Low  
**Effort:** High  
**Impact:** Medium

**Description:**
Add animation support for USD stages.

**Features:**
- Keyframe management
- Animation curves
- Timeline control

**Status:** 🔴 Not Started

---

#### C.4 Reference Manager Node ⏱️ 8 hours

**Priority:** Medium  
**Effort:** Medium  
**Impact:** Medium

**Description:**
Enhanced reference management for USD composition.

**Features:**
- Visual reference browser
- Reference resolution
- Composition debugging

**Status:** 🔴 Not Started

---

#### C.5 USDcodeNIM_MCP Integration Node ⏱️ 6 hours

**Priority:** High  
**Effort:** Medium  
**Impact:** High

**Description:**
Add ComfyUI node that calls USDcodeNIM_MCP for code generation.

**Features:**
- Natural language to USD code
- Code validation
- Workflow suggestions

**Status:** 🔴 Not Started

**Integration:**
- Connects USDcodeNIM_MCP with ComfyUI
- Enables AI-powered workflow generation

---

#### C.6 Workflow Template Library ⏱️ 8 hours

**Priority:** Medium  
**Effort:** Medium  
**Impact:** Medium

**Description:**
Create library of pre-built ComfyUI workflow templates.

**Templates:**
- Material library creation
- Scene analysis pipeline
- Multi-app import workflow
- Asset optimization pipeline

**Status:** 🔴 Not Started

---

## Phase 4: Advanced Features (Long-term)

### 4.1 Context-Aware Code Generation ⏱️ 16 hours

**Priority:** Medium  
**Effort:** High  
**Impact:** High

**Description:**
Enhance code generation with:
- Project context awareness
- File structure understanding
- Dependency detection
- Style consistency

**Status:** 🔴 Not Started

---

### 4.2 Code Refactoring Support ⏱️ 12 hours

**Priority:** Low  
**Effort:** High  
**Impact:** Medium

**Description:**
Add code refactoring capabilities:
- Optimize existing USD code
- Modernize API usage
- Performance improvements
- Best practice enforcement

**Status:** 🔴 Not Started

---

### 4.3 Learning from User Feedback ⏱️ Ongoing

**Priority:** Medium  
**Effort:** Ongoing  
**Impact:** High

**Description:**
Implement feedback loop:
- Collect user feedback
- Learn from common patterns
- Improve prompts
- Update best practices

**Status:** 🔴 Not Started

---

### 4.4 Multi-Model Support ⏱️ 8 hours

**Priority:** Low  
**Effort:** Medium  
**Impact:** Low

**Description:**
Support multiple NVIDIA NIM models:
- USD-specific models
- General code models
- Specialized models

**Status:** 🔴 Not Started

---

## Comparison Notes

### MCP Server Ecosystem

**usd-mcp-server:**
- ✅ Direct USD file manipulation (30+ tools)
- ✅ Production-ready
- ✅ Stateless operations
- **Integration:** Use together for complete workflow

**NVIDIA Blog MCP:**
- ✅ RAG-powered documentation search
- ✅ Grounded responses with citations
- ✅ Free cloud-hosted service
- **Integration:** Use for research before code generation

**USDcodeNIM_MCP (Ours):**
- ✅ AI-powered code generation
- ✅ Code validation
- ✅ Python ecosystem
- **Focus:** Learning and code generation

**Recommendation:** Use all three together for complete USD development ecosystem.

---

### Tool Comparisons

**Griptape vs ComfyUI:**
- **ComfyUI Nodes:** ✅ Use for visual USD workflows (recommended)
- **Griptape:** ⚠️ Only if you need AI automation

**ishandotsh Implementation:**
- **Learnings:** `.env` support, parameter exposure, simplicity
- **Adopt:** Quick wins from their approach
- **Keep:** Our multi-tool, comprehensive approach

---

## Success Metrics

### Phase 1 Success Criteria
- [ ] `.env` file support working
- [ ] More API parameters exposed
- [ ] Multi-client documentation complete
- [ ] Type hints improved

### Phase 2 Success Criteria
- [ ] Enhanced error messages
- [ ] Better code validation
- [ ] Batch operations working
- [ ] Streaming support (optional)

### Phase 3 Success Criteria
- [ ] Integration with usd-mcp-server documented
- [ ] Integration with NVIDIA Blog MCP working
- [ ] ComfyUI nodes integration working
- [ ] Integration examples provided

### ComfyUI Nodes Success Criteria
- [ ] AI Texture Generator node working
- [ ] Hydra Preview node working
- [ ] USDcodeNIM_MCP integration node working
- [ ] Workflow template library created

### Phase 4 Success Criteria
- [ ] Context-aware generation
- [ ] Refactoring support
- [ ] Feedback loop implemented

---

## Risk Assessment

### Low Risk
- ✅ Phase 1 items (quick wins)
- ✅ Documentation improvements
- ✅ Type hint improvements

### Medium Risk
- ⚠️ Integration work (compatibility issues)
- ⚠️ Advanced features (complexity)

### High Risk
- 🔴 Major architectural changes
- 🔴 Breaking changes

---

## Dependencies

### External Dependencies
- NVIDIA NIM API (required)
- Python 3.10+ (required)
- `httpx` library (required)
- `python-dotenv` (Phase 1.1)
- `mypy` (optional, for type checking)

### Internal Dependencies
- usd-mcp-server (for Phase 3.1)
- NVIDIA Blog MCP (for Phase 3.2)
- ComfyUI + ComfyUI Nodes (for Phase 3.3, C.5)
- USDcodeNIM_MCP (for ComfyUI integration node C.5)

---

## Timeline

### Q1 2025 (Jan-Mar)
- ✅ Complete Phase 1 (Quick Wins)
- 🟡 Start Phase 2 (Enhancements)

### Q2 2025 (Apr-Jun)
- ✅ Complete Phase 2 (Enhancements)
- 🟡 Start Phase 3 (Integration)

### Q3 2025 (Jul-Sep)
- ✅ Complete Phase 3 (Integration)
- 🟡 Start Phase 4 (Advanced Features)

### Q4 2025 (Oct-Dec)
- ✅ Complete Phase 4 (Advanced Features)
- 🟡 Maintenance and improvements

---

## Notes and Learnings

### From ishandotsh Implementation & Skywork Article
- ✅ Simplicity has value
- ✅ `.env` file support is convenient
- ✅ Expose more API parameters
- ✅ Multi-client support expands reach
- ✅ TypeScript type safety (apply to Python)
- ✅ **Mixture of Agents architecture** - NVIDIA USDCode uses 3 expert models
- ✅ **Real-world use cases validated** - Isaac Sim, learning, automation
- ✅ **Security considerations** - Local execution, HTTPS, explicit data sharing
- ✅ **Cost transparency** - Free software, paid API usage
- ✅ **Part of NVIDIA's agentic AI strategy** - NeMo Agent Toolkit integration

### From MCP Server Comparison
- ✅ Use all three MCP servers together
- ✅ Each serves different purpose
- ✅ Complete ecosystem approach

### From Griptape vs ComfyUI
- ✅ ComfyUI nodes are better for visual workflows
- ✅ Griptape only if AI automation needed
- ✅ Our ComfyUI nodes are production-ready

### From Tool Evaluations
- ✅ Multi-tool approach is better than single tool
- ✅ Comprehensive error handling is valuable
- ✅ Python ecosystem is right choice for USD

---

## Action Items

### Immediate (This Week)
1. [ ] Implement `.env` file support
2. [ ] Expose more API parameters
3. [ ] Add multi-client documentation
4. [ ] Update README with roadmap link

### Short-term (This Month)
1. [ ] Improve type hints
2. [ ] Enhance error messages
3. [ ] Add code validation improvements
4. [ ] Test integrations

### Medium-term (This Quarter)
1. [ ] Document usd-mcp-server integration
2. [ ] Document NVIDIA Blog MCP integration
3. [ ] Implement ComfyUI nodes integration (C.5)
4. [ ] Create integration examples
5. [ ] Gather user feedback

### ComfyUI Nodes (This Quarter)
1. [ ] Implement USDcodeNIM_MCP integration node (C.5)
2. [ ] Create workflow template library (C.6)
3. [ ] Plan Hydra Preview node (C.2)
4. [ ] Plan AI Texture Generator (C.1)

---

## Resources

### Documentation
- [MCP Server Comparison](./MCP_SERVER_COMPARISON.md)
- [Learnings from ishandotsh](./LEARNINGS_FROM_ISHANDOTSH.md)
- [Griptape vs ComfyUI](../OV_Dev/OV_USD_Scripts/tools_Scripts_Extensions/comfyui_nodes/GRIPTAPE_VS_COMFYUI_COMPARISON.md)
- [Omniverse MCP Server](../OV_Dev/OV_USD_Scripts/tools_Scripts_Extensions/00_Extensions/newExtension/omniverse_mcp_server/) - The missing piece: live Omniverse control

### External Links
- [NVIDIA NIM USDCode](https://build.nvidia.com/nvidia/usdcode)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [usd-mcp-server](https://github.com/TomBombadyl/usd-mcp-server)
- [NVIDIA Blog MCP](https://github.com/TomBombadyl/nvidia-blog)
- [ishandotsh Implementation](https://github.com/ishandotsh/nvidia-usdcode-mcp-server)
- [Skywork Analysis Article](https://skywork.ai/skypage/en/nvidia-usdcode-mcp-server/1981215663180709888) - Comprehensive guide and analysis

---

## Version History

### v1.0.0 (10.12.2025)
- Initial roadmap creation
- Consolidated learnings from comparisons
- Defined 4-phase development plan
- Documented action items and timeline

---

**Last Updated:** 10.12.2025  
**Next Review:** 17.12.2025  
**Status:** ✅ Active  
**Owner:** USDcodeNIM_MCP Development Team

---

## How to Use This Roadmap

1. **Review quarterly** - Update priorities and timelines
2. **Track progress** - Update status indicators (🔴 Not Started, 🟡 In Progress, ✅ Complete)
3. **Add learnings** - Document new insights in Notes section
4. **Adjust timeline** - Update based on actual progress
5. **Prioritize** - Focus on high-priority, high-impact items first

---

**🎯 Focus Areas:**
- **Phase 1:** Quick wins for immediate improvement
- **Phase 2:** Enhancements for better functionality
- **Phase 3:** Integration for ecosystem completeness
- **Phase 4:** Advanced features for power users
- **ComfyUI Nodes:** Enhancements and integration with USDcodeNIM_MCP

---

## Quick Reference: Key Decisions & Learnings

### MCP Server Ecosystem Strategy
**Decision:** Use all three MCP servers together
- **usd-mcp-server** → Direct USD file manipulation
- **USDcodeNIM_MCP** → AI code generation/validation
- **NVIDIA Blog MCP** → Documentation search
**Rationale:** Each serves different purpose, complementary

### ComfyUI vs Griptape
**Decision:** Stick with ComfyUI nodes for visual workflows
**Rationale:** Production-ready, 29 nodes, better for USD workflows
**Griptape:** Only if you need AI automation

### Implementation Approach
**Decision:** Adopt quick wins from ishandotsh, keep our comprehensive approach
**Quick Wins:**
- `.env` file support
- Expose more API parameters
- Multi-client documentation
- Better type hints

### Integration Priority
**High Priority:**
1. USDcodeNIM_MCP ↔ ComfyUI Nodes (C.5)
2. USDcodeNIM_MCP ↔ usd-mcp-server (3.1)
3. USDcodeNIM_MCP ↔ NVIDIA Blog MCP (3.2)

### Code Snippets

**`.env` File Support:**
```python
from dotenv import load_dotenv
load_dotenv()
NIM_API_KEY = os.getenv("NIM_API_KEY")
```

**Expose More Parameters:**
```python
{
  "temperature": {"type": "number", "default": 0.7},
  "max_tokens": {"type": "integer", "default": 1024},
  "top_p": {"type": "number", "default": 1},
  "expert_type": {"type": "string", "default": "auto"}
}
```

**Better Type Hints:**
```python
from typing import TypedDict

class GenerateCodeParams(TypedDict):
    prompt: str
    context: Optional[str]
    temperature: float
    max_tokens: Optional[int]
```

