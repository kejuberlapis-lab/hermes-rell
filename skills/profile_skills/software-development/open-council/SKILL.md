---
name: open-council
description: "Use when reviewing complex tasks. Runs multi-agent audit."
---

# Open Council (Adversarial Quality Control)

Adapted from `vinitjhawar/opencouncil` for Hermes Agent. Multi-perspective review to eliminate sycophancy and hallucinations.

## Protocol

1. **Drafter vs Auditor Separation:**
   - During multi-step complex work, separate the generator role from the reviewer role.
   - Use `delegate_task` or a subagent to independently inspect the generated diff, file, or report.

2. **Adversarial Checklist:**
   - Did the implementer make unwarranted assumptions?
   - Are there unverified edge cases or broken imports?
   - Does every claim in the summary have exact tool output proof?

3. **Unified Honest Verdict:**
   - Deliver findings plainly without softening or agreeing just to please the user (*anti-sycophancy*).
