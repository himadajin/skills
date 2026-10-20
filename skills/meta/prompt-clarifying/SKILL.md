---
name: prompt-clarifying
description: >-
  Iteratively clarify and improve agent-facing instructions —
  skills, slash commands, repository instruction files, code-gen prompts —
  by questioning the user with the grilling skill and rewriting the prompt
  based on their answers.
  Invoke only on the user's explicit request.
disable-model-invocation: true
---
# Prompt Clarifying

Invoke the installed "grilling" skill and create a prompt based on the information received from the user.

Select and read the relevant prompt engineering references below based on the language model the prompt is intended for. If no target model is specified, use the model you are currently using:

- [Claude Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview.md)
- [Claude Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)
- [OpenAI Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering.md)
- [OpenAI Prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance.md)
- [Prompt design strategies | Gemini API](https://ai.google.dev/gemini-api/docs/prompting-strategies.md)
