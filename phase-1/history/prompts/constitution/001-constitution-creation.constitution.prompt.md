---
id: "001"
title: "Constitution Creation"
stage: "constitution"
date: "2025-12-28"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "005-better-auth"
user: "aqsagulllinux"
command: "/sp.constitution"
labels: ["constitution","spec-driven","hackathon-2"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
  - ".claude/agents/todo-main-agent.md"
  - ".claude/subagents/installer.md"
  - ".claude/subagents/task-manager.md"
  - ".claude/subagents/state-manager.md"
  - ".claude/subagents/console-display.md"
  - ".claude/subagents/test-runner.md"
  - ".claude/skills/task-crud-skill/SKILL.md"
  - ".claude/skills/console-io-skill/SKILL.md"
tests: []
---

## Prompt

/sp.constitution

Project: In-Memory Todo Console Application (Hackathon 2 – Phase I)

Objective:
Build a clean, spec-driven, in-memory Todo application using Python that runs in the console and supports all basic task management operations. The project must demonstrate disciplined specification-first development using Claude Code and Spec-Kit Plus.

Core Principles:
- Spec-Driven Development: All functionality must originate from written specifications
- Simplicity: Focus on clarity, readability, and beginner-friendly structure
- Correctness: Application behavior must strictly match approved specs
- Maintainability: Code should be easy to extend in later phases
- Determinism: No external storage or side effects beyond in-memory state

Key Standards:
- All features must be defined in specs before implementation
- Each spec change must be preserved in the `specs/history/` folder
- Code must follow clean code principles (small functions, clear naming, single responsibility)
- No external databases or file persistence (pure in-memory only)
- Python typing and docstrings encouraged where useful

Functional Requirements (Phase I – Basic Level):
The application MUST implement all of the following features:

1. Add Todo
   - Create a new task with a title
   - Task is stored in memory

2. View Todos
   - Display all tasks in a readable console format
   - Show completion status clearly

3. Update Todo
   - Modify an existing task's title

4. Delete Todo
   - Remove a task from memory

5. Mark Todo as Complete
   - Toggle or set a task's completion status

Non-Functional Requirements:
- Language: Python 3.13+
- Runtime: Console-based (CLI)
- Storage: In-memory only (no files, no database)
- Frameworks: None (standard library only)
- Environment management: UV

Technology Stack:
- Python 3.13+
- UV (environment & dependency management)
- Claude Code (implementation guided by specs)
- Spec-Kit Plus (spec authoring and iteration)

Project Structure Requirements:
- `/src/`
  - All Python source code
  - Clear module separation (e.g., models, services, cli)
- `/specs/`
  - Current active specs
- `/specs/history/`
  - All previous spec versions (never deleted)
- `/sp.constitution.md`
  - This constitution file
- `README.md`
  - Setup instructions
  - How to run the app
- `CLAUDE.md`
  - Instructions for Claude Code usage

Constraints:
- No persistence between runs
- No GUI or web interface
- No over-engineering (keep logic simple)
- No feature beyond the defined Phase I scope

Success Criteria:
- All 5 basic features implemented and working
- Code behavior matches specs exactly
- Project runs successfully via console
- Clean project structure followed
- Specs history is complete and traceable
- Ready for extension in Phase II

Definition of Done:
- Specs written and finalized
- Code implemented strictly from specs
- Manual testing confirms correct behavior
- Repository structure matches requirements

## Response snapshot

Created project constitution with 5 core principles:
- Spec-Driven Development
- Simplicity
- Correctness
- Maintainability
- Determinism

Added sections for:
- Technology Stack (Python 3.13+, UV, Spec-Kit Plus)
- Project Structure (/src/, /specs/, /specs/history/)
- Scope Boundaries (Phase I only, no persistence)
- Functional Requirements (5 basic features)
- Development Workflow (spec-first process)
- Governance (amendment process, compliance)

Created companion agents and skills for Hackathon 2 Phase 1:
- todo-main-agent.md (main coordinator)
- installer.md, task-manager.md, state-manager.md, console-display.md, test-runner.md (subagents)
- task-crud-skill, console-io-skill (reusable skills)

## Outcome

- ✅ Impact: Constitution established as source of truth for Hackathon 2 Phase 1
- 📁 Files: 1 constitution file + 1 main agent + 5 subagents + 2 skills created
- 🔁 Next prompts: /sp.specify to create feature specs for the 5 CRUD operations
- 🧠 Reflection: Constitution follows spec-driven development pattern with clear governance

## Evaluation notes (flywheel)

- Failure modes observed: "none"
- Graders run and results (PASS/FAIL): "PASS"
- Prompt variant (if applicable): "none"
- Next experiment (smallest change to try): "none"
