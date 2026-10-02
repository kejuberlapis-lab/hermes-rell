---
name: zero-hallucination-coder
description: "Use when writing code. Enforces verified paths and imports."
---

# Zero Hallucination Coder

Rigorous coding protocol adapted from `claude-skills/zero-hallucination-coder` for Hermes Agent.

## Rules for Code Generation

1. **Verify Dependencies Before Importing:**
   - Always inspect `package.json`, `requirements.txt`, `pyproject.toml`, or `Cargo.toml`.
   - Never import a library without confirming it is installed in the project environment.

2. **Verify File Paths & Signatures:**
   - Use `search_files` and `read_file` to confirm exact function signatures and file locations before calling them.
   - Never guess an internal API method name from memory.

3. **Atomic Red-Green-Refactor Loop:**
   - Write failing tests first.
   - Implement the smallest necessary fix.
   - Verify syntax and tests pass using real tool execution before claiming success.
