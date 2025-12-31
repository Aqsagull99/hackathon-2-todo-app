---
id: "010"
title: "Update CLAUDE.md with project instructions"
stage: "misc"
date: "2025-12-28"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "001-todo-console-app"
branch: "001-todo-console-app"
user: "aqsagulllinux"
command: "CLAUDE.md update"
labels: ["documentation", "claude-code", "instructions"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "/home/aqsagulllinux/Todo-app/CLAUDE.md"
tests:
  - "CLAUDE.md has project overview section"
  - "CLAUDE.md shows how to run the app"
  - "CLAUDE.md includes development commands"
  - "CLAUDE.md documents project structure"
  - "CLAUDE.md lists key files to modify"
---

## Prompt

User requested to add Claude Code instructions to CLAUDE.md per Phase 1 requirements. The existing CLAUDE.md had only SpecKit Plus general rules. User said "ok now do" after asking what specific instructions they wanted.

## Response snapshot

Updated `/home/aqsagulllinux/Todo-app/CLAUDE.md` with project-specific instructions at the top:

1. **Project Overview**:
   - Todo Console Application (Hackathon 2 Phase 1)
   - Python 3.13+, in-memory console app
   - Features list

2. **How to Run the App**:
   - `uv run todo`

3. **Testing the App**:
   - Interactive testing command
   - Quick feature test with echo

4. **Development Commands**:
   - Reinstall: `uv pip install -e .`
   - Syntax check: `python3 -m py_compile`
   - View all tasks

5. **Project Structure**:
   - Directory tree showing all files and their purposes

6. **Spec-Driven Development**:
   - List of SpecKit Plus commands (/sp.specify, /sp.plan, etc.)

7. **Key Files to Modify**:
   - Table showing which file does what

8. **PHR Records**:
   - Location of all recorded work

## Outcome

- ✅ Impact: CLAUDE.md now has project-specific instructions
- 🧪 Tests: Manual verification - file updated
- 📁 Files: CLAUDE.md updated
- 🔁 Next prompts: None - complete

## Evaluation notes (flywheel)

- Failure modes observed: N/A - documentation update
- Graders run and results (PASS/FAIL): File updated - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Could add debugging tips
