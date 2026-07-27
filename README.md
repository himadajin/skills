# Skills

Himadajin's personal agent skills.

## Recommended workflow

Personal skills should be managed in `~/.agents/skills/` as the single source of truth.
The skill format itself is shared, so keeping one canonical directory avoids duplicating the same skill per agent or per project.

This works well because Codex uses `~/.agents/skills/` natively,
GitHub Copilot also supports `~/.agents/skills/` across its agent surfaces,
and Claude Code can follow the same directory through a symlink.

Use `~/.agents/skills/` as the real directory, then connect agent-specific locations to it with symlinks where needed:

- **Claude Code**
  - Location: `~/.claude/skills/`
  - Setup: symlink `~/.claude/skills` -> `~/.agents/skills`

- **Codex**
  - Location: `~/.agents/skills/`
  - Setup: use directly

- **GitHub Copilot CLI**
  - Location: `~/.agents/skills/`
  - Setup: use directly

- **GitHub Copilot cloud agent**
  - Location: `~/.agents/skills/` or `~/.copilot/skills/`
  - Setup: manage shared personal skills in `~/.agents/skills/`

- **GitHub Copilot in VS Code**
  - Location: `~/.agents/skills/`, `~/.claude/skills/`, or `~/.copilot/skills/`
  - Setup: prefer `~/.agents/skills/`

This keeps shared skills centralized in one place while still matching each agent's discovery rules.

```sh
mkdir -p ~/.agents/skills ~/.claude
ln -sfn ~/.agents/skills ~/.claude/skills
```

## Using skills in chat apps

Claude and ChatGPT accept skills as zip uploads. Each release of this repository
attaches one `<skill-name>.zip` per skill, in the folder layout both services expect.

Download the zip for the skill you need from the
[latest release](https://github.com/himadajin/skills/releases/latest) and upload it
in the chat app's skill settings.
See [docs/releasing.md](docs/releasing.md) for how releases are produced.

Note: Claude Desktop (Cowork) sessions do not read `~/.claude/skills/`; they sync
the skills enabled on your claude.ai account instead. A skill uploaded to
claude.ai under the same name as a locally installed one therefore shows up
twice in those sessions, as a frozen copy that no longer tracks its source repo.
Keep the local install as the source of truth and upload to claude.ai only for
skills used in the chat apps themselves.

## See Also

References:

- [Overview - Agent Skills](https://agentskills.io/home)
- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Build skills – Codex | ChatGPT Learn](https://learn.chatgpt.com/docs/build-skills)
- [Adding agent skills for GitHub Copilot CLI - GitHub Docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
- [Use Agent Skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)

Related repositories:

- [anthropics/skills | GitHub](https://github.com/anthropics/skills)
- [ComposioHQ/awesome-claude-skills | GitHub](https://github.com/ComposioHQ/awesome-claude-skills)
- [google/skills | GitHub](https://github.com/google/skills)
- [mattpocock/skills | GitHub](https://github.com/mattpocock/skills)
- [mizchi/skills | GitHub](https://github.com/mizchi/skills)
- [openai/skills | GitHub](https://github.com/openai/skills)
