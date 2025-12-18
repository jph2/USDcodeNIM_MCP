# Omniverse MCP Server - Proposal & Architecture

**Date:** 10.12.2025  
**Purpose:** Design an MCP server that provides direct, real-time control of Omniverse runtime  
**Status:** 🎯 Vision Document

---

## Executive Summary

**The Missing Piece:** An MCP server that enables **direct chat-based control** of a running Omniverse instance, not just file manipulation or code generation, but **live interaction** with Omniverse.

**Vision:** Chat with Omniverse directly - "Move that cube", "Add a light here", "What's in the scene?" - and have it happen in real-time.

---

## Current State Analysis

### What We Have

✅ **usd-mcp-server** - File manipulation (30+ tools)
- Works on USD files
- Stateless operations
- **Gap:** No live Omniverse connection

✅ **USDcodeNIM_MCP** - Code generation
- Generates USD Python code
- Validates code
- **Gap:** Code needs to be executed separately

✅ **ComfyUI Nodes** - Visual workflows
- 29 production-ready nodes
- Visual USD workflows
- **Gap:** Not integrated with Omniverse runtime

### What's Missing

❌ **Live Omniverse Control**
- Direct chat with running Omniverse instance
- Real-time scene manipulation
- Live querying and inspection
- Extension/application control

---

## Architecture Proposal

### High-Level Architecture

```
AI Assistant (Cursor/Claude)
    ↓
Omniverse MCP Server (New)
    ↓
Omniverse Kit Extension (New)
    ↓
Omniverse Runtime (Live)
```

### Component Breakdown

#### 1. **Omniverse MCP Server** (Python)
- MCP protocol implementation
- Tool definitions for Omniverse operations
- Communication bridge to Omniverse extension

#### 2. **Omniverse Kit Extension** (Python)
- Runs inside Omniverse
- Exposes HTTP/WebSocket API
- Provides live Omniverse control
- Uses `omni.usd`, `omni.kit.commands`, etc.

#### 3. **Communication Layer**
- HTTP REST API (for MCP server ↔ Extension)
- WebSocket (for real-time updates)
- JSON-RPC or similar protocol

---

## What We Have to Build This

### ✅ Existing Pieces

1. **Omniverse Kit Application** (`Kit_APP_109`)
   - ✅ Kit application template
   - ✅ Extension structure
   - ✅ Python extension examples

2. **Omniverse Python API Knowledge**
   - ✅ `omni.usd` usage in scripts
   - ✅ `omni.kit.commands` examples
   - ✅ Extension patterns

3. **MCP Server Experience**
   - ✅ USDcodeNIM_MCP implementation
   - ✅ MCP protocol understanding
   - ✅ Tool definition patterns

4. **USD Operations**
   - ✅ 29 ComfyUI nodes (reference implementation)
   - ✅ USD manipulation patterns
   - ✅ Best practices

### ❌ Missing Pieces

1. **HTTP/WebSocket Server in Omniverse Extension**
   - Need to add HTTP server to Kit extension
   - WebSocket for real-time updates
   - API endpoint design

2. **MCP Server ↔ Extension Communication**
   - Protocol definition
   - Authentication/security
   - Error handling

3. **Live Omniverse Control Tools**
   - Scene querying (live)
   - Prim manipulation (live)
   - Viewport control
   - Extension management

---

## Proposed Tool Set

### Stage Management (Live)
- `getLiveStage` - Get current stage from Omniverse
- `listLivePrims` - List prims in live scene
- `getLivePrimInfo` - Get prim info from live scene
- `createLivePrim` - Create prim in live scene
- `deleteLivePrim` - Delete prim from live scene

### Transform Control (Live)
- `getLiveTransform` - Get transform from live prim
- `setLiveTransform` - Set transform on live prim
- `movePrim` - Move prim in scene
- `rotatePrim` - Rotate prim
- `scalePrim` - Scale prim

### Material Operations (Live)
- `listLiveMaterials` - List materials in scene
- `createLiveMaterial` - Create material in scene
- `bindLiveMaterial` - Bind material to prim
- `getLiveMaterialBinding` - Get material binding

### Viewport Control
- `getViewportInfo` - Get active viewport info
- `setCamera` - Set camera position/rotation
- `getScreenshot` - Capture viewport screenshot
- `focusOnPrim` - Focus viewport on prim

### Scene Querying (Live)
- `queryScene` - Natural language scene query
- `findPrims` - Find prims by criteria
- `getSceneStats` - Get scene statistics
- `getSelection` - Get current selection

### Extension Control
- `listExtensions` - List loaded extensions
- `executeCommand` - Execute Kit command
- `getExtensionInfo` - Get extension details

---

## Implementation Approach

### Phase 1: Foundation (Week 1-2)

**1.1 Create Omniverse Kit Extension with HTTP Server**
```python
# Extension that runs HTTP server inside Omniverse
import omni.ext
import asyncio
from aiohttp import web

class OmniverseMCPExtension(omni.ext.IExt):
    def on_startup(self):
        # Start HTTP server
        self.app = web.Application()
        self.app.router.add_get('/api/stage', self.get_stage)
        self.app.router.add_post('/api/prim/create', self.create_prim)
        # ... more routes
        
        # Start server on localhost:8765
        web.run_app(self.app, port=8765)
```

**1.2 Create MCP Server Client**
```python
# MCP server that connects to Omniverse extension
import httpx

class OmniverseMCPClient:
    def __init__(self, omniverse_url="http://localhost:8765"):
        self.client = httpx.AsyncClient(base_url=omniverse_url)
    
    async def get_live_stage(self):
        response = await self.client.get("/api/stage")
        return response.json()
```

**Status:** 🔴 Not Started

---

### Phase 2: Core Tools (Week 3-4)

**2.1 Implement Stage Management Tools**
- Get live stage
- List prims
- Create/delete prims
- Query scene

**2.2 Implement Transform Tools**
- Get/set transforms
- Move/rotate/scale prims

**Status:** 🔴 Not Started

---

### Phase 3: Advanced Features (Week 5-6)

**3.1 Material Operations**
- Create materials
- Bind materials
- Material queries

**3.2 Viewport Control**
- Camera control
- Screenshot capture
- Viewport focus

**Status:** 🔴 Not Started

---

### Phase 4: Integration (Week 7-8)

**4.1 Integration with USDcodeNIM_MCP**
- Generate code → Execute in Omniverse
- Validate code → Test in live scene

**4.2 Integration with usd-mcp-server**
- File operations → Live scene sync
- Batch operations → Live updates

**Status:** 🔴 Not Started

---

## Technical Requirements

### Omniverse Kit Extension

**Dependencies:**
- `omni.ext` - Extension framework
- `omni.usd` - USD operations
- `omni.kit.commands` - Command execution
- `aiohttp` or `fastapi` - HTTP server
- `websockets` - Real-time updates (optional)

**Extension Structure:**
```
omni_mcp_extension/
├── extension.toml
├── omni_mcp_extension/
│   ├── __init__.py
│   ├── server.py          # HTTP/WebSocket server
│   ├── handlers.py        # API handlers
│   ├── omniverse_api.py   # Omniverse API wrapper
│   └── tools.py           # Tool implementations
└── README.md
```

### MCP Server

**Dependencies:**
- `httpx` - HTTP client
- `mcp` - MCP protocol
- Python 3.10+

**Server Structure:**
```
omniverse_mcp_server/
├── src/
│   ├── omniverse_mcp/
│   │   ├── __init__.py
│   │   ├── server.py          # MCP server
│   │   ├── client.py           # Omniverse client
│   │   ├── tools/
│   │   │   ├── stage_tools.py
│   │   │   ├── transform_tools.py
│   │   │   ├── material_tools.py
│   │   │   └── viewport_tools.py
│   │   └── types.py
├── README.md
└── pyproject.toml
```

---

## Communication Protocol

### HTTP REST API (Extension → MCP Server)

**Base URL:** `http://localhost:8765/api`

**Endpoints:**
```
GET  /api/stage                    # Get current stage info
GET  /api/prims                    # List all prims
GET  /api/prims/{path}             # Get prim info
POST /api/prims                    # Create prim
DELETE /api/prims/{path}           # Delete prim
POST /api/prims/{path}/transform   # Set transform
GET  /api/materials                # List materials
POST /api/materials                # Create material
POST /api/viewport/camera          # Set camera
GET  /api/viewport/screenshot      # Get screenshot
POST /api/commands/execute         # Execute Kit command
```

### WebSocket (Optional - Real-time Updates)

**Connection:** `ws://localhost:8765/ws`

**Events:**
- `stage_changed` - Stage was modified
- `prim_added` - Prim was added
- `prim_removed` - Prim was removed
- `transform_changed` - Transform was modified
- `selection_changed` - Selection changed

---

## Example Usage

### Chat with Omniverse

**User:** "What's in the scene right now?"

**MCP Server:**
1. Calls `getLiveStage` tool
2. Extension queries Omniverse stage
3. Returns list of prims with details

**Response:** "The scene contains 5 prims: /World/Cube, /World/Sphere, /World/Light, /World/Camera, /World/Floor"

---

**User:** "Move the cube to position [5, 2, 0]"

**MCP Server:**
1. Calls `setLiveTransform` tool
2. Extension executes transform in Omniverse
3. Prim moves in real-time

**Response:** "Cube moved to [5, 2, 0]"

---

**User:** "Add a red material to the sphere"

**MCP Server:**
1. Calls `createLiveMaterial` tool (creates red material)
2. Calls `bindLiveMaterial` tool (binds to sphere)
3. Extension executes in Omniverse
4. Sphere turns red in viewport

**Response:** "Red material created and bound to /World/Sphere"

---

## Integration with Existing Tools

### Complete Workflow

```
1. NVIDIA Blog MCP → Research best practices
2. USDcodeNIM_MCP → Generate code
3. USDcodeNIM_MCP → Validate code
4. Omniverse MCP Server → Execute in live Omniverse
5. Omniverse MCP Server → Verify results
6. usd-mcp-server → Save to file (if needed)
```

### Hybrid Approach

```
1. Chat: "Create a scene with a red cube"
2. Omniverse MCP Server → Creates in live Omniverse
3. User reviews in viewport
4. Chat: "Save this to file"
5. Omniverse MCP Server → Exports to USD file
```

---

## Challenges & Solutions

### Challenge 1: Extension HTTP Server

**Problem:** Kit extensions don't typically run HTTP servers

**Solution:**
- Use `aiohttp` or `fastapi` in extension
- Run server in background thread
- Use Kit's event loop integration

### Challenge 2: Authentication

**Problem:** Need to secure localhost server

**Solution:**
- Token-based authentication
- Localhost-only binding
- Optional: User authentication

### Challenge 3: Real-time Updates

**Problem:** MCP server needs to know when Omniverse changes

**Solution:**
- WebSocket for push updates
- Polling fallback
- Event subscription system

### Challenge 4: Error Handling

**Problem:** Omniverse operations can fail

**Solution:**
- Comprehensive error handling
- Clear error messages
- Retry logic for transient errors

---

## Comparison with Alternatives

| Feature | File-Based (usd-mcp-server) | Code Generation (USDcodeNIM_MCP) | **Live Control (Proposed)** |
|---------|------------------------------|----------------------------------|------------------------------|
| **Operation** | File manipulation | Code generation | Live Omniverse control |
| **Real-time** | ❌ No | ❌ No | ✅ Yes |
| **Viewport** | ❌ No | ❌ No | ✅ Yes |
| **Live Query** | ❌ No | ❌ No | ✅ Yes |
| **Immediate Feedback** | ❌ No | ❌ No | ✅ Yes |
| **Use Case** | Batch processing | Learning/code | Interactive development |

---

## Success Criteria

### Phase 1 Success
- [ ] Extension runs HTTP server
- [ ] MCP server connects to extension
- [ ] Can query live stage
- [ ] Can create prims in live scene

### Phase 2 Success
- [ ] All core tools working
- [ ] Transform operations working
- [ ] Material operations working
- [ ] Viewport control working

### Phase 3 Success
- [ ] Integration with USDcodeNIM_MCP
- [ ] Integration with usd-mcp-server
- [ ] Complete workflow working
- [ ] Documentation complete

---

## Next Steps

### Immediate (This Week)
1. [ ] Research Kit extension HTTP server patterns
2. [ ] Create proof-of-concept extension
3. [ ] Test basic HTTP communication
4. [ ] Design API endpoints

### Short-term (This Month)
1. [ ] Implement core extension
2. [ ] Implement MCP server
3. [ ] Test basic tools
4. [ ] Document architecture

### Medium-term (This Quarter)
1. [ ] Complete tool set
2. [ ] Add WebSocket support
3. [ ] Integration testing
4. [ ] User testing

---

## Resources

### Omniverse Kit Documentation
- [Kit Extensions Guide](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/kit_exts.html)
- [Kit Python API](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/python_scripting.html)
- [omni.usd API](https://docs.omniverse.nvidia.com/kit/docs/omni.usd/latest/)

### MCP Protocol
- [MCP Specification](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

### Examples
- [USDcodeNIM_MCP](./) - Our existing MCP server
- [usd-mcp-server](../usd-mcp-server) - File manipulation patterns
- [Kit Extension Template](../Kit_APP_109/templates/extensions/basic_python) - Extension structure

---

## Decision Points

### 1. HTTP Server Library
**Options:**
- `aiohttp` - Async, lightweight
- `fastapi` - Modern, auto-docs
- `flask` - Simple, familiar

**Recommendation:** `fastapi` - Better documentation, type hints, modern

### 2. Communication Protocol
**Options:**
- HTTP REST only
- HTTP + WebSocket
- gRPC

**Recommendation:** HTTP + WebSocket - REST for requests, WebSocket for updates

### 3. Extension vs Standalone
**Options:**
- Kit extension (runs inside Omniverse)
- Standalone server (connects to Omniverse)

**Recommendation:** Kit extension - Tighter integration, direct API access

---

## Conclusion

**This is the missing piece!** An Omniverse MCP server that provides direct, real-time control of Omniverse would complete the ecosystem:

- **USDcodeNIM_MCP** → Generate code
- **usd-mcp-server** → Manipulate files
- **Omniverse MCP Server** → Control live Omniverse ✨

**The vision:** Chat directly with Omniverse, see changes in real-time, iterate quickly.

---

**Last Updated:** 10.12.2025  
**Status:** 🎯 Proposal - Ready for Implementation  
**Priority:** 🔥 High - This completes the ecosystem

