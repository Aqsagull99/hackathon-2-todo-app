---
id: "019"
title: "Create Tailwind CSS subagent and skill"
stage: "misc"
date: "2025-12-29"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "001-todo-console-app"
branch: "001-todo-console-app"
user: "aqsagulllinux"
command: "Create Tailwind CSS subagent and skill with context7 MCP"
labels: ["tailwind", "css", "agent", "skill", "context7", "mcp", "frontend"]
links:
  spec: "null"
  plan: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "/home/aqsagulllinux/Todo-app/.claude/subagents/tailwind-dev.md"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/tailwind-skill/SKILL.md"
tests:
  - "Tailwind subagent created with context7 MCP"
  - "Tailwind skill created with context7 MCP"
  - "All utility patterns documented"
---

## Prompt

User requested to create Tailwind CSS subagent and skill for Phase II frontend development. Additional requirement: Include context7 MCP server documentation for reading Tailwind CSS docs.

## Response snapshot

Created Tailwind CSS subagent and skill with context7 MCP integration:

### tailwind-dev.md (Subagent)

**Purpose:** Tailwind CSS developer for implementing responsive layouts, custom configuration, and utility-first styling.

**MCP Reference:**
- `context7` - Tailwind CSS documentation

**Fetching docs:** `@context7:get-library-docs` with topics:
- "configuration"
- "utility-classes"
- "responsive-design"
- "dark-mode"
- "forms"
- "plugins"

**Contents:**
1. Tailwind configuration (tailwind.config.ts)
2. Custom theme colors and spacing
3. globals.css with @layer components
4. Layout utilities (flexbox, grid)
5. Spacing patterns (margin, padding)
6. Typography utilities
7. Colors and backgrounds
8. Borders and shadows
9. Responsive breakpoints
10. State utilities (hover, focus, disabled)
11. Component patterns (Button, Input, Card)

### tailwind-skill/SKILL.md (Skill)

**Purpose:** Reusable Tailwind CSS patterns and utility classes.

**MCP Reference:**
- `context7` - Tailwind CSS documentation

**Contents:**
1. Layout utilities (container, flexbox, grid)
2. Spacing (margins, padding)
3. Typography (size, weight, alignment, color)
4. Color utilities (text, background, opacity)
5. Border utilities (width, color, radius)
6. Shadow utilities
7. Responsive design (breakpoints)
8. State utilities (hover, focus, active, disabled, transitions)
9. Common component patterns (Button, Input, Card, Badge)

## Key Features

### Tailwind Config Pattern
```typescript
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: { 500: "#3b82f6", 600: "#2563eb", 700: "#1d4ed8" },
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
```

### Common Component Pattern
```typescript
export function Button({ variant = "primary", size = "md" }) {
  const variants = {
    primary: "bg-blue-600 hover:bg-blue-700 text-white",
    secondary: "bg-gray-200 hover:bg-gray-300 text-gray-900",
  };
  // Return styled button
}
```

### Responsive Pattern
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Responsive grid items -->
</div>
```

## Context7 MCP Integration

Both files reference context7 MCP for fetching Tailwind documentation:

```yaml
mcp_servers:
  - context7

# Fetch docs with:
@context7:get-library-docs context7CompatibleLibraryID="/org/project" topic="utility-classes"
```

## Outcome

- ✅ Impact: Tailwind CSS subagent and skill ready for frontend development
- 🧪 Tests: 2 files created, all patterns validated
- 📁 Files: 1 subagent + 1 skill = 2 files
- 🔁 Next prompts: Ready to use in Phase II frontend development
- 🧠 Reflection: All utilities include context7 MCP references for docs

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All files created - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add dark mode patterns
