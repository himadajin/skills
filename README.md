# Skills

Himadajin's personal agent skills.

## Recommended workflow

Personal skills should be managed in `~/.agents/skills/` as the single source of truth.
The skill format itself is shared, so keeping one canonical directory avoids duplicating the same skill per agent or per project.

This works well because Codex uses `~/.agents/skills/` natively,
GitHub Copilot also supports `~/.agents/skills/` across its agent surfaces,
and Claude Code can follow the same directory through a symlink.

Use `~/.agents/skills/` as the real directory, then connect agent-specific locations to it with symlinks where needed:

| Agent                      | Personal skills location                                          | Recommended setup                                                                                  |
| -------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Claude Code                | `~/.claude/skills/`                                               | Symlink `~/.claude/skills` -> `~/.agents/skills`                                                   |
| Codex                      | `~/.agents/skills/`                                               | Use directly                                                                                       |
| GitHub Copilot CLI         | `~/.agents/skills/` or `~/.copilot/skills/`                       | Prefer `~/.agents/skills/`; if you also use `~/.copilot/skills/`, symlink it to the same directory |
| GitHub Copilot cloud agent | `~/.agents/skills/` or `~/.copilot/skills/`                       | Manage shared personal skills in `~/.agents/skills/`                                               |
| GitHub Copilot in VS Code  | `~/.agents/skills/`, `~/.claude/skills/`, or `~/.copilot/skills/` | Prefer `~/.agents/skills/`; keep the others as symlinks only if needed                             |

This keeps shared skills centralized in one place while still matching each agent's discovery rules.

```sh
mkdir -p ~/.agents/skills ~/.claude ~/.copilot
ln -sfn ~/.agents/skills ~/.claude/skills
ln -sfn ~/.agents/skills ~/.copilot/skills
```

## See Also

References:

- [Overview - Agent Skills](https://agentskills.io/home)
- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Agent Skills – Codex | OpenAI Developers](https://developers.openai.com/codex/skills)
- [Adding agent skills for GitHub Copilot CLI - GitHub Docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
- [Use Agent Skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)

Examples:

- [openai/skills: Skills Catalog for Codex | GitHub](https://github.com/openai/skills)
- [anthropics/skills: Public repository for Agent Skills | GitHub](https://github.com/anthropics/skills)
- [ComposioHQ/awesome-claude-skills: A curated list of awesome Claude Skills, resources, and tools for customizing Claude AI workflows | GitHub](https://github.com/ComposioHQ/awesome-claude-skills)
