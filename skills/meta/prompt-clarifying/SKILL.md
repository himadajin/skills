---
name: prompt-clarifying
description: >-
  Create a new agent-facing prompt or refine an existing one
  by questioning the user with the installed grilling skill,
  then write the result to ./tmp/<title>.md.
  Invoke only on the user's explicit request.
disable-model-invocation: true
---
# Prompt Clarifying

Turn the user's draft prompt or notes into a refined prompt.

1. Invoke the installed "grilling" skill.
   Ask for the target model in the first round;
   recommend the model you are running on,
   or every vendor below when the prompt is shared across agents.
2. Once the target model is settled, read every reference for that vendor.
   Use them to find what the prompt leaves undecided,
   and put those gaps to the user in later grilling rounds.
3. When the user confirms the grilling is done,
   write the prompt to `./tmp/<title>.md` under the current directory,
   creating `tmp/` if needed, unless the user named another path.
   Name `<title>` in kebab-case after the prompt's purpose,
   and add a numeric suffix such as `-2` rather than overwrite an existing file.
   Leave the original prompt file untouched;
   whether to adopt the result is the user's decision.
   Report the path and finish.
   On a follow-up change request, update the same file.

- Claude: [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview.md), [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)
- OpenAI: [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering.md), [Prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance.md)
- Gemini: [Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies.md.txt)
