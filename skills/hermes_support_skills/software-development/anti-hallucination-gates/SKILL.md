---
name: anti-hallucination-gates
description: "Use when completing tasks. Enforces execution proof gates."
---

# Anti-Hallucination Execution Gates

Execution gatekeeper adapted from `harness-anchor` for Hermes Agent.

## Gates Before Completion

1. **Gate 1 - File System Proof:**
   - If claiming a file was written/patched, verify hash and existence via `read_file` or `search_files`.

2. **Gate 2 - Build & Syntax Gate:**
   - Run linter / compiler / type checker on modified files before declaring done.

3. **Gate 3 - Honest Status Reporting:**
   - Never report "all tests pass" or "service deployed" without verbatim tool output showing exit code 0 and successful logs.
