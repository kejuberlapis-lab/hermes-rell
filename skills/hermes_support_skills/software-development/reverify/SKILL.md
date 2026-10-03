---
name: reverify
description: "Use when asserting results. Audits deterministic proof."
---

# Reverify (Deterministic Evidence Engine)

Adapted from `2akouwu/reverify` for Hermes Agent. Stop the AI from making things up by enforcing deterministic proof.

## Core Workflow

1. **Proposal vs Execution Separation:**
   - The agent proposes an action or claim.
   - Deterministic tools (`terminal`, `read_file`, `search_files`) execute and verify the state.
   - The claim is only accepted if tool output provides exact proof.

2. **Evidence Table:**
   Before declaring any deliverable complete, verify each component:
   - File creation: Checked with `ls -la <path>` and `read_file`.
   - Code edit: Checked with `git diff` or regex search.
   - Service/Process: Checked with live status/curl probe.

3. **Zero Faith Assumption:**
   - Do not trust memory or prior conversation history for file content. Re-verify the file state on disk.
