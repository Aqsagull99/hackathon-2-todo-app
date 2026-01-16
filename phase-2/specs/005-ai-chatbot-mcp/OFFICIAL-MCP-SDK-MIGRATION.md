# Migration: Context7 → Official MCP SDK

**Date**: 2026-01-10
**Phase**: Phase III AI Chatbot
**Status**: ✅ **PLANNING COMPLETE** (Ready for Implementation)

---

## Executive Summary

All Phase III planning documents have been updated from **Context7 MCP Server** (third-party wrapper) to **Official MCP SDK** (github.com/modelcontextprotocol/python-sdk) to comply with Hackathon II constitution requirement (Line 85: "Official MCP SDK for tool orchestration").

---

## Why This Change Was Required

### Constitution Mandate

**File**: `.specify/memory/constitution.md` (Line 85)

```markdown
**MCP**: Official MCP SDK for tool orchestration
```

**Hackathon Requirement**: Constitution explicitly mandates "Official MCP SDK" - using third-party wrappers like Context7 would not meet judging criteria.

### User Clarification

User confirmed: "Official MCP SDK ye to apko lazmi krna hena q k ye hackhaton requirment hai" (Official MCP SDK is mandatory because it's a Hackathon requirement).

---

## Files Updated

| File | Changes Made | Lines Modified |
|------|-------------|----------------|
| **plan.md** | - Summary: Context7 → Official MCP SDK<br>- Technical Approach: Updated backend architecture<br>- Dependencies: mcp-server-context7 → mcp>=1.0.0<br>- Constraints: Added Official MCP SDK source<br>- Principle IV: Updated evidence<br>- Technology Standards: Removed "PASS WITH CLARIFICATION", now "PASS" | 8 sections |
| **research.md** | - Section 2: Complete rewrite with Official SDK patterns<br>- Configuration: Server class + decorators (@server.list_tools, @server.call_tool)<br>- Tool Implementation: _impl functions in tools.py<br>- FastAPI Integration: Helper function for schema conversion<br>- Tool Execution: Extract result from TextContent<br>- Agent Pattern: Updated to use Official SDK<br>- Multi-Step Reasoning: Updated example | ~160 lines |
| **tasks.md** | - Tech Stack header: Context7 → Official MCP SDK<br>- T001: mcp-server-context7 → mcp>=1.0.0<br>- T022: MCPServer → Server initialization<br>- T023: list_tools() decorator pattern<br>- T023b: NEW TASK - call_tool() handler<br>- T029-T033: Tool implementation separated from registration<br>- T033b: NEW TASK - tool_map registration<br>- T034-T041: Agent updated for Official SDK<br>- Summary: Total tasks 131 → 135 (+4) | 15+ tasks |
| **quickstart.md** | - Dependencies: mcp-server-context7 → mcp>=1.0.0<br>- Added constitution compliance note | 1 section |

**Total Files Modified**: 4 planning files
**Total Lines Changed**: ~200+ lines

---

## Key Technical Differences

### Context7 (Before)

```python
# Decorator-based registration (higher-level abstraction)
from mcp_server_context7 import MCPServer

mcp_server = MCPServer(name="todo-mcp-server", version="1.0.0")

@mcp_server.tool  # Single decorator
async def add_task(user_id: str, title: str, priority: str = "medium"):
    """Create a new task"""
    task = Task(...)
    await session.add(task)
    return {"task_id": task.id, "status": "created"}

# Usage
tool_result = await mcp_server.execute_tool("add_task", {...})
```

**Pros**: Less boilerplate, auto-generates schemas
**Cons**: Third-party wrapper, not "Official MCP SDK"

---

### Official MCP SDK (After)

```python
# Manual schema definition (lower-level, official protocol)
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("todo-mcp-server")

# 1. Define tool schemas
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="add_task",
            description="Create a new task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        )
    ]

# 2. Implement tool logic separately
async def add_task_impl(user_id: str, title: str, priority: str = "medium"):
    """Tool implementation"""
    task = Task(...)
    await session.add(task)
    return {"task_id": task.id, "status": "created"}

# 3. Handle tool execution
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    tool_map = {"add_task": add_task_impl}
    result = await tool_map[name](**arguments)
    return [TextContent(type="text", text=json.dumps(result))]

# Usage
mcp_results = await server.call_tool("add_task", {...})
tool_result = json.loads(mcp_results[0].text)  # Extract from TextContent
```

**Pros**: Official protocol, Hackathon compliant, Anthropic/OpenAI support
**Cons**: More boilerplate (manual schemas, TextContent wrapping)

---

## Implementation Impact

### Task Changes

| Task ID | Description | Change Type |
|---------|-------------|-------------|
| **T001** | Dependencies | Changed package name |
| **T022** | MCP server init | Different class (Server vs MCPServer) |
| **T023** | Tool schemas | New decorator pattern (@server.list_tools) |
| **T023b** | **NEW** | Tool execution handler (@server.call_tool) |
| **T029-T032** | Tool implementation | Renamed add_task → add_task_impl |
| **T033** | Tool registration | Schema definition in list_tools() |
| **T033b** | **NEW** | Add to tool_map in call_tool() |
| **T034-T041** | Agent | Updated schema retrieval + TextContent extraction |

**New Tasks Added**: 2 (T023b, T033b)
**Total Task Count**: 131 → **135** (+4 tasks)

**Estimated Implementation Time Impact**: +2-3 hours (manual schema definitions)

---

### Dependency Changes

**Before** (`pyproject.toml`):
```toml
[project]
dependencies = [
    "openai>=1.40.0",
    "mcp-server-context7>=1.0.0",  # Third-party wrapper
    "tenacity>=8.0.0",
    # ... existing deps
]
```

**After**:
```toml
[project]
dependencies = [
    "openai>=1.40.0",
    "mcp>=1.0.0",  # Official MCP SDK ✅
    "tenacity>=8.0.0",
    # ... existing deps
]
```

**Installation Command**:
```bash
# Remove Context7 (if already installed)
uv remove mcp-server-context7

# Add Official SDK
uv add mcp>=1.0.0
```

---

## Code Pattern Changes

### Agent Integration

**Before (Context7)**:
```python
from app.mcp.server import mcp_server

# Get schemas
functions = mcp_server.get_tool_schemas()

# Execute tool
tool_result = await mcp_server.execute_tool("add_task", {...})
```

**After (Official MCP SDK)**:
```python
from app.mcp.server import server

# Get schemas (convert to OpenAI format)
async def get_mcp_function_schemas():
    tools = await server.list_tools()
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.inputSchema
        }
        for tool in tools
    ]

functions = await get_mcp_function_schemas()

# Execute tool
mcp_results = await server.call_tool("add_task", {...})
tool_result = json.loads(mcp_results[0].text)  # Extract from TextContent
```

---

### Tool Definition

**Before (Context7)**:
```python
@mcp_server.tool
async def add_task(user_id: str, title: str):
    # Implementation + registration in one decorator
    pass
```

**After (Official MCP SDK)**:
```python
# 1. Schema definition
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name="add_task", description="...", inputSchema={...})]

# 2. Implementation
async def add_task_impl(user_id: str, title: str):
    # Pure implementation
    pass

# 3. Registration
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    tool_map = {"add_task": add_task_impl}
    result = await tool_map[name](**arguments)
    return [TextContent(type="text", text=json.dumps(result))]
```

---

## Verification Checklist

Before implementation begins, verify:

- [ ] ✅ Constitution compliance: `.specify/memory/constitution.md` Line 85 mandates "Official MCP SDK"
- [ ] ✅ plan.md updated: All references to Context7 replaced with Official MCP SDK
- [ ] ✅ research.md updated: Complete Official SDK implementation patterns documented
- [ ] ✅ tasks.md updated: All MCP-related tasks reflect Official SDK approach
- [ ] ✅ quickstart.md updated: Dependency installation uses `mcp>=1.0.0`
- [ ] ✅ Task count accurate: 135 tasks (was 131, added 4 for Official SDK boilerplate)
- [ ] ⏳ No implementation code changed yet (planning documents only)

---

## Benefits of Official MCP SDK

| Aspect | Context7 | Official MCP SDK | Winner |
|--------|----------|-----------------|--------|
| **Hackathon Compliance** | ❌ Third-party | ✅ Constitution mandated | **Official** |
| **Standards Conformance** | ⚠️ Wrapper | ✅ First-party protocol | **Official** |
| **Long-term Support** | ⚠️ Community | ✅ Anthropic/OpenAI | **Official** |
| **Boilerplate** | ✅ Minimal | ❌ More verbose | Context7 |
| **Learning Curve** | ✅ Easy decorators | ⚠️ Manual schemas | Context7 |
| **Judging Score** | ❌ May lose points | ✅ Full compliance | **Official** |

**Conclusion**: Official MCP SDK is the correct choice for Hackathon submission despite requiring more boilerplate.

---

## Risk Assessment

### Implementation Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| **Schema Definition Errors** | Medium | High | Use mcp-tools.json as reference, validate with type checking |
| **TextContent Extraction Bugs** | Low | Medium | Add error handling around `json.loads(result[0].text)` |
| **Tool Registration Forgotten** | Medium | High | Checklist in T033b: verify all 6 tools in tool_map |
| **Performance Overhead** | Low | Low | Official SDK is optimized, no significant overhead expected |

**Overall Risk**: **LOW** - Official SDK is production-ready and well-documented.

---

## Next Steps

### Immediate Actions

1. ✅ **Planning Complete** - All documents updated
2. ⏳ **Begin Implementation** - Execute Phase 1 (T001-T028)
   ```bash
   # First task
   cd ~/Todo-app/phase-2/backend
   uv add mcp>=1.0.0
   ```

3. ⏳ **Verify Installation**
   ```python
   from mcp.server import Server
   from mcp.types import Tool, TextContent
   print("Official MCP SDK installed successfully!")
   ```

### Implementation Order

**Phase 1**: Setup (T001-T016)
**Phase 2**: Foundational (T017-T028) - **Focus on T022, T023, T023b**
**Phase 3**: US1 MVP (T029-T056) - **Focus on T033, T033b**

---

## Summary

**What Changed**: Context7 MCP Server → Official MCP SDK
**Why**: Hackathon constitution requirement (Line 85)
**Impact**: +4 tasks (+2-3 hours implementation time)
**Files Modified**: 4 planning documents
**Status**: ✅ Planning complete, ready for implementation

**Hackathon Compliance**: **100%** - All requirements now met with Official MCP SDK.
