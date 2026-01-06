# Agent Skills Documentation

Agent Skills are modular capabilities that extend Claude's functionality through organized folders containing instructions, scripts, and resources. They are **model-invoked** - Claude autonomously decides when to use them based on your request and the Skill's description, unlike slash commands which are user-invoked.

## Prerequisites
- Claude Code version 1.0 or later
- Basic familiarity with Claude Code

## Creating Skills

Skills are stored as directories containing a `SKILL.md` file with YAML frontmatter and Markdown content.

### Skill Locations

**Personal Skills** (available across all projects):
```bash
mkdir -p ~/.claude/skills/my-skill-name
```

**Project Skills** (shared with team via git):
```bash
mkdir -p .claude/skills/my-skill-name
```

**Plugin Skills** come from Claude Code plugins and work the same way as personal/project skills.

### Basic SKILL.md Structure

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---
# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

**Field requirements**:
- `name`: lowercase letters, numbers, hyphens only (max 64 characters)
- `description`: brief description of what the Skill does and when to use it (max 1024 characters)

The description is critical for Claude to discover when to use your Skill - it should include both what the Skill does and when Claude should use it.

### Multi-file Skills

Skills can include additional files:

```
my-skill/
├── SKILL.md (required)
├── reference.md (optional documentation)
├── examples.md (optional examples)
├── scripts/
│   └── helper.py (optional utility)
└── templates/
    └── template.txt (optional template)
```

Reference files from SKILL.md:
```markdown
For advanced usage, see [reference.md](reference.md).

Run the helper script:
```bash
python scripts/helper.py input.txt
```
```

## Tool Permissions

Use `allowed-tools` to restrict which tools Claude can use when a Skill is active:

```yaml
---
name: safe-file-reader
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---
# Safe File Reader

This Skill provides read-only file access.

## Instructions
1. Use Read to view file contents
2. Use Grep to search within files
3. Use Glob to find files by pattern
```

When specified, Claude can only use the listed tools without asking permission.

## Viewing Available Skills

Skills are automatically discovered from:
- Personal: `~/.claude/skills/`
- Project: `.claude/skills/`
- Plugin: bundled with installed plugins

Ask Claude directly:
```bash
What Skills are available?
```

Or inspect the filesystem:
```bash
# List personal Skills
ls ~/.claude/skills/

# List project Skills
ls .claude/skills/

# View specific Skill
cat ~/.claude/skills/my-skill/SKILL.md
```

## Testing and Debugging

### Common Issues:
1. **Make description specific** - include both what the Skill does and when to use it
2. **Verify file path** - ensure correct location and file exists
3. **Check YAML syntax** - ensure proper `---` delimiters and valid syntax
4. **View errors** - run `claude --debug` to see loading errors

### Debugging Checklist:
- Description too vague vs specific
- File path verification
- YAML syntax validation
- Dependencies availability
- Script execute permissions

## Best Practices

1. **Keep Skills focused** - one capability per Skill
2. **Write clear descriptions** - include specific triggers and when to use
3. **Test with team** - get feedback on activation and clarity
4. **Document versions** - track changes over time

## Example Skills

### Simple Skill:
```yaml
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---
# Generating Commit Messages

## Instructions
1. Run `git diff --staged` to see changes
2. I'll suggest a commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best practices
- Use present tense
- Explain what and why, not how
```

### Multi-file Skill:
```
pdf-processing/
├── SKILL.md
├── FORMS.md
├── REFERENCE.md
└── scripts/
    ├── fill_form.py
    └── validate.py
```

Skills can be shared with teams via git (for project skills) or through plugins, and updates take effect after restarting Claude Code.


