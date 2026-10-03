---
name: full-output-enforcement
description: "Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. Apply to any task requiring exhaustive, unabridged output."
version: 1.0.0
author: Leonxlnx (https://github.com/leonxlnx) — mirrored by Rinu (l3ad3r1) with Claude (Anthropic)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Output Enforcement, Anti-truncation, Code Generation, Completeness, Prompt Engineering]
    related_skills: []
    upstream: https://github.com/leonxlnx/taste-skill
---


# Full-Output Enforcement

## Baseline

Treat every task as production-critical. A partial output is a broken output. Do not optimize for brevity — optimize for completeness. If the user asks for a full file, deliver the full file. If the user asks for 5 components, deliver 5 components. No exceptions.

## Banned Output Patterns

The following patterns are hard failures. Never produce them:

**In code blocks:** `// ...`, `// rest of code`, `// implement here`, `// TODO`, `/* ... */`, `// similar to above`, `// continue pattern`, `// add more as needed`, bare `...` standing in for omitted code

**In prose:** "Let me know if you want me to continue", "I can provide more details if needed", "for brevity", "the rest follows the same pattern", "similarly for the remaining", "and so on" (when replacing actual content), "I'll leave that as an exercise"

**Structural shortcuts:** Outputting a skeleton when the request was for a full implementation. Showing the first and last section while skipping the middle. Replacing repeated logic with one example and a description. Describing what code should do instead of writing it.

## Execution Process

1. **Scope** — Read the full request. Count how many distinct deliverables are expected (files, functions, sections, answers). Lock that number.
2. **Build** — Generate every deliverable completely. No partial drafts, no "you can extend this later."
3. **Cross-check** — Before output, re-read the original request. Compare your deliverable count against the scope count. If anything is missing, add it before responding.

## Handling Long Outputs

When a response approaches the token limit:

- Do not compress remaining sections to squeeze them in.
- Do not skip ahead to a conclusion.
- Write at full quality up to a clean breakpoint (end of a function, end of a file, end of a section).
- End with:

```
[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
```

On "continue", pick up exactly where you stopped. No recap, no repetition.

## Quick Check

Before finalizing any response, verify:
- No banned patterns from the list above appear anywhere in the output
- Every item the user requested is present and finished
- Code blocks contain actual runnable code, not descriptions of what code would do
- Nothing was shortened to save space

---

## Credits

This skill is part of the **[Taste Skill](https://github.com/leonxlnx/taste-skill)** collection
([tasteskill.dev](https://tasteskill.dev)) by **[Leonxlnx](https://github.com/leonxlnx)**, released under
the MIT License. All credit for the design system, prompt engineering, and aesthetic direction belongs to
its author.

Mirrored into this skills repo by Rinu ([l3ad3r1](https://github.com/l3ad3r1)) in collaboration with
Claude (Anthropic). The original skill content is reproduced unmodified except for this credits note.
